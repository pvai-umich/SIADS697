import sys
import os
import zipfile
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models.phrases import Phrases, Phraser
from gensim.parsing.preprocessing import preprocess_string,strip_punctuation, strip_multiple_whitespaces, remove_stopwords, stem_text, STOPWORDS, strip_numeric, strip_tags
sys.path.insert(0,'/usr/lib/chromium-browser/chromedrive')
from selenium.webdriver import ChromeOptions
from selenium import webdriver
import bs4 as bs
import urllib.request
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import re






# define LinkedIn login function
def login_linkedin(driver):
    """
    input: {selenium webdriver} initialized webdriver
    return: {selenium webdriver} webdriver after performing LinkedIn login
    
    """
    driver.get ("https://www.linkedin.com")

    ## SCRAPER ACCOUNT INFORMATION (email and password REQUIRED)
    driver.find_element_by_id("session_key").send_keys("") # # REQUIRED EMAIL FOR LINKEDIN ACCOUNT TO BE USED FOR SCRAPING
    driver.find_element_by_id("session_password").send_keys("") # REQUIRED PASSWORD FOR LINKEDIN ACCOUNT TO BE USED FOR SCRAPING
    # Login using LinkedIn's sign-in form submit button
    driver.find_element_by_class_name("sign-in-form__submit-button").send_keys(Keys.RETURN)
    return driver

# define LinkedIn profile scraper
def scrape_linkedinprofile(linkedinprofile_URL):
    """
    input: {string object} LinkedIn profile URL
    return: {webdriver.page_source object} LinkedIn profile page source
    
    """
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless') ## disable to launch Chrome instance in foreground
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver = login_linkedin(driver)
    driver.get(linkedinprofile_URL)
    # sleep for 10s for page to ensure load
    time.sleep(10)
    
    source = driver.page_source
    driver.quit()
    return source

# define text tokenizer
def clean_tokenize_text(df, column):
    """
    input: {pandas DataFrame, string object} dataframe with text to be tokenized in column name provided
    return: {pandas DataFrame} dataframe with appended 'tokens' and 'stem_tokens' columns
    
    """
    CUSTOM_STOP_WORDS = ['â¢', 'â', 'â', 'â¢', 'â','®', '�',
                         '\\u200','comment','connect','message','\\xa0',
                         'share','mo','month','follow','report',
                         'block','profile','yr','year','date',
                         'contact','jan','january','feb','february',
                         'mar','march','apr','april','may','jun',
                         'june','jul','july','aug','august','sep',
                         'sept','september','oct','october','nov',
                         'november','dec','december','yddscsgylniquit',
                         'srmysiridmcwdydzygf'
                        ]
    CUSTOM_STEM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_numeric, stem_text]
    CUSTOM_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_numeric]
    tokens = []
    s_tokens = []
    stem_tokens = []
    s_stem_tokens = []
    for s in df[column]:
        tokens = preprocess_string(s, CUSTOM_FILTERS)
        tokens = [x for x in tokens if len(x) > 1]
        
        stem_tokens = preprocess_string(s, CUSTOM_STEM_FILTERS)
        stem_tokens = [x for x in stem_tokens if len(x) > 1]
        
        s_stem_tokens.append(stem_tokens)
        s_tokens.append(tokens)
    df['tokens'] = s_tokens
    df['stem_tokens'] = s_stem_tokens
    return df

if __name__ == '__main__':
    print('Starting script...')
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('linkedinprofile_URL', help='LinkedIn User Profile URL')
    parser.add_argument('selected_job_title', help='Selected Job Title')
    args = parser.parse_args()
    
    ## Scrap LinkedIn Profile
    ### linkedin profile url provided by user
    ### linkedinprofile_URL = 'https://ca.linkedin.com/in/lanamois' # EXAMPLE STRING OF THE USER INPUT.
    # call linkedin profile scraper
    source = scrape_linkedinprofile(args.linkedinprofile_URL)
    # parse linkedin profile source via Beautiful Soup 
    bsoup = bs.BeautifulSoup(source, 'lxml')
    # locate linkedin profile's Experience via class name as BeautifulSoup object
    linkedin_experience = bsoup.find_all(class_ = "background-details")
    # provide text attribute of the BeautifulSoup object (this should contain the user's linkedin profile's experience)
    profile_source = linkedin_experience[0].text


    ## Import Indeed Dataset as Pandas Dataframe
    # path to indeed-job-posting-dataset.zip
    path = '/home/friend/Documents/UM-MADS/courses/697_capstone/' # PATH TO CHANGE. 
    # filename of indeed job postings ZIP file ('indeed-job-posting-dataset.zip')
    filename = 'indeed-job-posting-dataset.zip'
    # unzip indeed job postings file
    with zipfile.ZipFile(f'{path}{filename}', 'r') as zip_ref:
        zip_ref.extractall(f'{path}')
    # filename of indeed job postings CSV file ('home/sdf/marketing_sample_for_trulia_com-real_estate__20190901_20191031__30k_data.csv')
    indeed_csv = 'home/sdf/marketing_sample_for_trulia_com-real_estate__20190901_20191031__30k_data.csv'
    # create dataframe of indeed job postings
    dat_indeed = pd.read_csv(f"{path}{indeed_csv}")


    ## Obtain Job Titles
    # copy 'Job Title' series to new variable
    job_titles = dat_indeed['Job Title']
    # user-selected job title
    ### selected_job_title = 'Enterprise Account Executive' EXAMPLE STRING OF THE USER INPUT
    # obtain index of user-selected job title
    job_title_idx = list(job_titles).index(f'{args.selected_job_title}')


    ## Parse LinkedIn page source for relevant information
    profile = pd.DataFrame({'resume': [bs.BeautifulSoup(profile_source, "lxml").text.replace('\n', ' ')]})
    # obtain job description of user-selected job
    job =  pd.DataFrame({'job_description': [bs.BeautifulSoup(dat_indeed.loc[job_title_idx,'Job Description'], "lxml").text.replace('\n', ' ')]})


    ## Obtain available skills set from skills files. These files should be saved to same path as the Indeed job postings ZIP file
    # list of skill set filenames
    skills_text_files = ['Skills.txt',
                        'Education, Training, and Experience.txt',
                        'Knowledge.txt',
                        ]
    # create dataframe of skill sets                
    skills = pd.DataFrame()
    for filename in skills_text_files:
        df_temp = pd.read_csv(f'{path}{filename}', delimiter = "\t")
        if ('Element Name' in df_temp.columns):
            df_temp['Commodity Title'] = df_temp['Element Name']
            df_temp.rename(columns={'Element Name':'Example'}, inplace = True)
        df_temp = df_temp[['Example', 'Commodity Title']]
        skills = pd.concat([skills, df_temp])


    ## Tokenize both LinkedIn profile and Job Description of Selected Job
    # Extract tokens of the LinkedIn profile, the job description, and the skills list
    profile = clean_tokenize_text(profile.copy(), 'resume')
    job = clean_tokenize_text(job.copy(), 'job_description')
    skills = clean_tokenize_text(skills.copy(), 'Example')
    # create a set of both profile and job stem tokens
    profile_stem_tokens = set(profile.loc[0,'stem_tokens'])
    job_stem_tokens = set(job.loc[0,'stem_tokens'])
    # #create list of skill tokens, combining multiple tokens, if necessary, to form phrases
    # skills_phrases = []
    # for technology_skill in skills['stem_tokens']:
    #     skill_phrase = []
    #     if len(technology_skill) == 1:
    #         skill_phrase.append(technology_skill[0])
    #     else:
    #         for idx, token in enumerate(technology_skill):
    #             if idx < len(technology_skill)-1:
    #                 skill_phrase.append(token +'_' + technology_skill[idx+1])
    #     skills_phrases.append(skill_phrase)   
    # skills['stem_tokens'] = skills_phrases    

    skills_exp = skills.explode('stem_tokens')
    skills_stem_tokens = list(skills_exp['stem_tokens'].unique())

    ## Identify skills (skills_stem_tokens) from the job description (job_stem_tokens) NOT found in the user's LinkedIn profile (profile_stem_tokens)
    job_skills = []
    missing_skills = None

    for j_stem_token in job_stem_tokens:
        
        if j_stem_token not in profile_stem_tokens:
            # if job description token NOT FOUND in linkedin profile.
            
            if j_stem_token in skills_stem_tokens: 
                # if job desription token IS FOUND in general skills.
                
                # append job description token to the list of skills found in the job description,
                #   but not found in the linked in profile.
                job_skills.append(j_stem_token)
                        
    # create mask for skills DataFrame where Truth=SKILL_NOT_FOUND_IN_LINKEDIN_PROFILE, False=SKILL_NOT_IN_JOB_DESCRIPTION_OR_SKILL_FOUND_IN_LINKEDIN_PROFILE
    skills_mask = skills_exp['stem_tokens'].isin(job_skills)

    ## Return missing skills
    missing_skills = list(skills_exp.loc[skills_mask, 'Commodity Title'].explode().unique())
    # missing_skills = list(skills_exp.loc[skills_mask, 'tokens'].explode().unique())
    print(missing_skills) ## List of missing skills, handle as needed
