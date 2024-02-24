from utils.database_connector import read_query
import plotly.express as px

#--------------------------------------- Define Graphs -------------------------------------#
def bookings_guests():
	sql_query = """
		SELECT
			booking_date,
			SUM(number_of_guests) as number_of_guests
		FROM booking
		GROUP BY booking_date
		/*Order by booking_date to prevent the messy graph*/
		ORDER BY booking_date;
	"""
	try:
		df = read_query(sql_query)
		graph = px.line(data_frame = df, x = "booking_date", y = "number_of_guests")
		return graph
	except Exception as err:
		return None

def menu_price_distribution():
	sql_query = """
		SELECT
			price
		FROM menu;
	"""
	try:
		df = read_query(sql_query)
		graph = px.histogram(data_frame = df, x = "price")
		return graph
	except Exception as err:
		return None

def menu_sales():
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
	try:
		df = read_query(sql_query)
		graph = px.bar(data_frame = df, x = "cuisine", y = "quantity")
		return graph
	except Exception as err:
		return None

def sales_scatter_chart():
	sql_query = """
		SELECT
			order_date,
			total_cost
		FROM
			orders;
	"""
	try:
		df = read_query(sql_query)
		graph = px.scatter(data_frame = df, x = "order_date", y = "total_cost")
		return graph
	except Exception as err:
		return None

def most_active_staff():
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
			ON s.staff_id = o.staff_id;
	"""
	try:
		df = read_query(sql_query)
		graph = px.bar(df, x = "total_cost", y = "staff_name", orientation = 'h')
		return graph;
	except Exception as err:
		return None
#------------------------------- Package graphs for import ------------------------------#
graphs_index = {
	"bookings_guests" : bookings_guests,
	"menu_price_distribution" : menu_price_distribution,
	"menu_sales" : menu_sales,
	"most_active_staff" : most_active_staff,
	"sales_scatter_chart" : sales_scatter_chart
	}