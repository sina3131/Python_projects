
import requests
from datetime import date
from bs4 import BeautifulSoup
import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt
import sys
import re


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

