

################## Education ################



# from spacy import displacy
import spacy
# import numpy as np
import pandas as pd
from pandas import DataFrame as df



def extract_education(resume_text):
    '''
    Helper function to extract different entities with custom
    trained model using SpaCy's NER

    :param custom_nlp_text: object of `spacy.tokens.doc.Doc`
    :return: dictionary of entities
    '''
    # model = spacy.load("ResumeParser/stanford-ner/model-best") #orignal gpu trainned
    model = spacy.load("/Users/sankalp/High5Repo/PthonResume/education_model")
    # model = spacy.load("model-best")
    entities = {}
    texts = model(resume_text)
    for ent in texts.ents:
        if ent.label_ not in entities.keys():
            entities[ent.label_] = [ent.text]
        else:
            entities[ent.label_].append(ent.text)
    for key in entities.keys():
        entities[key] = list(entities[key])
    # print(entities)

    degree = None
    school = None
    year = None
    major = None

    try:
        degree = entities['DEGREE']
        for i in range(len(degree)):
            degree[i] = degree[i].title()
    except KeyError:
        degree = [None]
    try:
        school = entities['SCHOOL']
        for i in range(len(school)):
            school[i] = school[i].title()
    except KeyError:
        school = [None]
    try:
        year = entities['YEAR']
    except KeyError:
        year = [None]
    try:
        major = entities['MAJOR']
        for i in range(len(major)):
            major[i] = major[i].title()
    except KeyError:
        major = [None]

    try:
        values = degree, school, year, major
        my_ent = (pd.DataFrame(values))
        my_ent.rename(index={0: 'program', 1: 'school',
                      2: 'year', 3: 'major'}, inplace=True)
        return [my_ent.to_dict(orient='dict')]
    except:
        return None
