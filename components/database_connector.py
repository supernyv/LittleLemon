import os
import mysql.connector as connector
import pandas as pd;

def get_user_connection(db_user = "admin", user_pwd = "admin", db = "LittleLemonDB"):
	connection = connector.connect(
		user = db_user,
		password = user_pwd,
		database = db
	)
	return connection

def handle_connections(query_function):
	def wrapper(query_statement):
		connection = get_user_connection("admin", "admin")
		cursor = connection.cursor(buffered=True)

		sql_query = query_function(cursor, query_statement)

		cursor.close()
		connection.close()

		return sql_query
	return wrapper

@handle_connections
def write_query(cursor, query_statement):
	cursor.execute(query_statement)

@handle_connections
def read_query(cursor, query_statement):
	cursor.execute(query_statement)
	column_names = cursor.column_names
	rows = cursor.fetchall()
	df = pd.DataFrame(rows, columns = column_names)
	return df

def close_user_cursor(user_connection):
	user_connection.close()