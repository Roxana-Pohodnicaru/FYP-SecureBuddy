# TODO: need to automatically run db file from start

import sqlite3


class DatabaseManager:
    
    # initialize class with database name
    def __init__(self, db_name="securebuddy.db"):
        
        # establish a connection to the SQLite db
        self.connection = sqlite3.connect(db_name)
        
        # create tables in db
        self.create_tables()


    # create tables in the database
    def create_tables(self):
        
        # create cursor object to interact with the db
        cursor = self.connection.cursor()

        # create ScannedFile table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ScannedFile (
                scanned_file_id INTEGER PRIMARY KEY,
                file_name TEXT NOT NULL,
                scan_date TEXT NOT NULL,
                status TEXT CHECK(status IN ('safe', 'suspicious', 'dangerous')),
                risk_level TEXT CHECK(risk_level IN ('high', 'medium', 'low'))
            )
        ''')

        # create ScanDetails table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ScanDetails (
                scan_details_id INTEGER PRIMARY KEY,
                scanned_file_id INTEGER,
                reason_for_flag TEXT NOT NULL,
                risk_category TEXT NOT NULL,
                FOREIGN KEY (scanned_file_id) REFERENCES ScannedFile(scanned_file_id)
            )
        ''')

        # create ThreatInfo table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ThreatInfo (
                threat_info_id INTEGER PRIMARY KEY,
                scanned_file_id INTEGER,
                what_happens_if_run TEXT NOT NULL,
                prevention_tips TEXT NOT NULL,
                FOREIGN KEY (scanned_file_id) REFERENCES ScannedFile(scanned_file_id)
            )
        ''')

        # commit transaction to save changes
        self.connection.commit()


    # add file details to ScannedFile table
    def add_scanned_file(self, file_name, scan_date, status, risk_level):
        
        # create cursor object to interact with the db
        cursor = self.connection.cursor()
        
        # inserting data into table
        # data is in tuple format
        # using placeholders (?) in order to prevent SQL injections
        cursor.execute('''
            INSERT INTO ScannedFile (file_name, scan_date, status, risk_level)
            VALUES (?, ?, ?, ?)
        ''', (file_name, scan_date, status, risk_level))
        
        # commit transaction
        self.connection.commit()
        
        # return ID of last inserted row for auto increment
        return cursor.lastrowid


    # add file details to ScanDetails table
    def add_scan_detail(self, scanned_file_id, reason_for_flag, risk_category):
        
        # create cursor object to interact with the db
        cursor = self.connection.cursor()
        
        # inserting data into table
        # data is in tuple format
        # using placeholders (?) in order to prevent SQL injections
        cursor.execute('''
            INSERT INTO ScanDetails (scanned_file_id, reason_for_flag, risk_category)
            VALUES (?, ?, ?)
        ''', (scanned_file_id, reason_for_flag, risk_category))
        
        # commit transaction
        self.connection.commit()



    def add_threat_info(self, scanned_file_id, what_happens_if_run, prevention_tips):
        
        # create cursor object to interact with the db
        cursor = self.connection.cursor()
        
        # inserting data into table
        # data is in tuple format
        # using placeholders (?) in order to prevent SQL injections
        cursor.execute('''
            INSERT INTO ThreatInfo (scanned_file_id, what_happens_if_run, prevention_tips)
            VALUES (?, ?, ?)
        ''', (scanned_file_id, what_happens_if_run, prevention_tips))
        
        # commit transaction
        self.connection.commit()


    # close connection to db
    def close(self):
        
        # closing connection
        self.connection.close()




# main
if __name__ == "__main__":

    # create instance of database manager class
    # initialize db and create tables
    db_manager = DatabaseManager()
    
    # success message
    print("Database initialized and tables created successfully")
    
    # close db connection
    db_manager.close()