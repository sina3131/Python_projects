import requests
from datetime import date
from bs4 import BeautifulSoup
import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt
import sys
import re


class Scraper:
    # I use postgresql for database interaction, i noticed recently that giving remot acess is extremly complicated so i dump the database structure
    # instead and send a copy of how my databse look like in a seperate file.
    try:
        # Establishing the connection to database using postgresql
        connection_super = pg.connect(
            database="scraper",
            user='postgres',
            password='123',
            host='127.0.0.1',
            port='5432'
        )
    except Exception as e:
        print("Problem when connecting to database")

    def __init__(self):
        self.reuters_url = "https://www.reuters.com/"
        self.apnews_url = "https://apnews.com/"
        self.all_links = []

    # Scrape methods usuing bs4 and requests library

    def scrape_apnews(self):
        try:
            html = requests.get(self.apnews_url).text
            soup = BeautifulSoup(html, "lxml")
            # Get article links and titles
            articles = soup.find_all("a", class_="hubPeekStory-2")
            self.apnews_links = set()
            self.apnews_titles = []
            for article in articles:
                link = "https://apnews.com" + article["href"]
                self.apnews_links.add(link)
                self.apnews_titles.append("Article title: " + article.text)
            self.all_links.append(self.apnews_links)
            print("The website has been scraped sucessfully! ")
        except Exception as e:
            print("Problem with scraping apnews")

    # Reuters had different class names for different parts in their website for articles, that's why i use three different classes here when i scrape.

    def scrape_reuters(self):

        # Getting article links and titles
        try:
            html = requests.get(self.reuters_url).text
            soup = BeautifulSoup(html, "lxml")

            # First set of article links
            articles_1 = soup.find_all(
                "a", class_="text__heading_5_and_half__3YluN")
            self.reuters_links_1 = set()
            self.reuters_titles_1 = []
            for article in articles_1:
                link = "https://www.reuters.com" + article["href"]
                self.reuters_links_1.add(link)
                self.sort_link_1 = sorted(self.reuters_links_1)
                self.reuters_titles_1.append("Article title: " + article.text)
            self.all_links.append(self.reuters_links_1)

            # Second set of article links
            articles_2 = soup.find_all(
                "ul", class_="text-story-card__underlinks__2A2bA")
            self.reuters_links_2 = set()
            self.reuters_titles_2 = []
            for article in articles_2:
                link = "https://www.reuters.com" + article.find("a")["href"]
                self.reuters_links_2.add(link)
                self.sort_link_2 = sorted(self.reuters_links_2)
                self.reuters_titles_2.append("Article title: " + article.text)
            self.all_links.append(self.reuters_links_2)

            # Third set of article links
            articles_3 = soup.find_all(
                "div", class_="media-story-card__hub__3mHOR story-card")
            self.reuters_links_3 = set()
            self.reuters_titles_3 = []
            for article in articles_3:
                link = "https://www.reuters.com" + article.find("a")["href"]
                self.reuters_links_3.add(link)
                self.sort_link_3 = sorted(self.reuters_links_3)
                self.reuters_titles_3.append("Article title: " + article.text)
            self.all_links.append(self.reuters_links_3)
            print("The website has been scraped sucessfully! ")
        except Exception as e:
            print("problem with scraping reuters")

        # Creating a table for saving all links to database

    def database(self, connection_super):  # storing the links in the database.
        try:
            self.today = date.today()
            cursor = connection_super.cursor()
            with cursor as cc:
                for i in self.sort_link_1:
                    cc.execute(
                        "insert into new_article(links,source) values (%s,%s)", (i, "Reuters"))
                for i in self.reuters_links_2:
                    cc.execute(
                        "insert into new_article(links,source) values (%s,%s)", (i, "Reuters"))
                for i in self.reuters_links_3:
                    cc.execute(
                        "insert into new_article(links,source) values (%s, %s)", (i, "Reuters"))
                for i in self.apnews_links:
                    cc.execute(
                        "insert into new_article(links,source) values (%s, %s)", (i, "Apnews"))
                connection_super.commit()
                print("The links has been stored sucessfuly!  ")
        except Exception as e:
            print("Problem with inserting links in database")


# Stores the article content in the database
# Looping through links and extract their contents then dumping it in the database.

    def articles_content(self, connection_super):
        try:
            cursor = connection_super.cursor()
            with cursor as cc:
                for i in self.reuters_links_1:  # extracting the contents of all the articles using the links and bs4
                    html = requests.get(i).text
                    ss = BeautifulSoup(html, "lxml")
                    self.art = ss.text
                    cc.execute(
                        "insert into text(cont, source) values (%s,%s)", (self.art, "Reuters"))
                for i in self.reuters_links_2:
                    html = requests.get(i).text
                    ss1 = BeautifulSoup(html, "lxml")
                    self.art1 = ss1.text
                    cc.execute(
                        "insert into text(cont, source) values (%s, %s)", (self.art1, "Reuters"))
                for i in self.reuters_links_3:
                    html = requests.get(i).text
                    ss2 = BeautifulSoup(html, "lxml")
                    self.art2 = ss2.text
                    cc.execute(
                        "insert into text(cont, source) values (%s, %s)", (self.art2, "Reuters"))
                for i in self.apnews_links:
                    html = requests.get(i).text
                    ss3 = BeautifulSoup(html, "lxml")
                    self.art3 = ss3.text
                    cc.execute(
                        "insert into text(cont, source) values (%s, %s)", (self.art3, "Apnews"))
                connection_super.commit()
                print("The article contents has been stored sucessfully! ")
        except Exception as e:
            print("Problem while inserting text to database")


# Acessing articles conetent
# this method selects all text from database and store it in a variable for analyzing later on.

    def acess_article_content(self):
        try:
            cursor = self.connection_super.cursor()
            with cursor as cc:
                # sql query for selecting all the data from the database
                cc.execute("select * from text;")
                self.data_article = cc.fetchall()
            self.connection_super.commit()
        except Exception as e:
            print("Problem with uploading the data from database")


# Acess article content in a specefic date deafult date is current.

    def acess_article_c_date(self, date=date.today()):
        try:
            cursor = self.connection_super.cursor()
            with cursor as cc:
                cc.execute(f"select * from text where dates = '{date}'")
                self.data_artic_date = cc.fetchall()
            self.connection_super.commit()
        except Exception as e:
            print("Problem with fetching data from database")


# Acessing all links from database

    def access_all_links(self):
        try:
            cursor = self.connection_super.cursor()
            with cursor as cc:
                cc.execute("select links from new_article")
                self.data_link = cc.fetchall()
            self.connection_super.commit()
        except Exception as e:
            print("Problem while trying uploading links from database")


# Acessing links in a specefic date

    def access_links_date(self, date):
        try:
            cursor = self.connection_super.cursor()
            with cursor as cc:
                cc.execute(
                    f"select links from new_article where date_link = '{date}'")
                self.data_link_d = cc.fetchall()
            self.connection_super.commit()
        except Exception as e:
            print("Problem while trying uploading links from database")


# Adding category

    def add_categor(self):
        cursor = self.connection_super.cursor()
        with cursor as cc:
            cc.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'all_category';")
            self.all_categories = cc.fetchall()
            for i in self.all_categories:
                for j in i:
                    print(j)
            name = input("please write a category name: ")
            cc.execute(f"alter table all_category add column {name} text")
        self.connection_super.commit()
        add_more = input("to add more press 1: "
                         "to exit press 2: ")
        if add_more == "1":
            self.add_categor()
        elif add_more == "2":
            sys.exit()


# Adding phrases to category

    def add_phrase(self):
        word = input("please write your phrase: ")
        category = input("please choose your category: ")
        cursor = self.connection_super.cursor()
        with cursor as cc:
            cc.execute(f"insert into {category} (item) values ('{word}')")
        self.connection_super.commit()
        add_more = input("to add more press 1: "
                         "to exit press 2: ")
        if add_more == "1":
            self.add_phrase()
        elif add_more == "2":
            sys.exit()

    def add_search_phrase(self):
        user = input("Please write the phrase you want to add: ")
        cursor = self.connection_super.cursor()
        with cursor as cc:
            cc.execute(f"insert into search_phrase (words) values ('{user}')")
        self.connection_super.commit()

    def search_phrases(self):
        cursor = self.connection_super.cursor()
        with cursor as cc:
            cc.execute(f"select words from search_phrase ")
            self.phrase_data = cc.fetchall()
            for i in self.phrase_data:
                for j in i:
                    print(j)
        self.connection_super.commit()


# this is acounter method that counts the occurence of words and each category
# this method first selects the elements of each category
# then it makes a list of it by removing unnessecary marks and signs
# finally it counts how many times each items and each category ocurred in the text that has been provided to it by another method.


    def category_data(self):
        cursor = self.connection_super.cursor()
        with cursor as cc:
            cc.execute(f"select item from art")
            self.art = cc.fetchall()
            cc.execute(f"select item from politic")
            self.politic = cc.fetchall()
            cc.execute(f"select item from climate")
            self.climate = cc.fetchall()
            cc.execute(f"select item from economy")
            self.economy = cc.fetchall()
            cc.execute(f"select item from sports")
            self.sports = cc.fetchall()
            cc.execute(f"select item from technology")
            self.technology = cc.fetchall()
        self.connection_super.commit()

        self.p_list = [re.sub(r'[()]', '', str(elem)) if isinstance(
            elem, tuple) else str(elem) for elem in self.politic]
        self.p_list_ = [elem.strip(", '") for elem in self.p_list]

        self.a_list = [re.sub(r'[()]', '', str(elem)) if isinstance(
            elem, tuple) else str(elem) for elem in self.art]
        self.a_list_ = [elem.strip(", '") for elem in self.a_list]

        self.c_list = [re.sub(r'[()]', '', str(elem)) if isinstance(
            elem, tuple) else str(elem) for elem in self.climate]
        self.c_list_ = [elem.strip(", '") for elem in self.c_list]

        self.e_list = [re.sub(r'[()]', '', str(elem)) if isinstance(
            elem, tuple) else str(elem) for elem in self.economy]
        self.e_list_ = [elem.strip(", '") for elem in self.e_list]

        self.s_list = [re.sub(r'[()]', '', str(elem)) if isinstance(
            elem, tuple) else str(elem) for elem in self.sports]
        self.s_list_ = [elem.strip(", '") for elem in self.s_list]

        self.t_list = [re.sub(r'[()]', '', str(elem)) if isinstance(
            elem, tuple) else str(elem) for elem in self.technology]
        self.t_list_ = [elem.strip(", '") for elem in self.t_list]

        all_elements = []
        all_elements.extend(self.p_list_+self.a_list_ +
                            self.c_list_+self.e_list_+self.s_list_+self.t_list_)
        self.element_count = {element: 0 for element in all_elements}
        self.p_occurence = 0
        self.e_occurence = 0
        self.c_occurence = 0
        self.s_occurence = 0
        self.a_occurence = 0
        self.t_occurence = 0
        for article in self.data_artic_date:
            for element in article:
                if isinstance(element, str):
                    for political_phrase in self.p_list_:
                        if political_phrase in element:
                            self.p_occurence += 1
                    for count_element in all_elements:
                        if count_element in element:
                            self.element_count[count_element] += 1
                    for e_phrase in self.e_list_:
                        if e_phrase in element:
                            self.e_occurence += 1
                    for c_phrase in self.c_list_:
                        if c_phrase in element:
                            self.c_occurence += 1
                    for s_phrase in self.s_list_:
                        if s_phrase in element:
                            self.s_occurence += 1
                    for a_phrase in self.a_list_:
                        if a_phrase in element:
                            self.a_occurence += 1
                    for t_phrase in self.t_list_:
                        if t_phrase in element:
                            self.t_occurence += 1

    # storing the occurence data in the database for comparing later on

    def category_insertion(self, dat=date.today()):
        self.today = date.today()
        cursor = self.connection_super.cursor()
        with cursor as cc:
            try:
                cc.execute("insert into ocurrence (politic, economy, climate_change, sports, art, technology, dates) values (%s,%s,%s,%s,%s,%s,%s)",
                           (self.p_occurence, self.e_occurence, self.c_occurence, self.s_occurence, self.a_occurence, self.t_occurence, dat))
                self.connection_super.commit()
            except Exception as e:
                # in order to avoid duplicate data, I set a unqie key constraint when creating the database on date column, so it doesn't get repeated.
                print("Problem with insertion of category data into database")


# This method analyzes the ocuurence of each category usuing matpotlip libraray


    def analyze(self):
        try:
            df = pd.read_sql_query(
                "select * from ocurrence", self.connection_super)
            data = df[['dates', 'politic', 'sports', 'economy',
                       'art', 'climate_change', 'technology']]
            data.set_index('dates', inplace=True)
            data.plot()
            plt.xlabel('Date')
            plt.ylabel('Occurrences')
            plt.title('Topic Occurrences over Time')
            plt.legend(loc='upper left')
            plt.show()
        except Exception as e:
            print("Problem while analyzing the data")

# this method analyzes a list of words
    def analyze_word(self):
        try:
            df = pd.read_sql_query(
                "select * from word_analyze", self.connection_super)
            data = df[['drought', 'inflation',
                       'ukraine', 'russia', 'nato', 'dates']]
            data.set_index('dates', inplace=True)
            data.plot()
            plt.xlabel('Date')
            plt.ylabel('Occurrences')
            plt.title('Occurrences over Time')
            plt.legend(loc='upper left')
            plt.show()
        except Exception as e:
            print("Problem while analyzing the data")


# this method analyzes list of phrases

    def analyze_phrase(self):
        try:
            df = pd.read_sql_query("select * from wordy",
                                   self.connection_super)
            data = df[['russia', 'ukraine', 'putin', 'drought', 'inflation',
                       'greta', 'moscow', 'nato', 'turkey', 'sweden', 'dates']]
            data.set_index('dates', inplace=True)
            data.plot.bar()
            plt.xlabel('Date')
            plt.ylabel('Occurrences')
            plt.title('Topic Occurrences over Time')
            plt.legend(loc='upper left')
            plt.show()
        except Exception as e:
            print("Problem while analyzing the data")


# another method for anlyzing specefic list of words over time

    def word_tracks(self, words_list):
        word_counts = {word: 0 for word in words_list}
        for article in self.data_artic_date:
            for sentence in article:
                if isinstance(sentence, str):
                    for word in words_list:
                        word_counts[word] += sentence.count(word)
        cur = self.connection_super.cursor()
        placeholders = ",".join(["%s"] * (len(words_list) + 1))
        query = f"INSERT INTO wordy ({','.join(words_list)}, dates) VALUES ({placeholders})"
        values = [word_counts.get(word, 0)
                  for word in words_list] + ['2023-02-26']
        cur.execute(query, values)
        self.connection_super.commit()
        cur.close()
        self.connection_super.close()

# this is also a word tracking alanyze method
    def word_track(self, keyword, k2, k3, k4, k5):
        self.acess_article_c_date('2023-02-26')
        self.el_0 = 0
        self.el_1 = 0
        self.el_2 = 0
        self.el_3 = 0
        self.el_4 = 0
        for article in self.data_artic_date:
            for sentence in article:
                if isinstance(sentence, str):
                    if keyword in sentence:
                        self.el_0 += 1
                    if k2 in sentence:
                        self.el_1 += 1
                    if k3 in sentence:
                        self.el_2 += 1
                    if k4 in sentence:
                        self.el_3 += 1
                    if k5 in sentence:
                        self.el_4 += 1
            cursor = self.connection_super.cursor()
            with cursor as cc:
                cc.execute(
                    f"insert into word_analyze(drought, inflation, Ukraine, russia, nato, dates) values({self.el_0},{self.el_1},{self.el_2},{self.el_3},{self.el_4},'2023-02-25')")
            self.connection_super.commit()


def main():
    instance = Scraper()
    instance.access_all_links()
    try:
        user = input("Welcome to scraper choose an option from below\n"
                     "[a] To see a list of all article urls \n"
                     "[b] To see a list of all article urls in a specefic date\n"
                     "[c] To see list of categories and add to categories\n"
                     "[d] To add phrase in the search phrase list\n"
                     "[e] To see list of search phrases\n"
                     "[f] Phrase and category occurence \n"
                     "[g] To see statistics \n"
                     "[h] To exit \n"
                     "[i] To scrape the websites \n"
                     )
    except Exception as e:
        print("wrong input try again ")
        main()

    if user == "i":
        instance.scrape_apnews()
        instance.scrape_reuters()
        instance.database(instance.connection_super)
        instance.articles_content(instance.connection_super)
        instance.acess_article_c_date()
        instance.category_data()
        instance.category_insertion()
        user = input("press 0 to go to main menue: ")
        if user == "0":
            main()

    if user == "d":
        instance.add_search_phrase()
        next = input("Press [0] To go to main menue\n")
        if next == "0":
            main()
    if user == "e":
        instance.search_phrases()
        next = input("Press [0] To go to main menue\n")
        if next == "0":
            main()
    if user == "c":
        instance.add_categor()
        next = input("Press [0] To go to main menue\n")
        if next == "0":
            main()

    if user == "b":
        f_in = input(
            "Data is avialible from 2023-02-15 - 2023-02-27\nWrite the date example(2023-02-15): ")
        instance.access_links_date(f_in)
        for i in instance.data_link_d:
            for p in i:
                print(p)
        next = input("Press [0] To go to main menue\n")
        if next == "0":
            main()

    if user == "a":
        instance.access_all_links()
        for i in instance.data_link:
            for p in i:
                print(p)
        next = input("Press [0] To go to main menue: ")
        if next == "0":
            main()

    if user == "f":
        try:
            user_ = input("[1] To see phrase occurence\n"
                          "[2] To see category occurence\n")
        except Exception as e:
            print("wrong input try again")
        if user_ == "1":
            user_1 = input(
                "Data is avialible from 2023-02-15 - 2023-02-27\nWhich date example(2023-02-16): ")
            user2 = input("Choose a category\n"
                          "All categories\n"
                          "[1] = politic\n"
                          "[2] = economics \n"
                          "[3] = climate_change \n"
                          "[4] = sports \n"
                          "[5] = arts \n"
                          "[6] = technology\n")
            if user2 == "1":
                instance.acess_article_c_date(user_1)
                instance.category_data()
                print("This category contains")
                for i in instance.p_list_:
                    print("-", i)
                for political_phrase in instance.p_list_:
                    print(
                        f"{political_phrase} has ocurrend {instance.element_count[political_phrase]} times in {user_1}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()

            if user2 == "2":
                instance.acess_article_c_date(user_1)
                instance.category_data()
                print("This category contains")
                for i in instance.e_list_:
                    print("-", i)
                for e_phrase in instance.e_list_:
                    print(
                        f"{e_phrase} has ocurrend,  {instance.element_count[e_phrase]} times")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "3":
                instance.acess_article_c_date(user_1)
                instance.category_data()
                print("This category contains")
                for i in instance.c_list_:
                    print("-", i)
                for c_phrase in instance.c_list_:
                    print(
                        f"{c_phrase} has ocurrend,  {instance.element_count[c_phrase]} times")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "4":
                instance.acess_article_c_date(user_1)
                instance.category_data()
                print("This category contains")
                for i in instance.s_list_:
                    print("-", i)
                for s_phrase in instance.s_list_:
                    print(
                        f"{s_phrase} has ocurrend,  {instance.element_count[s_phrase]} times")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "5":
                instance.acess_article_c_date(user_1)
                instance.category_data()
                print("This category contains")
                for i in instance.a_list_:
                    print("-", i)
                for a_phrase in instance.a_list_:
                    print(
                        f"{a_phrase} has ocurrend,  {instance.element_count[a_phrase]} times")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "6":
                instance.acess_article_c_date(user_1)
                instance.category_data()
                print("This category contains")
                for i in instance.t_list_:
                    print("-", i)
                for t_phrase in instance.t_list_:
                    print(
                        f"{t_phrase} has ocurrend,  {instance.element_count[t_phrase]} times")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
        if user_ == "2":
            user_s = input(
                "Data is avialible from 2023-02-15 - 2023-02-27\nChoose a date example(2023-02-16): ")
            instance.acess_article_c_date(user_s)
            user2 = input("Choose a category\n"
                          "All categories\n"
                          "[1] = politic\n"
                          "[2] = economics \n"
                          "[3] = climate_change \n"
                          "[4] = sports \n"
                          "[5] = arts \n"
                          "[6] = technology\n")
            if user2 == "1":
                instance.acess_article_c_date(user_s)
                instance.category_data()
                print(
                    f"Political related phrases ocuured {instance.p_occurence} times in {user_s}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "2":
                instance.acess_article_c_date(user_s)
                instance.category_data()
                print(
                    f"Economical related phrases ocuured {instance.e_occurence} times in {user_s}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "3":
                instance.acess_article_c_date(user_s)
                instance.category_data()
                print(
                    f"Climate_change related phrases ocuured {instance.c_occurence} times in {user_s}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "4":
                instance.acess_article_c_date(user_s)
                instance.category_data()
                print(
                    f"Sport related phrases ocuured {instance.s_occurence} times in {user_s}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "5":
                instance.acess_article_c_date(user_s)
                instance.category_data()
                print(
                    f"Art related phrases ocuured {instance.a_occurence} times in {user_s}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
            if user2 == "6":
                instance.acess_article_c_date(user_s)
                instance.category_data()
                print(
                    f"Technologiacl related phrases ocuured {instance.t_occurence} times in {user_s}")
                next = input("Press [0] To go to main menue\n")
                if next == "0":
                    main()
    if user == "g":
        us = input("[1]- To see the chart of category occurence\n"
                   "[2]- To see chart of the search phrase occurce\n"
                   "[3]- To see phrase occurence over time in bar chart \n")
        if us == "1":
            instance.analyze()
        if us == "2":
            instance.analyze_word()
        if us == "3":
            instance.analyze_phrase()
    if user == "4":
        sys.exit()

    # wro = ['Russia','Ukraine','Putin','drought', 'inflation',  'Greta', 'Moscow', 'Nato', 'Turkey', 'Sweden' ]
    # instance.word_tracks(wro)
    # instance.word_track('drought', 'inflation',  'Ukraine', 'Russia', 'Nato')
    # instance.acess_article_c_date('2023-02-15')
    # instance.word_tracks(['Russia','Ukraine','Putin','drought', 'inflation',  'Greta', 'Moscow', 'Nato', 'Turkey', 'Sweden' ])
    # instance.analyze_phrase()
if __name__ == "__main__":
    main()
