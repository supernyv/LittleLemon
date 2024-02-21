import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, ctx
import os

logo_path = os.path.join("assets", "little_lemon_logo.png")
logo = html.Img(src = logo_path, height = "65px")
brand = dbc.NavbarBrand("Little Lemon", href = "/")

page_buttons = html.Div(
	[
		dbc.Button(
			"Edit Data", id = "edit_data_button", outline = True,
			color = "warning", n_clicks = 0, style = {"margin-right": "10px"}
			),
		dbc.Button(
			"View Data", id = "view_data_button", outline = False,
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

@callback(
	Output("edit_data_button", "outline"),
	Output("view_data_button", "outline"),
	Input("edit_data_button", "n_clicks"),
	Input("view_data_button", "n_clicks")
)
def button_status(edit_click, vied_click):
	button_id = ctx.triggered_id if ctx.triggered_id else "view_data_button"
	if button_id == "edit_data_button":
		return (False, True)
	elif button_id == "view_data_button":
		return (True, False)
