from sqlalchemy.orm import sessionmaker
import create_db
import operator
Session = sessionmaker(bind=create_db.engine)
my_session = Session()

main_menu = """MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria"""

crud_menu = """CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies"""

top_ten_menu = """TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA"""


def show_main_menu():
    print(main_menu)


def show_crud_menu():
    print('\n' + crud_menu)


def show_top_ten_menu():
    print('\n' + top_ten_menu)


def show_not_implemented():
    print('Not implemented!\n')
    main()


def show_not_valid():
    print('Invalid option!\n')
    main()


def perform_main_menu(option):
    match option:
        case 0:
            print('Have a nice day!')
        case 1:
            perform_crud_menu()
            main()
        case 2:
            perform_top_ten_menu()
            main()
        case _:
            show_not_valid()


def create_company():
    company_ticker = input("Enter ticker (in the format 'MOON'):\n")
    company_name = input("Enter company (in the format 'Moon Corp'):\n")
    company_sector = input("Enter industries (in the format 'Technology'):\n")

    company_ebitda = int(
        input("Enter ebitda (in the format '987654321'):\n"))  # TODO: ver si se necesita float en lugar de int
    company_sales = int(input("Enter sales (in the format '987654321'):\n"))
    company_net_profit = int(input("Enter net profit (in the format '987654321'):\n"))
    company_market_price = int(input("Enter market price (in the format '987654321'):\n"))
    company_net_debt = int(input("Enter net dept (in the format '987654321'):\n"))  # TODO:texto debería ser debt
    company_assets = int(input("Enter assets (in the format '987654321'):\n"))
    company_equity = int(input("Enter equity (in the format '987654321'):\n"))
    company_cash_equivalents = int(input("Enter cash equivalents (in the format '987654321'):\n"))
    company_liabilities = int(input("Enter liabilities (in the format '987654321'):\n"))

    new_company = create_db.Companies(ticker=company_ticker, name=company_name, sector=company_sector)
    new_company_finance = create_db.Financial(ticker=company_ticker,
                                    ebitda=company_ebitda,
                                    sales=company_sales,
                                    net_profit=company_net_profit,
                                    market_price=company_market_price,
                                    net_debt=company_net_debt,
                                    assets=company_assets,
                                    equity=company_equity,
                                    cash_equivalents=company_cash_equivalents,
                                    liabilities=company_liabilities)
    my_session.add(new_company)
    my_session.add(new_company_finance)
    my_session.commit()
    print('Company created successfully!\n')


def financial_indicator(a, b, name):
    if a is None or b is None:
        result = None
    else:
        result = round(a / b, 2)
    print(name + ' = ' + str(result))


def simply_fi(a, b):
    if a is None or b is None:
        return None
    else:
        return round(a / b, 2)

def read_company():
    company_name = input('Enter company name:\n')
    query = my_session.query(create_db.Companies.ticker, create_db.Companies.name)
    count = 0
    selected_companies = {}
    for ticker, company in query:
        if company_name in company.lower():
            print(count, company)
            selected_companies[count] = (ticker, company)
            count += 1
    if count == 0:
        print('Company not found!\n')
    else:
        company_number = int(input('Enter company number:\n'))
        my_company_ticker = selected_companies[company_number][0]
        fquery = my_session.query(create_db.Financial).filter(create_db.Financial.ticker == my_company_ticker)
        print(*selected_companies[company_number])
        for row in fquery:
            financial_indicator(row.market_price, row.net_profit, 'P/E')
            financial_indicator(row.market_price, row.sales, 'P/S')
            financial_indicator(row.market_price, row.assets, 'P/B')
            financial_indicator(row.net_debt, row.ebitda, 'ND/EBITDA')
            financial_indicator(row.net_profit, row.equity, 'ROE')
            financial_indicator(row.net_profit, row.assets, 'ROA')
            financial_indicator(row.liabilities, row.assets, 'L/A')
        print() #TODO: revisar doble salto de línea
        print()


def update_company():
    company_name = input('Enter company name:\n')
    query = my_session.query(create_db.Companies.ticker, create_db.Companies.name)
    count = 0
    selected_companies = {}
    for ticker, company in query:
        if company_name in company.lower():
            print(count, company)
            selected_companies[count] = (ticker, company)
            count += 1
    if count == 0:
        print('Company not found!')
    else:
        company_number = int(input('Enter company number:\n'))
        my_company_ticker = selected_companies[company_number][0]
        new_values = {'ebitda': int(input("Enter ebitda (in the format '987654321'):\n")),
                      'sales': int(input("Enter sales (in the format '987654321'):\n")),
                      'net_profit': int(input("Enter net profit (in the format '987654321'):\n")),
                      'market_price': int(input("Enter market price (in the format '987654321'):\n")),
                      'net_debt': int(input("Enter net dept (in the format '987654321'):\n")),
                      'assets': int(input("Enter assets (in the format '987654321'):\n")),
                      'equity': int(input("Enter equity (in the format '987654321'):\n")),
                      'cash_equivalents': int(input("Enter cash equivalents (in the format '987654321'):\n")),
                      'liabilities': int(input("Enter liabilities (in the format '987654321'):\n"))}
        fquery = my_session.query(create_db.Financial).filter(create_db.Financial.ticker == my_company_ticker)
        fquery.update(new_values)
        my_session.commit()
        print('Company updated successfully!\n')


def delete_company():
    company_name = input('Enter company name:\n')
    query = my_session.query(create_db.Companies.ticker, create_db.Companies.name)
    count = 0
    selected_companies = {}
    for ticker, company in query:
        if company_name.lower() in company.lower():
            print(count, company)
            selected_companies[count] = (ticker, company)
            count += 1
    if count == 0:
        print('Company not found!')
    else:
        company_number = int(input('Enter company number:\n'))
        my_company_ticker = selected_companies[company_number][0]
        my_session.query(create_db.Financial).filter(create_db.Financial.ticker == my_company_ticker).delete()
        my_session.query(create_db.Companies).filter(create_db.Companies.ticker == my_company_ticker).delete()
        my_session.commit()
        print('Company deleted successfully!\n')


def list_companies():
    print('COMPANY LIST')
    query = my_session.query(create_db.Companies)
    all_companies = {row.ticker: [row.ticker, row.name, row.sector] for row in query}
    for i in sorted(all_companies.keys()):
        print(*all_companies[i])
    print()


def list_by(criteria):
    query = my_session.query(create_db.Financial.ticker,
                             create_db.Financial.net_debt,
                             create_db.Financial.ebitda,
                             create_db.Financial.net_profit,
                             create_db.Financial.equity,
                             create_db.Financial.assets)
    if criteria == 1:
        indicator = {row.ticker: simply_fi(row.net_debt, row.ebitda) for row in query}
        name_financial = 'ND/EBITDA'
    elif criteria == 2:
        indicator = {row.ticker: simply_fi(row.net_profit, row.equity) for row in query}
        name_financial = 'ROE'
    elif criteria == 3:
        indicator = {row.ticker: simply_fi(row.net_profit, row.assets) for row in query}
        name_financial = 'ROA'

    list_indicator = [{'ticker': t, 'value':indicator[t]} for t in indicator if indicator[t] is not None]
    list_indicator.sort(reverse=True, key=lambda d: d['value'])
    my_tickers = list_indicator[:10]
    print('TICKER', name_financial)
    for company in my_tickers:
        print(company['ticker'], company['value'])


def perform_crud_menu():
    show_crud_menu()
    try:
        option = int(input('\nEnter an option:\n'))
    except ValueError:
        show_not_valid()
    else:
        match option:
            case 0:
                main()
            case 1:
                create_company()
            case 2:
                read_company()
            case 3:
                update_company()
            case 4:
                delete_company()
            case 5:
                list_companies()
            case _:
                show_not_implemented()


def perform_top_ten_menu():
    show_top_ten_menu()
    try:
        option = int(input('\nEnter an option:\n'))
    except ValueError:
        show_not_valid()
    else:
        match option:
            case 0:
                main()
            case 1:
                list_by(1)
            case 2:
                list_by(2)
            case 3:
                list_by(3)
            case _:
                print('Invalid option!\n')


def main():
    show_main_menu()
    try:
        option_selected = int(input('\nEnter an option:\n'))
    except ValueError:
        show_not_valid()
    else:
        perform_main_menu(option_selected)
        my_session.close_all()


print('Welcome to the Investor Program!')
print()
main()
