# Forensics Study 2 - Analyzing the War over Diversity and Ethics in the AI Community
James Ecker

The code and data in this project were used to analyze activity of sockpuppets and the deletion of a Twitter account following a heated argument between two AI researchers regarding ethics in AI

Slides associated with this project are available on and in this repo as a Power Point presentation named [`Jim Ecker Forensics Study 2.pptx`](https://github.com/jim-ecker/cs895-f20/blob/master/assignments/Ecker/week-16-forensics-study-2/Jim%20Ecker%20Forensics%20Study%202.pptx)
# Requirements
python 3

Create a python 3 virtual environment and install the following python modules

`pip install botometer pandas tqdm json seaborn matplotlib` 

# Getting Botometer scores for blocked list accounts

botcheck.py

This script requires a list of Twitter handles named 'names.txt' In the interest of privacy I am not including the full list, and hashing that list would be unusable anyway. However, one can run this script and retrieve a JSON representation of each handle's scores from Botometer

## Prior to Utilizing Botometer
To begin using Botometer, you must follow the steps below before running any code:
1. Create a free [RapidAPI](https://rapidapi.com/) account.
2. Subscribe to [Botometer Pro](https://rapidapi.com/OSoMe/api/botometer-pro) on RapidApi by selecting a plan.
    > There is a completely free version (which does not require any credit card information) for testing purposes.
3. Create a Twitter application via https://developer.twitter.com/
    > Botometer utilizes the access credentials provided by Twitter for the application.
4. Ensure Botometer Pro's dependencies are already installed. 
    > See the [Dependencies](#dependencies) section for details.
    
Meanings of the elements in the response:

* **user**: Twitter user object (from the user) plus the language inferred from majority of tweets
* **raw scores**: bot score in the [0,1] range, both using English (all features) and Universal (language-independent) features; in each case we have the overall score and the sub-scores for each bot class (see below for subclass names and definitions)
* **display scores**: same as raw scores, but in the [0,5] range
* **cap**: conditional probability that accounts with a score **equal to or greater than this** are automated; based on inferred language

Meanings of the bot type scores:

* `fake_follower`: bots purchased to increase follower counts 
* `self_declared`: bots from botwiki.org
* `astroturf`: manually labeled political bots and accounts involved in follow trains that systematically delete content
* `spammer`: accounts labeled as spambots from several datasets
* `financial `: bots that post using cashtags
* `other`: miscellaneous other bots obtained from manual annotation, user feedback, etc.

For more information on the response object, consult the [API Overview](https://rapidapi.com/OSoMe/api/botometer-pro/details) on RapidAPI.


# Processing the Data

process.py

This script requires the JSON containing scores from Botometer. I have provided a hashed version of this data as 'hashed.json'

The script parses the json and generates three graphs:

* `Overall Scores`: a histogram using kernel density estimation showing the distribution of the overall bot scores in the data
* `Complete Automation Probability (cap)`: a histogram using kernel density estimation showing the distribution of the cap score, accounts with a score **equal to or greater than this** are automated; based on inferred language
* `Types`: a histogram showing the distribution of types of bots for accounts with high liklihood of being automated
