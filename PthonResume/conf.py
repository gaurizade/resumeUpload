



# stage 
connection_string = r"DefaultEndpointsProtocol=https;AccountName=high5stagestorage;AccountKey=zUA+3JSV02r2nTfY7l6LUPmsm+sUGCWI7+Sa3dcMFW/fZKgigSWg4NB02LcSn5qPMrxdQzr6NQ/uto8dFWUiBQ==;EndpointSuffix=core.windows.net"
container_name = r"high5hirecontainer/resumeParsed"
container_log = r"$logs"
storage_account = r"high5stagestorage"
storage_account_key = r"zUA+3JSV02r2nTfY7l6LUPmsm+sUGCWI7+Sa3dcMFW/fZKgigSWg4NB02LcSn5qPMrxdQzr6NQ/uto8dFWUiBQ=="




#  test
# connection_string = r"DefaultEndpointsProtocol=https;AccountName=testresumeparser;AccountKey=ScyM7Tb8fsu8aZ2aiGrVDIFCx/puNHUfJaIrZvvFJP9Ez0CW/7KiRRH8539TAWmkoSfE2JVWHuyQ+AStUI47hw==;EndpointSuffix=core.windows.net"
# container_name = r"resumetest"
# container_log = r"$logs"
# storage_account = r"testresumeparser"
# storage_account_key = r"ScyM7Tb8fsu8aZ2aiGrVDIFCx/puNHUfJaIrZvvFJP9Ez0CW/7KiRRH8539TAWmkoSfE2JVWHuyQ+AStUI47hw=="


# prod

# connection_string = r"DefaultEndpointsProtocol=https;AccountName=high5hirestorage;AccountKey=Vr7L27AsdBjR7pFL7cnvuR+gcaCiKt8RzUcMeUy3tCHre7YRpyAM+/eCc+mZS5BhXbYNcOcKnaYr+ASt1swY/w==;EndpointSuffix=core.windows.net"
# container_name = r"high5hirecontainer/resumeParsed"
# container_log = r"$logs"
# storage_account = r"high5hirestorage"
# storage_account_key = r"Vr7L27AsdBjR7pFL7cnvuR+gcaCiKt8RzUcMeUy3tCHre7YRpyAM+/eCc+mZS5BhXbYNcOcKnaYr+ASt1swY/w=="

def find_related_text(resume_text, keywords):
    """
    This function finds keywords in the resume text and extracts related text to those keywords.
    Returns a dictionary output.
    """
    parsed_content = {}
    for keyword in keywords:
        try:
            idx = resume_text.index(keyword)
            next_idx = len(resume_text)
            for kw in keywords:
                if kw != keyword:
                    try:
                        kw_idx = resume_text.index(kw)
                        if idx < kw_idx < next_idx:
                            next_idx = kw_idx
                    except:
                        pass
            parsed_content[keyword] = resume_text[idx+len(keyword):next_idx].strip()
        except:
            pass
    return parsed_content