import time

from models import currency_list, pcard_staging_table
from sqlalchemy import insert, select, func, delete, exc
from database_conn import engine
from config import PROCESSED_FOLDER, UNPROCESSED_FOLDER, WAIT_TIME, LOG_FILE
import pandas as pd
from os import listdir, replace, remove
from datetime import datetime
from pprint import pprint

connection = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
unprocessed_filepath = UNPROCESSED_FOLDER
processed_filepath = PROCESSED_FOLDER
timeout = WAIT_TIME
log_file = LOG_FILE


def check_setup_data(debug):
    # populate the currency table
    s = select([func.count(currency_list.c.currency_code).label('cnt')])
    rp = connection.execute(s)
    record = rp.first().cnt

    # if currency_list is empty, populate with initial data
    if record <= 0:

        items = []
        currency_file = pd.read_csv('ccy_data/currency.csv')
        ccy_list = currency_file.to_dict(orient="records")

        for record_list in ccy_list:
            items += [
                {
                    'currency_code': record_list['currency'],
                    'currency_desc': record_list['description']
                }
            ]

        ins = insert(currency_list)
        connection.execute(ins, items)
        if debug >= 1:  # 1
            msg = 'Currency list table is empty. Now populated'
            write_to_file(msg)
            print(msg)
    else:
        if debug >= 1:  # 1
            print('Setup Data not required')


def import_excel_data(debug):
    directory_list = listdir(unprocessed_filepath)
    arr = directory_list

    if not directory_list:
        if debug >= 1:
            msg = 'No file to process ...'
            write_to_file(msg)
            print(msg)
        time.sleep(timeout)
    else:
        if debug >= 0:
            msg = f'There are files {len(directory_list)} to be processed...'
            write_to_file(msg)
            print(msg)

        # Purge the staging table
        empty_staging_table(debug)

        for i, excel_file in enumerate(arr):
            data = pd.read_excel(unprocessed_filepath + '\\' + excel_file)
            # making sure the Excel sheets have the same header across
            # With this, I am renaming the Excel header to standardized header name
            data_tidy = data.rename(columns={data.columns[0]: 'division', data.columns[1]: 'batch_transaction_id',
                                             data.columns[2]: 'transaction_date', data.columns[3]: 'card_posting_dt',
                                             data.columns[4]: 'merchant_name', data.columns[5]: 'transaction_amt',
                                             data.columns[6]: 'trx_currency', data.columns[7]: 'original_amount',
                                             data.columns[8]: 'original_currency', data.columns[9]: 'gl_account',
                                             data.columns[10]: 'gl_account_description',
                                             data.columns[11]: 'cost_centre_wbs_element_order_no',
                                             data.columns[12]: 'cost_centre_wbs_element_order_no_description',
                                             data.columns[13]: 'merchant_type',
                                             data.columns[14]: 'merchant_type_description',
                                             data.columns[15]: 'purpose'})
            df = pd.DataFrame(data_tidy)
            df = df.dropna(subset=['division'])
            if debug >= 1:
                msg = f'{excel_file} has {str(len(data))} records of unclean data and {str(len(df))} of clean data'
                write_to_file(msg)

            # inserting records into the table pcard_staging_table
            for row in df.itertuples():
                connection.execute('''insert into pcard_staging_table (division ,
                                      batch_transaction_id ,
                                      transaction_date ,
                                      card_posting_dt,
                                      merchant_name ,
                                      transaction_amt ,
                                      trx_currency ,
                                      original_amount ,
                                      original_currency,
                                      gl_account ,
                                      gl_account_description ,
                                      cost_centre_wbs_element_order_no ,
                                      cost_centre_wbs_element_order_no_description,
                                      merchant_type,
                                      merchant_type_description,
                                      purpose  ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                   str(row.division),
                                   str(row.batch_transaction_id),
                                   row.transaction_date,
                                   row.card_posting_dt,
                                   str(row.merchant_name),
                                   float(row.transaction_amt),
                                   str(row.trx_currency),
                                   float(row.original_amount),
                                   str(row.original_currency),
                                   row.gl_account,
                                   str(row.gl_account_description),
                                   str(row.cost_centre_wbs_element_order_no),
                                   str(row.cost_centre_wbs_element_order_no_description),
                                   str(row.merchant_type),
                                   str(row.merchant_type_description),
                                   str(row.purpose)
                                   )

            # Move processed file from the unprocessed folder to processed folder
            replace(f'{unprocessed_filepath}/{excel_file}', f'{processed_filepath}/{excel_file}')

        normalised_proc = 'EXEC dbo.p_normalize_data'
        connection.execute(normalised_proc)
        if debug >= 2:
            msg = 'Imported data now normalised'
            write_to_file(msg)

        if debug >= 0:
            msg = f'Processing complete'
            write_to_file(msg)


def empty_staging_table(debug):
    if debug >= 2:
        msg = f'Emptying staging table...'
        write_to_file(msg)
    dlt = delete(pcard_staging_table)
    connection.execute(dlt)


def build_db_objects(folder_path):
    # Open and read the file as a single buffer
    with open(folder_path, 'r') as inp:
        connection.execute(f'''inp''')


def write_to_file(msg):
    timestamp = datetime.now().strftime("%d-%b-%Y %I:%M:%S.%f %p")
    with open(log_file, 'a') as f:
        f.write(f'{timestamp}: {msg}\n')
