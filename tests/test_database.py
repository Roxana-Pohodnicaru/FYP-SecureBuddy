import sys
import os
import pytest
import sqlite3


# add parent dir to system path
# so files from root dir can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# importing database
from database import DatabaseManager


# fixture to set up mock database instance
@pytest.fixture
def db():
   
    # in memory db for isolated testing
    manager = DatabaseManager(":memory:")

    # ensure tables are created
    manager.create_tables()

    return manager


# test that tables are created in db
def test_create_tables(db):
    
    # create cursor to interact with db
    cursor = db.connection.cursor()
    
    # fetch names of all tables in db
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # fetch all first column rows and put table names in a set
    tables = {row[0] for row in cursor.fetchall()}
    
    # define set of table names to be expected to exist in db
    expected_tables = {"EducationalProgress", "ScannedFile", "ScanDetails", "MalwareSignatures"}
    
    # check that expected table names are present in db
    assert expected_tables.issubset(tables)


# testing adding a scanned file to ScannedFile table
def test_add_scanned_file(db):
    
    # add new file
    new_id = db.add_scanned_file("file.exe", "2025-04-07", "safe", "low")
    
    # check if returned ID is an int
    assert isinstance(new_id, int)

    # fetch row from db to check it
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM ScannedFile WHERE scanned_file_id = ?", (new_id,))
    row = cursor.fetchone()

    # assert each column matches expected values
    assert row[1] == "file.exe"
    assert row[2] == "2025-04-07"
    assert row[3] == "safe"
    assert row[4] == "low"


# testing adding scna detail to ScanDetails table
def test_add_scan_detail(db):
    
    # add scanned file
    file_id = db.add_scanned_file("evil.exe", "2025-04-07", "dangerous", "high")
    
    # add scan detail associated with file
    db.add_scan_detail(file_id, "Detected Trojan", "high")

    # fetch scan details to check it
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM ScanDetails WHERE scanned_file_id = ?", (file_id,))
    detail = cursor.fetchone()

    # assert each column matches expected values
    assert detail[1] == file_id
    assert detail[2] == "Detected Trojan"
    assert detail[3] == "high"
    
    
# test prepopulating topics and marking one as read
def test_prepopulate_topics_and_read(db):
    
    # prefill table
    db.prepopulate_topics(["Viruses", "Obfuscation"])
    
    # mark viruses as read
    db.mark_topic_as_read("Viruses")
    
    # fetch read topics
    read_topics = db.get_read_topics()
    
    # should be read
    assert "Viruses" in read_topics
    
    # should not be read
    assert "Obfuscation" not in read_topics
    

# test marking quiz as passed for a topic
def test_mark_quiz_as_passed(db):
    
    # insert topic
    db.prepopulate_topics(["Obfuscation"])
    
    # mark quiz as passed
    db.mark_quiz_as_passed("Obfuscation")
    
    # fetch passed quizzes
    passed_quizzes = db.get_passed_quizzes()
    
    # should be marked as passed
    assert "Obfuscation" in passed_quizzes
    

# test retrieval of scan history
# most recent first
def test_get_scan_history(db):
    
    # add files in chronological order
    db.add_scanned_file("a.exe", "2023-12-12", "safe", "low")
    db.add_scanned_file("b.exe", "2024-01-01", "dangerous", "high")
    
    # should be sorted DESC by scan date
    history = db.get_scan_history()
    
    # there are exactly 2 records
    assert len(history) == 2
    
    # b.exe should come first
    assert history[0][1] == "b.exe"
    
    
# test getting file info and scan detail
def test_get_scan_details_and_info(db):
    
    # add scanned file to db and capture the id
    file_id = db.add_scanned_file("fileA.exe", "2024-03-01", "dangerous", "high")
    
    # add scan detailed to that file
    # id used for reference
    db.add_scan_detail(file_id, "Malicious", "signature")
    
    # get scan info for file
    scan_info = db.get_scanned_file_info(file_id)
    
    # get scan details for file 
    scan_details = db.get_scan_details(file_id)
    
    # check that file name matches
    assert scan_info[0] == "fileA.exe"
    
    # check that scan details match correct malicious pattern description
    assert scan_details[0][0] == "Malicious"
    
    
# test full signature match
# exact match
def test_add_and_check_full_signature_match(db):
    
    # known malware signature
    signature = {
        
        "signature_type": "MD5",
        "signature_value": "abcd1234abcd1234abcd1234abcd1234",
        "threat_level": "high"
    }
    
    # add malware signature to db
    db.add_malware_signatures([signature])
    
    # match exact file signature
    match = db.check_file_signature("abcd1234abcd1234abcd1234abcd1234")
    
    # if match is found in db for signature
    # should be found
    assert match is not None
    
    # check that threat level matches
    assert match[3] == "high"
    
    
# test partial signature match
# only first part of signature matches
def test_check_partial_signature_match(db):
    
    # known malware signature
    signature = {
        
        "signature_type": "SHA256",
        "signature_value": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "threat_level": "medium"
    }
    
    # add full signature to db
    db.add_malware_signatures([signature])
    
    # signature with only the first part matching and rest as random
    partial = db.check_file_signature("1234567890abcdefXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    
    # check if match found
    assert partial is not None
    
    
# test for no match when searching with an unknown signature
def test_check_signature_no_match(db):
    
    # fake malware signature
    signature = {
        
        "signature_type": "SHA1",
        "signature_value": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "threat_level": "low"
    }

    # add fake signature to db
    db.add_malware_signatures([signature])

    # give completely different signature
    result = db.check_file_signature("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    
    # check that no match is found
    assert result is None
    

# test that close method properly closes db connection
def test_close(db):
    
    # close db connection
    db.close()
    
    # assume any further interaction with closed db raises error
    with pytest.raises(sqlite3.ProgrammingError):
        
        # try to create a cursor on closed connection
        # expected to fail
        db.connection.cursor()