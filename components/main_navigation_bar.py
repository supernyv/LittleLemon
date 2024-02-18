import dash_bootstrap_components as dbc
from dash import html
import os

logo_path = os.path.join("assets", "lemon_logo.png")
logo = html.Img(src = logo_path, height = "80px")
brand = dbc.NavbarBrand("Little Lemon", href = "/")

page_buttons = html.Div(
	[
		dbc.Button(
			"Edit Data", id = "edit_data_button", outline = True,
			color = "warning", n_clicks = 0, style = {"margin-right": "10px"}
			),
		dbc.Button(
			"View Data", id = "view_data_button", outline = True,
			color = "primary", n_clicks = 0
			)
	]
	)

navigation_bar = dbc.Navbar(
	dbc.Container(
		[
			dbc.Row(
				[
					dbc.Col(logo),
					dbc.Col(brand)
				],
				align = "center"
				),
			page_buttons

		],
		fluid = True
	),
	color = "dark",
	dark = True,
	style = {"height":"60px"}
	)