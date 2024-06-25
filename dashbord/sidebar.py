from helper_functions import *

from dash import (
    dcc,
    html,
)

promotion_types = [
    'all',
    'Amazon PLCC Free-Financing Universal Merchant',
    'IN Core Free Shipping',
    "No"
]

all_unique_options = {
    'Status':  ['all'] + df_['Status'].unique().to_list(),
    'Courier Status': ['all'] + df_['Courier-Status'].unique().to_list(),
    'Category': ['all'] + df_['Category'].unique().to_list(),
    'Month': ['all'] + df_['Month'].unique().to_list(),
    'Fulfilment':  ['all'] + df_['Fulfilment'].unique().to_list(),
    'Promotion Type':  promotion_types,
    'B2B/B2C': ['all', 'B2B', 'B2C']
}

all_options_dropdowns_ = [
    [
        html.Label(f"Select {attr_name}:"),
        dcc.Dropdown(
            id=f'{attr_name}-dropdown',
            options=[{'label': opt, 'value': opt}
                     for opt in attr_options],
            value='all',
            clearable=False,
            multi=True
        ),
        html.Br()
    ]

    for attr_name, attr_options in all_unique_options.items()
]
all_options_dropdowns = []
for i in all_options_dropdowns_:
    all_options_dropdowns.extend(i)


# Define the sidebar with input components
sidebar = html.Div(
    [
        dbc.Card(
            [
                html.H4("Filter Options", style={'color': '#25426D'}),

                *all_options_dropdowns,

                html.Label("Select Day Range:"),
                dcc.RangeSlider(
                    id='day-slider',
                    min=1,
                    max=31,
                    value=[1, 31],
                    step=1,
                    marks={i: str(i) for i in range(1, 32, 5)}
                ),
                html.Br(),
            ],
            style={
                'padding': '10px',
                'backgroundColor': '#F8F9FA',
                'borderRadius': '10px',
                "box-shadow": "5px 5px 15px rgba(0,0,0,0.1)"
            },

        ),

    ],
    style={
        'width': '24%',  # Ensure fixed width for sidebar
        'padding': '20px',
        'position': 'fixed',  # Fix position for sidebar
        'top': '0',  # Stick to top of viewport
        'bottom': '0',  # Stick to bottom of viewport
        'overflow': 'auto',  # Enable scrolling in sidebar
        'height': '100vh',  # Full viewport height
        'backgroundColor': '#1E3456',
        'zIndex': 1000,  # Higher z-index to stay above main content
        'box-shadow': '5px 0 15px rgba(0,0,0,0.1)'  # Shadow for visibility

    }
)
