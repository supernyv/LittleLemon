import mysql.connector as connector
import pandas as pd

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
			query_result = query_function(cursor, query_statement)
			cursor.close()
			connection.close()
			return query_result
		else:
			return "No access"
	return wrapper

@handle_connections
def write_query(cursor, query_statement):
	try:
		cursor.execute(query_statement)
		return True
	except connector.Error as err:
		return err

@handle_connections
def read_query(cursor, query_statement):
	try:
		cursor.execute(query_statement)
		column_names = cursor.column_names
		rows = cursor.fetchall()
		df = pd.DataFrame(rows, columns = column_names)
		return df
	except connector.Error as err:
		return err

col = 'total_cost'
print(read_query(f"SELECT {col} FROM orders;"))