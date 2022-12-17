import sqlalchemy as sqlalchemy
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from client import get_server_prediction
import networkx as nx
from pyvis.network import Network

VALID_USERNAME_PASSWORD_PAIRS = [["team15", "made"]]

# подключение к базе данных со статьями
engine = sqlalchemy.create_engine(url="postgresql://mdb:Gsdbe4k754ghmf@185.87.50.149:6432/dblp")
con = engine.connect()

columns = ['title', 'abstract', 'id', 'volume', 'year', 'n_citation', 'lang']
df = []
for year in range(2000, 2020):
    df_year = pd.read_sql("SELECT title, abstract, id, volume, year, n_citation, lang "
                          f"FROM dblps.tarticle WHERE (year = '{year}') and (title is not null) "
                          f"and (abstract != '') LIMIT 28000",
                          con=con)[columns]
    df.append(df_year)
df = pd.concat(df, axis=0)
df['index'] = range(1, len(df) + 1)

article_columns = ['article_idx', 'name']
df_article_author = pd.read_sql(f"select * from dblps.tarticle2tauthor limit 500", con=con)[article_columns]
df_article_author[' index'] = range(1, len(df_article_author) + 1)

app = Dash(__name__)

PAGE_SIZE = 15


# визуализация графа
def add_edge(f_item, s_item, graph=None):
    graph.add_edge(f_item, s_item)
    graph.add_edge(s_item, f_item)


def make_graph(df):
    graph = nx.Graph()

    articles = {}

    for i in df.index:
        if df['article_idx'][i] not in articles.keys():
            articles[df['article_idx'][i]] = []
        else:
            articles[df['article_idx'][i]].append(df['name'][i])

    for article, authors in articles.items():
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                add_edge(authors[i], authors[j], graph)

    return graph


def show_net(graph):
    nt = Network(height='590px',
                 width='100%',
                 bgcolor='#222222',
                 font_color='white',
                 notebook=True)
    nt.barnes_hut()
    nt.from_nx(graph)
    nt.write_html('test_graph.html')
    return nt


def show_graph(df):
    df = df.dropna()
    graph = make_graph(df)
    return show_net(graph)


nt = show_graph(df_article_author)

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
    ),
    html.Br(),
    html.H3("Take a look at the citation graph."),
    html.Div(style={'text-align': 'center'},
             children=[html.Iframe(srcDoc=nt.html,
                                   style={
                                       "height": "600px",
                                       "width": "50%",
                                       'align': 'center'
                                   })
                       ]
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
    recommendation_data_id = get_server_prediction(new_data)
    recommendation_data = df.loc[df['id'].isin(recommendation_data_id)].iloc[:PAGE_SIZE]
    recommendation_tooltip_data = [
        {column: {'value': str(value), 'type': 'markdown'}
         for column, value in row.items()
         } for row in recommendation_data.to_dict('records')
    ]
    return recommendation_data.to_dict('records'), recommendation_tooltip_data


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050")
