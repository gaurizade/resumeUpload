import tika
tika.initVM()
from tika import parser as p
def extract_text_from_doc(doc_path):    
     
    try:   
        results = p.from_file(doc_path)
        data = (results["content"].strip())  
              
        return data      
    except:
        return ''