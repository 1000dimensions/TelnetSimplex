import socket
from threading import Thread
import threading
import sqlite3 as sql
from sqlite3 import Error
db = "login.db"

HOST = ""
##HOST = socket.gethostbyname(socket.gethostname()) 
print(socket.gethostname())
PORT = 1026

clients = set()
clientLock = threading.Lock()
q1 = """SELECT username, password FROM 'login' WHERE username = ?"""
#Threading is my favorite
def create_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file, isolation_level=None)
        print(sql.version)
    except Error as e:
        print(e)
    return conn
def create_table(conn, create_table_sql):
    try:
        c.execute(create_table_sql)
    except Error as e:
        print(e)

sql_create_login = """CREATE TABLE IF NOT EXISTS login (
                    player_id int PRIMARY KEY,
                    username VARCHAR(1024) NOT NULL,
                    password VARCHAR(1024) NOT NULL
                    );""" ##Well. This is going to be fun.
sql_new_account = """INSERT INTO login(username, password)
                    VALUES(?,?)"""
def on_new_client(cs, addr):
    global c
    conn = create_connection(db)
    c = conn.cursor()
    if conn is not None:
        create_table(conn, sql_create_login)
    print(conn)
    conn = create_connection(db)
    cs.send(b"""If you have a account type 'Login'.
Otherwise type 'Create Account'""")
    ans = cs.recv(1024).decode()
    ans = ans[:-2]
    print(cs)
    if ans == "Login":
        
        while True:
            try:
                cs.send(b"What is the username? ")
                username = cs.recv(1024).decode()
                username = username[:-2]
            except:
                print("Invalid character was submitted")
                cs.send(b"Invalid character was submitted")
            else:
                break
        
        rs = c.execute(q1, (username,))
        print(rs)
        print(username)
        result = rs.fetchall()
        print(result)
        for x in result:
            if username in x:
                while True:
                    try:
                        cs.send(b"What is the password?")
                        password = cs.recv(1024).decode()
                        password = password[:-2]
                    except:
                        print("Invalid Character was inputed")
                        cs.send(b"Invalid Character was inputed")
                    else:
                        break
                    if password in x:
                        cs.send(b"""Logged in
""")
                        print("works")
                        break
                    else:
                        print("Attempted login w/ password")
                        cs.send(b"Incorrect password")
                        cs.send(b"""Loginning in as Guest
""")
                        username = "Guest"
                        break
                else:
                    print("Username incorrect")
                    cs.send(b"Incorrect Username. Does not exist.")
                    cs.send(b"""Loginning in as Guest
""")
                    username = "Guest"
    elif ans == "Create Account":
        while True:
            cs.send(b"What is your Username? ")
            username = cs.recv(1024).decode()
            username = username[:-2]
            unique = c.execute(q1, (username,))
            hi = unique.fetchone()
            print(hi)
            if hi is not None:
                print("User already exists")
                cs.send(b"""Username already exists. Choose another
                        """)
            else:
                break
        cs.send(b"What is your password? ")
        password = cs.recv(1024).decode()
        password = password[:-2]
        account = (username, password)
        
        ten = c.execute(sql_new_account, account)
        conn.commit()
        print(ten)
        


    else:
        cs.send(b"""Guest it is then.
""")
        username = "Guest"
        print("Guest has logged in. Limiting rights.")
    
    cs.send(b"""Welcome to SimplexChat!
Created By 1000Dimensions.
To quit just type in quit()
Have fun communcating!
""")
    spam = 0
    k = " "
    while True:
        try:
            cs.send(b" ")
        except socket.error as e:
            ##Thanks to mhawke for answering this question https://stackoverflow.com/questions/180095/how-to-handle-a-broken-pipe-sigpipe-in-python
            if isinstance(e.args, tuple):
                print("error is" + e[0])
                if e[0] == errno.EPIPE:
                    print("Client Disconnected... Removing")
                    break
                else:
                    pass
    
        while True:
            try:
                data = cs.recv(1024).decode()
                data = data[:-2]
            except:
                cs.send(b"Invalid Character was submitted. Don't break the server kid")
                print("Invalid character")
                k = "Invalid"
                break
            else:
                break
            ##Spam Filter if user puts in 5 blanks it kicks them
        if data == "" :
            print(f"{username} has put in a blank")
            spam += 1
            if username == "Guest":
                if spam == 2:
                    cs.send(b"""We are disconnecting you because you are a guest,
and personally I don't trust guests.
You can relogin, but I recommend creating an account.
Thanks :)
""")
                    break
            if spam == 5:
                cs.send(b"""You have put in a blank 5 times.
Due to our spam policy we must disconnect you.
You are able to reconnect.
Good Bye.
""")
                break
        if data == "quit()":
            break
        if k == "Invalid":
            break
        with clientLock:
            data = "User:" + username + " > " + data + """
"""
            print(data)
            for c in clients:
                c.sendall(data.encode())
    cs.close()
    clients.remove(cs)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
##Binds socket.
s.listen()
while True:
    con, addr = s.accept()
    with clientLock:
        clients.add(con)
    print(f"New connection from {addr}" )
    thread = Thread(target=on_new_client, args=(con, addr))
    thread.start()
    
conn.close()
thread.join()        


