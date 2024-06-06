from pymongo import MongoClient
from bson.objectid import ObjectId
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from bson.json_util import dumps
import re
import psycopg2


client = MongoClient("localhost", 27017)
db = client.CloudComputing

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

    def findObject(self, post_body_str):
        l = []

        print("sunt in functie")
        books = db.books

        i = post_body_str.find("""title":""")
        j = post_body_str.find(",")
        title = post_body_str[i + 9:j - 1:]
        print(title)

        i = post_body_str.find("""author":""")
        j = post_body_str.index(",", i)
        author = post_body_str[i + 10:j - 1:]
        print(author)

        i = post_body_str.find("""genre":""")
        j = post_body_str.index(",", i)
        genre = post_body_str[i + 9:j - 1:]
        print(genre)

        i = post_body_str.find("""index":""")
        j = post_body_str.index("\n", i)
        index = post_body_str[i + 8:j - 1:]
        print(index)

        #book = books.find({"title" : {"$ne" : title}})
        #ok = 0
        #l = list(book)
       # for ind in book:
        #    ok = 1
         #   print(ind)
        #print(len(l))
        #if len(l) > 0:
            #print(books.count_documents({"title" : title, "author" : author, "genre":genre, "index":index}))
            #return 0

        book = books.findOne({"title" : title})
        if book is not null:
            return 0

        else:
            book = books.find({"title": title, "author": author, "genre": genre, "index": index})
            if book.count > 0:
                return 0
        return 1



    def do_GET(self):
        if self.path == "/books":
            try:
                books = db.books
                i = 1

                book = books.find()
                list_cur = list(book)
                if not list_cur:
                    self.send_response(204)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'204 - No Content')
                else:
                    json_data = dumps(list_cur, indent=2)
                    with open("sample.json", "w") as outfile:
                        outfile.write(json_data)

                    file_to_open = open("sample.json").read()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(file_to_open, 'utf-8'))

            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')

        elif re.match(r"/book/\d+", self.path):
            try:
                books = db.books

                try:
                    i = int(self.path[6::])
                    book = books.find({"index": i})
                    list_cur = list(book)
                    if not list_cur:
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'404 - Not Found')

                    else:
                        json_data = dumps(list_cur, indent=2)
                        with open("sample.json", "w") as outfile:
                            outfile.write(json_data)

                        file_to_open = open("sample.json").read()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(bytes(file_to_open, 'utf-8'))

                except:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'500 - Internal Server Error')
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')

        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'400 - Bad Request')

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
        if "/books" == self.path:
            try:
                self.send_response(405)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'405 - Method Not Allowed')

            except:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'500 - Internal Server Error')

        elif re.match(r"/book/\d+", self.path):
            try:
                books = db.books
                try:
                    i = int(self.path[6::])
                    book = books.find({"index": i})
                    list_cur = list(book)
                    if not list_cur:
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'404 - Not Found')

                    else:
                        content_len = int(self.headers.get('Content-Length'))
                        post_body = self.rfile.read(content_len)
                        post_body_str = post_body.decode('utf-8')
                        print(post_body_str)
                        data = json.loads(post_body_str)
                        print(data)

                        books.update_one({"index" : i}, {"$set": data})

                        for book in books.find():
                            print(book)

                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'200 - OK')

                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'500 - Internal Server Error')

            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')

        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'400 - Bad Request')


    def do_DELETE(self):
        if self.path == "/books":
            try:
                self.send_response(405)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'405 - Method Not Allowed')

            except:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'500 - Internal Server Error')

        elif re.match(r"/book/\d+", self.path):
            try:
                books = db.books

                try:
                    i = int(self.path[6::])
                    book = books.find({"index": i})
                    list_cur = list(book)
                    if not list_cur:
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'404 - Not Found')

                    else:
                        books.delete_one({"index": i})
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'200 - OK')

                except:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'500 - Internal Server Error')

            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')

        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'400 - Bad Request')



httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
print("The server is listening...")
httpd.serve_forever()
cur.close()
conn.close()

