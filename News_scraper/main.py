
from scraper import Scraper
import sys



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