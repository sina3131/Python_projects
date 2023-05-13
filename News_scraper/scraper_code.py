
import scraper

import requests
from datetime import date
from bs4 import BeautifulSoup
import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt
import sys
import re
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