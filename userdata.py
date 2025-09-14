import sys
import sqlite3
from sqlite3 import Error
from password_hash import crypto
from aes_class import aes

class UserData:
    def __init__(self):
        pass

    def create_name(self, conn, user):
        #  Benutzerprofil erstellen
        sql = """ INSERT INTO userdata(name, password, email, username) VALUES(?,?,?,?) """

        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()

        return cur.lastrowid

    def create_connection(self, userdata):
        #  Verbindungsaufbau
        conn = None
        try:
            conn = sqlite3.connect(userdata)
            # return conn
        except Error as e:
            print(e)
        return conn


    def register_name(self):
        #  Registrierung
        un = input("Geben Sie einen Namen ein:")
        ptpw = input("Geben Sie ein Passwort ein:")
        email = input("Geben Sie ihre E-Mail ein:")
        username = input("Geben Sie ihren Anmeldenamen ein:")

        ptpw = aes.encrypt(ptpw, crypto.password_uncode)

        user = (un, ptpw, email, username)
        return user


    def create_table(self, conn, create_table_sql):
        #  Erstellen eines neuen Tables in der DB
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def select_all_names(self, conn):
        cur = conn.cursor()
        cur.execute(""" SELECT user_id, name, username, email FROM userdata """)

        rows = cur.fetchall()
        for row in rows:
            print(row)

    def give_passwort(self, conn):
        id = input("ID des Dienstes: ")
        cur = conn.cursor()
        cur.execute("SELECT password FROM userdata WHERE user_id =?", (id,))
        passwort = cur.fetchone()[0]
        passwort = aes.decrypt(passwort, crypto.password_uncode)
        return passwort

    def delete_name(self, conn, id):
        #  Benutzerprofil löschen
        sql = """ DELETE FROM userdata WHERE user_id = ? """
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()

    def update_password(self, conn, id):
        cur = conn.cursor()
        storable_pw = None
        new_pw = input("Neues Passwort eingeben: ")
        new_pw_test = input("Neues Passwort bestätigen: ")
        if new_pw == new_pw_test:
            storable_pw = aes.encrypt(new_pw, crypto.password_uncode)
            cur.execute(" UPDATE userdata SET password = ? WHERE user_id = ? ", (storable_pw, id))
            conn.commit()
        else:
            print("Die eingegebenen Passwörter stimmen nicht überein!")



    def main_auth(self, user):
        database = "user_" + user + ".db"

        # create database connection
        conn = self.create_connection(database)
        sql_create_table = """ CREATE TABLE IF NOT EXISTS userdata (
                                               user_id integer PRIMARY KEY,
                                               name text NOT NULL,
                                               password text NOT NULL,
                                               email text,
                                               username text
                                           ); """
        self.create_table(conn, sql_create_table)
        return conn



