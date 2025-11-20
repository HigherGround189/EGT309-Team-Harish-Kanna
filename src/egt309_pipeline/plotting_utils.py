import operator
import warnings

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")
pl.Config(set_tbl_cols=-1, fmt_str_lengths=65535, set_tbl_width_chars=65535)


def lprint(dataframe, num=-1):
    with pl.Config(tbl_rows=num):
        print(dataframe)


def cprint(input, long=False, enable_print=False):
    if enable_print:
        if long:
            lprint(input)

        else:
            print(input)


def plot_categorical(df, col_name, debug=False):
    # Compute counts and percentages of each value, along with creating the graph's display label
    counts = df[col_name].value_counts()
    counts = (
        counts.with_columns(
            # Replace null with "Missing Data"
            pl.col(col_name).fill_null("Missing Data"),
            (pl.col("count") / df.shape[0] * 100).round(2).alias("percentage"),
        )
        .with_columns(
            # Outputs in this format: <COUNT> (<PERCENT>%)
            (
                pl.col("count").cast(pl.String)
                + " ("
                + pl.col("percentage").cast(pl.String)
                + "%)"
            ).alias("display_label")
        )
        .sort("count")
    )
    cprint(counts, enable_print=debug)

    # Plots distribution bar chart
    fig = px.bar(
        counts,
        x=col_name,
        y="count",
        text="display_label",
        color="count",
        color_continuous_scale="blues",
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=f"{col_name}: %{{x}}<br>Count: %{{text}}<extra></extra>",
    )
    fig.update_layout(
        title=f"{col_name} Distribution",
        yaxis_title="Count",
        title_x=0.5,
        showlegend=False,
    )

    fig.show()


def plot_subscription_distribution_categorical(
    df, col_name, distribution_col="Subscription Status", debug=False
):
    df = df.with_columns(pl.all().exclude(pl.Int64, pl.String).cast(pl.String))
    cprint(df)

    unique_values = sorted(df[distribution_col].unique().to_list(), reverse=True)
    cprint(unique_values, enable_print=debug)

    # Count number of unique values in "Subscription Status", and alias as value name.
    counts = df.group_by(col_name).agg(
        (
            (pl.col(distribution_col) == str(value)).sum().alias(str(value))
            for value in unique_values
        ),
    )
    cprint(counts, enable_print=debug)

    # Calculate total count of each category (yes + no)
    totals = counts.select(
        pl.col(col_name),
        pl.fold(
            acc=pl.lit(0),
            function=operator.add,
            exprs=pl.all().exclude(col_name),
        ).alias("Total Count"),
    )
    cprint(totals, enable_print=debug)

    # Convert from wide -> long format, add total_counts as a column, and calculate display label
    long_counts = (
        counts.sort(by=unique_values)
        .melt(col_name)
        .join(totals, on=col_name, how="left")
        .with_columns(
            # Outputs in this format: <COUNT> (<PERCENT>%)
            (
                pl.col("value").cast(pl.String)
                + " ("
                + (pl.col("value") / pl.col("Total Count") * 100)
                .round(2)
                .cast(pl.String)
                + "%)"
            ).alias("display_label")
        )
    )
    cprint(long_counts, enable_print=debug)

    # Create Stacked bar chart
    fig = px.bar(
        long_counts,
        x=col_name,
        y="value",
        color="variable",
        custom_data=["variable"],  # To access Subscription Status in hovertemplate
        labels={"variable": distribution_col},
        text="display_label",
        barmode="stack",
        color_discrete_map={  # Hardcoded colour values cause jun hoe has an extreme reaction to the regular one
            "no": "rgb(239, 85, 59)",
            "False": "rgb(239, 85, 59)",
            "false": "rgb(239, 85, 59)",
            "yes": "rgb(99, 110, 251)",
            "True": "rgb(99, 110, 251)",
            "true": "rgb(99, 110, 251)",
        },
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=f"Subscription Status: %{{customdata[0]}}<br>{col_name}: %{{x}}<br>Count: %{{y}}<extra></extra>",
    )
    fig.update_layout(
        title=f"{col_name} Subscribed Distribution", yaxis_title="Count", title_x=0.5
    )

    fig.show()


def plot_numerical(df, col_name, distribution_col="Subscription Status", debug=False):
    # Get describe info for the column
    column = df[col_name]
    describe = (
        column.describe()
        .transpose(column_names="statistic")
        .with_columns(pl.all().round(2))
    )

    # Get unique subscription values (we need each value to have its own stacked bar)
    subscription_values = sorted(df[distribution_col].unique().to_list(), reverse=True)

    # Calculate counts and package dataframe into dict
    # Goal is to construct a dictionary like this:
    # {
    # "yes": {0: 50, 1: 30, 2: 20},
    # "no":  {0: 20, 1: 70, 2: 10}
    # }
    counts_dict = {}
    for status in subscription_values:
        value_counts = df.filter(pl.col("Subscription Status") == status)[
            col_name
        ].value_counts()
        cprint(value_counts, enable_print=debug)
        # Creates dict of this format {x_value : x_value_count}
        counts_dict[status] = dict(
            zip(value_counts[col_name].to_list(), value_counts["count"].to_list())
        )
        cprint(counts_dict, enable_print=debug)

    # Count total number of each x_value / point (bar)
    x_values = sorted(df[col_name].unique().to_list())
    total_per_x = [
        sum(counts_dict[value].get(x, 0) for value in subscription_values)
        for x in x_values
    ]  # Sums both values (eg: If Key=Campaign Call, Value=Count: {yes: {12: 1}, no: {12: 3}} -> 3 + 1 = 4; Thus, Campaign call = 12 is 4 in total)

    hist_traces = []
    for status in subscription_values:
        # Get total count (y_value), and calculate percentage
        y_values = [counts_dict[status].get(x, 0) for x in x_values]
        percents = [
            (y / total * 100) if total > 0 else 0.0
            for y, total in zip(y_values, total_per_x)
        ]
        cprint(percents, enable_print=debug)

        # Create customdata and hovertemplate for graph.
        hist_customdata = [[percentage] for percentage in percents]
        hist_hovertemplate = (
            f"{col_name}: %{{x}}<br>"
            f"{distribution_col}: {status}<br>"
            f"Count: %{{y}} (%{{customdata[0]:.1f}}%)"
        )

        # Build & collect histogram traces to stack
        hist_traces.append(
            go.Bar(  # I know that everything else has been referring to this as a histogram, but I had to do a last minute change to use go.Bar instead. Just pretend it is a histogram, they look basically the same.
                x=x_values,
                y=y_values,
                name=status,
                customdata=hist_customdata,
                hovertemplate=hist_hovertemplate,
            )
        )

    # Create boxplot trace
    box_trace = go.Box(
        x=column, name="Boxplot", hovertemplate=f"{col_name}: %{{x}}<extra></extra>"
    )

    # Combine histogram & boxplot in subplots
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.05,
    )

    # Add both histogram traces to first row
    for trace in hist_traces:
        fig.add_trace(trace, row=1, col=1)

    # Add boxplot trace to second row
    fig.add_trace(box_trace, row=2, col=1)

    # Create annotation text
    stats_text = (
        f"Min: {describe['min'][0]:g}<br>"
        f"25%: {describe['25%'][0]:g}<br>"
        f"50%: {describe['50%'][0]:g}<br>"
        f"75%: {describe['75%'][0]:g}<br>"
        f"Max: {describe['max'][0]:g}<br>"
        f"Mean: {describe['mean'][0]:g}<br>"
        f"STD: {describe['std'][0]:g}"
    )

    # Add & style annotation box
    fig.add_annotation(
        text=stats_text,
        xref="paper",
        yref="paper",
        x=0.8,
        y=0.8,
        showarrow=False,
        font=dict(size=14, color="black"),
        align="left",
        bgcolor="rgba(255,255,255,0.75)",
        bordercolor="grey",
        borderwidth=1,
        borderpad=6,
    )

    # Update layout & style, and enable stacking for histogram
    fig.update_layout(
        title=f"{col_name} Distribution",
        title_x=0.5,
        bargap=0.05,
        barmode="stack",
        margin=dict(t=60, b=40, l=40, r=40),
        showlegend=False,
    )

    fig.update_xaxes(title_text=col_name, row=2, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=1)

    fig.show()


def plot_distribution(
    df, col_name, distribution_col="Subscription Status", debug=False
):
    # Check for pandas dataframe and convert it to Polars
    if isinstance(df, pd.DataFrame):
        cprint("Pandas Detected. Converting...", enable_print=debug)
        df = pl.from_pandas(df)

    column = df[col_name]
    if (
        column.dtype == pl.Categorical
        or column.dtype == pl.String
        or column.dtype == pl.Boolean
    ):  # Added pl.Boolean here
        plot_categorical(df, col_name, debug=debug)

        if col_name != distribution_col:
            plot_subscription_distribution_categorical(
                df, col_name, distribution_col, debug=debug
            )

    else:
        plot_numerical(df, col_name, distribution_col, debug=debug)
