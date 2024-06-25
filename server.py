from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import psycopg2
from psycopg2 import sql, errors
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import hashlib
import time
from datetime import datetime, timedelta
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

def generate_reset_token(email):
    timestamp = int(time.time())
    token = secrets.token_urlsafe()
    hash_token = hashlib.sha256(f"{email}{token}{timestamp}".encode()).hexdigest()
    return hash_token, timestamp

def store_token(email, token, timestamp):
    query = "SELECT id FROM password_reset_tokens WHERE email = %s"
    cur.execute(query, (email,))
    result = cur.fetchone()
    
    if result: 
        cur.execute(
        "UPDATE password_reset_tokens SET token = %s, created_at = to_timestamp(%s) WHERE email = %s",
        (token, timestamp, email)
        )
        conn.commit()
    else:
        cur.execute(
        "INSERT INTO password_reset_tokens (email, token, created_at) VALUES (%s, %s, to_timestamp(%s))",
        (email, token, timestamp)
        )
        conn.commit()

def send_verification_email(email, verification_link):
    sender_email = "site.glot@gmail.com"
    sender_password = "ejqz njjz aaxt mjau"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Verification"
    message["From"] = sender_email
    message["To"] = email

    text = f"Please click the link below to verify your email address:\n\n{verification_link}"
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
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

            query = "SELECT password, firstname, lastname FROM users WHERE email = %s"
            cur.execute(query, (email,))
            user = cur.fetchone()
                    
            if user:
                stored_hash, first_name, last_name = user

                verify_query = "SELECT is_verified FROM verify_email WHERE email = %s"
                cur.execute(verify_query, (email,))
                verification_status = cur.fetchone()
                print(password)

                if email == 'admin@gmail.com' and password == 'admin':
                    response = {
                        'message': 'Login successful!',
                        'status': 'success',
                        'user': {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email
                        }
                    }
                    self.send_response(200)
                elif email == 'admin@gmail.com' and password != 'admin':
                    response = {
                        'message': 'Unauthorized for official admin account!',
                        'status': 'fail',
                    }
                    self.send_response(401)
                elif email == 'site.glot@gmail.com' and password == 'admin':
                    response = {
                        'message': 'Login successful!',
                        'status': 'success',
                        'user': {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email
                        }
                    }
                    self.send_response(200)
                else:
                    verify_query = "SELECT is_verified FROM verify_email WHERE email = %s"
                    cur.execute(verify_query, (email,))
                    verification_status = cur.fetchone()

                    if verification_status and verification_status[0]:
                        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                            response = {
                                'message': 'Login successful!',
                                'status': 'success',
                                'user': {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'email': email
                                }
                            }
                            self.send_response(200)
                        else:
                            response = {
                                'message': 'The password is incorrect!',
                                'status': 'fail'
                            }
                            self.send_response(401)
                    else:
                        response = {
                            'message': 'Email not verified! Please verify your email in order to login!',
                            'status': 'fail'
                        }
                        self.send_response(401)
            else:
                response = {
                    'message': 'This email is not registered!',
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
                token, timestamp = generate_reset_token(email)
                verify_query = "INSERT INTO verify_email (email, token) VALUES (%s, %s)"
                cur.execute(verify_query, (email, token))
                conn.commit()

                verification_link = f"http://localhost:5500/verify_email.html?token={token}"
                send_verification_email(email, verification_link)

                response = {
                    'message': 'Registration successful! Please check your email to verify your account.',
                    'status': 'success'
                }
                self.send_response(200)

            except Exception as e:
                response = {
                    'message': str(e),
                    'status': 'fail'
                }
                self.send_response(500)
            finally:
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
        
        elif self.path == "/verify-email":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            token = data.get('token')

            try:
                query = "SELECT email FROM verify_email WHERE token = %s AND is_verified = FALSE"
                cur.execute(query, (token,))
                result = cur.fetchone()

                if result:
                    email = result[0]
                    update_query = "UPDATE verify_email SET is_verified = TRUE WHERE email = %s"
                    cur.execute(update_query, (email,))
                    conn.commit()

                    response = {
                    'message': 'Email verified successfully!',
                    'status': 'success'
                    }
                    self.send_response(200)
                else:
                    response = {
                    'message': 'Invalid or expired token! Or the email is already verified',
                    'status': 'fail'
                    }
                    self.send_response(401)
            except Exception as e:
                response = {
                    'message': 'Verification failed: ' + str(e),
                    'status': 'fail'
                }
                self.send_response(500)
            finally:
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            
        elif self.path == "/add-event":
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
                query_region = "SELECT id FROM regions WHERE name = %s"
                cur.execute(query_region, (region,))
                result = cur.fetchone()
                if result:
                    region_id = result[0]
                else:
                    query_region = "INSERT INTO regions (name) VALUES (%s) RETURNING id"
                    cur.execute(query_region, (region,))
                    region_id = cur.fetchone()[0]

                query_country = "SELECT id FROM countries WHERE name = %s AND region_id = %s"
                cur.execute(query_country, (country, region_id))
                result = cur.fetchone()
                if result:
                    country_id = result[0]
                else:
                    query_country = "INSERT INTO countries (name, region_id) VALUES (%s, %s) RETURNING id"
                    cur.execute(query_country, (country, region_id))
                    country_id = cur.fetchone()[0]

                query_provstate = "SELECT id FROM provstates WHERE name = %s AND country_id = %s"
                cur.execute(query_provstate, (state, country_id))
                result = cur.fetchone()
                if result:
                    state_id = result[0]
                else:
                    query_provstate = "INSERT INTO provstates (name, country_id) VALUES (%s, %s) RETURNING id"
                    cur.execute(query_provstate, (state, country_id))
                    state_id = cur.fetchone()[0]

                query_city = "SELECT id FROM cities WHERE name = %s AND provstate_id = %s AND country_id = %s AND lat = %s AND long = %s"
                cur.execute(query_city, (city, state_id, country_id, latitude, longitude))
                result = cur.fetchone()
                if result:
                    city_id = result[0]
                else:
                    query_city = "INSERT INTO cities (name, provstate_id, country_id, lat, long) VALUES (%s, %s, %s, %s, %s) RETURNING id"
                    cur.execute(query_city, (city, state_id, country_id, latitude, longitude))
                    city_id = cur.fetchone()[0]

                query_attack_type = "SELECT id FROM attack WHERE name = %s"
                cur.execute(query_attack_type, (attack_type,))
                result = cur.fetchone()
                if result:
                    attack_type_id = result[0]
                else:
                    query_attack_type = "INSERT INTO attack (name) VALUES (%s) RETURNING id"
                    cur.execute(query_attack_type, (attack_type,))
                    attack_type_id = cur.fetchone()[0]

                query_target_type = "SELECT id FROM target WHERE name = %s"
                cur.execute(query_target_type, (target,))
                result = cur.fetchone()
                if result:
                    target_type_id = result[0]
                else:
                    query_target_type = "INSERT INTO target (name) VALUES (%s) RETURNING id"
                    cur.execute(query_target_type, (target,))
                    target_type_id = cur.fetchone()[0]

                query_subtarget = "SELECT id FROM subtarget WHERE name = %s AND target_type = %s"
                cur.execute(query_subtarget, (subtarget, target_type_id))
                result = cur.fetchone()
                if result:
                    subtarget_type_id = result[0]
                else:
                    query_subtarget = "INSERT INTO subtarget (name, target_type) VALUES (%s, %s) RETURNING id"
                    cur.execute(query_subtarget, (subtarget, target_type_id))
                    subtarget_type_id = cur.fetchone()[0]

                query_event_exists = """
                    SELECT id FROM events WHERE date = %s AND city_id = %s AND summary = %s AND attack_type = %s 
                    AND corp = %s AND spec_target = %s AND criminal = %s AND motive = %s
                    """
                cur.execute(query_event_exists, (date, city_id, summary, attack_type_id, corp, spec_target, criminal, motive))
                result = cur.fetchone()
                if result:
                    response = {
                    'message': 'Event already exists!',
                        'status': 'duplicate'
                    }
                    self.send_response(409) 
                else:
                    query_event = """
                    INSERT INTO events (date, city_id, summary, attack_type, corp, spec_target, criminal, motive)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(query_event, (date, city_id, summary, attack_type_id, corp, spec_target, criminal, motive))
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

        elif self.path == "/send-reset-password-email":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            receiver_email = data.get('email')

            query = "SELECT id from users where email = %s"
            cur.execute(query, (receiver_email, ))
            result1 = cur.fetchone()

            verified_email = "SELECT id from verify_email where email = %s and is_verified = TRUE"
            cur.execute(verified_email, (receiver_email,))
            result2 = cur.fetchone()

            check_query = "SELECT id from password_reset_tokens WHERE email = %s "
            cur.execute(check_query, (receiver_email, ))
            result3 = cur.fetchone()

            token_query = "SELECT created_at FROM password_reset_tokens WHERE email = %s"
            cur.execute(token_query, (receiver_email,))
            created_at = cur.fetchone()

            if result1 and result2 and (not result3 or result3 and (datetime.now() - created_at[0]).total_seconds() > 3600):
                sender_email = "site.glot@gmail.com"
                sender_password = "ejqz njjz aaxt mjau"

                token, timestamp = generate_reset_token(receiver_email)
                store_token(receiver_email, token, timestamp)

                reset_link = f"http://localhost:5500/reset_password.html?token={token}"

                message = MIMEMultipart("alternative")
                message["Subject"] = "Reset Password"
                message["From"] = sender_email
                message["To"] = receiver_email

                text = f"Please click the link below to reset your password: \n\n{reset_link}"
                part = MIMEText(text, "plain")
                message.attach(part)

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                        response = {
                            'message': 'Email trimis cu succes!',
                            'status': 'succes'
                        }
                        self.send_response(200)
                except Exception as e:
                    response = {
                            'message': 'Eroare la trimiterea emailului:' + str(e),
                            'status': 'fail'
                        }
                    self.send_response(500)
                finally:
                    self._set_cors_headers()
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            elif result1 is None:
                response = {
                    'message': 'The email is not registred!',
                    'status': 'fail'
                }
                self.send_response(401)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            elif result3 is None:
                response = {
                    'message': 'The email is registered, but it wasn\'t verified!',
                    'status': 'fail'
                }
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            elif result3:
                #if (datetime.now() - created_at[0]).total_seconds() < 3600:
                    response = {
                        'message': 'The reset link was already sent!',
                        'status': 'fail'
                    }
                    self.send_response(400)
                    self._set_cors_headers()
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            response = {
                    'message': 'The endpoint doesn\'t exist!',
                    'status': 'fail'
                    }
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_PUT(self):
        if self.path == "/reset-password":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            email = data.get('email')
            new_password = data.get('new_password')
            token = data.get('token')

            try:
                token_query = "SELECT token, created_at FROM password_reset_tokens WHERE email = %s"
                cur.execute(token_query, (email,))
                result = cur.fetchone()

                if result:
                    db_token, created_at = result
                    if token != db_token:
                        response = {
                            'message': 'Token invalid!',
                            'status': 'fail'
                        }
                        self.send_response(401)
                    elif (datetime.now() - created_at).total_seconds() > 3600:
                        response = {
                            'message': 'Token expired!',
                            'status': 'fail'
                        }
                        self.send_response(401)
                    else:
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                        update_query = "UPDATE users SET password = %s WHERE email = %s"
                        cur.execute(update_query, (hashed_password.decode('utf-8'), email))
                        conn.commit()

                        delete_token_query = "DELETE FROM password_reset_tokens WHERE email = %s"
                        cur.execute(delete_token_query, (email,))
                        conn.commit()

                        response = {
                            'message': 'Password reset successful!',
                            'status': 'success'
                        }
                        self.send_response(200)
                else:
                    response = {
                        'message': 'Token not found!',
                        'status': 'fail'
                    }
                    self.send_response(401)

            except Exception as e:
                response = {
                    'message': 'Error: ' + str(e),
                    'status': 'fail'
                }
                self.send_response(500)

            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        elif self.path == "/update-password":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            current_password = data.get('currentPassword')
            new_password = data.get('newPassword')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            try:
                query = "SELECT id, password FROM users WHERE email = %s AND firstname = %s AND lastname = %s"
                cur.execute(query, (email, first_name, last_name))
                result = cur.fetchone()
                print(email, first_name, last_name)

                if result:
                    user_id, stored_password = result
                    if bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8')):
                        new_hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        print()
                        query = "UPDATE users SET password = %s WHERE email = %s AND id = %s"
                        cur.execute(query, (new_hashed_pw, email, user_id))
                        conn.commit()
                        response = {
                            'message': 'Password updated successfully!',
                            'status': 'success'
                        }
                        self.send_response(200)
                    else:
                        response = {
                            'message': 'Current password is incorrect!',
                            'status': 'fail'
                        }
                        self.send_response(401)
                else:
                    response = {
                        'message': 'Bad Request! Something went wrong!',
                        'status': 'fail'
                    }
                    self.send_response(400)
            except Exception as e:
                response = {
                    'message': str(e),
                    'status': 'fail'
                }
                self.send_response(500)

            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == "/update-email":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            current_email = data.get('currentEmail')
            new_email = data.get('newEmail')

            try:
                query = "SELECT id FROM users WHERE email = %s"
                cur.execute(query, (current_email, ))
                user_id = cur.fetchone()

                if user_id:
                    query = "UPDATE users SET email = %s WHERE id = %s"
                    cur.execute(query, (new_email, user_id))
                    conn.commit()

                    token, timestamp = generate_reset_token(new_email)
                    insert_query = "INSERT INTO verify_email (email, token) VALUES (%s, %s)"
                    cur.execute(insert_query, (new_email, token))

                    delete_query = "DELETE FROM verify_email WHERE email = %s"
                    cur.execute(delete_query, (current_email,))
                    conn.commit()

                    verification_link = f"http://localhost:5500/verify_email.html?token={token}"
                    send_verification_email(new_email, verification_link)

                    response = {
                        'message': 'Email updated!',
                        'status': 'success'
                    }
                    self.send_response(200)
                else:
                    conn.rollback()
                    response = {
                        'message': 'The email is not registred!',
                        'status': 'fail'
                    }
                    self.send_response(400)
            except psycopg2.errors.UniqueViolation as e:
                conn.rollback() 
                response = {
                    'message': 'Email already registered!',
                    'status': 'fail'
                }
                self.send_response(400)

            except Exception as e:
                conn.rollback() 
                response = {
                    'message': str(e),
                    'status': 'fail'
                }
                self.send_response(500)
            finally:
                conn.autocommit = True
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            response = {
                'message': 'Resource not found!',
                'status': 'fail'
            }
            self.send_response(404)
            self._set_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))


httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
print("The server is listening...")
httpd.serve_forever()
