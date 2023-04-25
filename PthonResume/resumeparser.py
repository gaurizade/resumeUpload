import os
import io
import spacy
from spacy.matcher import Matcher
import multiprocessing as mp

import nltk
#nltk.download()
nltk.download('stopwords')
nltk.download('popular')
############# funtional Imports ###############

import basic_details
import textextractor
import experienceent
import extractentites
import educationent
import skills
import locations
import social
import mysql.connector
import json

###############################################


class ResumeParser(object):
    def __init__(self, resume):
        self.__details = {
            "name": None,
            "email": None,
            "phone": None,
            "linkedin": None,
            "facebook": None,
            "twitter": None,
            "location": None,
            "primary_skills": None,
            "secondary_skills": None,
            "education": None,
            "designation": None,
            "experience": None,
            "resume_text": None


        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self._text = textextractor.extract_text(self.__resume, '.' + ext)

        self.remove_space = textextractor.remove_space(self._text)

        self.resume_unicar = textextractor.clean_resume(self.remove_space)

        self.clean_text = textextractor.preprocess_text(self.resume_unicar)

        text_lower = self.clean_text.lower()
        text_join = ' '.join(text_lower.splitlines())
        self.entites = extractentites.finding_indicates(text_join)

        ######## Basic Details ##########

        model = spacy.load('en_core_web_sm')  # spacy model
        texts = model(self.clean_text)

        self.__matcher = Matcher(texts.vocab)

        try:
            name = basic_details.extract_name(texts, self.__matcher)
            self.__details['name'] = name.title()
        except:
            return None

        try:
            email = basic_details.extract_email(self._text)
            self.__details['email'] = email
        except:
            return None

        try:
            phone = basic_details.extract_mobile_number(self._text)
            self.__details['phone'] = phone
        except:
            return None

        ############## profile links ########

        linkedin = social.linkedin(self.clean_text)
        facebook = social.facebook(self._text)
        twitter = social.twitter(self._text)

        self.__details['linkedin'] = linkedin
        self.__details['facebook'] = facebook
        self.__details['twitter'] = twitter

        ###############  Skills   #################

        skills_file = None
        texts = model(self.clean_text)
        self.__skills_file = skills_file
        self.__noun_chunks = list(texts.noun_chunks)

        primary_db = skills.primary1(self._text)
        db_data = list(primary_db)

        primary_nlp = skills.primary2(
            texts, self.__noun_chunks, self.__skills_file)
        resume_skills = []
        for i in primary_nlp:
            for j in db_data:
                resume_skills.append(i)
                resume_skills.append(j.title())
        finalskills = set(resume_skills)
        self.__details['primary_skills'] = list(finalskills)

        secondary = skills.extract_secondry_skills(self.clean_text)
        se_skills = set(secondary)
        self.__details['secondary_skills'] = list(se_skills)

        # ############# education ###############
        if self.entites:
            try:
                edu1 = ''
                edu1 = (self.entites['academic'])
                # print(data,'-----')
            except (KeyError):
                pass
            try:
                edu2 = ''
                edu2 = (self.entites['education'])
                # print(data,'-----')
            except (KeyError):
                pass
            try:
                edu3 = ''
                edu3 = (self.entites['academic credentials'])
            except (KeyError):
                pass

            try:
                edu4 = ''
                edu4 = (self.entites['academic profile'])
            except (KeyError):
                pass
            try:
                edu5 = ''
                edu5 = (self.entites['academia'])
                # print(data,'-----')
            except (KeyError):
                pass
            try:
                edu6 = ''
                edu6 = (self.entites['education, trainings & certifications'])
                # print(data,'-----')
            except (KeyError):
                pass

            education_ent = ''
            education_ent = edu1 + edu2 + edu3 + edu4 + edu5 + edu6
            education_text = " ".join(line.strip()
                                      for line in education_ent.splitlines())
            edu = educationent.extract_education(education_text)
            self.__details['education'] = edu

        ################## Experience ########################

        designantion = experienceent.extract_designation(self._text)
        self.__details["designation"] = designantion

        ########## resume text ###########

        self.__details["resume_text"] = self.clean_text

        ################# Experience ##########
        exp_data1 = ''
        exp_data2 = ''
        exp_data3 = ''
        exp_data4 = ''

        if self.entites:
            try:
                exp_data1 = (self.entites['experience'])
            except (KeyError):
                pass
            try:
                exp_data2 = (self.entites['work experience'])
            except (KeyError):
                pass

            try:
                exp_data3 = (self.entites['professional experience'])
            except (KeyError):
                pass
            try:
                exp_data4 = (self.entites['work history'])
            except (KeyError):
                pass

            try:
                exp_data4 = (self.entites['employment'])
            except (KeyError):
                pass

            exp_ent = exp_data1 + exp_data2 + exp_data3 + exp_data4

            exp = " ".join(line.strip() for line in exp_ent.splitlines())
            text_replace = exp.replace('experience', '')
            exper = experienceent.extract_experience(text_replace.title())
            # self.__details["experience"] = exper

        locationss = locations.address_func(self.clean_text)
        self.__details["location"] = locationss

        connection = mysql.connector.connect(host='localhost',
                            database='ResumeUpload',
                            user='root',
                            password='')
            # print(connection)
        insert_query =  "insert into TalentData (data) values(%s) "
        val = (json.dumps(self.__details))
            
        cursor= connection.cursor()
        cursor.execute(insert_query,(val,))
        connection.commit()
        print('Data has entered correctly')

    def get_extracted_data(self):
        try:
            # pass
            return self.__details
        except:
            return None

    def __get_basic_details(self):
        pass


def extract(resume):
    ent = ResumeParser(resume)
    ent.get_extracted_data()

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    resumes = []  
    data = []
    folder = (r'E:\resumes\resume_2021_90\2021\05')
    for root, directores, filenames in os.walk(folder):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)      
    results = [
        pool.apply_async(
            extract,
            args=(x,)
        ) for x in resumes
    ]
    
    results = [p.get() for p in results]    
    

#data = ResumeParser(r"/Users/sankalp/Downloads/Pratiksha Gude.pdf")
#print(data.get_extracted_data())

