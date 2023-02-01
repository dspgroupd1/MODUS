# NPS Popularity Monitoring & Analysis

**Group D1/2022-23**

 **Description**:  The project provides set of function to run the dashboard for  analyzing the popularity of NPS


# CONTENT:

## Data Sets

In order to use the dahsboard the inital datasets should be first downloaded from the  
https://drive.google.com/file/d/1gCj0Ryc9wiOV1TBZyrJDHAIe8f3Lpejl/view?usp=sharing




## directory and file structure

```
├── code   		- code of scrapers and different tools  
│   ├── scrapers  
│   |   ├── drugsforum  
│   |   ├── reddit  
│   |   └── vendors
│   └── analysis
|       └── drugsforum
|
├── corpus              - output from drug forums  
│   ├── forums  
│   │   └── drugsforum  
│   │       └── threads  
│   └── trimbos  
├── final_dashboard_D1 - dashboard   
│   ├── assets  
│   ├── data  
│   └── nl_corpus  
└── literature_review  - list of reviewed articles and there contents 
```
In order to run the dashboard, run the following command:  
``` python final_dashboard_D1/dashboard.py ```

In order to update data sets run the following:   
    reddit update      : ```python code/scrapers/reddit/reddit-scraper.ipynb```   
    list of nps update : ```python code/scrapers/vendors/combine_csv.ipynb```  
    drugsforum.nl update  : ```cd final_dashboard_D1/nl_corpus | python drugsforum-nl.py```


