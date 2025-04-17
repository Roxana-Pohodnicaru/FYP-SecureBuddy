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

        
        # create MalwareSignatures table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MalwareSignatures (
                signature_id INTEGER PRIMARY KEY,
                signature_type TEXT CHECK(signature_type IN ('MD5', 'SHA1', 'SHA256')) NOT NULL,
                signature_value TEXT NOT NULL,
                threat_level TEXT CHECK(threat_level IN ('low', 'medium', 'high'))
            )
        ''')

        # create EducationalProgress table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS EducationalProgress (
            progress_id INTEGER PRIMARY KEY,
            topic_name TEXT NOT NULL UNIQUE,
            read_completed BOOLEAN NOT NULL DEFAULT 0,
            quiz_passed BOOLEAN NOT NULL DEFAULT 0
        )
        ''')
        
        # commit transaction to save changes
        self.connection.commit()
        
        
    # prepopulate topics in EducationalProgress table
    def prepopulate_topics(self, topics):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # iterate through the list of topics
        for topic in topics:
            
            # insert each topic into EducationalProgress table
            # if does not already exist
            cursor.execute('''
                INSERT OR IGNORE INTO EducationalProgress (topic_name)
                VALUES (?)
            ''', (topic,))
            
        # commit transaction
        self.connection.commit()
        
    
    # mark a specific topic as read in EducationalProgress table
    def mark_topic_as_read(self, topic_name):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # update read_completed status to 1 for specified topic
        cursor.execute('''
            UPDATE EducationalProgress
            SET read_completed = 1
            WHERE topic_name = ?
        ''', (topic_name,))
        
        # commit transaction
        self.connection.commit()
        
        
    # get topic names from EducationalProgress table which marked as read
    def get_read_topics(self):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # select all topic names that are read
        cursor.execute('''
            SELECT topic_name
            FROM EducationalProgress
            WHERE read_completed = 1
        ''')
        
        # fetch all first column rows and put in a set
        read_topics = {row[0] for row in cursor.fetchall()}
        
        # return set of read topic names
        return read_topics
        
    
    # mark quiz as passed for specific topic in EducationalProgress table
    def mark_quiz_as_passed(self, topic_name):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # update quiz_completed status to 1 for specified topic
        cursor.execute('''
            UPDATE EducationalProgress
            SET quiz_passed = 1
            WHERE topic_name = ?
        ''', (topic_name,))
        
        # commit transaction
        self.connection.commit()
        
        
    # get topic names from EducationalProgress table which marked as quiz passed
    def get_passed_quizzes(self):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # select all topic names where quizzes are passed
        cursor.execute('''
            SELECT topic_name
            FROM EducationalProgress
            WHERE quiz_passed = 1
        ''')
        
        # fetch all first column rows and put in a set
        passed_quizzes = {row[0] for row in cursor.fetchall()}
        
        # return set of passed quiz topic names
        return passed_quizzes


    # add file details to ScannedFile table
    
    def add_scanned_file(self, file_name, scan_date, status, risk_level):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # inserting data into table
        # data is in tuple format
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
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # inserting data into table
        # data is in tuple format
        cursor.execute('''
            INSERT INTO ScanDetails (scanned_file_id, reason_for_flag, risk_category)
            VALUES (?, ?, ?)
        ''', (scanned_file_id, reason_for_flag, risk_category))
        
        # commit transaction
        self.connection.commit()

 
    # get all scan records for scan history page
    def get_scan_history(self):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # select data from scanned file table
        cursor.execute('''
            SELECT scanned_file_id, file_name, scan_date 
            FROM ScannedFile
            ORDER BY scan_date DESC
        ''')
        
        # fetch rows returned by query
        # return as list of tuples
        return cursor.fetchall()
    

    # get specific scan details for given scan id
    # from scan details table
    def get_scan_details(self, scan_id):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # select data from scan details table
        cursor.execute('''
            SELECT reason_for_flag, risk_category
            FROM ScanDetails
            WHERE scanned_file_id = ?
        ''', (scan_id,))
        
        # fetch rows returned by query
        # return as list of tuples
        return cursor.fetchall()


    # get specific scan details for given scan id
    # from scanned file table
    def get_scanned_file_info(self, scan_id):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # select data from table
        cursor.execute('''
            SELECT file_name, scan_date, status, risk_level
            FROM ScannedFile
            WHERE scanned_file_id = ?
        ''', (scan_id,))
        
        # fetch rows returned by query
        # return as list of tuples
        return cursor.fetchone()

   
    # add malware signatures to db
    def add_malware_signatures(self, signatures):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()
        
        # insert multiple malware signatures into table as batches
        cursor.executemany('''
            INSERT INTO MalwareSignatures (signature_type, signature_value, threat_level)
            VALUES (:signature_type, :signature_value, :threat_level)
        ''', signatures)
        
        # commit transaction
        self.connection.commit()


    # check if file signature matches known malware signatures in db
    # handles MD5, SHA1, SHA256
    def check_file_signature(self, signature_value):
        
        # create cursor object to interact with db
        cursor = self.connection.cursor()

        # full match query
        cursor.execute('''
            SELECT * FROM MalwareSignatures
            WHERE signature_value = ?
        ''', (signature_value,))

        # fetch result of full match query
        full_match = cursor.fetchone()

        # if full match found
        if full_match:
            
            # debugging
            print("Match found: ", full_match)
            
            # return match
            return full_match


        # if no full match found
        # check for partial matches
        # determine length needed based on signature type
        # MD5 32 characters
        # SHA1 40 characters
        # SHA256 64 characters
        
        # MD5 length
        if len(signature_value) == 32:
            
            # match first 8 chars
            partial_length = 8
            
        # SHA1 length
        elif len(signature_value) == 40:
            
            # match first 8 chars
            partial_length = 8
            
        # SHA256
        elif len(signature_value) == 64:
            
            # match first 16 chars
            partial_length = 16
            
        else:
            
            # default length for unknown sigantures
            partial_length = 8

        # Now check for partial matches using the determined length
        
        # perform match check query
        cursor.execute('''
            SELECT * FROM MalwareSignatures
            WHERE signature_value LIKE ?
        ''', (f'{signature_value[:partial_length]}%',))

        # fetch result of query
        partial_match = cursor.fetchone()

        # if partial match found
        if partial_match:
            
            # return matched value
            return partial_match

        # no match found        
        return None
    

    # close connection to db
    def close(self):
        
        # closing connection
        self.connection.close()
        
        
        
# main
if __name__ == "__main__":

    # create instance of database manager class
    # initialize db and create tables
    db_manager = DatabaseManager()
    
    # define list of educational topics
    topics = ["Executables", "File Spoofing", "Obfuscation", "Remote Access Control", "Viruses", "Credential Stealers", "Compressed Files", "Macros"]
    
    # prepopulate EducationalProgress table with topics
    db_manager.prepopulate_topics(topics)
    
    # success message
    print("Database initialized and tables created successfully")
    
    # close db connection
    db_manager.close()