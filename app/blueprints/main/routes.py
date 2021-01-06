from flask import current_app as app, render_template, url_for, redirect, request, json
import requests, os, time
from .import bp as main
from flask_login import login_required
from bs4 import BeautifulSoup
from .models import Country, SelectedCountry
from app import db
from .forms import GetCountryDataForm
from .seed import populate_database
from csv import writer
import csv
from selenium import webdriver

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = GetCountryDataForm()
    form.name.choices = [(c.id, c.name) for c in Country.query.order_by('name').all()]
    context = {
        'form': form,
        'countries': SelectedCountry.query.order_by('name').all()
    }
    return render_template('main/index.html', **context)

@main.route('/get_data', methods=['POST'])
def get_data():
    form = GetCountryDataForm()
    if request.method == 'POST':
        id_ = form.name.data

        #query original Country from database
        c = Country.query.get(id_)
        country_stuff_to_add = Country.query.get(id_)
        
        if not os.path.isfile("data.json"):
            with open("data.json", "w") as save_file:
                json.dump([], save_file)

        if os.path.isfile("data.json"):
            with open("data.json", "r+") as save_file:
                data = json.load(save_file)
                with open("data.json", "w+") as save_file:
                    data.append(c.to_dict())
                    json.dump(data, save_file)

        #create SelectedCountry so I can rep the info in table
        table_country = SelectedCountry()
        table_country.from_dict(country_stuff_to_add.to_dict())
        
        db.session.add(table_country)
        db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/delete_data', methods=['GET'])
def delete_data():
    form = GetCountryDataForm()

    id_ = request.args.get('id')

    c = SelectedCountry.query.get(id_)
    c.remove()

    if os.path.isfile("data.json"):
        with open("data.json", "r+") as save_file:
            data = json.load(save_file)
            with open("data.json", "w+") as save_file:
                data.remove(c.to_dict())
                json.dump(data, save_file)
        
    return redirect(url_for('main.index'))

@main.route('/about', methods=['GET'])
@login_required
def about():
    context = {}
    return render_template('main/about.html', **context)

@main.route('/seed_data', methods=['GET'])
def seed_data():
    url = 'https://coronavirus.jhu.edu/data/mortality'
    page = requests.get(url)
    populate_database(page.content)
    return redirect(url_for('main.index'))

@main.route('/cronjob', methods=['POST'])
def cronjob():
    c = SelectedCountry.query.get(request.args.get('id'))
    csv_columns = c.to_dict().keys()
    cdict = c.to_dict()
    csv_file = "countries.csv"

    while True:
        if not os.path.isfile('countries.csv'):
            try:
                with open(csv_file, 'w') as f:
                    writer = csv.DictWriter(f, fieldnames=csv_columns)
                    writer.writeheader()
            except IOError:
                print("I/O error")
        with open(csv_file, 'a+', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writerow(cdict)
        #time.sleep(5)
        time.sleep(86407)
    return redirect(url_for('main.index'))

@main.route('/selenium', methods=['GET'])
def selenium():
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get("https://coronavirus.jhu.edu/data/mortality")
    table = driver.find_element_by_css_selector("tbody")
    with open('datatable.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
    return redirect(url_for('main.index'))