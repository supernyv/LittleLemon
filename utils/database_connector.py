import mysql.connector as connector
import pandas as pd;

def get_user_connection(logon = "admin", pwd = "admin", db = "LittleLemonDB"):
	try:
		connection = connector.connect( user = logon, password = pwd, database = db)
		return connection
	except connector.Error as Err:
		return None

def handle_connections(query_function):
	def wrapper(query_statement):
		connection = get_user_connection("admin", "admin")
		if connection:
			cursor = connection.cursor(buffered=True)
			sql_query = query_function(cursor, query_statement)
			cursor.close()
			connection.close()
			return sql_query
		else:
			return None
	return wrapper

@handle_connections
def write_query(cursor, query_statement):
	try:
		cursor.execute(query_statement)
		return True
	except connector.Error as err:
		return False

@handle_connections
def read_query(cursor, query_statement):
	try:
		cursor.execute(query_statement)
		column_names = cursor.column_names
		rows = cursor.fetchall()
		df = pd.DataFrame(rows, columns = column_names)
		return df
	except connector.Error as err:
		return None