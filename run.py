# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

# Values of variables do not change so they are constant variables written in capital letters

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# Lists APIs that the program should access in order to run

CREDS = Credentials.from_service_account_file("creds.json")
# Uses a method from the Credentials class that was imported
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")
# Opens the exel sheet in google account that was set up before, name needs to be exact

# Following commented out code was used to check if API is working
#sales = SHEET.worksheet("sales")
# Access data from sales tab in excel sheet and stores it in variable
#data = sales.get_all_values()
# Uses a gspread method to get all values
#print(data)

def get_sales_data():
    """
    Get sales figures input from user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

get_sales_data()