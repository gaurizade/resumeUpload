
import nltk
import textextractor
import os 
import pandas as pd

#from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords') 


def primary1(resume_text):
        ''' 
         Helper function to extract skills from spacy nlp text
        :param nlp_text: object of `spacy.tokens.doc.Doc`
        :param noun_chunks: noun chunks extracted from nlp text
        :return: list of primary skills extracted using skills db file    
            
            
        '''
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(resume_text)
        
        filtered_tokens = [w for w in word_tokens if w not in stop_words]
        filtered_tokens = [w for w in word_tokens if w.isalpha()]    
        bigrams_trigrams = list(
            map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
        
        found_skills = []   
        skills_db = textextractor.convert_file_to_list("/Users/sankalp/High5Repo/PthonResume/skillsdb.txt")    
        for token in filtered_tokens:
            if token.lower() in skills_db:
                found_skills.append(token)
        for ngram in bigrams_trigrams:
            if ngram.lower() in skills_db:
                found_skills.append(ngram)   
        skills = set()
        for i in found_skills:
            skills.add(str(i).lower())       
        return skills
  


def primary2(nlp_text, noun_chunks, skills_file=None):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of primary skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    if not skills_file:
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'skills.csv')
        )
    else:
        data = pd.read_csv(skills_file)
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]



def extract_secondry_skills(resume_text):
    
    '''
        Helper function to extract skills from spacy nlp text

        :param nlp_text: object of `spacy.tokens.doc.Doc`
        :param noun_chunks: noun chunks extracted from nlp text
        :return: list of Secondry skills extracted
    '''
    
    
    try:
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(resume_text)
        filtered_tokens = [w for w in word_tokens if w not in stop_words]
        filtered_tokens = [w for w in word_tokens if w.isalpha()]
        bigrams_trigrams = list(
            map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
        found_skills = []
        final = set(found_skills)
        skills_db = textextractor.convert_file_to_list('/Users/sankalp/High5Repo/PthonResume/secondry_skills_db.txt')
        for token in filtered_tokens:
            if token.lower() in skills_db:
                found_skills.append(token)
        for ngram in bigrams_trigrams:
            if ngram.lower() in skills_db:
                found_skills.append(ngram)                
        return list(final)
    except:
        return None
    
    
    
### lightcast #####
    
# import requests
# import json
# url = "https://auth.emsicloud.com/connect/token"

# # id = "zextp4q0o3yraw0o"
# # client = 'XjngX2ZP'
# # emsi_open = 'emsi_open'
# # payload = "client_id=zextp4q0o3yraw0o&client_secret=XjngX2ZP&grant_type=client_credentials&scope=emsi_open"
# # headers = {'content-type': 'application/x-www-form-urlencoded'}




# # print(response.text)
# payload = "client_id=hzc29kdisg2ltnum&client_secret=79paZ3aH&grant_type=client_credentials&scope=emsi_open"
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# response = requests.request("POST", url, data=payload, headers=headers)
# print(response.text)
# token_dict = json.loads(response.text)    
# token = token_dict["access_token"]




# url = "https://emsiservices.com/skills/status"
# headers = {'Authorization': f'Bearer {token}'}
# response = requests.request("GET", url, headers=headers)
# print(response.text)


# url = "https://emsiservices.com/skills/meta"
# headers = {'Authorization': f'Bearer {token}'}
# response = requests.request("GET", url, headers=headers)
# print(response.text)


# import json
# def skills_api(resume):
#     url = "https://emsiservices.com/skills/versions/latest/extract/trace"
#     querystring = {"language":"en"}
#     payload = {
#     "text":f"{str(resume)}"
#     }    
#     headers = {
#         'Authorization': f"Bearer {token}",
#         'Content-Type': "application/json"
#         }
#     response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)
#     out = response.text
#     # print(out)
#     out_file = open("myfile.json", "w")    
#     json.dump(out, out_file)    
#     out_file.close()
    
#     # JSON string   
    
#     # Convert string to Python dict
#     skills_data = []
#     skills_dict = json.loads(out)   
#     # return skills_dict["data"]["skills"]  
#     # for i in range(100) :        
#         # skills_final = (skills_dict["data"]["skills"][i]["skill"]['name'])
#         # return skills_dict["data"]["skills"][i]["skill"]['name']
        


if __name__ == '__main__':
    pass

