""" 
Description: 
  Divides sales data CSV file into individual order data Excel files.

Usage:
  python process_sales_data.py sales_csv_path

Parameters:
  sales_csv_path = Full path of the sales data CSV file
"""
import pandas as pd
import sys 
import os.path 
from datetime import date
import re
def main():
    sales_csv_path = get_sales_csv_path()
    orders_dir_path = create_orders_dir(sales_csv_path)
    process_sales_data(sales_csv_path, orders_dir_path)

def get_sales_csv_path():
    """Gets the path of sales data CSV file from the command line
    Returns:
        str: Path of sales data CSV file
    """
    # TODO: Check whether command line parameter provided
    num_params = len(sys.argv) -1
    if num_params < 1:
        print("Error: Missiing CSV path parameter.")
        sys.exit()

    # TODO: Check whether provide parameter is valid path of file
    csv_path = sys.argv[1]
    if not os.path.isfile(csv_path):
        print("Error: CSV path is not an existing file.")
        sys.exit()


    # TODO: Return path of sales data CSV file
    return os.path.abspath(csv_path)

def create_orders_dir(sales_csv_path):
    """Creates the directory to hold the individual order Excel sheets

    Args:
        sales_csv_path (str): Path of sales data CSV file

    Returns:
        str: Path of orders directory
    """
    # TODO: Get directory in which sales data CSV file resides
    sales_csv_dir = os.path.dirname(sales_csv_path)

    # TODO: Determine the path of the directory to hold the order data files
    today_date = date.today().isoformat()
    orders_dir = f'orders_{today_date}'
    orders_dir_path = os.path.join(sales_csv_dir, orders_dir)


    # TODO: Create the orders directory if it does not already exist
    if not os.path.isdir(orders_dir_path):
        os.makedirs(orders_dir_path)

    # TODO: Return path of orders directory
    return orders_dir_path

def process_sales_data(sales_csv_path, orders_dir_path):
    """Splits the sales data into individual orders and save to Excel sheets

    Args:
        sales_csv_path (str): Path of sales data CSV file
        orders_dir_path (str): Path of orders directory
    """
    
    # TODO: Import the sales data from the CSV file into a DataFrame
    df = pd.read_csv(sales_csv_path)



    # TODO: Insert a new "TOTAL PRICE" column into the DataFrame
    df.insert(7, 'TOTAL PRICE',df['ITEM QUANTITY']* df['ITEM PRICE'])

    # TODO: Remove columns from the DataFrame that are not needed
    df.drop(columns=["ADDRESS", "CITY", "STATE", "POSTAL CODE", "COUNTRY"], inplace=True)

    # TODO: Groups orders by ID and iterate 
    for order_id, order_df in df.groupby("ORDER ID"):

        # TODO: Remove the 'ORDER ID' column
        order_df.drop(columns=["ORDER ID"], inplace=True)
        # TODO: Sort the items by item number
        order_df.sort_values(by="ITEM NUMBER", inplace=True)
        # TODO: Append a "GRAND TOTAL" row
        grand_total = order_df["TOTAL PRICE"].sum()
        grand_total_df = pd.DataFrame({"ITEM PRICE": ["GRAND TOTAL"], "TOTAL PRICE": [grand_total]})
        order_df = pd.concat
        ([order_df, grand_total_df])
        
        # TODO: Determine the file name and full path of the Excel sheet
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name = re.sub(r'\w', '', customer_name)
        order_file = f"ordr{order_id}_{customer_name}.xlsx" 
        order_excel_path = os.path.join(orders_dir_path, order_file) 

        # TODO: Export the data to an Excel sheet
        worksheet_name = f"Order #{order_id}"
        order_df.to_excel(order_excel_path, index=False, sheet_name=worksheet_name)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter("pandas_column_formats.xlsx", engine="xlsxwriter")

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name="Sheet1")

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Add some cell formats.
        format1 = workbook.add_format({"num_format": "#,##0.00"})
        format2 = workbook.add_format({"num_format": "0%"})

        # Note: It isn't possible to format any cells that already have a format such
        # as the index or headers or any cells that contain dates or datetimes.

        # Set the column width and format.
        worksheet.set_column(1, 1, 18, format1)

        # Set the format but not the column width.
        worksheet.set_column(2, 2, None, format2)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        # TODO: Format the Excel sheet
        # TODO: Define format for the money columns
        # TODO: Format each colunm
        # TODO: Close the Excelwriter 
    return

if __name__ == '__main__':
    main()