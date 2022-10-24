import sqlalchemy as sqlalchemy
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import pandas as pd

engine = sqlalchemy.create_engine(url="postgresql://mdb:Gsdbe4k754ghmf@185.87.50.149:6432/dblp")
con = engine.connect()

columns = ['title', 'abstract', 'id', 'volume', 'year', 'n_citation', 'lang']
df = pd.read_sql("select * from dblps.tarticle limit 100", con=con)[columns]
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)

app = Dash(__name__)

PAGE_SIZE = 15


app.layout = html.Div([
    html.H6("Write the text you want to search for!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='study', type='text')
    ]),
    html.Br(),
    dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {"name": i, "id": i} for i in df.columns
        ],
        style_data={
                'whiteSpace': 'normal',
                'lineWidth': '10px'
            },
        css=[{
            'selector': '.dash-spreadsheet td div',
            'rule': '''
                    line-height: 15px;
                    max-height: 30px; min-height: 30px; height: 30px;
                    display: block;
                    overflow-y: hidden;
                '''
        }],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom'
    )

])

@app.callback(
    Output('datatable-paging', 'data'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"),
    Input('my-input', 'value')
)
def update_table(page_current, page_size, pattern):
    return df.loc[df['title'].str.contains(pattern)].iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
