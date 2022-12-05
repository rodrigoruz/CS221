from collections import defaultdict
import re

def extract_quals(source:str)->dict:
    """This functions takes raw source code and output dictionaries of basic and preferred qualifications for given job

    Args:
        source (str): raw string with source code to be parsed

    Returns:
        dict: dictionary with basic and preferred qualifications for given job
    """    
    source_ls=source.split('QUALIFICATIONS') #in the source code this keyword is the best to be split on
    if len(source_ls) <3: #if there is no qualifications mentioned we skip this
        return 'No Qualifications Listed'
    quals=defaultdict()
    level={1:'basic',2:'preferred'} #this serves for dictionary later
    for i in range(1,3): #there are numerous ways that lists are generated in job descriptions, so we need everything to be accounted for
        if '\\xe2\\x80\\xa2' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0] #first split si done on longer keyword, since this one was problemtic. Second one is on line break
            first_repl=first_splt.replace('\\xe2\\x80\\xa2','') #list specific chars
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '\\xc2\\xb7' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0]
            first_repl=first_splt.replace('\\xc2\\xb7','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '\\xe2\\x97\\x8f' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0]
            first_repl=first_splt.replace('\\xe2\\x97\\x8f','').replace('\\xe2\\x80\\x99s','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '\\xe2\\x80\\x99s' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0]
            first_repl=first_splt.replace('\\xe2\\x80\\x99s','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '\\xe2\\x80\\x99' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0]
            first_repl=first_splt.replace('\\xe2\\x80\\x99','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '\\xe2\\x80\\x93' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0]
            first_repl=first_splt.replace('\\xe2\\x80\\x93','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '\xe2\x80\x99s' in source_ls[i]:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].rsplit('<br/>',1)[0]
            first_repl=first_splt.replace('\xe2\x80\x99s','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif 'CXT.CLIENT_SIDE_METRICS' in source_ls[i]: #this was a special case, where the lest wasn't ending as every other example
            first_splt=source_ls[i].rsplit('CXT.CLIENT_SIDE_METRICS')[0].rsplit('Amazon is an equal opportunities')[0]
            first_repl=first_splt.replace('\xe2\x80\x99s','')
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        elif '<ul>' not in source_ls[i]: #this was a case where the wasn't unordered list, but just some random listings
            first_splt=source_ls[i].replace('</h2><p>','').rsplit('Amazon is committed to a diverse')[0].split('<br/>')
            if '*' in first_splt[0]: #special case where list items were represented by '*'
                sub_s=[x for x in first_splt if '*' in x]
                first_repl=[x.replace('*','').strip() for x in sub_s]
            else:
                sub_s=first_splt
                first_repl=[x.replace('*','').strip() for x in sub_s]

            parsed=' '.join(first_repl)
            parsed=re.sub('<[^>]+>', '', first_repl).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
        else:
            first_splt=source_ls[i].rsplit('Amazon is committed to a diverse')[0].split('</ul>')[0]
            second_splt=first_splt.split('<li>')
            second_splt.pop(0)
            parsed=re.sub('<[^>]+>', '', second_splt).strip() #removing everything that is delimited by <>
            quals[level[i]]=parsed 
    return quals  

def extract_desc(source:str)->str:
    """Extract job description

    Args:
        source (str): string containing whole page source

    Returns:
        str: string containing job description
    """    
    source_ls=source.split('DESCRIPTION')
    if len(source_ls) <3: #if there is no description mentioned we skip this
        return 'No Description Listed'
    first_spl=source_ls[1].split('</p>')[0].replace('\\xe2\\x80\\x99s','').replace('</h2><p>','')
    parsed=first_spl.replace('\\xe2\\x80\\x99s','').replace('</h2><p>','').replace('<br/>','')
    return parsed

def extract_job_details(source:str)->dict:
    try:
        details=defaultdict()
        job_fam_split=source.split('jobDetails')
        job_fam=job_fam_split[1].split('category')[1].split(',')[0]
        details['job_family']=job_fam
        job_location_split=source.split('<div class="association location-icon">')
        job_loc=job_location_split[1].split('</div>')[0].split('>')[1]
        details['job_location']=job_loc
    except IndexError:
        return
    return details
