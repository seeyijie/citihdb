import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

app = dash.Dash()

# dummy lists
timels = [i for i in range(0,24)]
userls = []
for i in range(0,24):
	userls.append(4+np.random.randint(-3,7))
procls = []
for i in range(0,24):
	procls.append(10+np.random.randint(-5,10))



# app layout
app.layout = html.Div(children=[
    html.H1(children='Bot Monitoring',style={'font-family': 'sans-serif'}),
    html.P("This dashboard provides a quick visualisation of the user count per hour as well as the number of queries per hour. Hover over to determine the exact values! :)",style={'color': '#A9A9A9','font-family': 'sans-serif'}),
    dcc.Graph(
        id='user-graph',
        figure={
            'data': [
                {'x': timels, 'y': userls, 'type': 'bar', 'name': 'SF'}
            ],
            'layout': {
                'title': 'User Count Per Hour (24 Hour)'
            }
        }
    ),
        dcc.Graph(
        id='proc-graph',
        figure={
            'data': [
                {'x': timels, 'y': procls, 'type': 'bar', 'name': 'SF'}
            ],
            'layout': {
                'title': 'Queries Per Hour (24 Hour)'
            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)

