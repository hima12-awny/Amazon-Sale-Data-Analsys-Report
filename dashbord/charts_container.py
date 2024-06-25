
from dash import (
    dcc,
    html,
)
import dash_bootstrap_components as dbc
from helper_functions import *


container_level_1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    stat_num
                )
                for stat_num in get_sum_amount_qty(df_)
            ]
        )
    ],
    style={'margin-top': '50px'}
),

container_level_2 = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                [
                    dbc.Row([
                        html.H1("Top 5 Order Status",
                                style={'color': '#fff', }),
                    ]),
                    dcc.Graph(
                        id='pie_status_dist',
                        figure=pie_status_dist(df_),
                        style={'background': '#fff',
                               'border-radius': '20px',
                               'padding': '10px'}
                    )
                ],
                style={
                    'margin-top': '30px',
                }
            ),
            dbc.Col(
                [
                    dbc.Row([
                        html.H1("Number Order Overs Months",
                                style={'color': '#fff', }),
                    ]),
                    dcc.Graph(
                        id='bar_order_count',
                        figure=bar_order_count(df_),
                        style={'background': '#fff',
                               'border-radius': '20px',
                               'padding': '10px'}
                    )
                ], style={
                    'margin-top': '30px',
                }
            )
        ]),
    ]
),

container_level_3 = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                dbc.Row([
                    html.H2("Mean Amount by Category in Million",
                            style={'color': '#fff', }),
                ]),
                dcc.Graph(
                    id='bar_top_amount_cat',
                    figure=bar_top_amount_cat(df_),
                    style={'background': '#fff',
                           'border-radius': '20px',
                           'padding': '10px'}
                ),
            ],
            style={
                'margin-top': '30px',
            }
        ),
        dbc.Col(
            [
                dbc.Row([
                    html.H1("Number Of Orders over Cities",
                            style={'color': '#fff', }),
                ]),
                dcc.Graph(
                    id='map_order_count',
                    figure=gen_map_chart_type(
                        df_, 'Order-ID', 'Number Of Orders', 'count'),
                    style={'background': '#fff',
                           'border-radius': '20px',
                           'padding': '10px'}
                ),
            ],
            style={
                'margin-top': '30px',
            }
        )
    ],
    )
]),


container_level_4 = dbc.Container([

    dbc.Row([
        html.H1("Amazon B2B vs. B2C", style={'color': '#fff', }),
    ]),

    dbc.Row(
        children=[
            dbc.Col(
                dcc.Graph(
                    id=f'b2b_b2c_scatter_{i}',
                    figure=fig,
                    style={'background': '#fff',
                           'border-radius': '20px',
                           'padding': '10px'}
                )
            )
            for i, fig in enumerate(gen_b2b_b2c_scatter_plot(df_))
        ]
    )
], style={
    'margin-top': '30px',
}),


container_level_5 = dbc.Container([
    dbc.Row([
        html.H1("Fulfilment Types Over Time",
                style={'color': '#fff', }),
    ]),

    dbc.Row(
        [
            dcc.Graph(
                id=f'scatter_fulfilment',
                figure=scatter_fulfilment(df_),
                style={'background': '#fff',
                       'border-radius': '20px',
                       'padding': '10px'}
            )
        ]
    )
], style={
    'margin-top': '30px',
})


container_level_5 = dbc.Container([
    dbc.Row([
        html.H1("Fulfilment Types Over Time",
                style={'color': '#fff', }),
    ]),

    dbc.Row(
        [
            dcc.Graph(
                id=f'scatter_fulfilment',
                figure=scatter_fulfilment(df_),
                style={'background': '#fff',
                       'border-radius': '20px',
                       'padding': '10px'}
            )
        ]
    )
], style={
    'margin-top': '30px',
})
