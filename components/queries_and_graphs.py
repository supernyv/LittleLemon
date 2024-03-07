from utils.database_connector import read_query
import plotly.express as px

#To avoid repeating sql queries inside the graphs functions
#------------------------------ Define Generic query for tables ------------------------------#
def get_table_df(table_name):
	select_data = f""" SELECT * FROM {table_name} """
	df = read_query(select_data)
	return df
#--------------------------------------- Define Queries -------------------------------------#
def booking_history_df():
	sql_query = """
		SELECT
			booking_date,
			SUM(number_of_guests) as number_of_guests
		FROM booking
		GROUP BY booking_date
		/*Order by booking_date to prevent the messy graph*/
		ORDER BY booking_date;
	"""
	df = read_query(sql_query)
	return df

def menus_df():
	sql_query = """
		SELECT
			menu_name,
			cuisine,
			price
		FROM menu;
	"""
	df = read_query(sql_query)
	return df

def menus_sales_df():
	sql_query = """
		SELECT
			o.order_date,
			o.total_cost,
			o.order_status,
			oi.quantity,
			me.menu_name,
			me.cuisine
		FROM
			orders AS o
			INNER JOIN
			order_items AS oi
			ON oi.order_id = o.order_id
			INNER JOIN
			menu AS me
			ON me.menu_id = oi.menu_id;
	"""
	df = read_query(sql_query)
	return df

def sales_report_df():
	sql_query = """
		SELECT
			order_date,
			total_cost
		FROM
			orders;
	"""
	df = read_query(sql_query)
	return df

def staff_activity_df():
	sql_query = """
		SELECT
			CONCAT(s.first_name, ' ', s.last_name) AS staff_name,
			s.role,
			o.order_date,
			o.order_status,
			o.total_cost
		FROM
			orders AS o
			INNER JOIN
			staff AS s
			ON s.staff_id = o.staff_id
		ORDER BY total_cost DESC;
	"""
	df = read_query(sql_query)
	return df

#--------------------------------------- Make Graphs -------------------------------------#
def booking_history():
	df = booking_history_df()
	graph = px.scatter(data_frame = df, x = "booking_date", y = "number_of_guests")
	return graph

def premium_menu():
	df = menus_df().sort_values(by = ["price"]).iloc[-15:,:]
	graph = px.bar(data_frame = df, x = "price", y = "menu_name", orientation = "h")
	return graph

def menu_sales():
	df = menus_sales_df()
	graph = px.bar(data_frame = df, x = "cuisine", y = "quantity")
	return graph

def sales_scatter_chart():
	df = sales_report_df()
	graph = px.scatter(data_frame = df, x = "order_date", y = "total_cost")
	return graph

def most_active_staff():
	df = staff_activity_df()
	graph = px.bar(df, x = "total_cost", y = "staff_name", orientation = 'h')
	return graph;
#------------------------------- Package graphs for import ------------------------------#
graphs_index = {
	"booking_history" : booking_history,
	"premium_menu" : premium_menu,
	"menu_sales" : menu_sales,
	"most_active_staff" : most_active_staff,
	"sales_scatter_chart" : sales_scatter_chart
	}