import PyPDF2
import pandas as pd
import re

def parse_line(line):
    # Define regular expressions for the patterns
    print("-------------------------------------------------------------")
    print(line)
    parts = line.split()
    print(len(parts))

    sliced_array = parts[2:]
    account_no_index = 0
    party_name = ""
    for index, element in enumerate(sliced_array):
        if not element.startswith('*'): 
            party_name+= element+" "
        else:
            account_no_index = index
            break

    account_no_index+=2
    acc_no = parts[account_no_index]
    prefix = parts[account_no_index+1]
    bond_number = parts[account_no_index+2]
    amount = parts[account_no_index+3].replace(',', "")
    branch_code = parts[account_no_index+4]
    pay_teller = parts[account_no_index+5]

    return parts[0], parts[1], party_name.strip(), acc_no, prefix, bond_number, amount, branch_code, pay_teller

def extract_table_from_pdf(pdf_path, start_page, end_page):
    table_data = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:

            text = page.extract_text()
            
            title = ["Sr", "EncashmentName", "Political", 'PartyPrefixBond', 'NumberDenominationsPay', 'Branch', 'CodePay', 'Teller', 'Page']  # List of names to check against
            # Split text into lines and extract table-like data
            lines = text.split('\n')
            for line in lines:
                if len(line.split()) >= 8:  # Assuming at least 6 characters for each line
                    table_data.append(parse_line(line))           
            
    return table_data

def save_to_excel(table_data, output_path):
    df = pd.DataFrame(table_data, columns=['Sr.No', 'Date of Encashment', 'Name of Political Party', "Account no. political party",'Prefix', 'Bond Number', 'Denominations', 'Pay Branch Code', 'Pay Teller' ])
    df.to_excel(output_path, index=False)

def convert_pdf_to_excel(pdf_path, start_page, end_page, output_path):
    table_data = extract_table_from_pdf(pdf_path, start_page, end_page)
    save_to_excel(table_data, output_path)

# Example usage
pdf_path = 'party_list.pdf'  # Path to your PDF file
start_page = 1  # Start page of the table
end_page = 3  # End page of the table
output_path = 'party_list.xlsx'  # Path where the Excel file will be saved

convert_pdf_to_excel(pdf_path, start_page, end_page, output_path)
