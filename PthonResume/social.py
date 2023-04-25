import re


def linkedin(text):  
    '''
    Helper function to extract  linkedin links from resume text
    :param resume_text: Plain resume text
    :return: list of urls
    '''  
    
    linkedin_url = re.findall(r'[\w:\/\.]*linkedin.com\/[\w\/]{3,8}[\w-]{1,}[\/]?',text)
    for lnk in linkedin_url:
        return (lnk[0])


def facebook(text):
    '''
    Helper function to facebook links from resume text
    :param resume_text: Plain resume text
    :return: list of urls
    '''  
    fb_urls=re.findall(r"(?:mbasic\\.facebook|m\\.facebook|facebook|fb)\\.com/[A-z0-9_\\.-]+/?",text)
    if fb_urls:     
        return fb_urls[0]

def twitter(text):
    '''Helper function to twitter links from resume text

    :param resume_text: Plain resume text
    :return: list of urls
    '''  
    twitter_url = re.findall(r"twitter\\.com/[A-z0-9_]+/?",text)
    if twitter_url:
        return twitter_url[0]
          
          
