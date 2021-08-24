# MADS Capstone Project (SIADS697)

### Michael Zerman, Petras Vaiciunas, Keegan Heilman

Final Product:
http://3.228.107.175/


## Introduction
This is the github repository for our Capstone SIADS 697 project, part of the MADS program at the University of Michigan.

Our project is relatively straightforward: create a web-based application that helps a user plan towards a more desired career. The problem we are  hoping to solve is that many people looking towards the next step of their career have little information to help guide them. Either they are not sure what steps they need to take, or they might not know what their dream job even is!

Our web application would solve both of these problems. Using data collected from online job postings, the user’s LinkedIn profile, and a user-provided description of their interests and strengths, we utilize natural language processing to predict an ideal job as well as identify the skills that are missing from the user’s skillset. 

Our team decided to build an end-to-end solution that had a viable model not just deployed in Jupyter but also on a public endpoint. This was possible because of the free AWS credits generously provided by our teaching staff. 


## The Data

The initial plan for the project was to utilize three sources of data to build the web application

The first would be a set of online job postings from a variety of online career firms. We wanted to utilize the job description and job title from these data sets to train a classification model. The job description would be transformed into a set of pre-processed tokens that could be then  used to predict the job title. 

The second would be a web-scraped LinkedIn profile. Given a user-provided Linked url, we would take the data and identify what skills the user possesses. These could then be compared against the set of skills we had identified from the composite job description that is associated with the user’s predicted job title. The gap between the two would be part of the output, and would identify what skills need to be developed by the user.

And the third would be a user-provided description of themselves in paragraph form. This would be processed in the same way as the job description from the job title prediction model to create a set of tokens. These tokens would be fed into the job title prediction model to generate an “optimal” job for the user. This job title would in turn be used to predict the skills gap that exists given the user’s linkedin profile


## The Model
Our team decided that data cleaning and preprocessing would have the largest payoffs in terms of application success. The problem boils down to a relatively simple multiclass classification problem; given a description of what a user’s strengths and goals are, classify them into one of multiple job titles. Given this straightforward problem, we felt there was a larger payoff in ensuring the input data was the best it could be, rather than spending more time on training and parameterizing an overly complicated deep learning model. Something as simply as logistic regression was more than enough. 


## What's Inside
This github repo contains the underlying scripts that analyzed input data, as well as generated any necessary pickle files that would be used by the web application. The we application code does not sit in this github repo. Much of the work was done with Google Colab, which integrates really well with Github, and helped our team collaborate more effectively.

We pulled our data from Kaggle, so rather than store data on the github repo, we pull directly from there. The scripts that accomplish this can be found in the Data Folder.

The scripts that explored data, trained models, and wrote pickle files can be found in the Scripts folder.

The pickle files and other core data files that are used directly by the web app can be found in the Output folder.


## Reflection
Overall our team found this project to be very challenging and rewarding. The scope and trajectory of the project changed over the course of the project timeline. Constant communication between team members was critical to ensuring success. We really enjoyed the opportunity to work with real data. In fact, we now understand and respect how much work actually goes into data cleaning and preprocessing. This ended up being ok since our solution could be proven out with a standard supervised learning model.

Having this as a last milestone to graduation really enabled our group to build relationships and apply what we have learned. It was a great experience and opportunity for us to be creative with our solution design.
