import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sona-kitchen')

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data form the user via the terminal, which must be a string of 15 numbers separated by commas.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data form the last market.")
        print("Data should be fifteen numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150\n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(",")
    

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 15 values.
    """
    try:
        if len(values) != 15:
            raise ValueError(
                f"Exactly 15 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each itm type.

    The surplus is defined as the sales figure subtracted form the stock:
    - positive surplus indicates waste
    -Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to Sona Kitchen Data Automation")
main()

