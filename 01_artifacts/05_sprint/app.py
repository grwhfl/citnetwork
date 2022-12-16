import sqlalchemy as sqlalchemy
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from client import get_server_prediction

VALID_USERNAME_PASSWORD_PAIRS = [["team15", "made"]]

# подключение к базе данных со статьями
engine = sqlalchemy.create_engine(url="postgresql://mdb:Gsdbe4k754ghmf@185.87.50.149:6432/dblp")
con = engine.connect()

columns = ['title', 'abstract', 'id', 'volume', 'year', 'n_citation', 'lang']
df = pd.read_sql("select * from dblps.tarticle limit 100", con=con)[columns]
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df['index'] = range(1, len(df) + 1)

app = Dash(__name__)

PAGE_SIZE = 15

# описание веб интерфейса
app.layout = html.Div([
    html.H1("Citation network project"),
    html.H2("We will recommend some articles for you based on your search."),
    html.H3("Write the title you are looking for:"),
    html.Div([
        "Search: ",
        dcc.Input(id='my-input', value='', type='text')
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
    ),
    html.Br(),
    html.H3("These article might be interesting for you:"),
    dash_table.DataTable(
        id='datatable-recommendation',
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
    )
])


@app.callback(
    Output('datatable-paging', 'data'),
    Output('datatable-paging', 'tooltip_data'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"),
    Input('my-input', 'value')
)
def update_table(page_current, page_size, pattern):
    """фильтрация данных для одной странице по ключу pattern
    поиск происходит только по полному совпадению в колонке 'title'"""
    new_data = df.loc[df['title'].str.contains(pattern)].iloc[
               page_current * page_size:(page_current + 1) * page_size
               ]
    new_tooltip_data = [
        {column: {'value': str(value), 'type': 'markdown'}
         for column, value in row.items()
         } for row in new_data.to_dict('records')
    ]

    return new_data.to_dict('records'), new_tooltip_data


@app.callback(
    Output('datatable-recommendation', 'data'),
    Output('datatable-recommendation', 'tooltip_data'),
    Input('datatable-paging', 'data'),
)
def update_recommendation(new_data):
    """get prediction for current user search"""
    new_data = pd.DataFrame.from_records(new_data).copy()
    recommendation_data_id = list(set(get_server_prediction(new_data)) & set(df.index))
    recommendation_data = df.loc[recommendation_data_id].iloc[:PAGE_SIZE]
    recommendation_tooltip_data = [
        {column: {'value': str(value), 'type': 'markdown'}
         for column, value in row.items()
         } for row in recommendation_data.to_dict('records')
    ]
    return recommendation_data.to_dict('records'), recommendation_tooltip_data


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050")
