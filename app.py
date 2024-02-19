import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from components.main_navigation_bar import navigation_bar
from components.database_connector import read_query, write_query
import plotly.express as px
##from dash_bootstrap_templates import load_figure_template

#---------------------------------- Initialize the app ----------------------------------#
app = Dash(
		title = "Little Lemon App",
		external_stylesheets = [dbc.themes.SANDSTONE]
		)
server = app.server

##load_figure_template("sandstone")

#------------------------ Get the list of tables in the database ------------------------#

tables_list = read_query("""SHOW TABLES""")["Tables_in_littlelemondb"].tolist()

#------------------------------------ Get a dataframe -----------------------------------#
def get_df(table_name):
	select_data = f""" SELECT * FROM {table_name} """
	if select_data:
		df = read_query(select_data)
		return df
	else:
		return None
#-------------------------------- App layout Components ---------------------------------#

tables_dropdown = dcc.Dropdown(
	[{"label": " ".join(table.split("_")).title(), "value":table} for table in tables_list],
	tables_list[0],
	placeholder = "Select Table",
	id = "drop_down_for_tables",
	searchable = False
	)
tables_pane = [
	html.P(),
	dbc.Row(
		[
			dbc.Col(html.H6("Selected Table"), width = 2, align = "center"),
			dbc.Col(tables_dropdown, width = 10)
		]
		),
	html.P(),
	html.P(id = "grid_location"),
	]


graphs_list_switch = dbc.Switch(
	label = "All tables",
	value = True,
	id = "graphs_switch"
	)
graphs_dropdown = dcc.Dropdown(
	["Time series", "Bar Chart", "Histogram", "Pie Plot"],
	"Time series",
	placeholder = "Select Graphics",
	searchable = False
	)
graphs_pane = [
	html.P(),
	dbc.Row(
		[
		dbc.Col(html.H6("Select Graphs"), width = 3, align = "center"),
		dbc.Col(graphs_list_switch, width = 3, align = "center"),
		dbc.Col(graphs_dropdown, width = 6)
		]
		),
	html.P(),
	dbc.Card(
		dbc.CardBody(
			dcc.Graph(
				id = "graph_location",
				config = {"displaylogo" : False, "displayModeBar" : False},
				)
			),
		color = "secondary",
		outline = True
		)
	]

#----------------------------------- App Layout -----------------------------------#
app.layout = dbc.Container(
	[
	dbc.Row(dbc.Col(navigation_bar)),
	dbc.Row(
		[
		dbc.Col(tables_pane, width = 7),
		dbc.Col(graphs_pane, width = 5)
		]
		)
	],
	fluid = True
	)

#----------------------------------- Callbacks -----------------------------------#

@callback(
	Output("grid_location", "children"),
	Input("drop_down_for_tables", "value")
	)
def update_grid_table(selected_table):
	if not selected_table:
		return "No table Selected. Kindly select a table from the above dropdown."
	gdf = get_df(selected_table)

	grid = dag.AgGrid(
		rowData = gdf.to_dict('records'),
		columnDefs = [{"field": i, "filter":True} for i in gdf.columns],
		columnSize = "sizeToFit",
		style = {"height":"76vh"}
	)
	return grid


@callback(
	Output("graph_location", "figure"),
	Input("drop_down_for_tables", "value")
	)
def update_graph(table_name):
	if table_name == "orders":
		data = get_df(table_name)
		fig = px.scatter(data, x = "order_date", y = "total_quantity")
	else:
		dummy_df = pd.DataFrame({
			"mx":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
			"my":[20, 5, 63, 4, 14, 52, 4, 8, 63, 5]})
		fig = px.scatter(dummy_df, x = "mx", y = "my")

	fig.update_layout(
		template = "plotly_white",
		margin = {"l": 0, "r": 0, "t": 0, "b": 0})
	fig.update_xaxes(showline=True, linecolor='black')
	fig.update_yaxes(showline=True, linecolor='black')
	return fig

if __name__ == "__main__":
	app.run_server(debug = True)