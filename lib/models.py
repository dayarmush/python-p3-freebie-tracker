from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref='company')
    devs = association_proxy('freebies', 'dev',
        creator=lambda dev: Freebie(dev=dev))
    
    def give_freebie(self, dev, item_name, value):
        return Freebie(item_name=item_name, value=value, company_id=self.id, dev_id=dev.id)
    
    @classmethod
    def oldest_company(cls, session):
        oldest_company = session.query(cls).order_by(cls.founding_year.asc()).first()
        return oldest_company

    def __repr__(self):
        return f'<Company {self.name} Founding Year: {self.founding_year}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', backref='dev')
    companies = association_proxy('freebies', 'company',
        creator=lambda comp: Freebie(comp=comp))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    def print_details(self):
        return print(f'{self.dev.name} owns a {self.item_name} from {self.company.name}.')

    def __repr__(self):
        return f'Freebie(Item: {self.item_name}, Value: {self.value}, Company ID: {self.company_id}, Dev ID: {self.dev_id})'
