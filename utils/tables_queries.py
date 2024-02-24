from utils.database_connector import read_query

#------------------------------------ Get a dataframe -----------------------------------#
def get_df(table_name):
	select_data = f""" SELECT * FROM {table_name} """
	if select_data:
		df = read_query(select_data)
		return df
	else:
		return None