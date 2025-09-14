import sqlite3
import sys
from sqlite3 import Error
import password_hash
from password_hash import crypto


class DATABASE:
    def __init__(self):
        self.user_name = None
        self.password = None
        self.id = None
        self.stored_password = None


    #  Developer-Methode!
    def create_connection(self, auth):
        #  Verbindungsaufbau
        conn = None
        try:
            conn = sqlite3.connect(auth)
            # return conn
        except Error as e:
            print(e)
        return conn

    #  Developer-Methode!
    def create_table(self, conn, create_table_sql):
        #  Erstellen eines neuen Tables in der DB
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    #  Developer-Methode!
    def verify_password_input(self, conn, user_name):
        #  Inputcheck Passwort - Gespeichertes Passwort
        cur = conn.cursor()
        stored_password = "a"
        password = "b"
        if cur.execute(" SELECT EXISTS( SELECT 1 FROM auth WHERE username = ?) ", (user_name,)).fetchone()[0] == 1:
            #  print("nice")
            stored_password = cur.execute(" SELECT password FROM auth WHERE username = ? ",
                                          (user_name,)).fetchone()[0]
            password = input("Passwort: ")
        else:
            pass

        if password != "b":
            return crypto.verify_password(password, stored_password)
        else:
            pass

    #  Developer-Methode!
    def create_user(self, conn, user):
        #  Benutzerprofil erstellen
        sql = """ INSERT INTO auth(username,password) VALUES(?,?) """
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
        return cur.lastrowid

    def register_user(self, conn):
        #  Registrierung
        cur = conn.cursor()
        un = input("Geben Sie einen Benutzernamen ein:")
        if cur.execute(" SELECT EXISTS( SELECT 1 FROM auth WHERE username = ?) ", (un,)).fetchone()[0] == 1:
            print("Username already exists log in or use other name")
            return
        ptpw = input("Geben Sie ein Passwort ein: ")
        storable_pw = crypto.encrypt_password(ptpw)

        user = (un, storable_pw)
        return user

    def update_password(self, conn):
        cur = conn.cursor()
        self.user_name = input("Benutzername:")
        storable_pw = None
        if self.verify_password_input(conn, self.user_name):
            new_pw = input("Neues Passwort eingeben: ")
            new_pw_test = input("Neues Passwort bestätigen: ")
            if new_pw == new_pw_test:
                storable_pw = crypto.encrypt_password(new_pw)
                cur.execute(" UPDATE auth SET password = ? WHERE username = ? ", (storable_pw, self.user_name))
                conn.commit()
            else:
                print("Die eingegebenen Passwörter stimmen nicht überein!")
        else:
            print("Benutzername/Altes Passwort falsch!")

    def delete_user(self, conn, username):
        #  Benutzerprofil löschen
        sql = """ DELETE FROM auth WHERE username = ? """
        cur = conn.cursor()
        cur.execute(sql, (username,))
        conn.commit()

    #  Developer-Methode!
    def delete_all_users(self, conn):
        #  Alle Benutzerprofile löschen
        sql = """ DELETE FROM auth """
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    # Developer-Methode!
    def select_all_users(self, conn):
        #  Alle Benutzerprofile ausgeben
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM auth """)

        rows = cur.fetchall()
        for row in rows:
            print(row)

    def password_authentication(self, conn):
        #  Login
        count = 0  # counter for runthroughs
        max_count = 3  # max runthroughs

        #  First runthrough, welcome
        print("Guten Tag!\n")
        self.user_name = input("Benutzername: ")
        #  self.verify_password_input(conn)

        while True:
            #  If username and pw correct --> Exit authentication, progress with next operation
            if self.verify_password_input(conn, self.user_name):
                print("\nHerzlich Willkommen!")  # Access granted
                return self.user_name

            #  Count +1; test for max_count --> if too many runthroughs --> sys.exit
            else:
                count += 1
                if count == max_count:
                    #  Exit whole program, restart required
                    #  print("\nBenutzername und/oder Passwort falsch! Bitte versuchen Sie es erneut!")
                    sys.exit("\nZu viele gescheiterte Versuche! Starten Sie das Programm neu!")  # Exit program
                #  Not too many runthroughs --> another try
                print("\nBenutzername und/oder Passwort falsch! Bitte versuchen Sie es erneut!")
                self.user_name = input("Benutzername: ")
                continue  # Continue loop

    def main_menu(self):
        database = "auth.db"

        # create database connection
        conn = self.create_connection(database)

        sql_create_table = """ CREATE TABLE IF NOT EXISTS auth (
                                               user_id integer PRIMARY KEY,
                                               username text NOT NULL,
                                               password text
                                           ); """
        self.create_table(conn, sql_create_table)

        return conn
