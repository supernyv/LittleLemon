import os
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


user = os.environ.get("USERNAME").lower()
connection, cursor =  get_user_handles(user, "admin")

query = f""" SELECT * FROM orders """
df = read_query(cursor, query)

grid = dag.AgGrid(
	rowData = df.to_dict('records'),
	columnDefs = [{"field": i} for i in df.columns],
	columnSize = "sizeToFit"
	)

table_dropdown = dcc.Dropdown(
	["Orders", "Customers", "Menus", "Menu Items"],
	"Orders",
	placeholder = "Select Table"
	)
view_table = [
	html.P(),
	table_dropdown,
	html.P(),
	html.P(grid)
	]

graphics_dropdown = dcc.Dropdown(
	["Time series", "Bar Chart", "Histogram", "Pie Plot"],
	"Time series",
	placeholder = "Select Graphics"
	)
view_graphics = [
	html.P(),
	graphics_dropdown,
	html.P(),
	dcc.Graph()
	]

app.layout = dbc.Container(
	[
		dbc.Row(dbc.Col(navigation_bar)),
		dbc.Row(
			[
				dbc.Col(view_table, width = 7),
				dbc.Col(view_graphics, width = 5)
			]
			)
	],
	fluid = True
)

if __name__ == "__main__":
	app.run_server(debug = True)