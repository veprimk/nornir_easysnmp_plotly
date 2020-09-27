import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import csv
import plotly.io as pio



def calculate_bps(list):
    output = []
    for i in range(0, len(list)):
        p = i-1
        if i > 0:
            output.append(8*(int(list[i]) - int(list[p]))/5)

    return output



def read_csv(filename):
    output = {}
    timestamp_list = []
    utilization_in = []
    interface_list =[]
    utilization_out = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            timestamp_list.append(row[0])
            interface_list.append(row[1])
            utilization_in.append(row[2])
            utilization_out.append(row[3])
            
    
    output["timestamp"] = timestamp_list[1:]
    output["interface"] = interface_list[1:]
    output["utilization_in"] = calculate_bps(utilization_in)
    output["utilization_out"] = calculate_bps(utilization_out)

    return output


# If you need to customize your Dash / plotly head to https://dash.plotly.com/layout 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.DataFrame(
    read_csv("172.16.3.201_interface_gi0_7.txt") # passing the csv file created...
    )
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['utilization_in'], line=dict(color='royalblue', width=3), name='Utilization In'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['utilization_out'], line=dict(color='red', width=3), name='Utilization Out'))

app.layout = html.Div(children=[
    html.H1(children='Interface Utilization Report'),

    html.Div(children='''
        Built using nornir + easysnmp + dash.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)