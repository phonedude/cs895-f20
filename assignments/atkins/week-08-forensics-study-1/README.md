# Forensics Study 1

Google slides link:

- https://docs.google.com/presentation/d/1rqa2M-aC_iuZI7YvYB_hW_bVJUzS_ayaxdjHnFcLkdU/edit?usp=sharing

Slides also downloaded locally to this repo:

- [presentation1.pdf](./slides/Forensics%20Study%201.pdf)

## Data

In the data folder:

- **data/fake_news_sites.csv**: URIs identified as False misleading news sites originally collected by Melissa Zimdars (https://docs.google.com/document/d/10eA5-mCZLSS4MQY5QGb5ewC3VAL6pLkT53V_81ZyitM/preview)
- **data/sample_urirs.csv**: 100 Randomly sampled URIs from `data/fake_news_sites.csv`
- **data/timemaps/\*.json**: Timemaps taken from sampled URIs
- **data/tweets/*.csv**: Tweets collected via Twint contain that URI from the sample
- **data/*_small.csv**: Subset of the raw data taken from timemap, tweets, and cdx for the data we need to represent.

## Developer setup

Current working directory for running any of the provided code is expected to be `src`.

Requires pip3 & python3.
Install dependencies:

```
# Optional virtual environment (but good practice)
virtualenv -p python3 venv
. ./venv/bin/activate
# Required dependencies
pip3 install -r requirements
```

Docker dependencies:

```
docker pull oduwsdl/memgator:latest
docker container run -d --name=memgator-server -p 1208:1208 oduwsdl/memgator server
```
