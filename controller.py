import os
import zipfile
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

        print(f"Scanned file ID returned: {scanned_file_id}")

        # save scan details to db
        self.db_manager.add_scan_detail(
            
            scanned_file_id,
            
            reason_for_flag=reason_for_flag or "No issues detected", 
            
            risk_category=risk_category or "N/A"
        )
        
        
        # placeholder threat info
        self.db_manager.add_threat_info(
            
            scanned_file_id, 
            
            what_happens_if_run="File may execute malicious scripts", 
            
            prevention_tips="Avoid downloading files from untrusted sources"
        )

        # logging for debugging
        print(f"File '{file_name}' processed successfully with ID: {scanned_file_id}")


    
    # method to check for double extensions in the file name
    # checking file spoofing vulnerability
    def double_extension_checker(self, file_path):
        
        # get file name from file path
        file_name = os.path.basename(file_path)
        
        # split file name into parts seperated by dots
        parts = file_name.split('.')

        # if there are more than 2 parts, means that there is an extra extension
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
                
                "risk_category": "Executable File"
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
        
        # debugging
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
                
                print("Macros detected")
                
                # extract macros from file
                for macro_tuple in vba_parser.extract_macros():
                    
                    # debugging
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
                                    
                                    "reason_for_flag": f"Macros contain suspicious command: {keyword}.",
                                    
                                    "risk_category": "Macro-based Threats"
                                    
                                }

        except Exception as e:
            
            print(f"Error: {e}")
           
           
    # method to analyse ZIP files based on their compression size
    def detect_zip_bombs(self, file_path, compression_ratio_threshold=1000, max_decompressed_size=10**9):
        
        try:
            # open ZIP file in read mode
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                
                # calculate total compressed size of all files in ZIP
                total_compressed_size = sum(file.compress_size for file in zip_file.infolist())
                
                # calculate total decompressed size of all files in ZIP
                total_decompressed_size = sum(file.file_size for file in zip_file.infolist())

                # calculate compression ratio
                if total_compressed_size > 0:
                    
                    compression_ratio = total_decompressed_size / total_compressed_size
                
                else:
                    compression_ratio = 0

                # if compression ratio is bigger than ratio threshold
                if compression_ratio > compression_ratio_threshold:
                    
                    # mark file as unsafe
                    # store in db
                    return {
                        
                        "status": "dangerous",
                        
                        "reason_for_flag": f"Compression ratio ({compression_ratio}) exceeds safe threshold.",
                        
                        "risk_category": "Zip Bomb"
                    }

                # if total decompressed size is bigger than 1 GB
                if total_decompressed_size > max_decompressed_size:
                    
                    # mark file as unsafe
                    # store in db
                    return {
                        
                        "status": "dangerous",
                        
                        "reason_for_flag": f"Decompressed size ({total_decompressed_size} bytes) exceeds limit.",
                        
                        "risk_category": "Zip Bomb"
                    }


        except Exception as e:
            
            # debugging
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
    # temporarily checks file extensions
    # will add more functions which will be called in here
    # placeholder for scanning logic
    def scan_file(self, file_path):

        print(f"Scanning file: {file_path}")
        
        # default values
        status, risk_level = "safe", "low"
        
        reason_for_flag, risk_category = None, None

        # file checkers
        checkers = [
            
            self.double_extension_checker,
            
            self.executable_file_checker,
            
            self.office_file_checker,
            
            self.is_zip_file
            
        ]

        # iterate through checkers
        for checker in checkers:
            
            result = checker(file_path)
            
            if result:
               
                # update with results
                status = result["status"]
                
                risk_level = result["risk_level"]
                
                reason_for_flag = result["reason_for_flag"]
                
                risk_category = result["risk_category"]
                
                break

        # return results
        return status, risk_level, reason_for_flag, risk_category



    # close db connection
    def close(self):
        
        self.db_manager.close()
        