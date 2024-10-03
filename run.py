# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Run a while loop to get a valid string of data from the user
    via the terminal, which must be a string of six numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        # Loop for user input to repeat asking for input while data is invalid
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        # Print statement to check values from user input show up as expected
        #print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")
        
        if validate_data(sales_data): 
            # Breaks the loop if data is valid and ends user input
            print("Data is valid!")
            break

    return sales_data
    # Returns valid sales_data after user input was validated

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
        return False
        # Returns False because data is invalid 
        # which is picked up by while loop and tells it to continue running
    
    return True
    # Data is valid and returns true, tells the while loop to break

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    # Uses gspread method and refers to sales worksheet 
    # in excel sheet by correct name
    sales_worksheet.append_row(data)
    # Uses gspread method to add new row in sales worksheet 
    # and fill it with provided list data 
    print("Sales worksheet updated successfully.\n")

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    # Uses gspread method and refers to surplus worksheet 
    # in excel sheet by correct name
    surplus_worksheet.append_row(data)
    # Uses gspread method to add new row in surplus worksheet 
    # and fill it with provided list data 
    print("Surplus worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extra made when stock was sold out. 
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        # A list comprehension could be used to parse all strings in the list to integers, 
        # however this method converts the value at the same time it is accessed
        surplus_data.append(surplus)
    
    return surplus_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)
    # Common practice to wrap all function calls in a main function

print("Welcome to Love Sandwiches Data Automation")
main()
# Main function needs to be called; 
# a function can only be called after it was defined