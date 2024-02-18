import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from components.main_navigation_bar import navigation_bar
from components.database_connector import get_user_handles, read_query, write_query

app = Dash(
		title = "Little Lemon App",
		external_stylesheets = [dbc.themes.CERULEAN]
		)
server = app.server

connection, cursor =  get_user_handles("admin", "admin")

tables_list = read_query(cursor, """SHOW TABLES""")["Tables_in_littlelemondb"].tolist()

#------------------------ App layout Components ------------------------#

table_dropdown = dcc.Dropdown(
	[{"label": " ".join(table.split("_")).title(), "value":table} for table in tables_list],
	tables_list[0],
	placeholder = "Select Table",
	id = "drop_down_for_tables",
	searchable = False
	)
view_table_pane = [
	html.P(),
	dbc.Row(
		[
			dbc.Col(html.H6("Select a Table"), width = 2, align = "center"),
			dbc.Col(table_dropdown, width = 10)
		]
		),
	html.P(),
	html.P(id = "grid_location"),
	]

graphics_dropdown = dcc.Dropdown(
	["Time series", "Bar Chart", "Histogram", "Pie Plot"],
	"Time series",
	placeholder = "Select Graphics",
	searchable = False
	)
view_graphics_pane = [
	html.P(),
	dbc.Row(
		[
			dbc.Col(html.H6("Select a Visualization"), width = 4, align = "center"),
			dbc.Col(graphics_dropdown, width = 8)
		]
		),
	html.P(),
	dbc.Card(dbc.CardBody(dcc.Graph(id = "graph_location")))
	]

#------------------------ App Layout ------------------------#
app.layout = dbc.Container(
	[
		dbc.Row(dbc.Col(navigation_bar)),
		dbc.Row(
			[
				dbc.Col(view_table_pane, width = 7),
				dbc.Col(view_graphics_pane, width = 5)
			]
			)
	],
	fluid = True
)

#------------------------ Callbacks ------------------------#

@callback(
	Output("grid_location", "children"),
	Input("drop_down_for_tables", "value")
	)
def update_grid_table(selected_table):
	if not selected_table:
		return "No table Selected. Kindly select a table from the above dropdown."
	query = f""" SELECT * FROM {selected_table} """
	df = read_query(cursor, query)

	grid = dag.AgGrid(
		rowData = df.to_dict('records'),
		columnDefs = [{"field": i, "filter":True} for i in df.columns],
		columnSize = "sizeToFit",
		style = {"height":"76vh"}
	)
	return grid

if __name__ == "__main__":
	app.run_server(debug = True)