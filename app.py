"""
Application for entering pricing data and displaying basic analytics
"""
# Built-ins
import datetime
from turtle import update

import dash_bootstrap_components as dbc

# 3rd-party
import plotly.express as px
from dash import Dash, Input, Output, State, ctx, dash_table, dcc, html

# Internal
from cpi import Observation

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    [
        html.H1("Data Entry Dashboard", id="header"),
        html.Div(
            [
                html.Div(
                    children=[
                        html.H1("Price Observation Data Entry"),
                        html.Br(),
                        html.Label("Date"),
                        dcc.DatePickerSingle(date=datetime.date.today(), id="date-input"),
                        html.Br(),
                        html.Label("Category"),
                        dcc.Dropdown(
                            options=Observation.available_categories(),
                            value="Food",
                            id="category-input",
                        ),
                        html.Br(),
                        html.Label("Item"),
                        dcc.Dropdown(
                            options=Observation.available_items(),
                            value="USDA Grade-A eggs",
                            id="item-input",
                        ),
                        html.Br(),
                        html.Label("Price"),
                        dbc.Input(type="number", id="price-input", min=0, step=0.01),
                        html.Br(),
                        html.Label("State"),
                        dcc.Dropdown(
                            options=Observation.available_states(),
                            value="Texas",
                            id="state-input",
                        ),
                        html.Br(),
                        html.Label("City"),
                        dcc.Dropdown(
                            options=Observation.available_cities(),
                            value="Dallas",
                            id="city-input",
                        ),
                        html.Br(),
                        dbc.Button(
                            "Save Observation",
                            color="success",
                            className="me-1",
                            id="save-button",
                            n_clicks=0,
                        ),
                        html.Br(),
                        html.Br(),
                        html.Label("Number of Matching Observations to delete"),
                        dbc.Input(type="number", value=1, id="delete-n-observations"),
                        html.Br(),
                        html.Label("Delete Most Recent First?"),
                        dbc.Checklist(
                            options=[
                                {"label": "Yes"},
                            ],
                            id="delete-most-recent-toggle",
                        ),
                        html.Br(),
                        dbc.Button(
                            "Delete Matching Observations",
                            color="danger",
                            className="me-1",
                            id="delete-button",
                            n_clicks=0,
                        ),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
                html.Div(
                    children=[
                        html.Label("Graph Type"),
                        dcc.Dropdown(
                            options=[
                                "Item Prices Over Time",
                                "Average Item Price by City",
                            ],
                            value="Item Prices Over Time",
                            id="graph-type",
                        ),
                        dcc.Graph(
                            figure=px.scatter(
                                Observation.table_df(),
                                x="Date",
                                y="Price",
                                color="Item",
                                title="Item Prices Over Time",
                            ),
                            id="observation-graph",
                        ),
                        html.H3(
                            "Table of Observations", style={"text-align": "center"}
                        ),
                        dash_table.DataTable(
                            Observation.table_df().to_dict("records"),
                            id="observation-table",
                            # style dash table
                            style_table={"height": "400px", "overflowY": "auto"},
                            style_cell={"textAlign": "center", "padding": "5px"},
                        ),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
    ],
)


@app.callback(
    Output(component_id="observation-table", component_property="data"),
    Output(component_id="observation-graph", component_property="figure"),
    Input(component_id="save-button", component_property="n_clicks"),
    Input(component_id="delete-button", component_property="n_clicks"),
    Input(component_id="graph-type", component_property="value"),
    Input(component_id="date-input", component_property="date"),
    State(component_id="category-input", component_property="value"),
    State(component_id="item-input", component_property="value"),
    State(component_id="price-input", component_property="value"),
    State(component_id="state-input", component_property="value"),
    State(component_id="city-input", component_property="value"),
    State(component_id="delete-n-observations", component_property="value"),
)
def update_observation(
    n_clicks: float,
    n_clicks2,
    graph_type: str,
    date: str,
    category: str,
    item: str,
    price: str,
    state: str,
    city: str,
    observations_to_delete,
    *args
):
    triggered_id = ctx.triggered_id  # Id of the input that triggered the callback

    if triggered_id == "graph-type":
        return update_graph(graph_type, date)

    if triggered_id == "date-input":
        if graph_type != "Average Item Price by City":
            return update_graph(graph_type, date)
        return update_graph("Average Item Price by City", date)

    elif triggered_id == "delete-button":
        return delete_observations(
            n_clicks2=n_clicks2,
            date=date,
            category=category,
            item=item,
            price=price,
            state=state,
            city=city,
            observations_to_delete=observations_to_delete,
        )
    else:
        if n_clicks >= 1:
            obj = Observation(
                Date=datetime.datetime.strptime(date, "%Y-%m-%d").date(),
                Category=category,
                Item=item,
                Price=float(price),
                State=state,
                City=city,
            )
            obj.write()
        df = Observation.table_df()
        return df.to_dict("records"), px.scatter(df, x="Date", y="Price", color="Item")


def delete_observations(
    n_clicks2, observations_to_delete, date, category, state, city, price, item
):
    """
    Function to delete an Observation using the data from the entry.
    """
    if n_clicks2 >= 1:
        number_to_delete = observations_to_delete
        obj = Observation(
            Date=datetime.datetime.strptime(date, "%Y-%m-%d").date(),
            Category=category,
            Item=item,
            Price=float(price),
            State=state,
            City=city,
        )
        obj.delete_matching(
            state=state,
            city=city,
            date=date,
            category=category,
            n_to_delete=number_to_delete,
        )
    df = Observation.table_df()
    return df.to_dict("records"), px.scatter(df, x="Date", y="Price", color="Item")


def update_graph(graph_type: str, date: str):
    if graph_type == "Average Item Price by City":
        df = Observation.table_df()
        # The selected date is not represented the same way in the dataframe.
        # Hence the selected date is modified to match that of the dataframe to
        # enable filtering of the data.
        date_format_for_custom_added_data = str(
            datetime.datetime.strptime(date, "%Y-%m-%d").date()
        )
        date_format_for_preinstantiated_data = str(
            datetime.datetime.strptime(date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        )
        data_for_selected_date = df.loc[
            (df["Date"] == date_format_for_preinstantiated_data)
            | (df["Date"] == date_format_for_custom_added_data)
        ]
        return df.to_dict("records"), px.bar(
            data_for_selected_date.groupby(["City", "Item"]).mean().reset_index(),
            x="Item",
            y="Price",
            color="City",
            hover_data=["Item"],
            barmode="group",
        )
    df = Observation.table_df()
    return df.to_dict("records"), px.scatter(df, x="Date", y="Price", color="Item")


if __name__ == "__main__":
    app.run_server(debug=True)  # Runs at localhost:8050 by default
