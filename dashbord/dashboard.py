
from dash import (
    Dash,
    dcc,
    html,
    callback,
    Input, Output
)
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

from sidebar import *
from charts_container import *


# Initialize Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Amazon Sale Dashboard'


# Header title
head_title = dbc.Card(
    dbc.CardBody(html.H1("Amazon Sale Dashboard", style={'color': '#fff', })),
    style={
        'width': '500px',
        'borderRadius': '10px',
        "box-shadow": "11px 9px 0px #FFFFFF",
        'backgroundColor': '#25426D',
        'fontWeight': 'bold'
    }
)


main_content = html.Div(
    children=[
        head_title,

        *container_level_1,

        *container_level_2,
        *container_level_3,


        *container_level_4,
        container_level_5
    ],
    style={
        'width': '75%',
        'display': 'inline-block',
        'verticalAlign': 'top',
        'padding': '15px',
        'marginLeft': '24%',
        'box-sizing': 'border-box'
    }
)

app.layout = html.Div(
    [
        sidebar,
        main_content
    ],
    style={
        'display': 'flex',
        'flex-direction': 'row',
        'backgroundColor': '#1E3456',
        'width': '100%',
        'height': '100%',
    }
)


@app.callback(
    [
        Output('total-amount', 'children'),
        Output('total-qty', 'children'),

        Output('pie_status_dist', 'figure'),
        Output('bar_order_count', 'figure'),
        Output('bar_top_amount_cat', 'figure'),
        Output('map_order_count', 'figure'),

        Output('b2b_b2c_scatter_0', 'figure'),
        Output('b2b_b2c_scatter_1', 'figure'),

        Output('scatter_fulfilment', 'figure'),

    ],

    [
        *[
            Input(f'{attr_name}-dropdown', 'value')
            for attr_name in all_unique_options.keys()
        ],

        Input('day-slider', 'value')
    ]
)
def update_main_content(
    status,
    courier_status,
    category,
    month,
    fulfilment,
    promotion_type,
    b2b,
    day_range
):

    new_df = filer_df(status, courier_status, category, month,
                      fulfilment, promotion_type, b2b, day_range)

    gen_graphs = len(new_df) > 0

    if not gen_graphs:
        return (

            *['0']*2,
            *[go.Figure()]*7
        )

    total_amount = num_str(new_df['Amount'].sum())
    total_qty = num_str(new_df['Qty'].sum())
    b2b_and_b2c_charts = gen_b2b_b2c_scatter_plot(new_df)

    return (
        total_amount,
        total_qty,
        pie_status_dist(new_df),
        bar_order_count(new_df),
        bar_top_amount_cat(new_df),
        gen_map_chart_type(new_df, 'Order-ID', 'Number Of Orders', 'count'),
        b2b_and_b2c_charts[0],
        b2b_and_b2c_charts[1],
        scatter_fulfilment(new_df),
    )


if __name__ == '__main__':
    app.run_server(debug=True)
