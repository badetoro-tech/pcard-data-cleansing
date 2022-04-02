from sqlalchemy import MetaData, Table, Column, Integer, String, Numeric, ForeignKey, Index
from sqlalchemy.types import DateTime

metadata = MetaData()

pcard_staging_table = Table('pcard_staging_table', metadata,
                            Column('division', String(250)),
                            Column('batch_transaction_id', String(50)),
                            Column('transaction_date', DateTime()),
                            Column('card_posting_dt', DateTime()),
                            Column('merchant_name', String(250)),
                            Column('transaction_amt', Numeric(20, 2)),
                            Column('trx_currency', String(20)),
                            Column('original_amount', Numeric(20, 2)),
                            Column('original_currency', String(20)),
                            Column('gl_account', String(20)),
                            Column('gl_account_description', String(250)),
                            Column('cost_centre_wbs_element_order_no', String(20)),
                            Column('cost_centre_wbs_element_order_no_description', String(250)),
                            Column('merchant_type', String(20)),
                            Column('merchant_type_description', String(250)),
                            Column('purpose', String(250))
                            )

division = Table('division', metadata,
                 Column('division_id', Integer(), primary_key=True, autoincrement=True),
                 Column('division', String(250))
                 )

merchant = Table('merchant', metadata,
                 Column('merchant_id', Integer(), primary_key=True, autoincrement=True),
                 Column('merchant_name', String(250))
                 )

gl_account = Table('gl_account', metadata,
                   Column('gl_account', String(20), primary_key=True),
                   Column('gl_account_description', String(250))
                   )

cost_center = Table('cost_center', metadata,
                    Column('cost_centre_wbs_element_order_no', String(20), primary_key=True),
                    Column('cost_centre_wbs_element_order_no_description', String(250))
                    )

merchant_type = Table('merchant_type', metadata,
                      Column('merchant_type', String(20), primary_key=True),
                      Column('merchant_type_description', String(250))
                      )

currency_list = Table('currency_list', metadata,
                      Column('currency_code', String(20), primary_key=True),
                      Column('currency_desc', String(250))
                      )

transactions = Table('transactions', metadata,
                     Column('division_id', Integer(), ForeignKey('division.division_id')),
                     Column('batch_transaction_id', String(50)),
                     Column('transaction_date', DateTime()),
                     Column('card_posting_dt', DateTime()),
                     Column('merchant_name', String(250)),
                     Column('transaction_amt', Numeric(20, 2)),
                     Column('trx_currency', String(20), ForeignKey('currency_list.currency_code')),
                     Column('original_amount', Numeric(20, 2)),
                     Column('original_currency', String(20), ForeignKey('currency_list.currency_code')),
                     # Column('gl_account', String(10), ForeignKey('gl_account.gl_account')),
                     Column('gl_account', String(20)),
                     Column('gl_account_description', String(250)),

                     # Column('cost_centre_wbs_element_order_no', String(20),
                     #        ForeignKey('cost_center.cost_centre_wbs_element_order_no')),
                     Column('cost_centre_wbs_element_order_no', String(20)),
                     Column('cost_centre_wbs_element_order_no_description', String(250)),

                     Column('merchant_type', String(20), ForeignKey('merchant_type.merchant_type')),
                     Column('purpose', String(250)),
                     Index('ix01_transactions', 'division_id', 'transaction_date', 'card_posting_dt')
                     )
