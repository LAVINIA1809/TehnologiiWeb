import psycopg2
import matplotlib.pyplot as plt

# Conectare la baza de date PostgreSQL
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


def get_pie_chart():
    # attack_counts_by_region = get_regions_by_attack_count()
    # attack_counts_by_region = get_general_countries()
    attack_counts_by_region = get_general_provstates()
    #attack_counts_by_region = get_general_cities()

    regions = [result[0] for result in attack_counts_by_region]
    attack_counts = [result[1] for result in attack_counts_by_region]

    plt.figure(figsize=(8, 8))
    plt.pie(attack_counts, labels=regions, autopct='%1.1f%%', startangle=140)

    plt.title('Distribuția atacurilor pe regiuni')

    plt.axis('equal')
    plt.show()


def get_bar_chart():
    attack_counts_by_region = get_general_attacks()
    #attack_counts_by_region = get_general_targets()

    categories = [result[0] for result in attack_counts_by_region]
    values = [result[1] for result in attack_counts_by_region]

    plt.barh(categories, values)

    plt.title('Distribuția atacurilor pe regiuni')

    plt.xlabel('Attack type')
    plt.ylabel('Attack counts')
    plt.show()


get_pie_chart()

conn.close()
