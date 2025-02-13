import os
from datetime import datetime
from database import DatabaseManager


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
        # gets the last item of filepath and converts to lowercase
        file_name = os.path.basename(file_path).strip()  # Strip any leading/trailing whitespace
        _, file_extension = os.path.splitext(file_name)  # Split the file name and extension
        file_extension = file_extension.lower()  # Convert to lowercase for consistency

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



    # method to check file for vulnerabilities
    # temporarily checks file extensions
    # will add more functions which will be called in here
    # placeholder for scanning logic
    def scan_file(self, file_path):
        
        # start with safe status
        status, risk_level = "safe", "low"
        
        reason_for_flag, risk_category = None, None

        # check for double extensions
        result = self.double_extension_checker(file_path)
        
        # if double extension finds an issue
        if result:
            
            # update data with results
            status = result["status"]
            
            risk_level = result["risk_level"]
            
            reason_for_flag = result["reason_for_flag"]
            
            risk_category = result["risk_category"]

        
        
        # check if file is executable
        exec_result = self.executable_file_checker(file_path)
        
        # if executable finds an issue
        if exec_result:
            
            # update data with results
            status = exec_result["status"]
            
            risk_level = exec_result["risk_level"]
            
            reason_for_flag = exec_result["reason_for_flag"]
            
            risk_category = exec_result["risk_category"]



        # return results
        return status, risk_level, reason_for_flag, risk_category



    # close db connection
    def close(self):
        
        self.db_manager.close()