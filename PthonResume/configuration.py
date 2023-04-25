"""
Configuration Class
"""
import os
import json
class Configuration(object):
    """A configuration to load json Configuration
    has following properties:
        Attributes:
            id: A string representing the unique id.
            param: A dictionary of <k,v> pairs for parameters.
    """
    def __init__(self, param=None):
        """Return a Configuration object"""
        self.param = param
        if param is None:
            data = {
                "path": {
                    "file_path": " ",
                    "log_folder" : "logs"
                },
              
                "content_type": {
                    "json_content_type": "application/json"
                },
                "strings": {
                    "dt_format": "%Y-%m-%d %H:%M:%S",
                    "dt_format_log" : "%Y-%m-%d_%H-%M-%S",
                    "name_char_set": "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "test_str": "hello world",
                    "pref_loc": "preferred location",
                    "junior_exp_level": "Junior: 0-3 years",
                    "mid_exp_level": "Mid: 4-7 years",
                    "senior_exp_level": "Senior: 8-10 years",
                    "lead_exp_level": "Subject Matter Expert"
                },
      
                "thresholds": {
                    "sectionize_line_limit": 40,
                    "skills_char_limit" : 30
                },
                "api": {
                    "post": "POST",
                    "get": "GET",
                    "base_url": "http://dev.high5hire.com:1021/",
                    "save_details": "AddCandidate",
                    # DEV
                    "csv_matcher_url" : "https://uatresumeextmatcher.azurewebsites.net/api/CsvMatcher",
                    "csv_matcher_key" : "o8gDQc8aGZbZNS8TQoktQX8AM6zaacQTn5MXwUnlPDzjOZRHfwtb6A=="
                },
                "regex": {
                    "date_format_1": "[ADFJMNOS]\\w*\\s*[-–—’',: ]\\s*[\\d]{2,4}\\s*(?:[-–—:]|To)\\s*[ADFJMNOS]\\w*\\s*[-–—’',: ]\\s*[\\d]{2,4}|[ADFJMNOS]\\w*\\s*[-–—’',: ]\\s*[\\d]{2,4}\\s*(?:[-–—:]|To)\\s*(?:Present|Current)",
                    "date_format_2": "[\\d]{1,2}\\s*[-–—/\\.]\\s*[\\d]{2,4}\\s*(?:[-–—:]|To)\\s*[\\d]{1,2}\\s*[-–—/\\.]\\s*[\\d]{2,4}|[\\d]{1,2}\\s*[-–—/\\.]\\s*[\\d]{2,4}\\s*(?:[-–—:]|To)\\s*(?:Present|Current)",
                    "date_format_3": "(?:['’]|[\\d]{2})[\\d]{2}\\s*(?:[-–—:]|To)\\s*(?:['’]|[\\d]{2})[\\d]{2}|(?:['’]|[\\d]{2})[\\d]{2}\\s*(?:[-–—:]|To)\\s*(?:Present|Current)",
                    "clean_date": "(?:[-–—’',:./]|\\s*To\\s*)",
                    "present": "(?:Present|Current)",
                    "date_standard": "%d-%m-%Y",
                    "remove_duplicate_whitespace": "[ \\t]+",
                    "sectionize_all": ".*summary.*|.*synopsis.*|.*objective.*|.*qualification.*|.*education.*|.*skill.*|.*competenc.*|.*core.*strength.*|.*expertise.*|.*proficienc.*|.*career.*|.*project.*detail.*|.*experience.*|.*work.*history.*|.*employment.*|.*certification.*|.*training.*|.*professional.*development.*|.*technical.*development.*|.*accomplishments.*",
                    "sectionize_summary": ".*summary.*|.*synopsis.*|.*objective.*",
                    "sectionize_qualfication": ".*qualification.*|.*education.*",
                    "sectionize_skills": ".*skill.*|.*competenc.*|.*core.*strength.*|.*expertise.*|.*proficienc.*",
                    "sectionize_experience": ".*career.*|.*project.*detail.*|.*experience.*|.*work.*history.*|.*employment.*",
                    "sectionize_certification":  ".*certification.*|.*training.*|.*professional.*development.*|.*technical.*development.*|.*accomplishments.*",
                    "linkedin_url": "linkedin\\.com/in/[A-z0-9_-]+/?",
                    "fb_url": "(?:mbasic\\.facebook|m\\.facebook|facebook|fb)\\.com/[A-z0-9_\\.-]+/?",
                    "twitter_url": "twitter\\.com/[A-z0-9_]+/?",
                    "gmail_url": "[a-zA-Z0-9]+[a-zA-Z0-9\\.]*[a-zA-Z0-9]+@g(?:oogle)?mail\\.com",
                    "email_url": "[a-zA-Z0-9]+[a-zA-Z0-9!#$&'*+-=?^_|.-]*[a-zA-Z0-9]+@[a-zA-Z0-9-\\.]+\\.[a-zA-Z]+",
                    "skills_type_1" : "\\w+\\s{0,1}[,|]\\s{0,1}\\w+",
                    "skills_type_2" : "\\w+\\s{0,1}(:|-|:-|—)\\s{0,1}([\\w/. ]+)\\s{0,1}[,|]\\s{0,1}([\\w/. ]+)"
                },
                "azure": {
                    "container_res": "resumetest",
                    "container_res_logs" : "resume-extraction-logs",
                    #UAT
                     "storage_acc_res": "testresumeparser",
                     "account_key_res": "ScyM7Tb8fsu8aZ2aiGrVDIFCx/puNHUfJaIrZvvFJP9Ez0CW/7KiRRH8539TAWmkoSfE2JVWHuyQ+AStUI47hw=="
                    
                }
            }
        else:
            data = dict(param)

        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        """
        Call function recursively until
        returning configuration object
        """
        if type(value) is list:
            return [self.compute_attr_value(x) for x in value]
        elif type(value) is dict:
            return Configuration(value)
        else:
            return value
