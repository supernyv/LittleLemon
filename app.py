import os
import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output, ctx
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px
from components.main_navigation_bar import navigation_bar
from utils.database_connector import read_query, write_query
from components.queries_and_graphs import get_table_df, graphs_index

##from dash_bootstrap_templates import load_figure_template

#---------------------------------- Initialize the app ----------------------------------#
app = Dash(
		title = "Little Lemon",
		external_stylesheets = [dbc.themes.SANDSTONE, dbc.icons.FONT_AWESOME]
		)
app._favicon = os.path.join("asset", "favicon.ico")
server = app.server

##load_figure_template("sandstone")

#------------------------ Get the list of tables in the database ------------------------#

tables_list = read_query("""SHOW TABLES""")["Tables_in_littlelemondb"].tolist()
graphs_list = list(graphs_index.keys())

#-------------------------------- App layout Components ---------------------------------#

tables_dropdown = dcc.Dropdown(
	options = [{"label": " ".join(t.split("_")).title(), "value":t} for t in tables_list],
	value = tables_list[0],
	placeholder = "Select Table",
	id = "id_tables_dropdown",
	searchable = False
	)
tables_pane = [
	html.P(),
	dbc.Row(
		[
			dbc.Col(
				[
				html.I(className="fa fa-solid fa-eye me-2"), #me = margin-end
				"Select Table"
				],
				width = 3,
				className = "d-flex align-items-center"),
			dbc.Col(tables_dropdown, width = 9)
		]
		),
	html.P(),
	dbc.Row(id = "id_grid_location"),
	]

graphs_dropdown = dcc.Dropdown(
	options = [{"label": " ".join(g.split("_")).title(), "value":g} for g in graphs_list],
	value = graphs_list[0],
	id = "id_graphs_dropdown",
	placeholder = "Select Graph",
	searchable = False
	)
graphs_pane = [
	html.P(),
	dbc.Row(
		[
		dbc.Col(
			[
			html.I(className = "fa fa-solid fa-chart-line me-2"),
			"Select Graph"
			],
			width = 4,
			className = "d-flex align-items-center"
			),
		dbc.Col(graphs_dropdown, width = 8)
		]
		),
	html.P(),
	dbc.Card(
		dbc.CardBody(
			dcc.Graph(
				id = "id_graphs_location",
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
	Output("id_grid_location", "children"),
	Input("id_tables_dropdown", "value")
	)
def update_grid_table(selected_table):
	if not selected_table:
		return "No table Selected. Kindly select a table from the above dropdown."
	gdf = get_table_df(selected_table)

	grid = dag.AgGrid(
		rowData = gdf.to_dict('records'),
		columnDefs = [{"field": i, "filter":True} for i in gdf.columns],
		columnSize = "sizeToFit",
		style = {"height":"76vh"},
		defaultColDef = {"editable":True}
	)
	return grid

@callback(
	Output("id_graphs_location", "figure"),
	Input("id_graphs_dropdown", "value")
	)
def update_graph(selected_graph):
	fig = graphs_index[selected_graph]()
	fig.update_layout(
		template = "plotly_white",
		margin = {"l": 0, "r": 0, "t": 0, "b": 0})
	fig.update_xaxes(showline=True, linecolor='black')
	fig.update_yaxes(showline=True, linecolor='black')
	return fig

if __name__ == "__main__":
	app.run_server(debug = True)