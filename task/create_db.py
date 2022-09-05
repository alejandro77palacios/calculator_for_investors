import csv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Float, String
from sqlalchemy import create_engine


def clear_record(record):
    clean_record = [None if entry == '' else entry for entry in record]
    return clean_record


def clear_na(data):
    clean = [clear_record(rec) for rec in data]
    return clean


engine = create_engine('sqlite:///investor.db', echo=False)

Base_companies = declarative_base()


class Companies(Base_companies):
    __tablename__ = 'companies'

    ticker = Column(String(50), primary_key=True)
    name = Column(String(50))
    sector = Column(String(50))


Base_companies.metadata.create_all(engine)

Base_financial = declarative_base()


class Financial(Base_financial):
    __tablename__ = 'financial'

    ticker = Column(String(50), primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


Base_financial.metadata.create_all(engine)

if __name__ == '__main__':
    with open('data/companies.csv', newline='') as c, open('data/financial.csv', newline='') as f:
        companies, financial = [], []
        for line in csv.reader(c, delimiter=","):
            companies.append(line)
        for line in csv.reader(f, delimiter=","):
            financial.append(line)
    companies = clear_na(companies)
    financial = clear_na(financial)
    Session = sessionmaker(bind=engine)
    session = Session()
    fill_companies = [Companies(ticker=record[0], name=record[1], sector=record[2]) for record in companies[1:]]
    fill_financial = [
        Financial(ticker=record[0], ebitda=record[1], sales=record[2], net_profit=record[3], market_price=record[4],
                  net_debt=record[5], assets=record[6], equity=record[7], cash_equivalents=record[8],
                  liabilities=record[9]) for record in financial[1:]]
    session.add_all(fill_companies)
    session.add_all(fill_financial)
    session.commit()
    print('Database created successfully!')
