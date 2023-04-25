import combination

parsed_content = {}
def finding_indicates(text):
    """
    ### This Function is helps us to find the keywords in the resume and extract data 
        find the releted text to that keywords
        Returns a dictionary output 
    """
    try:
        content = {}
        indices = []
        keys = []
        for key in combination.Keywords:
            try:
                content[key] = text[text.index(key) + len(key):]
                indices.append(text.index(key))
                keys.append(key)
            except:
                pass         
        zipped_lists = zip(indices, keys)
        sorted_pairs = sorted(zipped_lists)
        # sorted_pairs

        tuples = zip(*sorted_pairs)
        indices, keys = [ list(tuple) for tuple in  tuples]
        # return keys
        # print(keys)

        content = []
        for idx in range(len(indices)):
            if idx != len(indices)-1:
                content.append(text[indices[idx]: indices[idx+1]])
            else:
                content.append(text[indices[idx]: ])
            
        for i in range(len(indices)):
            parsed_content[keys[i]] = content[i]         
        # print(parsed_content)
        return parsed_content
    except:
        return None

