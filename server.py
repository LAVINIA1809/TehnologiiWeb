from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from bson.json_util import dumps
import re
import psycopg2


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
          pass

#formularele o sa fie de tip POST
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            email = data.get('email')
            password = data.get('password')

            query = "SELECT id FROM users WHERE email = %s AND password = %s"
            cur.execute(query, (email, password))
            user = cur.fetchone()
                    
            if user:
                response = {
                    'message': 'Login successful!',
                    'status': 'success'
                }
            else:
                self.send_response(401)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                        
                response = {
                    'message': 'Invalid email or password',
                    'status': 'fail'
                    }
            self.send_response(200)
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
                query = "INSERT INTO users (firstname, lastname, email, regnum, password) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query, (first_name, last_name, email, reg_number, password))
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

                # query_attack_type = "INSERT INTO attack (name) VALUES (%s) RETURNING id"
                # cur.execute(query_attack_type, (attack_type,))
                # attack_type_id = cur.fetchone()[0]

                query_target_type = "INSERT INTO target (name) VALUES (%s) RETURNING id"
                cur.execute(query_target_type, (target,))
                target_type_id = cur.fetchone()[0]

                query_subtarget = "INSERT INTO subtarget (name, target_type) VALUES (%s, %s) RETURNING id"
                cur.execute(query_subtarget, (subtarget, target_type_id))
                subtarget_type_id = cur.fetchone()[0]

                query_event = """
                INSERT INTO events (date, city_id, summary, attack_type, target_type, subtarget_type, corp, spec_target, criminal, motive)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                cur.execute(query_event, (date, city_id, summary, attack_type,
                          target, subtarget, corp,
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
