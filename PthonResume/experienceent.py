

# from spacy import displacy
import spacy
# import numpy as np
import pandas as pd
from pandas import DataFrame as df



def extract_experience(resume_text):
    '''
    Helper function to extract different entities with custom
    trained model using SpaCy's NER

    :param custom_nlp_text 
    :return: dictionary of entities
    '''
    model = spacy.load("/Users/sankalp/High5Repo/PthonResume/model-best1")     
    entities = {}
    texts = model(resume_text)
    for ent in texts.ents:
        if ent.label_ not in entities.keys():
            entities[ent.label_] = [ent.text]
        else:
            entities[ent.label_].append(ent.text)
    for key in entities.keys():
        entities[key] = list(entities[key])

    employer = None
    designation = None
    start_date = None
    end_date = None

    try:
        employer = entities['EMPLOYER']
    except KeyError:
        employer = [None]
    try:
        designation = entities['DESIGNATION ']
    except KeyError:
        designation = [None]
    try:
        start_date = entities['STARTDATE']
    except KeyError:
        start_date = [None]
    try:
        end_date = entities['ENDDATE']
    except KeyError:
        end_date = [None]

    try:
        values = employer, designation, start_date, end_date
        my_ent = (pd.DataFrame(values))
        my_ent.rename(index={0: 'Employer',
                             1: 'designation',                             
                             2: 'start_date',
                             3: 'end_date'},
                      inplace=True)
        return [my_ent.to_dict(orient='dict')]
    except:
        return None



def extract_designation(resume_text):
    '''
    Helper function to extract different entities with custom
    trained model using SpaCy's NER

    :param custom_nlp_text 
    :return: dictionary of entities
    '''
    model = spacy.load("/Users/sankalp/High5Repo/PthonResume/model-best1") 
    entities = {}
    texts = model(resume_text)
    for ent in texts.ents:
        if ent.label_ not in entities.keys():
            entities[ent.label_] = [ent.text]
        else:
            entities[ent.label_].append(ent.text)
    for key in entities.keys():
        entities[key] = list(entities[key])
        
    designation = None
 
    try:
        designation = entities['DESIGNATION ']
        if designation:
            return designation[0]
    except KeyError:
        designation = [None]
        
    
