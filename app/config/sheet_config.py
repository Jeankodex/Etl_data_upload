
# Sheet configuration for ETL
# Defines sheet names, header rows, data start rows, and unique key per sheet

SHEET_CONFIG = {
    "Indian Companies": {
        "header_row": 9,      # row index in Excel (1-based)
        "data_start_row": 10, # row index where actual data starts
        "unique_key": "CIN"
    },
    "LLP Companies": {
        "header_row": 10,
        "data_start_row": 11,
        "unique_key": "LLPIN"
    },
    "Foreign Companies": {
        "header_row": 11,
        "data_start_row": 12,
        "unique_key": "FCIN"
    }
}
