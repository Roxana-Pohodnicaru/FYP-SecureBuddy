import sys
import os
import pytest
import math
import tempfile
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from io import BytesIO


# add parent dir to system path
# so files from root dir can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# importing controller
from controller import Controller

# fixture to set up mock controller instance
@pytest.fixture
def controller():
    
    # create controller instance
    controller_instance = Controller()

    # mock db_manager as an object
    controller_instance.db_manager = MagicMock()

    # mock all db methods used in controller
    controller_instance.db_manager.add_scanned_file = MagicMock(return_value=123) 
    controller_instance.db_manager.add_scan_detail = MagicMock() 
    controller_instance.db_manager.get_scanned_file_info = MagicMock()
    controller_instance.db_manager.get_scan_details = MagicMock()
    controller_instance.db_manager.get_scan_history = MagicMock()
    controller_instance.db_manager.get_passed_quizzes = MagicMock()
    controller_instance.db_manager.get_read_topics = MagicMock()
    controller_instance.db_manager.mark_topic_as_read = MagicMock()
    controller_instance.db_manager.mark_quiz_as_passed = MagicMock()

    return controller_instance


# test process file and store result in db
def test_process_file(controller):
    
    # file path for testing file
    file_path = "testing_files/file.txt"
    
    # extract file name from path
    file_name = os.path.basename(file_path)
    
    # get current date and time in specific format
    scan_date = datetime.now().strftime('%d %m %Y %H:%M:%S')
    
    # expected result values for safe file
    status, risk_level, reason_for_flag, risk_category = "safe", "low", None, "N/A"
    
    # call method to process file
    scanned_file_id = controller.process_file(file_path)

    # verify that file was added to db with correct values
    controller.db_manager.add_scanned_file.assert_called_once_with(file_name, scan_date, status, risk_level)
    
    # verify that scan details were added with correct values
    controller.db_manager.add_scan_detail.assert_called_once_with(123, reason_for_flag="No issues detected", risk_category="N/A")
    
    # check that returned id matches expected return value
    assert scanned_file_id == 123
    
    
# test that correct results are being displayed
def test_show_scan_results_controller(controller):
    
    # example scanned file id
    scanned_file_id = 123
    
    # scanned file info
    scanned_file_info = {"file_name": "test_file.txt", "scan_date": "01-01-2025"}
    
    # scan details
    scan_details = {"status": "safe", "risk_level": "low", "reason_for_flag": "N/A"}
    
    # set mocked return values for db fetches
    controller.db_manager.get_scanned_file_info.return_value = scanned_file_info
    controller.db_manager.get_scan_details.return_value = scan_details
    
    # mock function to simulate GUI handler for displaying
    show_scan_results_mock = MagicMock()

    # call controller method
    controller.show_scan_results_controller(scanned_file_id, show_scan_results_mock)

    # check that scanned file info was fetched with correct id
    controller.db_manager.get_scanned_file_info.assert_called_once_with(scanned_file_id)

    # check that scan details was fetched with correct id
    controller.db_manager.get_scan_details.assert_called_once_with(scanned_file_id)
    
    # check that GUI display function was called with correct data
    show_scan_results_mock.assert_called_once_with(scanned_file_info, scan_details)
    

# test that correct data is being fetched for scan history
# check that dates are correctly formatted
def test_fetch_scan_history(controller):
    
    # mock scan results data for scan history
    # dates and times are not sorted
    scan_history_data = [
        
        (1, 'file1.txt', '01 01 2025 12:30:00'),
        (2, 'file2.txt', '02 02 2025 14:45:00'),
        (3, 'file3.txt', '03 03 2025 16:00:00'),
    ]
    
    # set mocked scan history return value
    controller.db_manager.get_scan_history.return_value = scan_history_data

    # call controller method
    result = controller.fetch_scan_history()

    # verify scan history was requested from db
    controller.db_manager.get_scan_history.assert_called_once()

    # expected results with correctly formatted dates and times
    expected_result = [
        
        (1, 'file1.txt', '2025-01-01 12:30:00'),
        (2, 'file2.txt', '2025-02-02 14:45:00'),
        (3, 'file3.txt', '2025-03-03 16:00:00'),
    ]

    # check that result matches expected output
    assert result == expected_result
    
    
# test that both scan details and file info are fetched correctly
# using file id
def test_get_scan_details_and_info(controller):
    
    # test scan id
    scan_id = 123
    
    # mock return values from db
    scan_details = {"status": "safe", "risk_level": "low", "reason_for_flag": "N/A"}
    scanned_file_info = {"file_name": "test_file.txt", "scan_date": "2025-01-01 12:30:00"}
    
    # set mocked return values
    controller.db_manager.get_scan_details.return_value = scan_details
    controller.db_manager.get_scanned_file_info.return_value = scanned_file_info

    # call controller method
    scanned_file_info_result, scan_details_result = controller.get_scan_details_and_info(scan_id)

    # check db methods were called with correct id
    controller.db_manager.get_scan_details.assert_called_once_with(scan_id)
    controller.db_manager.get_scanned_file_info.assert_called_once_with(scan_id)

    # check return values match expected mock data
    assert scanned_file_info_result == scanned_file_info
    assert scan_details_result == scan_details
    
    
# test if list of quizzes marked as passed is correctly fetched
def test_get_passed_quizzes(controller):
    
    # mock data for quizzes marked as passed
    passed_quizzes = [
        
        {"progress_id": 1, "topic_name": "Executables", "quiz_passed": 1},
        {"progress_id": 2, "topic_name": "File Spoofing", "quiz_passed": 1}
    ]

    # mock return value of db method
    controller.db_manager.get_passed_quizzes.return_value = passed_quizzes

    # call controller method
    result = controller.get_passed_quizzes()

    # check if method was called
    controller.db_manager.get_passed_quizzes.assert_called_once()

    # verify the result matches mocked return data
    assert result == passed_quizzes
    
    
# tests if list of topics marked as read is correctly fetched
def test_get_read_topics(controller):
    
    # mock data for topics marked as read
    read_topics = [
        
        {"progress_id": 1, "topic_name": "Executables", "read_completed": 1},
        {"progress_id": 2, "topic_name": "File Spoofing", "read_completed": 1}
        
    ]

    # mock return value of db method
    controller.db_manager.get_read_topics.return_value = read_topics

    # call controller method
    result = controller.get_read_topics()

    # check if method was called
    controller.db_manager.get_read_topics.assert_called_once()

    # verify the result matches mocked return data
    assert result == read_topics
    
    
# tests marking topic as read is correct
def test_mark_topic_as_read(controller):
    
    # sample topic
    topic_name = "Executables"
    
    # call controller method
    controller.mark_topic_as_read(topic_name)

    # check the db method is called with correct topic
    controller.db_manager.mark_topic_as_read.assert_called_once_with(topic_name)
    
    
# test marking a quiz as passed is correct
def test_mark_quiz_as_passed(controller):
    
    # sample topic
    topic_name = "Executables"
    
    # call controller method
    controller.mark_quiz_as_passed(topic_name)

    # check the db method is called with correct topic
    controller.db_manager.mark_quiz_as_passed.assert_called_once_with(topic_name)
    

# tests quiz scoring system works and incorrect questions are returned
def test_get_quiz_results(controller):
    
    # sample questions for quiz
    executables_questions = [
        
        {"question": "What are executables?", "options": [
            
            "Files that store personal data for users",
            "Files that contain instructions for a computer to perform specific tasks or run programs",
            "Files used only for temporary storage on a computer"
            
        ], "answer": 1},

        {"question": "Which of the following is a common executable file extension?", "options": [
            
            ".txt",
            ".exe",
            ".jpeg"
            
        ], "answer": 1},

        {"question": "Why are executables considered dangerous?", "options": [
            
            "They interact with the computer system and give attackers direct access",
            "They are always scanned and approved by antivirus software",
            "They do not require any permissions to execute"
            
        ], "answer": 0},

        {"question": "How do attackers disguise malicious executables?", "options": [
            
            "By embedding them in harmless image files",
            "By packaging them as seemingly safe executables",
            "By naming them after popular music files"
            
        ], "answer": 1},

        {"question": "Which of the following is NOT a way executables can be obtained?", "options": [
            
            "Through a phishing email attachment",
            "By downloading from official websites",
            "From auto-run executables on USB drives"
            
        ], "answer": 1}
    ]
    
    # simulate user answers with 1 wrong
    user_answers = [1, 1, 0, 1, 0]

    # call controller method
    score, incorrect_questions = controller.get_quiz_results(executables_questions, user_answers)

    # check score is correct
    assert score == 4
    
    # check 1 question incorrect
    assert len(incorrect_questions) == 1
    
    # check incorrect question is returned correctly
    assert incorrect_questions[0] == {
        
        "question": "Which of the following is NOT a way executables can be obtained?",
        "correct_answer": "By downloading from official websites",
        "user_answer": "Through a phishing email attachment"
        
    }


# test if files with multiple extensions are flagged as spoofed
def test_double_extension_checker(controller):

    # case 1 - single file extension - valid
    file1 = "file.txt"
    
    # call controller method
    result1 = controller.double_extension_checker(file1)
    
    # check that no issue is detected for valid file
    assert result1 is None, f"Expected None for file '{file1}', but got {result1}"

    # case 2 - double file extension - flagged
    file2 = "file.txt.exe"
    
    # call controller method
    result2 = controller.double_extension_checker(file2)
    
    # check that spoofing is detected with correct result
    assert result2 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File contains double extensions or more, indicating file spoofing",
        "risk_category": "File Spoofing"
        
    }, f"Expected 'dangerous' flag for file '{file2}', but got {result2}"

    # case 3 - multiple extensions - flagged
    file3 = "document.pdf.rar.zip"
    
    # call controller method
    result3 = controller.double_extension_checker(file3)
    
     # check that spoofing is detected with correct result
    assert result3 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File contains double extensions or more, indicating file spoofing",
        "risk_category": "File Spoofing"
        
    }, f"Expected 'dangerous' flag for file '{file3}', but got {result3}"


    # case 5 - compressed file with multiple parts - valid
    file4 = "archive.tar.gz"
    
    # call controller method
    result4 = controller.double_extension_checker(file4)
    
    # check that no issue is detected for valid file
    assert result4 is None, f"Expected None for file '{file4}', but got {result4}"
    

# tests if known executable extensions are correctly flagged
def test_executable_file_checker(controller):

    # case 1 - .exe file - flagged
    file1 = "file.exe"
    
    # call controller method
    result1 = controller.executable_file_checker(file1)
    
    # check its flagged as dangerous
    assert result1 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File has an executable extension, indicating possible malware program",
        "risk_category": "Executables"
        
    }, f"Expected dangerous flag for file '{file1}', but got {result1}"

    # case 2 - .sh file - flagged
    file2 = "script.sh"
    
    # call controller method
    result2 = controller.executable_file_checker(file2)
    
    # check its flagged as dangerous
    assert result2 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File has an executable extension, indicating possible malware program",
        "risk_category": "Executables"
        
    }, f"Expected dangerous flag for file '{file2}', but got {result2}"

    # case 3 - .py file - flagged
    file3 = "script.py"
    
    # call controller method
    result3 = controller.executable_file_checker(file3)
    
    # check its flagged as dangerous
    assert result3 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File has an executable extension, indicating possible malware program",
        "risk_category": "Executables"
        
    }, f"Expected dangerous flag for file '{file3}', but got {result3}"

    # case 4 - .txt file - valid
    file4 = "file.txt"
    
    # call controller method
    result4 = controller.executable_file_checker(file4)
    
    # check not flagged
    assert result4 is None, f"Expected None for file '{file4}', but got {result4}"

    # case 5 - .jpg file - valid
    file5 = "image.jpg"
    
    # call controller method
    result5 = controller.executable_file_checker(file5)
    
    # check not flagged
    assert result5 is None, f"Expected None for file '{file5}', but got {result5}"

    # case 6 - .exe file uppercase - flagged
    file6 = "file.EXE"
    
    # call controller method
    result6 = controller.executable_file_checker(file6)
    
    # check its flagged as dangerous
    assert result6 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File has an executable extension, indicating possible malware program",
        "risk_category": "Executables"
        
    }, f"Expected dangerous flag for file '{file6}', but got {result6}"

    # case 7 - no extension - valid
    file7 = "no_extension"
    
    # call controller method
    result7 = controller.executable_file_checker(file7)
    
    # check not flagged
    assert result7 is None, f"Expected None for file '{file7}', but got {result7}"

    # case 8 - .py file mixed case - flagged
    file8 = "script.Py"
    
    # call controller method
    result8 = controller.executable_file_checker(file8)
    
    assert result8 == {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "File has an executable extension, indicating possible malware program",
        "risk_category": "Executables"
        
    }, f"Expected dangerous flag for file '{file8}', but got {result8}"


# tests if office file extension correctly triggers macro analysis
def test_office_file_checker(controller):

    # case 1 - .docx file - macro analysis called
    file1 = "document.docx"
    
    # maock macro analysis function to return result
    with patch.object(controller, 'analyse_macro', return_value="Mocked Result") as mock_analyse_macro:
        
        # call controller method
        result1 = controller.office_file_checker(file1)
        
        # check result matches mocked return value
        assert result1 == "Mocked Result", f"Expected 'Mocked Result' for file '{file1}', but got {result1}"
        
    # case 2 - .xlsx file - macro analysis called
    file2 = "spreadsheet.xlsx"
    
    # mock macro analysis for excel file
    with patch.object(controller, 'analyse_macro', return_value="Mocked Result") as mock_analyse_macro:
        
        # call controller method
        result2 = controller.office_file_checker(file2)
        
        # check result matches mocked return value
        assert result2 == "Mocked Result", f"Expected 'Mocked Result' for file '{file2}', but got {result2}"

    # case 3 - .pptx file - macro analysis called
    file3 = "presentation.pptx"
    
    # mock macro analysis for powerpoint file
    with patch.object(controller, 'analyse_macro', return_value="Mocked Result") as mock_analyse_macro:
        
        # call controller method
        result3 = controller.office_file_checker(file3)
        
        # check result matches mocked return value
        assert result3 == "Mocked Result", f"Expected 'Mocked Result' for file '{file3}', but got {result3}"

    # case 4 - non microsoft file - macro analysis not called
    file4 = "file.txt"
    
    # call controller method
    result4 = controller.office_file_checker(file4)
    
    # check that macro analysis was not called
    assert result4 is None, f"Expected None for file '{file4}', but got {result4}"

    # case 5 - .jpg file - macro analysis not called
    file5 = "image.jpg"
    
    # call controller method
    result5 = controller.office_file_checker(file5)
    
    # check that macro analysis was not called
    assert result5 is None, f"Expected None for file '{file5}', but got {result5}"

    # case 6 - .docx mixed case - macro analysis called
    file6 = "document.DoCx"
    
    # mock macro analysis for doc file
    with patch.object(controller, 'analyse_macro', return_value="Mocked Result") as mock_analyse_macro:
        
        # call controller method
        result6 = controller.office_file_checker(file6)
        
        # check result matches mocked return value
        assert result6 == "Mocked Result", f"Expected 'Mocked Result' for file '{file6}', but got {result6}"

    # case 7 - file with no extension - macro analysis not called
    file7 = "file_without_extension"
    
    # call controller method
    result7 = controller.office_file_checker(file7)
    
    # check that macro analysis was not called
    assert result7 is None, f"Expected None for file '{file7}', but got {result7}"


# tests if controller properly analyses malicious macros in office documents
def test_analyse_macro(controller):
    
    # case 1 - document file with macro
    file1 = "macro.docm"

    # call controller method
    result1 = controller.analyse_macro(file1)

    # expected result with flagged details
    expected_result = {
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "Macros contain suspicious command: Shell.",
        "risk_category": "Macros"
    }

    # check that anaylsis returned correct flagged result
    assert result1 == expected_result, f"Expected result for file '{file1}', but got {result1}"

    # case 2 - document file with no macro
    file2 = "test_safe.docx"

    # call controller method
    result2 = controller.analyse_macro(file2)

    # check that result is None as expected
    assert result2 is None, f"Expected None for file '{file2}', but got {result2}"
    

# tests that controller flags zip bombs based on decompression size and compression ratio
def test_detect_zip_bombs(controller):
    
    # mock zip info with extreme and normal value
    mock_zip_info_list = [
        
        # extreme compression ratio
        MagicMock(file_size=1_000_000_000, compress_size=1_000),
        
        # normal compression ratio
        MagicMock(file_size=1_000_000, compress_size=500),
    ]

    # simulate behaviour of opening a zip file
    with patch("zipfile.ZipFile") as mock_zip:
        
        # when zip file is opened
        # return list of file info
        mock_zip.return_value.__enter__.return_value.infolist.return_value = mock_zip_info_list

        # call controller method
        result = controller.detect_zip_bombs("mock_file.zip")
        
        # check that file is flagged due to extreme compression size
        assert result["status"] == "dangerous"
        assert "Decompressed size" in result["reason_for_flag"]

        # mock large decompressed file 2GB with a more normal compression size
        mock_zip_info_list[0].file_size = 2 * 10**9 
        
        # set compressed size to 1MB
        mock_zip_info_list[0].compress_size = 1_000_000

        # call controller method
        result = controller.detect_zip_bombs("mock_file.zip")
        
        # check file marked as dangerous
        assert result["status"] == "dangerous"
        assert "Decompressed size" in result["reason_for_flag"]

        # mock file with normal decompressed size 1MB but extreme compression ratio
        mock_zip_info_list[0].file_size = 1_000_000
        
        # 1KB compressed size
        mock_zip_info_list[0].compress_size = 1_000

        # call controller method
        result = controller.detect_zip_bombs("mock_file.zip")
        
        # check file marked as dangerous due to suspicious compression ratio
        assert result["status"] == "dangerous"
        assert "Compression ratio" in result["reason_for_flag"]

        # mock file with normal decompressed size 1MB and normal compression ratio
        mock_zip_info_list[0].file_size = 1_000_000
        
        # 500KB compressed size
        mock_zip_info_list[0].compress_size = 500_000

        # call controller method
        result = controller.detect_zip_bombs("mock_file.zip")
        
        # check that file is not flagged
        assert result is None
        
        
# tests if function correctly identifies zip and non zip files
def test_is_zip_file(controller):
    
    # mock file with .zip extension
    zip_file = "test_file.zip"
    
    # mock detect_zip_bombs method to track if its being called if file is zip
    controller.detect_zip_bombs = MagicMock()
    
    # call controller method
    controller.is_zip_file(zip_file)
    
    # check if detect_zip_bombs was called - file is correctly identified as zip
    controller.detect_zip_bombs.assert_called_once_with(zip_file)
    
    # mock non zip file
    non_zip_file = "test_file.txt"
    
    # call controller method and check it does not trigger anything
    assert controller.is_zip_file(non_zip_file) is None
    

# tests that scan_file stops on the first detected issue
# calls all checkers if no issues are found
def test_scan_file(controller):

    # mock all checker methods to return None - safe file
    controller.double_extension_checker = MagicMock(return_value=None)
    controller.executable_file_checker = MagicMock(return_value=None)
    controller.office_file_checker = MagicMock(return_value=None)
    controller.is_zip_file = MagicMock(return_value=None)
    controller.credential_stealer_checker = MagicMock(return_value=None)
    controller.remote_access_tool_checker = MagicMock(return_value=None)
    controller.file_header_signature_checker = MagicMock(return_value=None)
    controller.detect_obfuscated_entropy = MagicMock(return_value=None)


    # case 1 - simulate file flagged by double extension checker
    controller.double_extension_checker = MagicMock(return_value={
        
        "status": "dangerous",
        "risk_level": "high",
        "reason_for_flag": "Suspicious double extension",
        "risk_category": "File Extensions"
    })
    
    # call controller method
    result = controller.scan_file("mock_file.exe")
    
    # check file is flagged for double extension
    assert result == ("dangerous", "high", "Suspicious double extension", "File Extensions")
    
    # check that scan stops since first one flagged an issue
    controller.executable_file_checker.assert_not_called()

    # case 2 - safe file with no flags
    controller.double_extension_checker = MagicMock(return_value=None)
    controller.executable_file_checker = MagicMock(return_value=None)
    controller.office_file_checker = MagicMock(return_value=None)
    
    # call controller method
    result = controller.scan_file("mock_file.txt")
    
    # check file is not flagged as expected
    assert result == ("safe", "low", None, None)
    
    # check that each checker was called exactly once
    controller.double_extension_checker.assert_called_once()
    controller.executable_file_checker.assert_called_once()
    controller.office_file_checker.assert_called_once()
    controller.is_zip_file.assert_called_once()
    controller.credential_stealer_checker.assert_called_once()
    controller.remote_access_tool_checker.assert_called_once()
    controller.file_header_signature_checker.assert_called_once()
    controller.detect_obfuscated_entropy.assert_called_once()
    
    
# tests if checker correctly identifies credential stealing keywords
def test_credential_stealer_checker(controller):
  
    # mock binary content with credential keyword
    mock_file_content = b"SetWindowsHookEx"
    
    # simulate opening file and reading content
    with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
        
        # call controller method
        result = controller.credential_stealer_checker("mock_file.txt")
        
        #  check that a threat was detected and marked as dangerous
        assert result is not None
        assert result["status"] == "dangerous"
        assert "SetWindowsHookEx" in result["reason_for_flag"]


# tests if checker correctly identifies remote access tool keywords
def test_remote_access_tool_checker(controller):
    
    # case 1 - single RAT keyword in file
    mock_file_content = b"RemoteAccess"
    
    # simulate opening file and reading content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        
        # call controller method
        result = controller.remote_access_tool_checker("mock_file.txt")
        
        # check that file is flagged as dangerous
        assert result["status"] == "dangerous"
        assert result["risk_category"] == "Remote Access Control"
        assert "RemoteAccess" in result["reason_for_flag"]

    # case 2 - multiple RAT keywords
    mock_file_content = b"netcat, ReverseShell."
    
    # simulate opening file and reading content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        
        # call controller method
        result = controller.remote_access_tool_checker("mock_file.txt")
        
        # check that file is flagged dangerous
        assert result["status"] == "dangerous"
        assert result["risk_category"] == "Remote Access Control"
        
        # check that keywords appeared in reason for flagging
        assert any(keyword in result["reason_for_flag"] for keyword in ["netcat", "ReverseShell"])

    # case 3 - no RAT keywords
    mock_file_content = b"no suspicious keywords"
    
    # simulate opening file and reading content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        
        # call controller method
        result = controller.remote_access_tool_checker("mock_file.txt")
        
        # check that file is not flagged
        assert result is None


# tests to ensure it correctly reads and returns file signature bytes
def test_extract_file_signature(controller):
    
    # case 1 - PNG file with valid header
    # mock PNG file
    mock_file_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    
    # extract first 16 bytes and convert to hex string for expected result
    expected_signature = mock_file_content[:16].hex()
    
    # simulate opening file that returns mocked binary content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        
        # call controller method
        result = controller.extract_file_signature("mock_file.txt")
        
        # check that result matches expected hex signature
        assert result == expected_signature, f"Expected signature '{expected_signature}', but got '{result}'."


    # case 2 - file with smaller signature
    mock_file_content = b"\x89PNG"
    
    # get expected hex of mock file
    expected_signature = mock_file_content.hex()
    
    # simulate opening file that returns mocked binary content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        
        # call controller method
        result = controller.extract_file_signature("mock_file.txt", num_bytes=16)
        
        # check that result matches expected hex signature
        assert result == expected_signature, f"Expected signature '{expected_signature}', but got '{result}'."

    # case 3 - empty file
    mock_file_content = b""
    
    # simulate opening file that returns mocked binary content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        
        # call controller method
        result = controller.extract_file_signature("mock_file.txt", num_bytes=16)
        
        # check that result is empty as expected
        assert result == "", "Expected an empty string for an empty file, but got something else."
        

# tests to ensure function correctly detects known malware file headers
def test_file_header_signature_checker(controller):
    
    # mock signature checker and signature extractor
    with (
    
        patch.object(controller.db_manager, 'check_file_signature') as mock_db_check,
        patch.object(controller, 'extract_file_signature') as mock_extract_signature
    ):

        # case 1 - known malware file header
        mock_extract_signature.return_value = "d41d8cd98f00b204e9800998ecf8427e"
        
        # simulate db match
        mock_db_check.return_value = True
        
        # call controller method
        result = controller.file_header_signature_checker("malicious_file.exe")
        
        # check that file has been flagged and marked as dangerous
        assert result is not None
        assert result["status"] == "dangerous"
        assert result["risk_level"] == "high"
        assert "File header matches known malware signature" in result["reason_for_flag"]
        assert result["risk_category"] == "Virus"


        # case 2 - safe file
        # no match found
        result = controller.file_header_signature_checker("safe_file.exe")
        
        # check file has not been flagged
        assert result is None


# tests entropy calculation is correct
def test_calculate_entropy(controller):
    
    # low entropy
    data = bytearray([0, 0, 0, 255, 255, 255])
    
    # manually calculate entropy for above data
    expected_entropy = -(3/6 * math.log(3/6, 2) + 3/6 * math.log(3/6, 2))

    # call controller method
    result = controller.calculate_entropy(data)

    # verify that result is close to expected value
    # using floating point comparison
    assert math.isclose(result, expected_entropy, rel_tol=1e-9), f"Expected entropy: {expected_entropy}, but got: {result}"

    # high entropy
    data_high_entropy = bytearray(range(256))
    
    # expected entropy for uniform distribution of 256 values
    expected_entropy_high = 8.0
    
    # call controller method
    result_high = controller.calculate_entropy(data_high_entropy)

    # check that calculated result is close to 8.0
    assert math.isclose(result_high, expected_entropy_high, rel_tol=1e-9), f"Expected high entropy: {expected_entropy_high}, but got: {result_high}"


# tests if function correctly flags high entropy files
def test_detect_obfuscated_entropy(controller):
    
    # temp file with low entropy
    low_entropy_file = tempfile.NamedTemporaryFile(delete=False)
    
    # get file path of temp file
    low_entropy_file_path = low_entropy_file.name
    
    # file contains 1000 'A' chars to simulate low entropy
    low_entropy_file.write(b"A" * 1000)
    
    # close file
    low_entropy_file.close()

    # call controller method
    result = controller.detect_obfuscated_entropy(low_entropy_file_path)
    
    # check that file was not flagged
    assert result is None
    
    # remove file
    os.remove(low_entropy_file_path)

    # temp file with high entropy file
    high_entropy_file = tempfile.NamedTemporaryFile(delete=False)
    
    # get file path
    high_entropy_file_path = high_entropy_file.name
    
    # write byte values 0-255 to simulate random data
    high_entropy_file.write(bytes([i for i in range(256)]))
    
    # close file
    high_entropy_file.close()

    # call controller method
    result = controller.detect_obfuscated_entropy(high_entropy_file_path)
    
    # file should be flagged
    assert result is not None
    assert result["status"] == "dangerous"
    assert result["risk_level"] == "high"
    assert "obfuscation" in result["reason_for_flag"].lower()
    
    # remove file
    os.remove(high_entropy_file_path)

    # empty temp file
    empty_file = tempfile.NamedTemporaryFile(delete=False)
    
    # get file path
    empty_file_path = empty_file.name
    
    # close file
    empty_file.close()

    # call controller method
    result = controller.detect_obfuscated_entropy(empty_file_path)
    
    # check that file is not flagged
    assert result is None
    
    # remove file
    os.remove(empty_file_path)

    # temp file with entropy at threshold
    boundary_file = tempfile.NamedTemporaryFile(delete=False)
    
    # get file path
    boundary_file_path = boundary_file.name
    
    # file with 255 unique bytes
    boundary_file.write(bytes([i for i in range(255)]))
    
    # close file
    boundary_file.close()

    # set threshold to 7.5 for testing
    # call controller method
    result = controller.detect_obfuscated_entropy(boundary_file_path, threshold=7.5)

    # check file is flagged and marked dangerous
    # entropy is slightly high
    assert result is not None
    assert result["status"] == "dangerous"
    assert result["risk_level"] == "high"
    assert "obfuscation" in result["reason_for_flag"].lower()
    
    # remove file
    os.remove(boundary_file_path)
    

# tests to correctly detect EICAR test files
def test_detect_eicar_test_file(controller):
    
    # EICAR antivirus test signature in binary
    eicar_signature = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    
    # simulate opening file containing EICAR test signature
    with patch("builtins.open", mock_open(read_data=eicar_signature)):
        
        # call controller method
        result = controller.detect_eicar_test_file("mock_eicar_file.txt")
        
        # check that file was flagged
        assert result is not None
        assert result["status"] == "detected"
        assert result["risk_level"] == "low"
        assert "EICAR test file detected" in result["reason_for_flag"]

    # file with no EICAR signature
    with patch("builtins.open", mock_open(read_data=b"Random content that is not EICAR signature.")):
        
        # call controller method
        result = controller.detect_eicar_test_file("mock_non_eicar_file.txt")
        
        # check file not flagged
        assert result is None


# test that controller properly closes db connectio
def test_close(controller):
    
    # replace db_manager with mock
    controller.db_manager = MagicMock()
    
    # call controller method
    controller.close()
    
    # check that db connection was closed exactly once
    controller.db_manager.close.assert_called_once()