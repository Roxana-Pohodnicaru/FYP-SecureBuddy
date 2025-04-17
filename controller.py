import os
import zipfile
import re
import math
from datetime import datetime
from database import DatabaseManager
from oletools.olevba import VBA_Parser


class Controller:
    
    # initialize class
    def __init__(self):
        
        # initialize with instance of database manager
        self.db_manager = DatabaseManager()


    # process the file
    # extract metadata and save to db
    def process_file(self, file_path):
        
        # extract metadata
        # get file name from file path
        file_name = os.path.basename(file_path)
        
        # get current time and date
        scan_date = datetime.now().strftime('%d %m %Y %H:%M:%S')
        
        # scan file to determine its status, risk level, reason, and category
        status, risk_level, reason_for_flag, risk_category = self.scan_file(file_path)
        
        # save metadata to db
        scanned_file_id = self.db_manager.add_scanned_file(
            
            file_name, scan_date, status, risk_level
        )

        # logging
        print(f"Scanned file ID returned: {scanned_file_id}")

        # save scan details to db
        self.db_manager.add_scan_detail(
            
            scanned_file_id,
            
            reason_for_flag=reason_for_flag or "No issues detected", 
            
            risk_category=risk_category or "N/A"
        )
        
        # logging
        print(f"File '{file_name}' processed successfully with ID: {scanned_file_id}")

        # return scanned file id
        return scanned_file_id


    # fetch scan results and pass them to gui
    def show_scan_results_controller(self, scanned_file_id, show_scan_results):
    
        # fetch scan data from db using scanned file id
        scanned_file_info = self.db_manager.get_scanned_file_info(scanned_file_id)
        scan_details = self.db_manager.get_scan_details(scanned_file_id)

        # pass data to gui for rendering
        show_scan_results(scanned_file_info, scan_details)


    # fetch scan history from db and reformat dates
    def fetch_scan_history(self):
        
        # fetch scan history from db
        scan_history = self.db_manager.get_scan_history()

        # convert scan date to YYYY-MM-DD HH:MM:SS
        for i in range(len(scan_history)):
            
            # extract values from scan history tuple
            scan_id, file_name, scan_date = scan_history[i]
        
            # convert date from DD MM YYYY HH:MM:SS to YYYY-MM-DD HH:MM:SS
            formatted_date = datetime.strptime(scan_date, '%d %m %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            
            # update scan history with formatted date
            scan_history[i] = (scan_id, file_name, formatted_date)

        # return updated scan history with formatted dates
        return scan_history
    
    
    # fetches both scan fetails and scanned file info for given scan ID
    def get_scan_details_and_info(self, scan_id):
    
        # fetch scan data from db for given scan ID
        scan_details = self.db_manager.get_scan_details(scan_id)
        scanned_file_info = self.db_manager.get_scanned_file_info(scan_id)
        
        # return scan data
        return scanned_file_info, scan_details
    
    
    # fetches list of quizzes marked as passed from db
    def get_passed_quizzes(self):
        
        # gets passed quizzes
        return self.db_manager.get_passed_quizzes()
    
    
    # fetches list of topics marked as read from the db
    def get_read_topics(self):

        # fetches read topics
        return self.db_manager.get_read_topics()
    
    
    # marks specific topic as read in db
    def mark_topic_as_read(self, topic_name):
        
        # mark topic as read
        self.db_manager.mark_topic_as_read(topic_name)
        
        
    # marks a specific quiz as passed in db
    def mark_quiz_as_passed(self, topic_name):
        
        # mark quiz topic as passed
        self.db_manager.mark_quiz_as_passed(topic_name)

    
    # calculates user score on quiz
    # tracks incorrect answers
    def get_quiz_results(self, questions, user_answers):
        
        # set score to 0
        score = 0
        
        # list for incorrect questions
        incorrect_questions = []
        
        # loop through user answers to check against correct answers
        for i, user_answer in enumerate(user_answers):
            
            # get correct answer for current question
            correct_answer = questions[i]["answer"]
            
            # check if user answer matches correct answer
            if user_answer == correct_answer:
                
                # increment score
                score += 1
                
            # if user answer is incorrect
            # add question details to incorrect answer list
            else:
                
                incorrect_questions.append({
                    
                    # question text
                    "question": questions[i]["question"],
                    
                    # the correct answer option
                    "correct_answer": questions[i]["options"][correct_answer],
                    
                    #  user selected answer
                    # or no answer if user did not select an option
                    "user_answer": questions[i]["options"][user_answer] if user_answer != -1 else "No answer selected"
                    
                })
                
        # return score and list of incorrect questions
        return score, incorrect_questions


    # method to check for double extensions in the file name
    # checking file spoofing vulnerability
    def double_extension_checker(self, file_path):
        
        # get file name from file path
        file_name = os.path.basename(file_path)
        
        # split file name into parts seperated by dots
        parts = file_name.split('.')

        # if there are more than 2 parts
        # means that there is an extra extension
        if len(parts) > 2:
            
            # get actual extension
            primary_extension = parts[-1].lower()
            
            # get extension before it
            spoofed_extension = parts[-2].lower() 

            # list of file extensions
            file_extensions = [
                
                # document extensions
                'doc', 'docx', 'pdf', 'txt', 'rtf', 'odt', 'ppt', 'pptx', 'xls', 'xlsx', 'csv',
                
                # image extensions
                'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'ico',
                
                # audio extensions
                'mp3', 'wav', 'aac', 'flac', 'ogg', 'wma', 'm4a',
                
                # video extensions
                'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mpeg',
                
                # compressed extensions
                'zip', 'rar', 'tar', 'gz', '7z', 'bz2', 'xz'
                
                ]
            
            # define list of valid multi extensions 
            # should not be flagged dangerous by this function
            valid_multi_extensions = ['tar.gz', 'tar.xz', 'zip.gz']
            
            # check if current file has valid multi extension
            if '.'.join(parts[-2:]).lower() in valid_multi_extensions:
                
                # valid multi extension
                # not marked as issue by this function
                return None
        
            
            # check if spoofed extension matches file types
            if spoofed_extension in file_extensions:
                
                # file marked as unsafe
                # store result in db
                return {
                    
                    "status": "dangerous",
                    "risk_level": "high",
                    "reason_for_flag": "File contains double extensions or more, indicating file spoofing",
                    "risk_category": "File Spoofing"
                }

        # if no double extension found, return None
        return None


    # method to check if file is an executable
    def executable_file_checker(self, file_path):
        
        # get file extension from path
        file_name = os.path.basename(file_path).strip()
        
        # split file name into name and extension
        _, file_extension = os.path.splitext(file_name)
        
        # gets the last item of filepath and converts to lowercase
        file_extension = file_extension.lower()

        # list of executable file extensions
        executable_extensions = [
            
            '.exe', '.bat', '.cmd', '.sh', '.bin', '.run', '.py', '.pl', '.php', '.rb', '.jar', '.apk', '.com', '.msi', '.vbs', '.wsf', '.gadget'
        ]

        # check if file matches executable extensions
        if file_extension in executable_extensions:
            
            # file marked as unsafe
            # store in db
            return {
                
                "status": "dangerous",
                "risk_level": "high",
                "reason_for_flag": f"File has an executable extension, indicating possible malware program",
                "risk_category": "Executables"
            }

        # if no executable extension, return None
        return None


    # method to check if file type is of microsoft office type (doc, xml etc)
    def office_file_checker(self, file_path):
        
        # get file extension from path 
        file_name = os.path.basename(file_path).strip()
        
        # split file name into name and extension
        _, file_extension = os.path.splitext(file_name)
        
        # convert file extension to lowercase
        file_extension = file_extension.lower()
        
        # logging
        print(f"Processing file: {file_name}, Extension: {file_extension}")
        
        # list of file extensions for microsoft office files
        office_extensions = [
            
            '.doc', '.docm', '.docx', '.dot', '.odt', '.pdf', '.xml', '.xps', '.csv', '.dbf', '.ods', '.xla', '.xlam', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xlw', '.xml', '.xps', '.potm', '.potx', '.ppa', '.ppam', '.ppsx', '.ppt', '.pptm', '.pptx', '.xps' 
            
        ]
        
        # check if file extension is in office list
        if file_extension in office_extensions:
            
            # if true calls analyse macro function to check for macros
            return self.analyse_macro(file_path)
        
        
    # method to analyse a file for malicious macros
    def analyse_macro(self, file_path):
        
        try:
            # initialise VBA parser
            vba_parser = VBA_Parser(file_path)
            
            # list of suspicious keywords used in malicious macros
            suspicious_content = [
                
                        # common malicious script commands
                        "Shell", "CreateObject", "Execute", "Run", "Open", "Close", "Kill", "Terminate", "Delete", "Format", "WScript.Shell", "AppActivate", "Application.Run", "AutoOpen", "AutoClose", "Document_Open", "Workbook_Open", "Workbook_BeforeClose",

                        # file manipulation
                        # system commmands
                        "FileSystemObject", "Write", "Read", "CopyFile", "DeleteFile", "MoveFile", "GetSpecialFolder", "CreateFolder", "DeleteFolder",

                        # network commands
                        "XMLHTTP", "WinHttpRequest", "Send", "Post", "Get", "UploadFile", "DownloadFile", "ADODB.Stream",

                        # process commands
                        "ShellExecute", "CreateProcess", "WinExec", "LoadLibrary", "GetProcAddress", "VirtualAlloc", "VirtualProtect",

                        # registry manipulation commands
                        "RegWrite", "RegRead", "RegDelete", "HKLM", "HKCU", "HKEY_LOCAL_MACHINE", "HKEY_CURRENT_USER",

                        # powershell commands
                        "PowerShell", "Invoke-Expression", "Set-ExecutionPolicy", "Bypass", "Start-Process", "Invoke-WebRequest",
                        
                        # windows management instrumentation commands
                        "WMIService", "ExecQuery", "Win32_Process", "GetObject", "ExecMethod", "SpawnInstance",

                        # encoding 
                        # obfuscation
                        "Base64Decode", "Base64Encode", "Chr", "ChrW", "StrReverse", "Xor", "Hex", "Randomize", "Eval",

                        # file paths
                        # environment variables
                        "C:\\Windows", "C:\\System32", "%TEMP%", "%APPDATA%", "%PROGRAMDATA%", "%USERPROFILE%", "%SYSTEMROOT%",

                        # exploits
                        "HeapAlloc", "HeapFree", "ROP", "BufferOverflow", "UseAfterFree", "FormatString"
                        
            ]
            
            # check if file contains VBA macros
            if vba_parser.detect_vba_macros():
                
                # extract macros from file
                for macro_tuple in vba_parser.extract_macros():
                    
                    # logging
                    print(f"Extracted Macro Tuple: {macro_tuple}")
                
                    # iterate through each element in macro tuple
                    for element in macro_tuple:
                        
                        # skip non string elements
                        if not isinstance(element, str):
                            
                            continue
                    
                        # check each element if it contains any malicious commands
                        for keyword in suspicious_content:
                            
                            # case insensitive search
                            if keyword.lower() in element.lower():
                                
                                # suspicious keyword found
                                # file marked as unsafe
                                # store in db
                                return {
                                    
                                    "status": "dangerous",
                                    "risk_level": "high",
                                    "reason_for_flag": f"Macros contain suspicious command: {keyword}",
                                    "risk_category": "Macros"
                                    
                                }                    
        # catch error
        except Exception as e:
            
            # logging
            print(f"Error: {e}")
           
        
    # method to detect zip bombs based on file size and compression ratio
    def detect_zip_bombs(self, file_path, compression_ratio_threshold=1000, max_decompressed_size=10**9):
        
        try:
            
            # open zip file in read mode
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                
                # calculate total size of all compressed files inside zip
                total_compressed_size = sum(file.compress_size for file in zip_file.infolist())
                
                # calculate total size of all files after decompression
                total_decompressed_size = sum(file.file_size for file in zip_file.infolist())

                # if compressed size is greater than 0
                if total_compressed_size > 0:
                    
                    # compute compression ratio
                    compression_ratio = total_decompressed_size / total_compressed_size
                
                # compression size is 0
                else:
                    # avoid divison by 0
                    # set ratio to 0
                    compression_ratio = 0
                    
                # check if total decompressed size exceeds limit
                if total_decompressed_size > max_decompressed_size:
                    
                    # mark file unsafe
                    # store in db
                    return {
                        
                        "status": "dangerous",
                        "reason_for_flag": f"Decompressed size ({total_decompressed_size} bytes) exceeds limit",
                        "risk_category": "Compressed Files"
                    }

                # check if compression ratio exceeds threshold
                if compression_ratio > compression_ratio_threshold:
                    
                    # mark file unsafe
                    # store in db
                    return {
                        
                        "status": "dangerous",
                        "reason_for_flag": f"Compression ratio ({compression_ratio}) exceeds safe threshold",
                        "risk_category": "Compressed Files"
                    }

        # catch error
        except Exception as e:
            
            # logging
            print(f"Error: {e}")

        
    # method to check if file is ZIP to analyze for ZIP bombs
    def is_zip_file(self, file_path):
        
        # get file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # check if file is ZIP
        if file_extension == ".zip":
            
            # call detect_zip_bombs
            self.detect_zip_bombs(file_path)


    # method to check file for vulnerabilities
    # calls all other methods which scans files
    def scan_file(self, file_path):

        # logging
        print(f"Scanning file: {file_path}")
        
        # default values
        # assume safe file initially
        status, risk_level = "safe", "low"
        reason_for_flag, risk_category = None, None


        # file checkers
        checkers = [
            
            self.double_extension_checker,
            
            self.executable_file_checker,
            
            self.office_file_checker,
            
            self.is_zip_file,
            
            self.credential_stealer_checker,
            
            self.remote_access_tool_checker,
            
            self.file_header_signature_checker,
            
            self.detect_obfuscated_entropy
            
        ]

        # iterate through checkers
        for checker in checkers:
            
            # call checker method with file path
            result = checker(file_path)
            
            # if checker finds an issue
            # update with results
            if result:
               
                status = result["status"]
                
                risk_level = result["risk_level"]
                
                reason_for_flag = result["reason_for_flag"]
                
                risk_category = result["risk_category"]
                
                # if issue is found
                # no need to check further
                break

        # return results
        return status, risk_level, reason_for_flag, risk_category


    # method to process signature files and add them to db
    def process_signature_files(self, base_dir="malicious_file_signatures", batch_size=1000):
        
        # iterate through each folder
        for folder in ["MD5", "SHA1", "SHA256"]:
            
            # construct full path for current folder by combining base dir and folder name
            folder_path = os.path.join(base_dir, folder)
            
            # using folder name as signature type
            signature_type = folder

            # iterate through each file in current folder
            for file_name in os.listdir(folder_path):
                
                # construct full path for current file by combining folder path and file name
                file_path = os.path.join(folder_path, file_name)
                
                # logging file currently being processed
                print(f"Processing file: {file_path}")

                # buffer for batch inserts
                batch = []
                
                # open current file for reading
                with open(file_path, "r") as file:
                    
                    # read file line by line
                    for line in file:
                        
                        # remove any whitespace
                        signature_value = line.strip()
                        
                        # add info to batch
                        batch.append(
                            {
                                "signature_type": signature_type,
                                "signature_value": signature_value,
                                "threat_level": "high",
                            }
                        )
                        
                        # if batch size is reached
                        if len(batch) >= batch_size:
                            
                            # insert into db
                            self.db_manager.add_malware_signatures(batch)
                            
                            # clear batch
                            batch = []

                # insert remaining signatures in last batch
                if batch:
                    
                    self.db_manager.add_malware_signatures(batch)


    # method to detect spyware such as keyloggers or credential stealers
    # checks for keywords with input capture, credential storage, data exfiltration (email, URLs), packet sniffing, registry manipulation
    def credential_stealer_checker(self, file_path):
        
        suspicious_keywords = [
            
            # keyloggers and input captures
            "SetWindowsHookEx", "GetAsyncKeyState", "GetKeyState", "SendInput", "GetForegroundWindow", "GetWindowText", "Clipboard.GetText",
            
            # credentials storage
            "NetUserEnum", "NetUserGetInfo", "CredentialCache.DefaultNetworkCredentials", "PasswordVault", "CredentialManager",
            
            # data exfiltration
            "HttpWebRequest", "FtpWebRequest", "UploadString", "UploadData", "WebClient.Upload",
            
            # HTTPS communication
            "POST", "GET", "PUT", "DELETE", "multipart/form-data", "Content-Disposition", "application/x-www-form-urlencoded", "api_key", "token", "authorization", "curl",  "wget",
            
            # DNS
            "gethostbyname", "DnsQuery", "nslookup", "Base64 over DNS",
            
            # ftp
            # remote access
            "ftp://", "SFTP", "WinSCP", "libcurl", "scp",
            
            # cloud services
            "AWS_SECRET_ACCESS_KEY", "Google Cloud API",
            
            # networks and packet sniffing
            "pcap_open_live", "pcap_loop", "WinPcap", "raw socket", "WSARecv", "recvfrom", "socket.connect",
            
            # manipulation of registry
            "RunOnce", "RunServices", "RunServicesOnce", "AutoRun", "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            
            # emails
            "SMTPClient", "mail.smtp.host", "mail.smtp.auth", "mailto", "SMTP.Send", "MailMessage", "System.Net.Mail",
            
            # suspicious keywords
            "pwd", "credential", "secret", "token", "hash", "password", "login"
        ]
        
        # regular expression for detecting URLs
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"


        try:

            # open file in binary read mode to prevent execution
            with open(file_path, "rb") as file:
                
                # decode
                content = file.read().decode(errors="ignore")

                # check for suspicious keywords
                for keyword in suspicious_keywords:
                    
                    # if keyword is found
                    if keyword in content:
                        
                        # mark file unsafe
                        # store in db
                        return {
                            
                            "status": "dangerous",
                            "risk_level": "high",
                            "reason_for_flag": f"Detected suspicious keyword: {keyword}",
                            "risk_category": "Credential Stealer",
                        }
                        
                # check for URLs with regex
                urls_found = re.findall(url_pattern, content)
                
                # if url is found
                if urls_found:
                    
                    # mark file unsafe
                    # store in db
                    return {
                        
                        "status": "dangerous",
                        "risk_level": "high",
                        "reason_for_flag": f"Detected suspicious URLs: {', '.join(urls_found[:5])}",
                        "risk_category": "Credential Stealer",
                    }

        # catch error
        except Exception as e:
            
            # logging
            print(f"Error {e}")

        # no issues found
        return None


    # checks file for keywords related to remote access tools, backdoors, reverse shells
    def remote_access_tool_checker(self, file_path):
        
        
        rat_keywords = [
            
            "RAT", "backdoor", "remote control", "netcat", "ReverseShell", "bind shell",
            
            "RemoteAccess", "netcat", "Telnet", "VNC", "SSH", "sockets", "bind", "exec", 
            
            "CreateObject", "Shell", "WinRM", "Powershell", "Remote Desktop", "ftps", "sftp",
             
            "upload", "download", "cmd", "powershell", "wget", "curl", "TCP", "UDP", "open port", 
            
            "listener", "command_and_control", "shellcode", "bind tcp", "reverse shell"
        ]
        
          
        try:
            
            # open file in binary read move to prevent execution
            with open(file_path, "rb") as file:
                
                # read file content and decode
                content = file.read().decode(errors="ignore")

                # iterate through list of keywords
                for keyword in rat_keywords:
                    
                    # case insensitive match for keyword
                    if keyword.lower() in content.lower():
                        
                        # mark file as unsafe
                        # store in db
                        return {
                            
                            "status": "dangerous",
                            "risk_level": "high",
                            "reason_for_flag": f"Detected RAT-related keyword: {keyword}",
                            "risk_category": "Remote Access Control"
                        }
            
        # catch error
        except Exception as e:
            
            # logging
            print(f"Error while checking for RAT: {e}")
        
        return None
    
    
    # extracts hex of file signature from first few bytes of file
    def extract_file_signature(self, file_path, num_bytes=16):
        
        try:
            
            # logging
            print(f"Trying to open file at {file_path}")
            
            # open file in binary read mode to prevent execution
            with open(file_path, "rb") as file:
                
                # read the specified number of bytes
                # convert to hex format
                signature = file.read(num_bytes).hex()
                
                # logging
                print(f"Extracted signature: {signature}")
                
                # return extracted file signature
                return signature
            
        # catch error
        except Exception as e:
            
            # logging
            print(f"Error extracting file signature: {e}")
            
            return None


    # check file header against a db of known malware signatures
    # if match found, mark file as unsafe
    def file_header_signature_checker(self, file_path):
        
        try:
            
            # extract file signature header
            signature = self.extract_file_signature(file_path)
            
            # if signature extraction fails
            if not signature:
                
                # logging
                print("Error no signature extracted")
                
                return None

            # logging
            print(f"Extracted signature to check: {signature}")

            # check extracted signature against db
            result = self.db_manager.check_file_signature(signature)
            
            # logging
            print("Database check result:", result)

            # if signature matches
            # flag file as unsafe
            if result:
                
                # logging
                print(f"File header matches known malware signature: {signature}")
                
                # store in db
                return {
                    
                    "status": "dangerous",
                    "risk_level": "high",
                    "reason_for_flag": f"File header matches known malware signature: {signature}",
                    "risk_category": "Virus"
                }
            
            # if signature does not match
            else:
                
                # no match found
                print(f"File header {signature}. No match found")
            
            # file not flagged
            return None

        # catch error
        except Exception as e:
            
            # logging
            print(f"An error occurred: {e}")
            
            return None


    
    # calculate entropy of file (randomness)
    # uses Shannon entropy
    # higher entropy indicates obfustication or encrypted content
    def calculate_entropy(self, data):
        
        # initialise list to store frequency of each byte
        byte_freq = [0] * 256
        
        # iterate through each byte in data
        for byte in data:
            
            # update frequency
            byte_freq[byte] += 1
        
        # initialise entropy value
        entropy = 0
        
        # calculate entropy based on byte frequency
        for freq in byte_freq:
            
            # ignore bytes with zero frequency
            if freq > 0:
                
                # calculate probability of byte
                prob = freq / len(data)
                
                # update entropy using log
                entropy -= prob * math.log(prob, 2)
                
        # return calculated entropy
        return entropy


    # detect obfustication based on entropy
    def detect_obfuscated_entropy(self, file_path, threshold=7.5):
        
        try:
            # open file in binary read mode to prevent execution
            with open(file_path, 'rb') as file:
                
                # read file as bytes
                content = file.read()

                # calculate entropy of file
                entropy = self.calculate_entropy(content)

                # logging
                print(f"Entropy of file '{file_path}': {entropy:.2f}")

                # if entropy exceeds threshold
                # mark file as unsafe
                if entropy > threshold:
                    
                    # store in db
                    return {
                        
                        "status": "dangerous",
                        "risk_level": "high",
                        "reason_for_flag": f"File has high entropy ({entropy:.2f}), indicating possible obfuscation",
                        "risk_category": "Obfuscation"
                        
                    }

        # catch error
        except Exception as e:
            
            # logging
            print(f"Error occurred while processing the file: {e}")
        
        return None
    

    # method to detect EICAR antivirus test file
    def detect_eicar_test_file(self, file_path):
        
        # define EICAR test file signature in binary
        eicar_signature = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        
        try:
            # open file in binary mode
            with open(file_path, "rb") as file:
                
                # read entire file content as bytes
                content = file.read()
                
                # check if known EICAR signature exists within the file content
                if eicar_signature in content:
                    
                    # mark file as unsafe
                    # store in db
                    return {
                        
                        "status": "detected",
                        "risk_level": "low",
                        "reason_for_flag": "EICAR test file detected",
                        "risk_category": "Test File"
                        
                    }
                    
        # catch error
        except Exception as e:
            
            # logging
            print(f"Error while checking EICAR test file: {e}")
            
            return None
        
        return None

             
    # close db connection
    def close(self):
        
        # close connection with db
        self.db_manager.close()