from http.server import HTTPServer, BaseHTTPRequestHandler
import json
# from bson.json_util import dumps
import psycopg2
import bcrypt
from urllib.parse import urlparse, parse_qs
import call_plsql
import urllib

conn = psycopg2.connect(
    dbname="glot",
    user="postgres",
    password="student",
    host="localhost",
    port="5432")
cur = conn.cursor()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):

        print(self.path)

        if self.path.startswith('/index'):
            print("Sunt in index")

            data1 = call_plsql.get_regions_by_attack_count(cur, conn)
            data2 = call_plsql.get_general_countries(cur, conn)
            data3 = call_plsql.get_general_attacks(cur, conn)
            data4 = call_plsql.get_general_targets(cur, conn)
            data5 = call_plsql.get_count_attacks_by_year(cur, conn)

            print("Data1: ", data1)

            response = {'message': 'OK',
                        'status': 'success',
                        'data1': data1,
                        'data2': data2,
                        'data3': data3,
                        'data4': data4,
                        'data5': data5}

            self.send_response(200)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            try:
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except ConnectionAbortedError as e:
                print(f"Error writing response: {e}")

        elif self.path.startswith('/reg_result'):
            print("sunt in api")
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

            if 'type' in query_params and 'name' in query_params:
                entity_name = query_params['name'][0]
                # print(entity_type, entity_name)

                data1 = call_plsql.get_coutries_in_reg(cur, conn, entity_name)
                data2 = call_plsql.get_attacks_in_reg(cur, conn, entity_name)
                data3 = call_plsql.get_targets_in_regg(cur, conn, entity_name)
                data4 = call_plsql.get_attacks_by_year_in_reg(cur, conn, entity_name)

                print("sunt in region1")

                response = {'message': 'OK',
                            'status': 'success',
                            'data1': data1,
                            'data2': data2,
                            'data3': data3,
                            'data4': data4}

                print("sunt in region2")

                self.send_response(200)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                except ConnectionAbortedError as e:
                    print(f"Error writing response: {e}")

            else:
                # Dacă lipsește parametrul necesar "name", returnăm un cod de eroare 400 (Bad Request)
                self.send_response(400)

                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'Missing required parameter "name"')

        elif self.path.startswith('/country_result'):

            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

            if 'type' in query_params and 'name' in query_params:
                entity_name = query_params['name'][0]
                print("country")

                data1 = call_plsql.get_provstates_in_country(cur, conn, entity_name)
                data2 = call_plsql.get_attacks_in_country(cur, conn, entity_name)
                data3 = call_plsql.get_targets_in_country(cur, conn, entity_name)
                data4 = call_plsql.get_attacks_by_year_in_country(cur, conn, entity_name)
                print(data1)

                response = {'message': 'OK',
                            'status': 'success',
                            'data1': data1,
                            'data2': data2,
                            'data3': data3,
                            'data4': data4
                            }

                self.send_response(200)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                except ConnectionAbortedError as e:
                    print(f"Error writing response: {e}")

            else:
                # Dacă lipsește parametrul necesar "name", returnăm un cod de eroare 400 (Bad Request)
                self.send_response(400)

                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'Missing required parameter "name"')

        elif self.path.startswith('/provstate_result'):

            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

            if 'type' in query_params and 'name' in query_params:
                entity_name = query_params['name'][0]
                print("provstate")

                data1 = call_plsql.get_cities_in_provstate(cur, conn, entity_name)
                data2 = call_plsql.get_attacks_in_provstate(cur, conn, entity_name)
                data3 = call_plsql.get_targets_in_provstate(cur, conn, entity_name)
                data4 = call_plsql.get_attacks_by_year_in_provstate(cur, conn, entity_name)
                print("data provstate", data1)

                response = {'message': 'OK',
                            'status': 'success',
                            'data1': data1,
                            'data2': data2,
                            'data3': data3,
                            'data4': data4
                            }

                self.send_response(200)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                except ConnectionAbortedError as e:
                    print(f"Error writing response: {e}")

            else:
                # Dacă lipsește parametrul necesar "name", returnăm un cod de eroare 400 (Bad Request)
                self.send_response(400)

                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'Missing required parameter "name"')

        elif self.path.startswith('/city_result'):
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

            if 'type' in query_params and 'name' in query_params:
                entity_name = query_params['name'][0]
                print("city")

                events = call_plsql.get_city_events(cur, conn, entity_name)
                data2 = call_plsql.get_attacks_in_city(cur, conn, entity_name)
                data3 = call_plsql.get_targets_in_city(cur, conn, entity_name)
                data4 = call_plsql.get_attacks_by_year_in_city(cur, conn, entity_name)

                events_data = []
                for event in events:
                    event_date = event[1]
                    event_year = event_date.year

                    events_data.append({
                        'event_id': event[0],
                        'date': event[1].strftime('%Y-%m-%d'),
                        'year': event_year,
                        'summary': event[2],
                        'city_name': event[3],
                        'provstate_name': event[4],
                        'country_name': event[5],
                        'region_name': event[6],
                        'attack_name': event[7],
                        'target_name': event[8],
                        'subtarget_name': event[9],
                        'corp': event[10],
                        'spec_target': event[11],
                        'criminal': event[12],
                        'motive': event[13]
                    })

                response = {
                    'message': 'OK',
                    'status': 'success',
                    'data1': events_data,
                    'data2': data2,
                    'data3': data3,
                    'data4': data4,
                }

                print("data1: ", events_data)
                print("data2: ", data2)
                print("data3: ", data3)
                print("data4: ", data4)

                self.send_response(200)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                except ConnectionAbortedError as e:
                    print(f"Error writing response: {e}")

            else:
                # Dacă lipsește parametrul necesar "name", returnăm un cod de eroare 400 (Bad Request)
                self.send_response(400)

                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'Missing required parameter "name"')

        else:
            self.send_response(404)

            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(b'Page not found')

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            email = data.get('email')
            password = data.get('password')

            # first_query = "SELECT firstname, lastname FROM users "

            query = "SELECT password, firstname, lastname FROM users WHERE email = %s"
            cur.execute(query, (email,))
            user = cur.fetchone()

            if user:
                stored_hash, first_name, last_name = user
                stored_hash = stored_hash.encode('utf-8')

                if email == 'admin@gmail.com':
                    response = {
                        'message': 'Login successful!',
                        'status': 'success',
                        'user': {
                            'first_name': first_name,
                            'last_name': last_name
                        }
                    }
                    self.send_response(200)

                else:

                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        response = {
                            'message': 'Login successful!',
                            'status': 'success',
                            'user': {
                                'first_name': first_name,
                                'last_name': last_name
                            }
                        }
                        self.send_response(200)
                    else:
                        response = {
                            'message': 'The password is incorect!',
                            'status': 'fail'
                        }
                        self.send_response(401)
            else:
                response = {
                    'message': 'This email is not registred!',
                    'status': 'fail'
                }
                self.send_response(401)

            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == "/register":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            reg_number = data.get('reg_number')
            password = data.get('password')

            try:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                query = "INSERT INTO users (firstname, lastname, email, regnum, password) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query, (first_name, last_name, email, reg_number, hashed_password.decode('utf-8')))
                conn.commit()

                response = {
                    'message': 'Registration successful!',
                    'status': 'success'
                }
                self.send_response(200)
            except Exception as e:
                response = {
                    'message': 'Registration failed: ' + str(e),
                    'status': 'fail'
                }
                self.send_response(500)
            finally:
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == "/addEvent":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            region = data.get('region')
            country = data.get('country')
            state = data.get('state')
            city = data.get('city')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            date = data.get('date')
            attack_type = data.get('attack_type')
            summary = data.get('summary')
            target = data.get('target')
            subtarget = data.get('subtarget')
            corp = data.get('corp')
            spec_target = data.get('spec_target')
            criminal = data.get('criminal')
            motive = data.get('motive')

            try:
                query_region = "INSERT INTO regions (name) VALUES (%s) RETURNING id"
                cur.execute(query_region, (region,))
                region_id = cur.fetchone()[0]

                query_country = "INSERT INTO countries (name, region_id) VALUES (%s, %s) RETURNING id"
                cur.execute(query_country, (country, region_id))
                country_id = cur.fetchone()[0]

                query_provstate = "INSERT INTO provstates (name, country_id) VALUES (%s, %s) RETURNING id"
                cur.execute(query_provstate, (state, country_id))
                state_id = cur.fetchone()[0]

                query_city = "INSERT INTO cities (name, provstate_id, country_id, lat, long) VALUES (%s, %s, %s, %s, %s) RETURNING id"
                cur.execute(query_city, (city, state_id, country_id, latitude, longitude))
                city_id = cur.fetchone()[0]

                query_attack_type = "INSERT INTO attack (name) VALUES (%s) RETURNING id"
                cur.execute(query_attack_type, (attack_type,))
                attack_type_id = cur.fetchone()[0]

                query_target_type = "INSERT INTO target (name) VALUES (%s) RETURNING id"
                cur.execute(query_target_type, (target,))
                target_type_id = cur.fetchone()[0]

                query_subtarget = "INSERT INTO subtarget (name, target_type) VALUES (%s, %s) RETURNING id"
                cur.execute(query_subtarget, (subtarget, target_type_id))
                subtarget_type_id = cur.fetchone()[0]

                query_event = """
                INSERT INTO events (date, city_id, summary, attack_type, corp, spec_target, criminal, motive)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                cur.execute(query_event, (date, city_id, summary, attack_type_id, corp,
                                          spec_target, criminal, motive))
                conn.commit()

                response = {
                    'message': 'Upload successful!',
                    'status': 'success'
                }
                self.send_response(200)
            except Exception as e:
                response = {
                    'message': 'Upload failed: ' + str(e),
                    'status': 'fail'
                }
                self.send_response(500)
            finally:
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(400)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(b'400 - Bad Request')

    def do_PUT(self):
        pass


httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
print("The server is listening...")
httpd.serve_forever()
cur.close()
conn.close()
