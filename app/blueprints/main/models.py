from app import db
from bs4 import BeautifulSoup

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    confirmed = db.Column(db.String)
    deaths = db.Column(db.String)
    case_fatality_percentage = db.Column(db.String)
    deaths_per_100k = db.Column(db.String)

    def __repr__(self):
        return f"<Country: {self.name}>"

    def expire(self):
        db.session.expire(self)
        db.session.commit()

    def from_dict(self, data):
        for field in ['name', 'confirmed', 'deaths', 'case_fatality_percentage', 'deaths_per_100k']:
            if field in data:
                setattr(self, field, data[field])
    
    def to_dict(self):
        country_dict = {
                'name': self.name,
                'confirmed': self.confirmed,
                'deaths': self.deaths,
                'case_fatality_percentage': self.case_fatality_percentage,
                'deaths_per_100k': self.deaths_per_100k,
            }
        return country_dict

class SelectedCountry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    confirmed = db.Column(db.String)
    deaths = db.Column(db.String)
    case_fatality_percentage = db.Column(db.String)
    deaths_per_100k = db.Column(db.String)

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Country: {self.name}>"

    def from_dict(self, data):
        for field in ['name', 'confirmed', 'deaths', 'case_fatality_percentage', 'deaths_per_100k']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        country_dict = {
                'name': self.name,
                'confirmed': self.confirmed,
                'deaths': self.deaths,
                'case_fatality_percentage': self.case_fatality_percentage,
                'deaths_per_100k': self.deaths_per_100k,
            }
        return country_dict
