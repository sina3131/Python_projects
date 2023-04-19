







import requests
import json
from datetime import timedelta, datetime
import sys


class CurrencyConverter:
    def __init__(self):  # Class constructor contains the data that could be used in all methods
        self.fetch = self.fetch_currency_data()
        self.api_data = self.load_currency_data()
        if self.api_data is None:
            self.api_data = self.fetch_currency_data()

    def load_data_file(self):  # Loading data from a json file
        try:
            with open('export_data.json', "r") as curr_file:
                currency = json.load(curr_file)
                x = currency['rates']
                return x
        except (FileNotFoundError):
            print("seems that the file doesn't exist, please upload the file")

    def fetch_currency_data(self):  # Fetching the data from the API
        try:
            url = f"https://openexchangerates.org/api/latest.json?app_id=9d97247b1a104ebd8d3f401bd25f40d2"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()
            self.rates = data['rates']
        except (ConnectionError, requests.ConnectionError):
            print("Please check your internet conncetion")

    def convert_from_usd(self):  # Converting from USD to currency of choice
        try:
            self.load_data_file()

            user_choice = (input("USD to which currency? ")).upper()
            amount = int(input("how much? "))
            # picking out the chosen currency rate
            chosen_rate = self.rates[user_choice]
            conversion = round(amount*chosen_rate, 3)
            print(amount, "USD is equal to:", conversion, user_choice)
        except (ValueError, KeyError, TypeError):
            print("Please check your spelling")
            try:
                self.load_data_file()
                x = self.rates
                user_choice = (input("USD to which currency? ")).upper()
                amount = int(input("how much? "))
                # picking out the chosen currency rate
                chosen_rate = x[user_choice]
                conversion = round(amount*chosen_rate, 3)
                print(amount, "USD is equal to:", conversion, user_choice)
            except (FileNotFoundError):
                try:
                    self.api_data()
                    x = self.api_data['rates']
                    user_choice = (input("USD to which currency? ")).upper()
                    amount = int(input("how much? "))
                    # picking out the chosen currency rate
                    chosen_rate = x[user_choice]
                    conversion = round(amount*chosen_rate, 3)
                    print(amount, "USD is equal to:", conversion, user_choice)
                # Catch errors that is common in this section
                except (TypeError, ValueError, ConnectionError, KeyError):
                    print(
                        "Please check internet connection and make sure you write the input properly")
                convert_again = input(
                    "To convert again press 1 to go back to menu press 2")
                if convert_again == "1":
                    self.convert_from_usd()
                if convert_again == "2":
                    main()

    def convert_any_currency(self):  # Converting any currency
        while True:
            try:
                self.load_data_file()
                # acsess rates information in the dict
                from_what_currency = (input("from what currency? ")).upper()
                to_currency = (input("to what currency?")).upper()
                amount = int(input("how much? "))
                # This formel converts from any currency to any currency
                conversion_any = round(amount *
                                    self.rates[to_currency] / self.rates[from_what_currency], 3)
                print(amount, from_what_currency, "is equal to ",
                    conversion_any, "of", to_currency)
                converting_again = input(
                    "To convert again press 1, To go back to menue press 2 ")
                if converting_again == "1":
                    self.convert_any_currency()
                if converting_again == "2":
                    main()
            except (KeyError, ValueError, TypeError):
                try_again = input(
                    "Please check your spelling, press 1 for trying again")
                if try_again == "1":
                    self.convert_any_currency()
                    break
            try:
                self.api_data()
                x = self.api_data['rates']
                # acsess rates information in the dict
                from_what_currency = (input("from what currency? ")).upper()
                to_currency = (input("to what currency?")).upper()
                amount = int(input("how much? "))
                # This formel converts from any currency to any currency
                conversion_any = round(amount *
                                       x[to_currency] / x[from_what_currency], 3)
                print(amount, from_what_currency, "is equal to ",
                      conversion_any, "of", to_currency)
                converting_again = input(
                    "To convert again press 1, To go back to menue press 2 ")
                if converting_again == "1":
                    self.convert_any_currency()
                if converting_again == "2":
                    main()
            except (FileNotFoundError, FileExistsError):
                try:
                    self.api_data()  # Loading data
                    x = self.api_data['rates']
                    # acsess rates information in the dict
                    from_what_currency = (
                        input("from what currency? ")).upper()
                    to_currency = (input("to what currency?")).upper()
                    amount = int(input("how much? "))
                    # This formel converts from any currency to any currency
                    conversion_any = round(amount *
                                           x[to_currency] / x[from_what_currency], 3)
                    print(amount, from_what_currency, "is equal to ",
                          conversion_any, "of", to_currency)
                    converting_again = input(
                        "To convert again press 1, To go back to menue press 2 ")
                    if converting_again == "1":
                        self.convert_any_currency()
                    if converting_again == "2":
                        main()
                except (TypeError, KeyError, ConnectionError, requests.ConnectionError):  # Catching errors
                    print(
                        "Please check your internet connection and make sure to write the input properly")
                go_back = input("Press 1 to go to main menu")
                if go_back == "1":
                    break

    def list_currencies(self):
        url = "https://openexchangerates.org/api/currencies.json?prettyprint=false&show_alternative=false&show_inactive=false&app_id=9d97247b1a104ebd8d3f401bd25f40d2"
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            list_json = response.json()

            filename = 'list_currencies.json'
            with open(filename, 'w')as f:  # This code stores the data to a json file
                json.dump(list_json, f)
            for k, v in list_json.items():  # this code block prints out availible currencies as a list
                print(k, v)
            go_back = input("To go back to first menu press 1\n")
            if go_back == "1":
                main()
        # In the event of no internet connection we list currencies from an already existing file.
        except (requests.ConnectionError):
            try:
                with open('currency_list.json', "r") as curr_file:
                    currency = json.load(curr_file)
                    for k, v in currency.items():  # this code block prints out availible currencies as a list
                        print(k, v)
                    go_back = input("To go back to first menu press 1\n")
                    if go_back == "1":
                        main()
            # If the file doesn't exist and we are not connected to internet user gets the info.
            except (FileNotFoundError):
                recover = input(
                    "Seems that the data file doesn't exist, make sure you are connected to internet and Press 1 to go to main menu and then press 3 for recovering the data.")
                if recover == "1":
                    self.list_currencies()  # Recovering th data.

    def load_currency_data(self):  # Loading data from a json file
        try:
            with open('export_data.json', "r") as curr_file:
                currency = json.load(curr_file)
                self.rates = currency['rates']
                # Acsessing the timestap information in the data dict
                time_stap = currency['timestamp']
                # Changing the timestap format to readable format
                timeobject = datetime.fromtimestamp(time_stap)
                # Check if data is older that 1 hour update the data
                if timeobject < datetime.utcnow() + timedelta(minutes=-60):
                    self.fetch_currency_data()
        except (FileNotFoundError):
            upload_file = input(
                "Seems that the data file doesn't exist, make sure you are connected to internet and Press 1 to go to main menu and then press 3 for recovering the data.")
            if upload_file == "1":
                self.fetch_currency_data()

    def export_to_json(self):  # Updating the data by fetching new data from the api
        while True:
            url = "http://www.google.com"  # Check wether user is connected to internet or not
            timeout = 3
            try:
                request = requests.get(url, timeout=timeout)
                print("Connected")
            except (ConnectionError, requests.ConnectionError):
                print("Please check your internet connection")
                break

            try:
                url = f"https://openexchangerates.org/api/latest.json?app_id=9d97247b1a104ebd8d3f401bd25f40d2"
                # This needs to be added, it tells the API that they should return JSON
                headers = {"accept": "application/json"}
                response = requests.get(url, headers=headers)
                new_data = response.json()
                # Get updatet data from API
                filename = 'export_data.json'
                with open(filename, 'w')as f:  # This code stores the data to a json file
                    json.dump(new_data, f)
                back = input(
                    "Data has been exported press 1 to go to the main menu\n")
                if back == "1":
                    break
            except (ConnectionError, requests.ConnectionError):
                print("Please check your internet connection")


def main():
    usd_currency_converter = CurrencyConverter()

    while True:
        print("Welcome to the currency converter application ")
        user_choice = input("press [0] To list all currencies\n"
                            "press [1] Convert USD to a currency of choice\n"
                            "press [2] Refresh the data\n"
                            "press [3] Export the data to JSON\n"
                            "press [4] for converting any currency\n"
                            "press [5] for exiting the program\n")

        if user_choice == "0":
            usd_currency_converter.list_currencies()
        if user_choice == "1":
            usd_currency_converter.convert_from_usd()
        if user_choice == "2":
            usd_currency_converter.fetch_currency_data()
        if user_choice == "3":
            usd_currency_converter.export_to_json()
        if user_choice == "4":
            usd_currency_converter.convert_any_currency()
        if user_choice == "5":
            sys.exit("Take care :)")


if __name__ == "__main__":
    main()
