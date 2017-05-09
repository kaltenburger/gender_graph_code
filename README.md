## Replication code: "Bias and variance in the social structure of gender"


### Directions

This repository set-up assumes that the FB100 (raw .mat files) and Add Health datasets have been acquired and are saved the data/original folder. Here are the directions:

    1) Save raw files in following folders: 
        * FB100 .mat files in data/original/fb_100/  
        * Add Health files in data/original/add_health/cd/
    2) Update file paths to your local directory settings in the following programs:
        * code/0_analyze_FB100_AddHealth/a_convert_add_health_pajek_to_gml.R - line 6
        * code/0_analyze_FB100_AddHealth/b_Case Study -- Amherst and AddHealth23 Figures.ipynb -- line 6, set fb_100 variable, and set add_health_file variable
        * code/0_analyze_FB100_AddHealth/d_All -- process all FB100 Schools and Add Health Schools.ipynb - line 5, set fb_file variable, set Add Health path 
    3) Run code which is briefly described below:
        * 0_analyze_FB100_AddHealth/ - includes all relevant FB100 and Add Health processing
            - a_convert_add_health_pajek_to_gml.R: 


### Documentation

This repository contains all the correponding code to replicate the figures in "Bias and variance in the social structure of gender". We provide links to the datasets (Facebook100 and AddHealth) in the data sub-folder. 

### Authors
* Kristen M. Altenburger, kaltenb@stanford.edu
* Johan Ugander, jugander@stanford.edu
