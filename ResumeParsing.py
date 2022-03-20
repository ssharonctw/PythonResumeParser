#!/usr/bin/env python
# coding: utf-8

# In[1]:


#load all packages required for the project
import spacy #for nlp
import pdfminer #pdf to txt
import re #regex
import os #file manip
import pandas as pd #csv - tabular
import pdf2txt #converting pdf to  txt


# In[2]:


#converting pdf to  txt
#this function takes one argument: the file name
def convert_pdf(f):
    #1. Creating output filename 
    #parsed through name.pdf -> name.txt
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    
    #2. Creating output filepath
    #the folder in the same directory is output/txt/ 
    #so add output file name after the folder
    output_filepath = os.path.join("output/txt/", output_filename)
    
    #3. convert the input pdf to output txt with pdf2txt
    #pdf2txt main function takes [intputFileName, outputFile, outputFilepath]
    #convert pdf to txt and save it in the given location
    pdf2txt.main(args=[f, "--outfile", output_filepath]) 
    print(output_filepath + " saved successfully!!!")
    
    #4. return the outputted file in read mode
    return open(output_filepath, encoding="utf-8").read()


# In[3]:


# load the language model
nlp = spacy.load("en_core_web_sm")


# In[4]:


#Creating place holder for output
#a.k.a. dictionary structure which stores the four key info (4 columns)
result_dict = {'name': [], 'phone': [], 'email': [], 'skills': []} 
names = []
phones = []
emails = []
skills = []


# In[5]:


#To parse the content and store in output placeholder
def parse_content(text):
    
    #annotate before using spacy for entity identifying
    doc = nlp(text)
    
    #1. Get name 
    #use list comprehension to replace for loop
    #whenever recognized entity is person, then return the entity.text
    #name are assumed to be the first name detected
    name = [entity.text for entity in doc.ents if entity.label_ is "PERSON"][0]
    print(name)
    
    #2. Get email
    #list comprehension to replace for loop
    #whenever recognized word is email, then return the word
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    
    #3. Find all skills that matches
    # change all to lower case first to resolve case issues (normalizing)
    skillset = re.compile("python|java|sql|hadoop|tableau") #define regex
    skills_list = re.findall(skillset, text.lower()) #pass defined reges into findAll
    #convert multiples to set, since we don't want duplicate values for the same skill
    #and then convert the sets to string
    unique_skills_list = str(set(skills_list)) 
    
    #4. Use regex to identify phone_num
    # change all to lower case first to resolve case issues
    phone_num = re.compile(
        "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )#define regex
    phone = str(re.findall(phone_num, text.lower()))#pass defined reges into findAll, and conver to string object
    
    
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfully!!!")


# In[6]:


#list all files in the resume folder
#iterate through all resumes that are pdf
for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
        print('Reading.....' + file)
        txt = convert_pdf(os.path.join('resumes/',file))
        parse_content(txt)


# In[7]:


result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email'] = emails
result_dict['skills'] = skills
#print(result_dict)


# In[8]:


#convert the dictionary to pandas dataframe to store to csv
result_df = pd.DataFrame(result_dict)
result_df


# In[9]:


result_df.to_csv('output/csv/parsed_resumes.csv')

