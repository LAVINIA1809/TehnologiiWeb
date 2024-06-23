import psycopg2
import json

conn = psycopg2.connect(
    dbname="glot",
    user="postgres",
    password="student",
    host="localhost"
)


def get_regions_by_attack_count():
    cur = conn.cursor()
    cur.callproc("func", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_countries():
    cur = conn.cursor()
    cur.callproc("get_general_countries", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_provstates():
    cur = conn.cursor()
    cur.callproc("get_general_provstates", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_cities():
    cur = conn.cursor()
    cur.callproc("get_general_cities", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_attacks():
    cur = conn.cursor()
    cur.callproc("get_general_attacks", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_targets():
    cur = conn.cursor()
    cur.callproc("get_general_targets", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data

def get_count_attacks_by_year():
    cur = conn.cursor()
    cur.callproc("count_attacks_by_year", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    return converted_data


def export_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

export_data(get_regions_by_attack_count(), 'data1.json')
export_data(get_general_countries(), 'data2.json')
export_data(get_general_provstates(), 'data3.json')
export_data(get_general_cities(), 'data4.json')
export_data(get_general_attacks(), 'data5.json')
export_data(get_general_targets(), 'data6.json')
export_data(get_count_attacks_by_year(), 'data7.json')

conn.close()
