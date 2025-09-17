from pathlib import Path
from openpyxl import Workbook
import pdfplumber
import re
from datetime import datetime
import mysql.connector

def execute_insert(cursor, invoice_number, invoice_date, file_name, status):
    sql = "INSERT INTO invoice_records (invoice_number, invoice_date, file_name, status) VALUES (%s, %s, %s, %s)"
    val = (invoice_number, invoice_date, file_name, status)
    cursor.execute(sql, val)
    

def main():
    # STARTUP

    # Database Connection
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "process_invoice"
    )
    cursor = db.cursor()
    print("---- Sucessfully connect to database... ---")


    directory =  Path('pdf_invoices')
    pdf_files = list(directory.glob("*.pdf"))
    files_quantity = len(pdf_files)


    if files_quantity == 0:
        raise Exception("No files found in the directory")

    # Create Excel file
    #Criando o workbook, e nomeando a worksheet
    wbook = Workbook()
    wsheet = wbook.active
    wsheet.title = 'Invoice Imports'

    # Definindo colunas na worksheet
    wsheet['A1'] = 'Invoice #'
    wsheet['B1'] = 'Date'
    wsheet['C1'] = 'File Name'
    wsheet['D1'] = 'Status'

    # Resgatando a ultima linha preenchida para poder 
    # confirmar se a proxima esta vazia
    last_empty_line = 1

    while wsheet['A{}'.format(last_empty_line)].value is not None:
        last_empty_line += 1

    # Work
    for file_path in pdf_files:
        try:
            with pdfplumber.open(file_path) as pdf:
                first_page = pdf.pages[0]
                pdf_text = first_page.extract_text()
            
            # expressão regex para encontrar o texto
            inv_number_re_pattern = r'INVOICE #(\d+)'
            inv_date_re_patter = r'DATE: (\d{2}/\d{2}/\d{4})'
            
            # ele procura a expressão regex no pdf_text
            match_number = re.search(inv_number_re_pattern, pdf_text)
            match_date = re.search(inv_date_re_patter, pdf_text)

            #se achar o texto que der o match com a expressão, inclui no grupo
            if match_number:
                #atribui o valor de invoice_number a ultima linha preenchida
                wsheet['A{}'.format(last_empty_line)] = match_number.group(1)
            else:
                raise Exception("Couldn't find invoice number")
            
            if match_date:
                wsheet['B{}'.format(last_empty_line)] = match_date.group(1)
            else:
                raise Exception("Couldn't find invoice date")
                        
            wsheet['C{}'.format(last_empty_line)] = file_path.name
            wsheet['D{}'.format(last_empty_line)] = 'Completed'

            execute_insert(cursor, match_number.group(1), match_date.group(1), file_path.name, "Completed")
            db.commit()

            last_empty_line += 1

        except Exception as ex:
            print(f"Error processing file: {ex}")

            wsheet['C{}'.format(last_empty_line)] = file_path.name
            wsheet['D{}'.format(last_empty_line)] = "Exception {}".format(ex)

            execute_insert(cursor, "N/A", "N/A", file_path.name, "Exception: {}".format(ex))
            db.commit()

            last_empty_line += 1

    cursor.close()
    db.close()

    full_now = str(datetime.now()).replace(":", "-")
    dot_index = full_now.index(".")
    now = full_now[:dot_index]
    wbook.save("Invoices - {}.xlsx".format(now))

if __name__ == "__main__":
    main()