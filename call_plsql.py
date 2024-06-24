import psycopg2
import json


def get_regions_by_attack_count(cur, conn):
    cur.callproc("func", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_countries(cur, conn):
    cur.callproc("get_general_countries", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_attacks(cur, conn):
    cur.callproc("get_general_attacks", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_general_targets(cur, conn):
    cur.callproc("get_general_targets", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_count_attacks_by_year(cur, conn):
    cur.callproc("count_attacks_by_year", [])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    return converted_data


def get_coutries_in_reg(cur, conn, reg_name):
    cur.callproc("get_coutries_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    ref_cursor.close()
    return data


def get_attacks_in_reg(cur, conn, reg_name):
    cur.callproc("get_attacks_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_targets_in_regg(cur, conn, reg_name):
    cur.callproc("get_targets_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    return data


def get_attacks_by_year_in_reg(cur, conn, reg_name):
    cur.callproc("get_attacks_by_year_in_reg", [reg_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    return converted_data


def get_provstates_in_country(cur, conn, c_name):
    cur.callproc("get_provstates_in_country", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_attacks_in_country(cur, conn, c_name):
    cur.callproc("get_attacks_in_country", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_targets_in_country(cur, conn, c_name):
    cur.callproc("get_targets_in_country", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_attacks_by_year_in_country(cur, conn, c_name):
    cur.callproc("get_attacks_by_year_in_country", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    return converted_data


def get_cities_in_provstate(cur, conn, p_name):
    cur.callproc("get_cities_in_provstate", [p_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_attacks_in_provstate(cur, conn, p_name):
    cur.callproc("get_attacks_in_provstate", [p_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_targets_in_provstate(cur, conn, p_name):
    cur.callproc("get_targets_in_provstate", [p_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_attacks_by_year_in_provstate(cur, conn, p_name):
    cur.callproc("get_attacks_by_year_in_provstate", [p_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    return converted_data


def get_city_events(cur, conn, c_name):
    cur.callproc("get_city_events", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_attacks_in_city(cur, conn, c_name):
    cur.callproc("get_attacks_in_city", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_targets_in_city(cur, conn, c_name):
    cur.callproc("get_targets_in_city", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    print("data", data)
    return data


def get_attacks_by_year_in_city(cur, conn, c_name):
    cur.callproc("get_attacks_by_year_in_city", [c_name])
    ref_cursor_name = cur.fetchone()[0]
    ref_cursor = conn.cursor(ref_cursor_name)
    data = ref_cursor.fetchall()
    converted_data = [(int(row[0]), int(row[1])) for row in data]
    return converted_data
