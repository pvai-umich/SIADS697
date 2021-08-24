# MADS Capstone Project (SIADS697) Readme

This is the github repository for our Capstone SIADS 697 project, part of the MADS program at the University of Michigan.

Our project is relatively straightforward: create a web-based application that helps a user plan towards a more desired career. The problem we are  hoping to solve is that many people looking towards the next step of their career have little information to help guide them. Either they are not sure what steps they need to take, or they might not know what their dream job even is!

Our web application would solve both of these problems. Using data collected from online job postings, the user’s LinkedIn profile, and a user-provided description of their interests and strengths, we utilize natural language processing to predict an ideal job as well as identify the skills that are missing from the user’s skillset. 

Our team decided to build an end-to-end solution that had a viable model not just deployed in Jupyter but also on a public endpoint. This was possible because of the free AWS credits generously provided by our teaching staff. 

This github repo contains the underlying scripts that analyzed input data, as well as generated any necessary pickle files that would be used by the web application. The we application code does not sit in this github repo. Much of the work was done with Google Colab, which integrates really well with Github, and helped our team collaborate more effectively.

We pulled our data from Kaggle, so rather than store data on the github repo, we pull directly from there. The scripts that accomplish this can be found in the Data Folder.

The scripts that explored data, trained models, and wrote pickle files can be found in the Scripts folder.

The pickle files and other core data files that are used directly by the web app can be found in the Output folder.

Overall our team found this project to be very challenging and rewarding. The scope and trajectory of the project changed over the course of the project timeline. Constant communication between team members was critical to ensuring success. We really enjoyed the opportunity to work with real data. In fact, we now understand and respect how much work actually goes into data cleaning and preprocessing. This ended up being ok since our solution could be proven out with a standard supervised learning model.

Having this as a last milestone to graduation really enabled our group to build relationships and apply what we have learned. It was a great experience and opportunity for us to be creative with our solution design.
