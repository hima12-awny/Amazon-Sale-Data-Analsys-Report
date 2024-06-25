

from networkx import dfs_edges
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from polars import col
import humanize
from dash import (
    html,
)
import dash_bootstrap_components as dbc
import polars as pl
from polars import col

import warnings
warnings.filterwarnings('ignore')

# Load and prepare data
df_ = pl.read_csv('Amazon_Sale_Report_Cleaned.csv')
df_ = df_.with_columns([
    col("Date")                 .str.strptime(pl.Date, format="%Y-%m-%d"),
    col("Qty")                  .cast(pl.UInt8),
    col("Amount")               .cast(pl.Float32),
    col("ship-postal-code")     .cast(pl.UInt32),
    col("promotion_type1_count").cast(pl.UInt8),
    col("promotion_type2_count").cast(pl.UInt8),
    col("B2B").replace({False: "B2C", True: "B2B"})
])

df_ = df_.with_columns([
    pl.col('Date').dt.strftime('%B').alias('Month')
])

location_df = pd.read_csv('ship-city-location.csv')
location_df = location_df.set_index('ship-city')

promotion_types = [
    'all',
    'Amazon PLCC Free-Financing Universal Merchant',
    'IN Core Free Shipping',
    "No"
]


def pie_status_dist(df) -> go.Figure:

    status_dist = df['Status'].value_counts().sort(
        by='count').top_k(5, by='count')

    fig = px.pie(
        status_dist.to_pandas(),
        names='Status',
        values='count',
        template='seaborn',
        height=400,
    )
    return fig


def bar_order_count(df) -> go.Figure:

    t_df = df.group_by([col("Date").dt.month().alias("Month")]).agg(
        col("Order-ID").count().alias("Order Count")
    ).sort(by='Order Count', descending=True)\
        .to_pandas()

    fig = px.bar(t_df,
                 x='Month',
                 y='Order Count',
                 template='seaborn',
                 height=400,
                 orientation='v'
                 )
    return fig


def bar_top_amount_cat(df) -> go.Figure:

    tdf = df.group_by('Category').agg(
        (col('Amount').sum()/10e6).alias('Mean Amount')
    ).sort(by='Mean Amount', descending=True).to_pandas()

    fig = px.bar(tdf,
                 x='Category',
                 y='Mean Amount',
                 height=400,
                 template='seaborn',
                 orientation='v')
    return fig


def gen_map_df_based_count(col_name, df):

    if len(df) == 0:
        return df

    tdf = df.group_by(['ship-city', 'ship-state']).agg(
        col(col_name).count().name.suffix('_count')
    ).top_k(20, by=f'{col_name}_count').to_pandas()

    def get_lat_lon(row):
        city = row['ship-city']
        if city in location_df.index:
            lat_lon = location_df.loc[city]
            return (lat_lon['Latitude'], lat_lon['Longitude'])
        else:
            return (None, None)

    lat_lon_values = tdf.apply(
        lambda row: get_lat_lon(row), axis=1, result_type='expand'
    )

    tdf[['latitude', 'longitude']] = lat_lon_values

    new_tdf = tdf.dropna(
        subset=['latitude', 'longitude']).reset_index(drop=True)

    return new_tdf


def gen_map_df_based_sum(col_name, df):

    tdf = df.group_by(['ship-city', 'ship-state'])\
        .agg(col(col_name).sum().name.suffix('_sum'))\
        .top_k(20, by=f'{col_name}_sum').to_pandas()

    tdf[['latitude', 'longitude']] = tdf.apply(
        lambda row:
            location_df
            .loc[row['ship-city']],
            axis=1,
            result_type='expand'
    )

    return tdf


def gen_map_chart(tdf, col_name, title_col_name):

    # Create the scatter plot on the map
    fig = px.scatter_geo(
        tdf,
        lat='latitude',
        lon='longitude',
        size=col_name,
        color='ship-city',
        height=400,
        template='seaborn',
        hover_name='ship-city',
        hover_data={
            'ship-state': True,
            col_name: True,
            'latitude': False,
            'longitude': False
        },
        projection='natural earth',

    )
    fig.update_layout(
        geo=dict(
            scope='asia',  # Focus on the Asia region, including India
            coastlinecolor="gray",
            projection_scale=3,  # Adjust for zoom level
            center={"lat": 20.5937, "lon": 78.9629}  # Center of India
        )
    )
    return fig


def gen_map_chart_type(df, col_name, title_col_name, type='count') -> go.Figure:

    tdf = gen_map_df_based_count(col_name, df)
    return gen_map_chart(tdf, f'{col_name}_count', title_col_name)


def gen_b2b_b2c_scatter_plot(df) -> tuple[go.Figure, go.Figure]:

    t_df = df\
        .select(['Date', 'B2B', 'Order-ID'])\
        .group_by(["Date", 'B2B'])\
        .agg(col('Order-ID').count().alias('Number Of Orders'))

    b2b_data = t_df.filter(col('B2B') == 'B2B').to_pandas()
    b2c_data = t_df.filter(col('B2B') == 'B2C').to_pandas()

    fig1 = px.scatter(
        b2b_data,
        x='Date',
        y='Number Of Orders',
        title='B2B',
        template='seaborn',
        color_discrete_sequence=['red']
    )

    fig2 = px.scatter(
        b2c_data,
        x='Date',
        y='Number Of Orders',
        title='B2C',
        template='seaborn',
        color_discrete_sequence=['blue']
    )

    return (fig1, fig2)


def scatter_fulfilment(df) -> go.Figure:

    tdf = df.group_by(['Date', 'Fulfilment']).agg(
        col('Order-ID').count().alias('order_count')).to_pandas()

    return px.scatter(
        tdf,
        x='Date',
        y='order_count',
        color='Fulfilment',
        template='seaborn',
    )


def makeNum(num: str):
    if '.0' in num:
        return num.replace('.0', '')
    return num


def num_str(num):

    n_str = humanize.intword(num)

    char = {
        'thousand': 'K',
        'million': 'M',
        'billion': 'B'
    }

    if len(n_str.split()) == 2:
        num, abv = n_str.split()
        abv = char[abv]
        num = makeNum(num)
        return num+abv

    return makeNum(n_str)


def gen_stat_card(stat_num, text, id_):

    if isinstance(stat_num, int) or isinstance(stat_num, float):
        stat_num = str(int(stat_num))

    stat_res = stat_num if '$' in stat_num else num_str(stat_num)

    return dbc.Container([
        dbc.Col([
            html.H1(
                stat_res,
                id=id_,
                style={
                    'fontWeight': 'bold'
                }),
            html.P(text, style={'font-size': '15px'})
        ],
            style={
            'color': '#fff',
            'textAlign': 'center',
            'background': '#0E2446',
            'border-radius': '15px',
            'padding': '10px',
        },
            align='center'
        )
    ])


def get_sum_amount_qty(df):
    total_amount = df['Amount'].sum()
    total_qty = df['Qty'].sum()
    return (
        gen_stat_card(total_amount, 'Total Amount', 'total-amount'),
        gen_stat_card(total_qty, 'Total Quantity', 'total-qty'),
    )


def filer_df(
        status,
        courier_status,
        category,
        month,
        fulfilment,
        promotion_type,
        b2b,
        day_range) -> pl.DataFrame:

    print(f"{'-'*20}\nFiltering dataframe...")

    filtered_df = df_

    in_list = {
        'Status': status,
        "Courier-Status": courier_status,
        "Category": category,
        "Month": month,
        "Fulfilment": fulfilment,
        "B2B": b2b
    }

    for in_attr, in_options in in_list.items():

        print(f"Filtering by {in_attr}: {in_options}")

        if not in_options and len(in_options) == 0:
            continue

        in_options = in_options if isinstance(
            in_options, list) else [in_options]

        if 'all' in in_options:
            continue

        filtered_df = filtered_df.filter(
            pl.col(in_attr).is_in(in_options)
        )

    if promotion_type:
        promotion_type = promotion_type if isinstance(
            promotion_type, list) else [promotion_type]

        print(f"Filtering by promotion type: {promotion_type}")

        if 'all' not in promotion_type:

            if 'No' in promotion_type:
                filtered_df = filtered_df.filter(
                    pl.col('promotion_type1_count').is_in([0]) &
                    pl.col('promotion_type2_count').is_in([0])
                )

            elif promotion_types[1] in promotion_type and \
                    promotion_types[2] in promotion_type:

                filtered_df = filtered_df.filter(
                    pl.col('promotion_type1_count') > 0
                    | pl.col('promotion_type2_count') > 0
                )
            elif promotion_types[1] in promotion_type:
                filtered_df = filtered_df.filter(
                    pl.col('promotion_type1_count') > 0
                )
            elif promotion_types[2] in promotion_type:
                filtered_df = filtered_df.filter(
                    pl.col('promotion_type2_count') > 0
                )

        elif 'No' in promotion_type and 'all' not in promotion_type:
            filtered_df = filtered_df.filter(
                pl.col('promotion_type1_count').is_in([0]) &
                pl.col('promotion_type2_count').is_in([0])
            )

    min_day, max_day = day_range
    print(f"Filtering by day range: {min_day} - {max_day}")
    filtered_df = filtered_df.filter(
        pl.col('Date').dt.day().is_between(min_day, max_day))

    print("Filtering completed.")

    return filtered_df
