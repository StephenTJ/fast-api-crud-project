import psycopg2
import json

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""

connection = psycopg2.connect(database=DB_NAME,
						user=DB_USER,
						password=DB_PASS,
						host=DB_HOST,
						port=DB_PORT
                        )

def convert_to_json(data_list):
    data_string = json.dumps(data_list).replace("'", "\"")
    json_data = json.loads(data_string)
    return json_data

def perform_select_operation(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        result_dicts = [dict(zip(column_names, row)) for row in result]
        connection.commit()
        cursor.close()
        if len(result) == 0:
            return "no data"
        return json.loads(json.dumps(result_dicts))
    except Exception as ex:
        return str(ex)

def perform_iud_operation(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        return "success"
    except Exception as ex:
        return str(ex)
