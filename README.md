NAME: NPS Popularity Monitoring - Group D1/2022-23

DESCRIPTION:
        The project provides set of function to run the dashboard for  analyzing the popularity of NPS


CONTENT:

## Data Sets

In order to use the dahsboard the inital datasets should be first downloaded from the
https://drive.google.com/file/d/1gCj0Ryc9wiOV1TBZyrJDHAIe8f3Lpejl/view?usp=sharing



## directory and file structure


├── code
│   └── scrapers
│       ├── drugsforum
│       ├── reddit
│       └── vendors
├── corpus
│   ├── forums
│   │   └── drugsforum
│   │       └── threads
│   └── trimbos
├── final_dashboard_D1
│   ├── assets
│   ├── data
│   └── nl_corpus
└── literature_review


In order to update data sets run the follwing:

		- [search-scraper.ipynb](./code/scrapers/reddit/search-scraper.ipynb)
		- [vendors](./code/scrapers/vendors)
		- [drugsforum-nl.py](./code/scrapers/drugsforum/drugsforum-nl.py) 
- corpus
	- [drugsforum](./corpus/forums/drugsforum)
