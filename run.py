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

# The following two functions were refactored into one function
#def update_sales_worksheet(data):
   # """
   # Update sales worksheet, add new row with the list data provided
   # """
   # print("Updating sales worksheet...\n")
   # sales_worksheet = SHEET.worksheet("sales")
   # sales_worksheet.append_row(data)
   # print("Sales worksheet updated successfully.\n")

#def update_surplus_worksheet(data):
   # """
   # Update surplus worksheet, add new row with the list data provided
   # """
   # print("Updating surplus worksheet...\n")
   # surplus_worksheet = SHEET.worksheet("surplus")
   # surplus_worksheet.append_row(data)
   # print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    # Refactored function to combine two previous functions to update each worksheet
    # General function works by using parameters that are specified 
    # when function is called in main function, 
    # e.g. data = sales_data and worksheet = "sales"
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    # Uses gspread method to refer to worksheet in excel, 
    # the worksheet parameter is specified in function call, 
    # allowing different worksheets to be called depending on which parameter is given
    worksheet_to_update.append_row(data)
    # Uses gspred method to add new row to worksheet and 
    # fill it with provided data
    print(f"{worksheet} worksheet updated successfully.\n")


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

def get_last_five_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting 
    the last 5 entries for each sandwich and returns the data 
    as a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        # The length could also be set to 5, 
        # as we know the length will always be 5
        stock_num = average * 1.1
        # This adds 10% to the average
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_five_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    # Common practice to wrap all function calls in a main function

print("Welcome to Love Sandwiches Data Automation")
main()
# Main function needs to be called; 
# a function can only be called after it was defined;
# A handy way to test new functions is to comment out call to main() 
# and call new function below, so it is the only function called
