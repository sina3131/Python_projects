
import json
from operator import itemgetter
import sys


class TvDatabase:
    def __init__(self, language):
        self.languages = ['tl', 'pt', 'fr', 'sv', 'en', 'ko', 'it', 'ja', 'no', 'ca',
                        'he', 'ar', 'nl', 'is', 'tr', 'ru', 'de', 'hi', 'es', 'pl', 'th', 'zh', 'da']
        self.tv_shows = []
        self.language = language
        self.load = self.load_tv_shows()

    def load_tv_shows(self):
        try:
            with open('tv.json', "r") as show_file:  # Opening the json file in read mode.
                shows = json.load(show_file)
                self.data = shows
            self.dict = {}
            for f in shows:
                self.dict.update(f)
        except (FileNotFoundError):
            raise FileNotFoundError(f"Unable to find the data file, Please check and try again")

    def search_tv_show(self, word_to_search_for):
        try:
            for show in self.data:  # Loop and acsessing the items within the list of dict.
                if word_to_search_for == show['name']:  # if input matches any names in the dataset return the name.
                    return show['name']
        except(TypeError, ValueError, KeyError, AttributeError):
            raise ValueError("Please make sure that you have right vlaue")
        for charcters in word_to_search_for:
            self.cha = charcters
        for i in self.data:
            if self.cha in i['name']:
                self.result = i['name']
        raise ValueError("Please make sure that you have the right value")
    def popular_tv_shows(self, number_shows_to_list):
        try:
            if number_shows_to_list < 5:
                return None
            if number_shows_to_list > 20:
                return None
            # Sort the list by popularity attribute using itemgetter funtion.
            newlist = sorted(self.data, key=itemgetter('popularity'), reverse=True)
            # Slicing the outcome which is a list, starting from 0 to the number entered by the user.
            result = newlist[0:number_shows_to_list]
            self.list_shows = result
        except(FileNotFoundError):
            raise TypeError("Please make sure your spelling is correct")
        raise FileNotFoundError("please make sure that you have the data file")
        
        

        # 99%
    def list_shows_based_on_language(self, language):
        try:
            for i in self.data:
                lang = i['original_language']  # Acsessing the specefic item within the dataset.
                if lang == language:
                    # getting matched data by parameter input
                    self.data_show_lang = (f"{i['name']} {i['original_language']}")
        except(FileNotFoundError):
            raise FileNotFoundError ("Please make sure that you have the data file avialible")
        raise ValueError("Please make sure that you have correct input")

    def compare_tv_show_ratings(self, first_tv_show, second_tv_show):
        try:
            for i in self.data:
                rating = i['name']
                if rating == first_tv_show:
                    self.compare_tv_show_first = (f"First Tv show vote: {i['vote_average']}")
                    self.a = i["vote_average"]
            for i in self.data:
                rating = i['name']
                if rating == second_tv_show:
                    self.compare_tv_show_secound = (f"Secound Tv show vote:{i['vote_average']}")
                    self.b = i["vote_average"]
        except(FileNotFoundError, FileExistsError):
            raise FileNotFoundError ("Please make sure that you have the data file availibe ")
        raise ValueError("Please make sure that you have correct input")

    def list_latest_shows(self, number_of_shows_to_list):
        try:

            #self.data.sort(key = lambda x: datetime.strptime(x['first_air_date'], '%d-%-%'))
            #self.data.sort(key=itemgetter("first_air_date"), reverse=True)
            # it works with int keys but not strings.
            something_sorted = sorted(self.data, key=itemgetter("first_air_date"), reverse=True)
            #print(something_sorted)
        except(ValueError, AttributeError, KeyError):
            raise ValueError ("Please make sure you have correct input")


class Menu():
    def __init__(self):
        self.tv_db_en = TvDatabase(language="en")
        self.start_main_menu()

    def start_main_menu(self):

        print("Welcome to movie application choose one of the options below\n")
        user_choice = input("[1] - TV-show summary\n"
                            "[2] - Compare tv-shows\n"
                            "[3] - List popular tv-shows\n"
                            "[4] - Export tv-shows from a language of choice\n"
                            "[q] - Quit \n"
                            )

        if user_choice == "1":
            try:

                self.tv_db_en.load_tv_shows()
                self.tv_show_summary()
            except (FileNotFoundError):
                print("The data file is missing, please check and try again")

            exit = input("To exit the programe press 1\n")
            if exit == "1":
                sys.exit()
        if user_choice == "2":
            try:
                self.tv_db_en.load_tv_shows()  # Error file not found
            except (FileNotFoundError):
                print("The data file is missing, please check and try again")
            self.compare_ratings()
            exit = input("To exit the programe press 1\n")
            if exit == "1":
                sys.exit()
        if user_choice == "3":
            try:
                self.tv_db_en.load_tv_shows()
            except (FileNotFoundError):
                print("The data file is missing, please check and try again")
            self.list_popular_shows()
            exit = input("To exit the programe press 1\n")
            if exit == "1":
                sys.exit()
        if user_choice == "4":
            try:
                self.tv_db_en.load_tv_shows()
            except (FileNotFoundError):
                print("The data file is missing, please check and try again")
            self.export_tv_shows()
        if user_choice == "q":
            sys.exit()
        if user_choice == "5":
            self.tv_db_en.load_tv_shows()
            self.tv_db_en.list_latest_shows("somethin")

    def tv_show_summary(self):
        try:
            self.tv_db_en.load_tv_shows()
            for c, v in enumerate(self.tv_db_en.data):
                print(f"ID: {c} = Origin counrty: {v['origin_country']}  Name:{v['name'] }")
            user_input = input("Tv show summary, to search tv show by name press 1\n"
                            "Tv show summary, to search tv show by ID nr press 2\n")
        except (TypeError, ValueError, KeyError, AttributeError):
            print("Please check your typing")
        try:
            if user_input == "1":
                user_input_name = input("write the name of your favorit show example(Game of Thrones):\n")
                for i in self.tv_db_en.data:
                    if user_input_name == i['name']:
                        print(
                            f"Name: {i['name']} Avreage vote: {i['vote_average']} First air date: {i['first_air_date']} Origin Country: {i['origin_country']}")
                        print(f"Short overview of the movie:\n{i['overview']}")
                for charcters in user_input_name:
                    self.cha = charcters
                for i in self.tv_db_en.data:
                    if self.cha in i['name']:
                        self.result = i['name']
                        print(
                            f"Name: {i['name']}  Avreage vote: {i['vote_average']} First air date: {i['first_air_date']} Origin Country: {i['origin_country']}\n")
                        print(f"Short overview of the movie:\n{i['overview']}\n")
                        go_back = input("This show contains your input press any key to see next one\n")

        except (KeyError, TypeError, ValueError, AttributeError):
            print("Please check your spelling")

        try:
            if user_input == "2":
                user_input_id = int(
                    input("to see a summary of a show, type the id nr of your favorit show that you see in the list above:\n"))
                print(
                    f"First air date: {self.tv_db_en.data[user_input_id]['first_air_date']} Name: {self.tv_db_en.data[user_input_id]['name']} , Origin country: {self.tv_db_en.data[user_input_id]['origin_country']} Average vote: {self.tv_db_en.data[user_input_id]['vote_average']}")
                print(f"Short overview of the movie:\n{self.tv_db_en.data[user_input_id]['overview']}")
        except (KeyError, TypeError, ValueError, AttributeError):
            print("Please check your typing example(2632)")

    def list_popular_shows(self):
        try:
            user_input = int(
                input("please provide a number between (5-20) for the amount of most popular shows that you want to see "))
            self.tv_db_en.popular_tv_shows(user_input)
            for i, v in enumerate(self.tv_db_en.list_shows):
                print(f"{i}=Name: {v['name']}\nFirst_air_date: {v['first_air_date']}\nOrigin_country: {v['origin_country']}\nPopularity_rating: {v['popularity']}\nAverage_vote:{v['vote_average']}\n")
        except (KeyError, TypeError, ValueError, AttributeError):
            print("Please check your spelling and try again")

    def export_tv_shows(self):
        try:
            user_input = input(
                "Please write the first two letters of a lanugage to see a list of shows based on that language, and export the data to a json file:")
            self.tv_db_en.list_shows_based_on_language(user_input)
            print(self.tv_db_en.data_show_lang)
            for k, v in enumerate(self.tv_db_en.data):
                data = f"{v['name']} {v['original_language']}"
                if v['original_language'] == user_input:
                    data_1 = f"{v['name']} {v['original_language']}"
                    print(data_1)

                    filename = "data.json"
                    with open(filename, "w") as g:
                        json.dump(data_1, g, indent=4)
        except (KeyError, TypeError, ValueError, AttributeError):
            print("Please check your spelling and try again.Example for english write(en)\n")
        exit = input("To exit press 1: \n")
        if exit == "1":
            sys.exit()

    def compare_ratings(self):
        try:
            user_input_1 = input("Please write the name of first tv show that you want to comapre:\n")
            user_input_2 = input("Please write the name of secound tv show that you want to comapre:\n")
            self.tv_db_en.compare_tv_show_ratings(user_input_1, user_input_2)  # Acess the method

            if self.tv_db_en.a > self.tv_db_en.b:
                print("True")
            if self.tv_db_en.a < self.tv_db_en.b:
                print("False")

            #print(user_input_1 > user_input_2)
            # print(self.tv_db_en.compare_tv_show_first < self.tv_db_en.compare_tv_show_secound) # Comparing the movies based on vote average
            print(f"{self.tv_db_en.compare_tv_show_first}")
            print(f"{self.tv_db_en.compare_tv_show_secound}\n")
        except (KeyError, TypeError, ValueError, AttributeError):
            print("Please check your spelling and try again later")

    def export_image(self, language):
        # 13 - Last one (VG)
        pass


if __name__ == "__main__":
    menu = Menu()
