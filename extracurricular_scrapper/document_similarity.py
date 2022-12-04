import spacy
nlp = spacy.load('en_core_web_sm')
string1 = u'Hello hi there!'
string2 = u'Hello hi there!'
string3 = u'Hey whatsup?'
string4 = u'Hey whats the day looking like?'
string5 = u'Hey my name is'
doc1 = nlp(string1)
doc2 = nlp(string2)
doc3 = nlp(string3)
doc4 = nlp(string4)
doc5 = nlp(string5)

# print (doc1.similarity(doc2)) # 1.0
# print (doc2.similarity(doc3)) # 0.3977804622226361
# print (doc1.similarity(doc3)) # 0.3977804622226361
# print (doc1.similarity(doc4)) # 0.4393414342057937
# print (doc1.similarity(doc5)) # 0.29307694741965834

# Problem: How to make doc4 increase similarity from 0.29 to resemble doc 1
# Function that adds the other available strings (str 3 and str 4)and chooses which 
# one best complements str5 to resemble str1

def best_complement(base,target,list_possible_strings):
    """
    This function takes a base string and seeks to make it more cosine
    similar to the target string by adding to it a string from the 
    list_possible_strings
    """
    best_option = ""
    sim_score = 0
    doc_base = nlp(base)
    doc_target = nlp(target)
    doc_ideal = nlp(base + ' ' + target)
    print(doc_target.similarity(doc_base)) # Sanity check: better than original
    print(doc_target.similarity(doc_ideal)) # Sanity check: worse than ideal
    for i in list_possible_strings:
        doc_new = nlp(base + ' ' + i)
        new_sim_score = doc_target.similarity(doc_new) 
        if new_sim_score > sim_score:
            sim_score = new_sim_score
            best_option = i
            print(sim_score,best_option)

        # print(string1.similarity(i))
    # Sanity check, the output should be better than adding the target string or the base string
        #  Add the two desired strings, that would be ideal similarity
        # string_ideal = string1 + ' ' + string4
        # doc_ideal = nlp(string_ideal)
        # print (doc1.similarity(doc_ideal))

if __name__ == "__main__":
    list_possible_strings = [string3, string4]
    best_complement(string5,string1,list_possible_strings)
