#!/usr/bin/env python3
from models import Company, Dev, Freebie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
import random
# Script goes here!

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def create_company():
    companies = [ 
        Company(
        name=fake.company(), 
        founding_year=fake.date_this_century()
        ) for i in range(100)]
    session.add_all(companies)
    session.commit()
    return companies

def create_dev():
    devs = [
        Dev(name=fake.name())
        for i in range(100)
    ]
    session.add_all(devs)
    session.commit()
    return devs

def create_freebie():
    freebies = [
        Freebie(item_name=fake.word(), 
                value=random.randint(1,30),
            ) for i in range(300)]
    session.add_all(freebies)
    session.commit()
    return freebies

def delete_tables():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

def relate_one_to_many(companies, freebies, devs):
    for freebie in freebies:
        freebie.dev = random.choice(devs)
        freebie.company = random.choice(companies)

    session.add_all(freebies)
    session.commit()
    return companies, freebies, devs

if __name__ == "__main__":
    session.close()
    delete_tables()
    companies = create_company()
    freebies = create_freebie()
    devs = create_dev()
    companies, freebies, devs = relate_one_to_many(companies, freebies, devs)

