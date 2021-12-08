# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import datetime
import dateutil.parser


app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
import requests
def get_data():
    req = requests.request('GET', 'http://localhost:1400/')
    all = req.json()

    temp_x = []
    temp_y = []
    temp_t = []

    for point in all:
        temp_x.append(point[0])
        temp_y.append(point[1])
        # temp_t.append(int(dateutil.parser.isoparse(point[2]).strftime("%Y%m%d%H%M%S")))
        temp_t.append(point[2])
        # print(temp_t)
    df = pd.DataFrame(dict(
        x = temp_x, y = temp_y, t = pd.Series(temp_t)
    ))
    return df


df = get_data()
print(df)

app.layout = html.Div(style={'textAlign': 'center'},
    children=[
    html.H1(children='Ground Robot'),
    html.Div(id='hidden-div', style={'display':'none'}, lang='en'),
    html.Button('Start/Stop', id='submit-val', n_clicks=0),
    html.Div(style={'textAlign':'center', 'width':'1000px'},children = [
    dcc.Graph(
        id='example-graph',
    ),
    ]),
    html.Div(id='slider',style={'width':'1000px' },children = [
        dcc.Slider(
            id='Time-Slider',
            min=df['t'].min(),
            max=df['t'].max(),
            value=df['t'].max(),
            # marks={str(t): str(datetime.datetime.strptime(str(t), "%Y%m%d%H%M%S")) for t in df['t'].unique()},
            marks={str(t): str(t) for t in df['t'].unique()},
            step=None
        ),
        dcc.Interval(
        id = 'interval-component',
        interval = 1*1000,
        n_intervals=0
        )
    ])
])

@app.callback(Output('Time-Slider', 'max'),
                Output('Time-Slider', 'marks'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    global df
    df = get_data()

    max=df['t'].max()
    # marks={str(t): str(datetime.datetime.strptime(str(t), "%Y%m%d%H%M%S")) for t in df['t'].unique()}
    marks={str(t): str(t) for t in df['t'].unique()}
    return max, marks

@app.callback(
    Output('example-graph', 'figure'),
    Input('Time-Slider', 'value'))
def update_figure(selected_t):
    global df
    df = get_data()
    filtered_df = df[(df.t) <= (selected_t)]

    fig = px.line(filtered_df, x="x", y="y", title="Navigation", markers=True) 

    fig.update_layout(transition_duration=500)
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    fig.update_layout(
        # autosize=False,
        width=800,
        height=800,
    )
    fig.update_layout(yaxis_range=[-1000,1000])
    fig.update_layout(xaxis_range=[-1000,1000])

    return fig

@app.callback(
    Output('hidden-div','lang'),
    Input('submit-val', 'n_clicks'),

)
def update_output(n_clicks):
    req = requests.request('POST', 'http://192.168.43.24:80/')
    return 'en'

if __name__ == '__main__':
    app.run_server(debug=True)




