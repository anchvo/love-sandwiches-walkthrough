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

    # Print statement to check values from user input show up as expected
    #print(f"The data provided is {data_str}")

    sales_data = data_str.split(",")
    validate_data(sales_data)

def validate_data(values):
    """
    Checks if user input data is valid by
    Converts all string values to integers inside the try
    Raises ValueError if strings cannot be converted into int
    or if there aren't exactly 6 values
    """
    try:
        # Code that should work with no errors if data is valid
        [int(value) for value in values]
        if len(values) != 6:
            # Should length of the values list not be six
            raise ValueError(
                f"Exactly six values are required, you provided {len(values)}"
            )
    except ValueError as e:
        # Common shorthand variable e for error
        print(f"Invalid data: {e}, please try again.\n")

get_sales_data()