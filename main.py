import csv
import os
from datetime import datetime
from time import sleep

import isort
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from rich import console, print

console = console.Console()

project_environment_file_exists = os.path.isfile(
    os.path.dirname(
        os.path.realpath(__file__)) + "\\.env")

project_environment_file = os.path.dirname(
    os.path.realpath(__file__)) + "\\.env"

if not project_environment_file_exists:
    print("\n[blue bold]Let's set your masterpassword...[/blue bold]")
    USER_KEY = console.input("\n[deep_sky_blue1]ENTER master password: [/deep_sky_blue1]", password=True)

    with console.status("[bold green]Working...") as status:
        sleep(1)
        console.print("\n[bold magenta]> Making .env[/bold magenta]")
        sleep(1)

        with open(project_environment_file, "w") as environment:
            console.print("[bold magenta]> Setting up environment[/bold magenta]")
            environment.write(f"USER_KEY = {str(USER_KEY)}\nTOKEN = {Fernet.generate_key().decode('utf-8')}")

            sleep(2)
            console.print("[bold magenta]> Starting App[/bold magenta]")
            sleep(1)


load_dotenv()

SECRET_KEY_MAIN = str(os.getenv('USER_KEY'))
SECRET_KEY = str(os.getenv("TOKEN")).encode("utf-8")
FERNET = Fernet(SECRET_KEY)
CIPHER_SUITE = FERNET


class Database:
    def __init__(self):
        self.escape_loop = "!q"
        self.to_escape = ""
        self.fieldnames = ["name", "password", "added-on"]
        self.filename = "passwords.csv"
        self.copy_filename = "passwords(copy).csv"
        self.file_directory = os.path.dirname(os.path.realpath(__file__))
        self.file_path = "\\".join([self.file_directory, self.filename])

    def create_db(self):
        if os.path.exists(self.file_path):
            return True
        else:
            with open(self.file_path, mode="w") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)

            return app.verify_key()

    def add(self):
        with open(self.file_path, mode="a") as file:
            row = {"name": "", "password": "", "added-on": self.encrypt_data(datetime.now().strftime("%d/%m/%y %H:%M"))}
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)

            console.print(
                f"\n[aquamarine1]To EXIT press:[/aquamarine1] [light_green]'{self.escape_loop}[light_green]'\n")

            while self.to_escape != self.escape_loop:
                for field in row:
                    if field == "added-on":
                        continue
                    value = console.input(f"[deep_sky_blue1]Enter {field}: [/deep_sky_blue1]")
                    if value == "" or value == None:
                        break
                    row[field] = self.encrypt_data(value)

                writer.writerow(row)
                self.to_escape = console.input(
                    "\n[dark_olive_green2][SAVED][/dark_olive_green2]\n[dark_sea_green2]To continue press 'ENTER KEY' or 'RETURN KEY' [/dark_sea_green2]")
            self.to_escape = ""

        return app.menu_or_quit()

    def update(self):
        with open(self.file_path, mode="r") as file:
            writer = csv.DictReader(file)
            console.print(
                f"\n[aquamarine1]To EXIT press:[/aquamarine1] [light_green]'{self.escape_loop}[light_green]'\n")
            update_list = []

            while self.to_escape != self.escape_loop:
                name = console.input("[deep_sky_blue1]Enter name to update: [/deep_sky_blue1]")
                traversing_line = None
                for line in writer:
                    traversing_line = line
                    if self.decrypt_data(line["name"]) == name:
                        for field in line:
                            if field != "added-on":
                                change = console.input(f"\n[light_slate_blue]Change '{field}': [/light_slate_blue]")
                                if change:
                                    traversing_line[field] = self.encrypt_data(
                                        change)
                        update_list.append(traversing_line)
                        console.print("\n[dark_olive_green2][SAVED][/dark_olive_green2]")
                    else:
                        update_list.append(line)

                traversing_line = None
                self.to_escape = console.input(
                    "\n[dark_sea_green2]To continue press 'Enter' or 'Return' [/dark_sea_green2]")
            self.to_escape = ""

        with open(self.file_path, mode="w") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(update_list)

        return app.menu_or_quit()

    def delete(self):
        lines = list()
        name = console.input("\n[deep_sky_blue1]Enter name to[/deep_sky_blue1][bright_red] DELETE[/bright_red]: ")

        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            fields = next(reader)
            lines.append(fields)

            for row in reader:
                if row != []:
                    lines.append(row)
                    for field in row:
                        if name == self.decrypt_data(field):
                            lines.remove(row)

        with open(self.file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

        console.print("\n[red3][DELETED][/red3]\n")
        return app.menu_or_quit()

    def view(self):
        option = console.input(
            "\n[deep_sky_blue1]Enter you master password to continue: [/deep_sky_blue1]", password=True)
        console.print("\n[pale_turquoise1]Your password(s)[/pale_turquoise1]")

        if option == SECRET_KEY_MAIN:
            with open(self.file_path, mode="r") as file:
                csvreader = csv.DictReader(file)
                count = 0

                for row in csvreader:
                    if row != {}:
                        for col in row.keys():
                            row[col] = self.decrypt_data(row[col])
                        console.print(f"\n[dark_sea_green2]>[/dark_sea_green2] [pale_green1]{row}[/pale_green1]")
                        count += 1

            console.print("\n[aquamarine1]# Total:[/aquamarine1]", count, "\n")
            return app.menu_or_quit()
        else:
            console.print("\n[red3][WRONG PASSWORD]\n[/red3]")
            if option == self.escape_loop:
                return app.menu()
            return self.view()

    def download(self):
        console.print(
            f"[turquoise2]Leave empty if you want the file to be in current directory.[/turquoise2]\n[aquamarine1]Current directory:[/aquamarine1] '{self.file_directory}'\n")
        usr_destination = console.input("[deep_sky_blue1]Enter the path: [deep_sky_blue1]")
        destination = self.file_directory

        if usr_destination != "":
            source = os.path.exists(usr_destination)
            if not source:
                console.print("[red3][PATH / FILE NOT EXIST][/red3]")
                return self.download
            destination = usr_destination
        else:
            with open(self.file_path, 'r') as file:
                reader = csv.reader(file)
                fields = next(reader)
                lines = []
                lines.append(fields)
                fields = []
                for row in reader:
                    if row != []:
                        for field in row:
                            fields.append(self.decrypt_data(field))
                        lines.append(fields)
                        fields = []

            with open("/".join([destination, f"{self.copy_filename}"]), 'w') as file:
                writer = csv.writer(file)
                writer.writerows(lines)

        console.print("\n[bright_green][DONE][/bright_green]\n")
        return app.menu_or_quit()

    def encrypt_data(self, string):
        return CIPHER_SUITE.encrypt(bytes(string, encoding="utf-8")).decode("utf-8")

    def decrypt_data(self, string):
        return CIPHER_SUITE.decrypt(bytes(string, encoding="utf-8")).decode("utf-8")


db = Database()


class App:
    def verify_key(self):
        key = console.input("\n[deep_sky_blue1]ENTER Key: [/deep_sky_blue1]", password=True)

        with console.status("[bold green]Verifying...") as status:
            sleep(0.5)
            if key == SECRET_KEY_MAIN:
                console.print("\n[bright_green][VERIFICATION SUCCESSFULL][/bright_green]\n")
                status.stop()
                return self.menu()
            else:
                console.print("\n[red][KEY ERROR]\n\n[EXITING]\n[/red]")

    def menu(self):
        options = {
            "1": lambda: db.add(),
            "2": lambda: db.update(),
            "3": lambda: db.delete(),
            "4": lambda: db.view(),
            "5": lambda: db.download(),
            "!q": lambda: exit()
        }

        option = console.input(
            "1: [green3]Add password(s)\n[/green3]"
            "2: [spring_green3]Update password(s)\n[/spring_green3]"
            "3: [cyan3]Delete existing password(s)\n[/cyan3]"
            "4: [dark_turquoise]View Passwords\n[/dark_turquoise]"
            "5: [turquoise2]Download passwords\n[/turquoise2]"

            "\n[light_goldenrod1]!q to EXIT[light_goldenrod1]\n\n"

            "[deep_sky_blue1]ENTER CHOICE: [/deep_sky_blue1]"
        )

        options[option]()

    def menu_or_quit(self):
        option = console.input("[slate_blue1]\nEnter '!m' for menu or '!q' for exit: [/slate_blue1]").lower()
        print("")
        if option == "!m":
            return self.menu()
        elif option == "!q":
            exit()
        else:
            console.print("\n[red3][INVALID][/red3]\n")
            return self.menu_or_quit()


app = App()


if __name__ == "__main__":
    print(r"""
   ___                                    _                                                
  / _ \__ _ ___ _____      _____  _ __ __| |       /\/\   __ _ _ __   __ _  __ _  ___ _ __ 
 / /_)/ _` / __/ __\ \ /\ / / _ \| '__/ _` |_____ /    \ / _` | '_ \ / _` |/ _` |/ _ \ '__|
/ ___/ (_| \__ \__ \\ V  V / (_) | | | (_| |_____/ /\/\ \ (_| | | | | (_| | (_| |  __/ |   
\/    \__,_|___/___/ \_/\_/ \___/|_|  \__,_|     \/    \/\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                           |___/           
        """)

    isort.file(__file__)

    if db.create_db():
        app.verify_key()
