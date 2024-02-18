import os
import mysql.connector as connector
import pandas as pd;

def get_user_handles(db_user, user_pwd, db = "LittleLemonDB"):
	connection = connector.connect(
		user = db_user,
		password = user_pwd,
		database = db
	)
	cursor = connection.cursor()
	return connection, cursor

def write_query(user_cursor, query_statement):
	user_cursor.execute(query_statement)

def read_query(user_cursor, query_statement):
	user_cursor.execute(query_statement)
	column_names = user_cursor.column_names
	rows = user_cursor.fetchall()
	df = pd.DataFrame(rows, columns = column_names)
	return df

def close_user_cursor(user_connection, user_cursor):
	user_cursor.close()
	user_connection.close()