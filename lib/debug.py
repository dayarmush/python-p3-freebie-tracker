#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    dev1 = session.query(Dev).first()
    company1 = session.query(Company).first()
    freebie1 = session.query(Freebie).first()

    import ipdb; ipdb.set_trace()
