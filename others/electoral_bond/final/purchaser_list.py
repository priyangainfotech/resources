import PyPDF2
import pandas as pd
import re

def parse_line(line):
    prefixs = ['OT','TT', 'OL', 'TL', 'OC']  # List of names to check against


    print("-------------------------------------------------------------")
    print(line)
    parts = line.split()
    sliced_array = parts[5:]
    prefix_index = 5
    party_name = ""
    for index, element in enumerate(sliced_array):
        if not any (element.startswith(deno) for deno in prefixs):
            party_name+= element+" "
        else:
            prefix_index += index
            break
    print("End of loop")
    print(prefix_index)
    prefix = parts[prefix_index]

    return parts[0], parts[1], parts[2], parts[3], parts[4], party_name.strip(), prefix, parts[prefix_index+1], parts[prefix_index+2].replace(",", ""),parts[prefix_index+3], parts[prefix_index+4],parts[prefix_index+5]

def extract_table_from_pdf(pdf_path, start_page, end_page):
    table_data = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:

            text = page.extract_text()
            # Split text into lines and extract table-like data
            lines = text.split('\n')
            for line in lines:
                if len(line.split()) >= 10:  # Assuming at least 6 characters for each line
                    table_data.append(parse_line(line))           
            
    return table_data

def save_to_excel(table_data, output_path):
    df = pd.DataFrame(table_data, columns=['Sr.No', 'Reference No (URN)', 'Journal Date', "Date Of Purchase",'Date of Expiry','Name of the Purchaser','Prefix', 'Bond Number', 'Denominations', 'Issue Branch Code', 'Issue Teller', 'Status'])
    df.to_excel(output_path, index=False)

def convert_pdf_to_excel(pdf_path, start_page, end_page, output_path):
    table_data = extract_table_from_pdf(pdf_path, start_page, end_page)
    save_to_excel(table_data, output_path)

# Example usage
pdf_path = 'purchaser_list.pdf'  # Path to your PDF file
start_page = 1  # Start page of the table
end_page = 3  # End page of the table
output_path = 'purchaser_list.xlsx'  # Path where the Excel file will be saved

convert_pdf_to_excel(pdf_path, start_page, end_page, output_path)
