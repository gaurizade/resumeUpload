import io
import re 
import os
import docx2txt
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
import nltk
import logging





def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text    '''
  
    if not isinstance(pdf_path, io.BytesIO):        
        with open(pdf_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,
                        codec='utf-8',
                        laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text             
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    else:        
        try:
            for page in PDFPage.get_pages(
                    pdf_path,
                    caching=True,
                    check_extractable=True
            ):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(
                    resource_manager,
                    fake_file_handle,
                    codec='utf-8',
                    laparams=LAParams()
                )
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text             
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            return



def extract_text_from_docx(doc_path):
    '''
    Helper function to extract plain text from .docx files

    :param doc_path: path to .docx file to be extracted
    :return: string of extracted text
    '''
    try:
        temp = docx2txt.process(doc_path)
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    except KeyError:
        return ' '


from bs4 import BeautifulSoup as bs
def extract_text_from_doc(doc_path):
    
    '''
    Helper function to extract plain text from .doc files

    :param doc_path: path to .doc file to be extracted
    :return: string of extracted text
    ''' 
    try:
        soup = bs(open(doc_path).read())
        [s.extract() for s in soup(['style', 'script'])]
        tmpText = soup.get_text()
        # text = " ".join(" ".join(tmpText.split('\t')).split('\n')).encode('utf-8').strip()    
        return tmpText
    except :
            return 'Unable to read doc file'



def extract_text(file_path,extension):
    '''
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''     
        
    if extension =='.pdf':
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page               
    elif str(extension).endswith('docx'):# =='docx':
        text = extract_text_from_docx(file_path)
    elif str(extension).endswith('doc'):# =='doc':
        text = extract_text_from_doc(file_path)
    # print(text)
   
    return text



def preprocess_text(text):
    """
        Remove blank lines from text
    """
    try:        
        clean_text_list = []
        clean_text = None
        try:
            text = os.linesep.join([s for s in text.splitlines() if s.strip()])
            text_lines = text.splitlines()        
            for each_text in text_lines:
                each_text.strip()
                each_text = " ".join(re.split("\\s+", each_text, flags=re.UNICODE))
                clean_text_list.append(each_text)
                clean_text = "\n".join(clean_text_list)
            """
            remove different dashes in text
            """
            clean_text = re.sub("[—‐᠆﹣－⁃−—―־–]+",'-',clean_text)
        
        except Exception as ex:
            logging.exception(str(ex))
            logging.exception("Exception in preprocess_text.")
        return clean_text
    except:
        return ''

def clean_resume(text):
    """
        Helper function help to clean the symbols unwanted unicodes from text
        
    """
    try:      
        
        
        text = text.replace("\n"," ")
        text = text.replace("\uf0b7"," ")
        text = text.replace("\uf06c"," ")
        text = text.replace("\u201f"," ")
        text = text.replace("\u2019"," ")
        text = text.replace("\u201d"," ")
        text = text.replace("\u201c"," ")
        text = text.replace("\u200b"," ")
        text = text.replace("\uf020'"," ")
        text = text.replace("\u0007"," ")
        text = text.replace("\ufb00"," ")
        text = text.replace("•  •  •  •"," ")
        text = text.replace(" ● "," ")
        text = text.replace(" • "," ")
        text = text.replace(" ➢"," ")
        text = text.replace(":"," ")
        text = text.replace("[^a-zA-Z0-9]", " ") 
        re.sub('\W+','', text)
        # text = text.lower()    
        return str(text)
    except AttributeError:
        return ''


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


def convert_file_to_list(file):
    '''
    convert file text to list so we can access that for read file and convert it into the list 
    '''
    file = open(file, encoding="utf8")
    file = file.readlines()
    lines = []
    lines = [line.strip() for line in file]
    return lines

def remove_space(text):
    '''
    Required the remove unwanted spaces from resume text to get clean text 
    '''
    newtext = ''    
    counter = 0
    for line in text.splitlines():
        line = line.strip()
        if len(line)==0:
            counter += 1
            if counter<=2:
                newtext += line + '\n'
        else:
            newtext += line + '\n'
            counter = 0
    clean = "".join([s for s in newtext.strip().splitlines(True) if s.strip()])
    return clean