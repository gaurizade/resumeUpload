import spacy
import textextractor 

    


import pyap
from pprint import pprint
from geopy.geocoders import Nominatim
from indian_address_parser import PostalAddress



def world_citys(text):  
    """ This Helper funtion helps to find `Address State`
    
        This func is help to find  the world citys using a text file         
        and use that city to get its state and country
    """
   
    # print(text1)
    try:  
        state = []
        # address_s = convert_file_to_list(r"C:\Users\Sagar\Desktop\bluestack\jsonl\words.txt")    
        address_s = textextractor.convert_file_to_list(r'/Users/sankalp/High5Repo/PthonResume/world_list.txt')    
        for word in address_s:
            if word in text:
                if word == address_s:
                    state.append(word)
                else:
                    state.append(word)
        print("addressB",state)
        return state[0]
    except:
        return None


def find_us_address(text):
    """
    Helper function to find the `US Locations `
     
    US address lib Which is find us address patterns if address is in format 
    
    """
    addresses = pyap.parse(text, country='US')   
    for address in addresses: 
        address = address.as_dict()  
        return address

      
      

def address_func(resume_text):
    """ 
    Helper func to find the `Address` in the resume 
    
    We need the zip code , city , state and country
    
    Returns a `dictionary`
    """
    
    resume_address = None
    try:    
        resume_address = find_us_address(resume_text)
        country = resume_address['country_id']
        state = resume_address['region1']
        district = resume_address['city']
        zipcode = resume_address['postal_code']
        addresses = resume_address['full_address']
        final_address = {
                    "zipCode": zipcode,
                    "address": addresses,
                    "city" : district,
                    "state" : state,
                    "country" : country         
                    }
        return final_address
    except:
        pass
    if resume_address is None:      
        city = world_citys(resume_text.title())       
        if city is not None:
            geolocator = Nominatim(user_agent="H5")
            location = geolocator.geocode(city)   
            address = PostalAddress(str(location)).__dict__             
            zipcode = address.get('pin_codes_found')
            addresses = address.get('raw_address') 
            country = addresses.split(', ')[-1].title()  
            remove_pin = ''.join(c for c in addresses if not c.isdigit())
            removies = remove_pin.replace(", ,",",")                 
            state = removies.split(', ')[-2].title()   
            
            #state = None        
            final_address = {
                "zipCode": zipcode,
                "address": addresses.title(),
                "city" : city,
                "state" : state,
                "country" : country         
            }
            return final_address
        elif city is None:
             final_address = {
                "zipCode": None,
                "address": None,
                "city" : None,
                "state" : None,
                "country" :None    
            }                      
        return final_address