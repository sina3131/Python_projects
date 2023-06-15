import sqlite3
import pandas as pd 


# so when we call the class it will connect to db and create a table 
# if table not exists.
class DBstorage():
    def __init__(self):
        self.con = sqlite3.connect("links.db")
        self.setup_table()
    
    def setup_table(self):
        cur = self.con.cursor()
        results_table = r"""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY,
            query TEXT,
            rank INTEGER,
            link TEXT,
            title TEXT,
            snippet TEXT,
            html TEXT,
            created DATETIME,
            relevance INTEGER,
            CONSTRAINT unique_query_link UNIQUE (query, link)
            
        );
        
        """
        
        cur.execute(results_table)
        self.con.commit()
        cur.close()
    
    # this function will query from the results table  
    def query_result(self, query):
        df = pd.read_sql(f"select * from results where query = '{query}' order by rank asc;", self.con)
        return df
    
    def insert_values(self, values):
        cur =  self.con.cursor()
        try:
            cur.execute('INSERT INTO results (query,rank, link, title, snippet, html, created) VALUES(?,?,?,?,?,?,?)', values)
            self.con.commit()
        except sqlite3.IntegrityError: # if the data already exist
            pass
        cur.close()
    
    
    def update_relevance(self, query, link, relevance):
        cur = self.con.cursor()
        cur.execute("UPDATE results SET relevance=? WHERE query=? AND link=?", [relevance, query, link])
        self.con.commit()
        cur.close()