import psycopg2
from psycopg2 import sql
import csv


def connect_to_db():
    return psycopg2.connect(
        dbname='glot',
        user='postgres',
        password='student',
        host='localhost',
        port='5432'
    )


def get_or_create_id(cursor, table, field, value):
    cursor.execute(sql.SQL("SELECT id FROM {} WHERE {} = %s").format(
        sql.Identifier(table),
        sql.Identifier(field)),
        [value])
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(sql.SQL("INSERT INTO {} ({}) VALUES (%s) RETURNING id").format(
            sql.Identifier(table),
            sql.Identifier(field)),
            [value])
        return cursor.fetchone()[0]


def insert_data_from_csv(file_path):
    conn = connect_to_db()
    cursor = conn.cursor()

    with open(file_path, 'r') as fisier_csv:
        reader = csv.reader(fisier_csv)
        prima_linie = next(reader)

        for linie in reader:
            date_linie = dict(zip(prima_linie, linie))
            print(date_linie)

            region_id = get_or_create_id(cursor, 'regions', 'name', date_linie['region_txt'])
            country_id = get_or_create_id(cursor, 'countries', 'name', date_linie['country_txt'])
            cursor.execute("UPDATE countries SET region_id = %s WHERE id = %s", (region_id, country_id))

            if len(date_linie['provstate']) != 0:
                provstate_id = get_or_create_id(cursor, 'provstates', 'name', date_linie['provstate'])
                cursor.execute("UPDATE provstates SET country_id = %s WHERE id = %s", (country_id, provstate_id))

                city_id = get_or_create_id(cursor, 'cities', 'name', date_linie['city'])

                if not date_linie['latitude'].strip():
                    date_linie['latitude'] = 0

                if not date_linie['longitude'].strip():
                    date_linie['longitude'] = 0

                cursor.execute("UPDATE cities SET provstate_id = %s, country_id = %s, lat = %s, long = %s WHERE id = %s",
                                (provstate_id, country_id, date_linie['latitude'], date_linie['longitude'], city_id))

            else:
                city_id = get_or_create_id(cursor, 'cities', 'name', date_linie['city'])

                if not date_linie['latitude'].strip():
                    date_linie['latitude'] = 0

                if not date_linie['longitude'].strip():
                    date_linie['longitude'] = 0

                cursor.execute(
                    "UPDATE cities SET country_id = %s, lat = %s, long = %s WHERE id = %s",
                    (country_id, date_linie['latitude'], date_linie['longitude'], city_id))

            if len(date_linie['attacktype1_txt']) != 0:
                attack_id = get_or_create_id(cursor, 'attack', 'name', date_linie['attacktype1_txt'])

            if len(date_linie['targtype1_txt']) != 0:
                target_id = get_or_create_id(cursor, 'target', 'name', date_linie['targtype1_txt'])

            if len(date_linie['targsubtype1_txt']) != 0:
                subtarget_id = get_or_create_id(cursor, 'subtarget', 'name', date_linie['targsubtype1_txt'])
                cursor.execute("UPDATE subtarget SET target_type = %s WHERE id = %s", (target_id, subtarget_id))

            an = date_linie['iyear']
            luna = str(int(date_linie['imonth'])).zfill(2)
            zi = str(int(date_linie['iday'])).zfill(2)

            if luna == '00':
                luna = '01'
            if zi == '00':
                zi = '01'

            if len(date_linie['attacktype1_txt']) == 0:
                if len(date_linie['targtype1_txt']) == 0:
                    if len(date_linie['targsubtype1_txt']) == 0:
                        cursor.execute("""
                                        INSERT INTO events (date, city_id, summary, corp, spec_target, criminal, motive)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                            f"{an}-{luna}-{zi}",
                            city_id,
                            date_linie['summary'],
                            date_linie['corp1'],
                            date_linie['target1'],
                            date_linie['gname'],
                            date_linie['motive']
                        ))
                    else:
                        cursor.execute("""
                                        INSERT INTO events (date, city_id, summary, subtarget_type, corp, spec_target, criminal, motive)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                            f"{an}-{luna}-{zi}",
                            city_id,
                            date_linie['summary'],
                            subtarget_id,
                            date_linie['corp1'],
                            date_linie['target1'],
                            date_linie['gname'],
                            date_linie['motive']
                        ))
                else:
                    cursor.execute("""
                                INSERT INTO events (date, city_id, summary, target_type, subtarget_type, corp, spec_target, criminal, motive)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                        f"{an}-{luna}-{zi}",
                        city_id,
                        date_linie['summary'],
                        target_id,
                        subtarget_id,
                        date_linie['corp1'],
                        date_linie['target1'],
                        date_linie['gname'],
                        date_linie['motive']
                    ))
            else:
                cursor.execute("""
                                INSERT INTO events (date, city_id, summary, attack_type, target_type, subtarget_type, corp, spec_target, criminal, motive)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    f"{an}-{luna}-{zi}",
                    city_id,
                    date_linie['summary'],
                    attack_id,
                    target_id,
                    subtarget_id,
                    date_linie['corp1'],
                    date_linie['target1'],
                    date_linie['gname'],
                    date_linie['motive']
                ))

    conn.commit()
    cursor.close()
    conn.close()


insert_data_from_csv('D:\\Proiect WEB\\globalterrorismdb_0718dist.csv')
