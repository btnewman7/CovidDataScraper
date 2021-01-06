import requests
from bs4 import BeautifulSoup
from app import db
from .models import Country

def populate_database(data):
    #Create BS4 Object from data
    soup = BeautifulSoup(data, 'html.parser')

    #Acquire all country data
    tbody=[i for i in soup.find('tbody')]
    tr_list=[i for i in tbody if i !='\n']
    
    #compile a list of all countries
    country_list =[]
    for idx, value in enumerate(tr_list):
        new_row = [row.text for row in tr_list[idx] if row != '\n'][0:]
        country_list.append(new_row)

    list_to_add = []
    for country in country_list:
        existing_country = Country.query.filter_by(name=country[0]).first()
        if existing_country is None:
            #pool data into dictionary
            country_data = {
                'name': country[0],
                'confirmed': country[1],
                'deaths': country[2],
                'case_fatality_percentage': country[3][:-1],
                'deaths_per_100k': country[4],
            }
            #instantiate a new country
            c = Country()
            # set the country's (c) attributes
            c.from_dict(country_data)
            list_to_add.append(c)

    db.session.add_all(list_to_add)
    db.session.commit()