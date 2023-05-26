###########################################################################
#     schema.sql
#
#     Database schema for SQLite
#     Table structure for table 'financial_data'
###########################################################################

CREATE TABLE financial_data(
          symbol TEXT,
          date TEXT,
          open_price REAL,
          close_price REAL,
          volume INTEGER,
          PRIMARY KEY (symbol, date)
      )
