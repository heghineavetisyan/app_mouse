import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load data
mouse_data = pd.read_csv('Mouse_metadata.csv')
study_results = pd.read_csv('Study_results.csv')
merged_df = pd.merge(mouse_data, study_results, on='Mouse ID')

# External stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Design parameters
colors = {
    'full-background': '#DCDCDC',
    'block-borders': '#000000'
}

margins = {
    'block-margins': '10px 10px 10px 10px',
    'block-margins': '4px 4px 4px 4px'
}

sizes = {
    'subblock-heights': '290px'
}

# Title
div_title = html.Div(
    children=html.H1('Drug Analysis Dashboard'),
    style={
        'border': '3px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'text-align': 'center'
    }
)

# Chart 1: Histogram of mice weights for each drug
div_1_1_button = dcc.Checklist(
    id='weight-histogram-checklist',
    options=[
        {'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])
    ],
    value=['Placebo'],
    labelStyle={'display': 'inline-block'}
)

div_1_1_graph = dcc.Graph(id='weight-histogram')

div_1_1 = html.Div(
    children=[div_1_1_button, div_1_1_graph],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '50%',
        'height': sizes['subblock-heights']
    }
)

# Chart 2: Weight Distribution Comparison (Using RadioItems)
div_1_2_radio = dcc.RadioItems(
    id='drug-type-chart-2',
    options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
    value='Placebo',
    labelStyle={'display': 'inline-block'}
)

div_1_2_graph = dcc.Graph(id='weight-distribution-comparison-graph')

div_1_2 = html.Div(
    children=[div_1_2_radio, div_1_2_graph],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '50%',
        'height': sizes['subblock-heights']
    }
)

# Collecting Chart 1 and Chart 2 into a row
div_row1 = html.Div(
    children=[div_1_1, div_1_2],
    style={
        'border': '3px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'display': 'flex',
        'flex-flow': 'row nowrap'
    }
)

# Chart 3: Weight Distribution Histogram with Checklist
div_2_1_dropdown = dcc.Checklist(
    id='weight-histogram-checklist-2',
    options=[
        {'label': 'Lightweight', 'value': 'Lightweight'},
        {'label': 'Heavyweight', 'value': 'Heavyweight'},
        {'label': 'Placebo', 'value': 'Placebo'}
    ],
    value=['Placebo'],
    labelStyle={'display': 'inline-block'}
)

div_2_1_graph = dcc.Graph(id='weight-histogram-chart3')

div_2_1 = html.Div(
    children=[div_2_1_dropdown, div_2_1_graph],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '50%',
        'height': sizes['subblock-heights']
    }
)

# Chart 4: Survival Function for All Drugs
div_2_2_dropdown = dcc.Checklist(
    id='drug-type-chart-4',
    options=[
        {'label': 'Lightweight', 'value': 'Lightweight'},
        {'label': 'Heavyweight', 'value': 'Heavyweight'},
        {'label': 'Placebo', 'value': 'Placebo'}
    ],
    value=['Placebo'],
    labelStyle={'display': 'inline-block'}
)

div_2_2_graph = dcc.Graph(id='survival-function-chart')

div_2_2 = html.Div(
    children=[div_2_2_dropdown, div_2_2_graph],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '50%',
        'height': sizes['subblock-heights']
    }
)

# Collecting Chart 3 and Chart 4 into a row
div_row2 = html.Div(
    children=[div_2_1, div_2_2],
    style={
        'border': '3px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'display': 'flex',
        'flex-flow': 'row nowrap'
    }
)

# Collecting all DIVs in the final layout DIV
app.layout = html.Div(
    children=[
        div_title,
        div_row1,
        div_row2
    ],
    style={'backgroundColor': colors['full-background']}
)

# Callback for Chart 1
@app.callback(
    Output(component_id='weight-histogram', component_property='figure'),
    [Input(component_id='weight-histogram-checklist', component_property='value')]
)
def update_weight_histogram(drug_names):
    traces = []
    for drug in drug_names:
        traces.append(go.Histogram(
            x=mouse_data[mouse_data['Drug Regimen'] == drug]['Weight (g)'],
            name=drug,
            opacity=0.9
        ))
    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            xaxis={'title': 'Mouse weight'},
            yaxis={'title': 'Number of mice'},
            autosize=False,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1}
        )
    }

# Callback for Chart 2
@app.callback(
    Output('weight-distribution-comparison-graph', 'figure'),
    [Input('drug-type-chart-2', 'value')]
)
def update_weight_distribution_comparison(drug_type):
    selected_drug_data = mouse_data[mouse_data['Drug Regimen'] == drug_type]
    selected_weights = selected_drug_data['Weight (g)']
    overall_weights = merged_df['Weight (g)']
    trace_selected = go.Histogram(x=selected_weights, name=drug_type)
    trace_overall = go.Histogram(x=overall_weights, name='Overall')
    layout = dict(title='Weight Distribution Comparison',
                  xaxis={'title': 'Mouse Weight (g)'},
                  yaxis={'title': 'Number of Mice'},
                  barmode='overlay')
    return {'data': [trace_selected, trace_overall],
            'layout': layout}

# Callback for Chart 3
@app.callback(
    Output('weight-histogram-chart3', 'figure'),
    [Input('weight-histogram-checklist-2', 'value')]
)
def update_weight_histogram_chart3(selected_drugs):
    traces = []
    for drug in selected_drugs:
        traces.append(go.Histogram(
            x=mouse_data[mouse_data['Drug Regimen'] == drug]['Weight (g)'],
            name=drug,
            opacity=0.9
        ))
    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            xaxis={'title': 'Mouse weight'},
            yaxis={'title': 'Number of mice'},
            autosize=False,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1}
        )
    }

# Callback for Chart 4
@app.callback(
    Output('survival-function-chart', 'figure'),
    [Input('drug-type-chart-4', 'value')]
)
def update_survival_function(drug_names):
    traces = []
    for drug in drug_names:
        drug_data = merged_df[merged_df['Drug Regimen'] == drug]
        survival_function = []
        timepoints = sorted(drug_data['Timepoint'].unique())
        for time in timepoints:
            num_alive = len(drug_data[drug_data['Timepoint'] >= time]['Mouse ID'].unique())
            survival_function.append(num_alive)
        traces.append(go.Scatter(
            x=timepoints,
            y=survival_function,
            mode='lines+markers',
            name=drug
        ))
    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Time'},
            yaxis={'title': 'Number of Mice Alive'},
            autosize=False,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1}
        )
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
