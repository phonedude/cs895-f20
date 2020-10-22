# How well is Instagram archived? 
## A quantitative case study using Katy Perry’s Instagram account

### Slides

#### Link to the slides: https://docs.google.com/presentation/d/1Rp_0L7lpFgiAvd7y2p64O8NZRzw11fYHxBHlHQDssCY/edit?usp=sharing

### Data and Code

#### A. Userfeed

* Link to the HAR file in google drive: https://drive.google.com/file/d/1yJERZZeknkX5vIY3ZIW8ID-z4RQ8FzPd/view?usp=sharing
This contains the HAR data for Katy Perry's IG feed as of September 24th 2020.
(Unable to include it in github due to the file size limitation)

* A1_IGPostData/har_analyser.py: Extracts the shortcode,url,time,utc,likes,comments for each post
* A1_IGPostData/katy_perry_posts.csv: Data file
* A2_ Mementos/memento_analysis/Final_data.csv: Data file with the addition of memento count
* R: Data and code used for the plots

#### B. FollowerCount


* followecount.py: Extracts the follower count from each URI-M
* get_URIM_DT.py: To get the memento-datetime header value of the landing page for each URI-M
* KatyPerryTimeMap_Followers_Final.csv: Data file
* R: Data and code used for the plots


#### C. Account_IG_FB_Twitter

* memento_count.py: To calculate the number of mementos for FB, Twitter, and IG using MemGator.
