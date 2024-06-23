import psycopg2
import json


def get_regions_by_attack_count(cur, conn):

    cur.callproc("func", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data1.json', 'w') as file:
        json.dump(data, file)


def get_general_countries(cur, conn):

    cur.callproc("get_general_countries", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data2.json', 'w') as file:
        json.dump(data, file)


def get_general_provstates(cur, conn):

    cur.callproc("get_general_provstates", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data3.json', 'w') as file:
        json.dump(data, file)


def get_general_cities(cur, conn):

    cur.callproc("get_general_cities", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data4.json', 'w') as file:
        json.dump(data, file)


def get_general_attacks(cur, conn):

    cur.callproc("get_general_attacks", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data5.json', 'w') as file:
        json.dump(data, file)


def get_general_targets(cur, conn):

    cur.callproc("get_general_targets", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data6.json', 'w') as file:
        json.dump(data, file)


def get_count_attacks_by_year(cur, conn):

    cur.callproc("count_attacks_by_year", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    with open('data7.json', 'w') as file:
        json.dump(converted_data, file)


def get_coutries_in_reg(cur, conn, reg_name):
    try:
        cur.callproc("get_coutries_in_reg", [reg_name])
        ref_cursor_name = cur.fetchone()[0]
        ref_cursor = conn.cursor(ref_cursor_name)
        data = ref_cursor.fetchall()

        with open('data2.json', 'w') as file:
            json.dump(data, file)

    except psycopg2.Error as e:
        conn.rollback()  # Anulează tranzacția în caz de eroare
        print('Error:', e)


def get_attacks_in_reg(cur, conn, reg_name):
    cur.callproc("get_attacks_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data5.json', 'w') as file:
        json.dump(data, file)


def get_targets_in_regg(cur, conn, reg_name):
    cur.callproc("get_targets_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    with open('data6.json', 'w') as file:
        json.dump(data, file)


def get_attacks_by_year_in_reg(cur, conn, reg_name):
    cur.callproc("get_attacks_by_year_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    with open('data7.json', 'w') as file:
        json.dump(converted_data, file)
