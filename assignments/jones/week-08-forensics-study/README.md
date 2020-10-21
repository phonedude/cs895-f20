# Will the @realDonaldTrump please stand up?

@realDonaldTrump is the official Twitter acocunt of the 45th President of the United States. It is a verified account created in March 2009 and has 87.2M followers. Trump issues policy from his tweets. There exist *fake* Trump accounts on Twitter, often for parody purposes. Due to misspellings and misunderstandings, Twitter users have mistaken these fake accounts for @realDonaldTrump. This project attempted to measure the reach of these fake accounts through the verified accounts that mentioned them.

## File listing

This repository consists of the following files:
* `WillTheRealDonaldTrumpPleaseStandUp.pptx` - the presentation for the CS895 Fall 202 class
* `dataset` - a directory containing all data gathered
  * `RealDonalDrumpf.json` - verified account tweets for @RealDonalDrumpf
  * `all-verified-accountids.txt` - all verified account IDs for accounts that mentioned a fake Donald Trump account
  * `all-verified-follower-account-info.jsonl` - Twitter API data for all verified account IDs for accounts that mentioned a fake Donald Trump account
  * `impersonation-policy.json` - Carbon Date data for Twitter's Impersonation Policy
  * `parody-account-rules.json` - Carbon Date data for Twitter's Parody Accout Rules
  * `reaDonaldTrump.json` - verified account tweets for @reaDonaldTrump
  * `realDonTrump.json` - verified account tweets for @realDonTrump
  * `realDonaldT.json` - verified account tweets for @realDonaldT
  * `realDonaldTramp.json` - verified account tweets for @realDonaldTramp
  * `realDonaldTranp.json` - verified account tweets for @realDonaldTranp
  * `realDonaldTrump.json` - some verified account tweets for @realDonaldTrump - Twint was cut off Twitter after ~7042 search results
  * `realDonaldTrunp.json` - verified account tweets for @realDonaldTrunp
  * `redonaldtrump.json` - verified account tweets for @redonaldtrump
* `notebooks` - a directory containing the Jupyter notebook used to generate the visualizations used in the presentation
  * `Verified Accounts Tweeting To Fake Trump Accounts.ipynb` - the Jupyter notebook used to generate the visualizations for the slides, along with some analysis that did not end up in the slides
* `scripts` - a directory of scripts used to process and download data
  * `get_twitter_account_info.py` - gets the account information for 100 twitter users at a time
  * `extract_data_to_tsv.py` - converts some of the JSON fields from twint into TSV output

## Generating the dataset

The JSON datafiles were generated for different fake Trump accounts by [Twint](https://github.com/twintproject/twint) by using a command like the following:

`# twint -s @reaDonaldTrump --verified -o reaDonaldTrump.json --json`

The datafile `all-verified-follower-account-info.jsonl` was genenerated by:

1. running the script `extract_data_to_tsv.py` on each of these JSON files to produce a TSV file
2. running `awk -F $'\t' '{ print $3 }' *.tsv > all-verified-accountids.txt` on each of the TSV files, which is where that datafile comes from
3. splitting the dataset into sets of 100 each by `split -l 100 all-verified-accountids.txt`
4. running `get_twitter_account_info.py` on each set of 100 accounts and then combining the results with `cat`.

Steps 3 and 4 were necessary because the Twitter API only permits queries of 100 accounts at a time to its [Get users/lookup](https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup) service. 

## Running the Notebook

The file `Verified Accounts Tweeting To Fake Trump Accounts.ipynb` contains the code used to generate the visualizations in the presentation. It was run in a homebrew Python 3.8 environment on macOS 10.15.6. It has imports at the top for various libraries, to run it, you will need:
* Jupyter
* Matplotlib
* wordcloud
* NLTK
* Numpy
* Tabulate
* Scipy


