import auth
# import password_hash as phS
import userdata as ud
from aes_class import aes
from password_hash import crypto
import secrets
import string


databae = auth.DATABASE()
usrdata = ud.UserData()

class Main:

    def __init__(self):
        pass

    def main_menu(self, obj: databae):
        conn = obj.main_menu()
        with conn:
            user_inp = input("Registrieren: R | Login: L | Passwort ändern: U | Alle Profile ausgeben "
                             "(Funktion wird später entfernt): S | User löschen: D | Beenden: X\n")

            if user_inp.upper() == "R" or user_inp == "r":
                user = obj.register_user(conn)
                if user is not None:
                    user_id = obj.create_user(conn, user)

            elif user_inp == "L" or user_inp == "l":
                user_name = obj.password_authentication(conn)
                self.login(user_name, usrdata)

            elif user_inp == "U" or user_inp == "u":
                obj.update_password(conn)

            elif user_inp == "S" or user_inp == "s":
                obj.select_all_users(conn)

            elif user_inp == "D" or user_inp == "d":
                user_name = obj.password_authentication(conn)
                choice = input("Wollen sie diesen User wirklich entfernen? (y zum Bestätigen)")
                if choice == "y":
                    obj.delete_user(conn, user_name)

            elif user_inp == "X" or user_inp == "x":
                exit("Das Programm ist beendet.")
            self.main_menu(databae)

    def login(self, usern, obj: usrdata):
        conn2 = obj.main_auth(usern)
        with conn2:
            user_inp = input("Neuen Dienst registrieren: R | Passwort eines Dienstes ausgeben: P |  "
                             "Alle gespeicherten Dienste ausgeben: S | Passwort eines Dienstes ändern: A "
                             "| Zufälliges Passwort ausgeben : Z | Dienst löschen : D | "
                             "Beenden: X\n")
            if user_inp == "R" or user_inp == "r":
                user = obj.register_name()
                user_id = obj.create_name(conn2, user)
                self.login(usern, usrdata)

            elif user_inp == "S" or user_inp == "s":
                obj.select_all_names(conn2)
                self.login(usern, usrdata)

            elif user_inp == "X" or user_inp == "x":
                exit("Das Programm ist beendet.")

            elif user_inp == "P" or user_inp == "p":
                password = obj.give_passwort(conn2)
                print(password)
                self.login(usern, usrdata)

            elif user_inp == "a" or user_inp == "A":
                ID = input("Geben Sie die Id des zu ändernden Dienstes an: ")
                obj.update_password(conn2, ID)
                self.login(usern, usrdata)

            elif user_inp =="Z" or user_inp == "Z":
                passw_length = input("Geben sie die Länge des Passworts ein: ")
                passw_length = int(passw_length)
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(passw_length))
                print("Ihr zufälliges Passwort: \t" + password)

                self.login(usern, usrdata)
            elif user_inp == "D" or user_inp == "d":
                ID = input("Geben Sie die Id des zu entfernenden Dienstes an: ")
                choice = input("Wollen sie diesen Dienst wirklich entfernen? (y zum Bestätigen) ")
                if choice == "y":
                    obj.delete_name(conn2, ID)
                    self.login(usern, usrdata)
                else:
                    print("Wurde nicht gelöscht")
                    self.login(usern, usrdata)

            else:
                print("Nicht definiert")
                login(usern, usrdata)


if __name__ == '__main__':
    start = Main()
    start.main_menu(databae)