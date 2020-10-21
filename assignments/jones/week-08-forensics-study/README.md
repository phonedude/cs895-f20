# Will the @realDonaldTrump please stand up?

This repository consists of the following files:
* WillTheRealDonaldTrumpPleaseStandUp.pptx - the presentation for the CS895 Fall 202 class
* dataset - a directory containing all data gathered
* notebooks - a directory containing the Jupyter notebook used to generate the visualizations used in the presentation
* scripts - a directory of scripts used to process and download data

## Dataset

The JSON datafiles were generated for different fake Trump accounts by [Twint](https://github.com/twintproject/twint) by using a command like the following:

`# twint -s @reaDonaldTrump --verified -o reaDonaldTrump.json --json`

Each datafile is named after its corresponding fake Trump account:
* RealDonalDrumpf.json
* reaDonaldTrump.json
* realDonTrump.json
* realDonaldT.json
* realDonaldTramp.json
* realDonaldTranp.json
* realDonaldTrump.json
* realDonaldTrunp.json
* redonaldtrump.json

The datafile `all-verified-follower-account-info.jsonl` was genenerated by:

1. running the script `extract_data_to_tsv.py` on each of these JSON files to produce a TSV file
2. running `awk -F $'\t' '{ print $3 }' *.tsv > all-verified-accountids.txt` on each of the TSV files, which is where that datafile comes from
3. splitting the dataset into sets of 100 each by `split -l 100 all-verified-accountids.txt`
4. running `get_twitter_account_info.py` on each set of 100 accounts and then combining the results with `cat`.

Steps 3 and 4 were necessary because the Twitter API only permits queries of 100 accounts at a time to its [Get users/lookup](https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup) service. 

## Notebooks

The file `Verified Accounts Tweeting To Fake Trump Accounts.ipynb` contains the code used to generate the visualizations in the presentation. It was run in a homebrew Python 3.8 environment on macOS 10.15.6. It has imports at the top for various libraries, to run it, you will need:
* Jupyter
* Matplotlib
* wordcloud
* NLTK
* Numpy
* Tabulate
* Scipy

## Scripts

This directory contains the following scripts used to generate or download data for this project.
* `get_twitter_account_info.py` - gets the account information for 100 twitter users at a time
* `extract_data_to_tsv.py` - converts some of the JSON fields from twint into TSV output

The Dataset section covers how these scripts were used.
