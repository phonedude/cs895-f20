# Will the @realDonaldTrump please stand up?

@realDonaldTrump is the official Twitter acocunt of the 45th President of the United States. It is a verified account created in March 2009 and has 87.2M followers. Trump issues policy from his tweets. There exist *fake* Trump accounts on Twitter, often for parody purposes. Due to misspellings and misunderstandings, Twitter users have mistaken these fake accounts for @realDonaldTrump. This project attempted to measure the reach of these fake accounts through the verified accounts that mentioned them.

## File listing

This repository consists of the following files:
* `WillTheRealDonaldTrumpPleaseStandUp.pptx` - the presentation for the CS895 Fall 202 class
* `dataset` - a directory containing all data gathered
  * `RealDonalDrumpf.json` - verified account tweets for @RealDonalDrumpf
  * `all-verified-accountids.txt` - all verified account IDs for accounts that mentioned a fake Donald Trump account
  * `all-verified-follower-account-info.jsonl` - Twitter API data for all verified account IDs for accounts that mentioned a fake Donald Trump account
  * `impersonation-policy.json` - [Carbon Date](http://carbondate.cs.odu.edu/) data for [Twitter's Impersonation Policy](https://help.twitter.com/en/rules-and-policies/twitter-impersonation-policy)
  * `parody-account-rules.json` - [Carbon Date](http://carbondate.cs.odu.edu/) data for [Twitter's Parody Accout Rules](https://help.twitter.com/en/rules-and-policies/parody-account-policy)
  * `reaDonaldTrump.json` - tweets containing mentions of [@reaDonaldTrump](https://twitter.com/reaDonaldTrump) from verified accounts
  * `realDonTrump.json` - tweets containing mentions of [@realDonTrump](https://twitter.com/realDonTrump) from verified accounts
  * `realDonaldT.json` - tweets containing mentions of [@realDonaldT](https://twitter.com/realDonaldT) from verified accounts
  * `realDonaldTramp.json` - tweets containing mentions of [@realDonaldTramp](https://twitter.com/realDonaldTramp) from verified accounts
  * `realDonaldTranp.json` - tweets containing mentions of [@realDonaldTranp](https://twitter.com/realDonaldTranp) from verified accounts
  * `realDonaldTrump.json` - tweets containing mentions of [@realDonaldTrump](https://twitter.com/realDonaldTrump) from verified accounts - Twint was cut off Twitter after ~7042 search results
  * `realDonaldTrunp.json` - tweets containing mentions of [@realDonaldTrunp](https://twitter.com/realDonaldTrunp) from verified accounts
  * `redonaldtrump.json` - tweets containing mentions of [@redonaldtrump](https://twitter.com/redonaldtrump) from verified accounts
* `notebooks` - a directory containing the [Jupyter](https://jupyter.org/) notebook used to generate the visualizations used in the presentation
  * `Verified Accounts Tweeting To Fake Trump Accounts.ipynb` - the [Jupyter](https://jupyter.org/) notebook used to generate the visualizations for the slides, along with some analysis that was abandoned and did not end up in the slides
* `scripts` - a directory of scripts used to process and download data
  * `get_twitter_account_info.py` - gets the account information for 100 twitter users at a time
  * `extract_data_to_tsv.py` - converts some of the JSON fields from twint into TSV output

## How the dataset was generated

The JSON datafiles were generated for different fake Trump accounts by [Twint](https://github.com/twintproject/twint) by using a command like the following:

`# twint -s @reaDonaldTrump --verified -o reaDonaldTrump.json --json`

The datafile `all-verified-follower-account-info.jsonl` was genenerated by:

1. running the script `extract_data_to_tsv.py` on each of these JSON files to produce a TSV file
2. running `awk -F $'\t' '{ print $3 }' *.tsv > all-verified-accountids.txt` on each of the TSV files, which is where that datafile comes from
3. splitting the dataset into sets of 100 each by `split -l 100 all-verified-accountids.txt`
4. running `get_twitter_account_info.py` on each set of 100 accounts and then combining the results with `cat`.

Steps 3 and 4 were necessary because the Twitter API only permits queries of 100 accounts at a time to its [Get users/lookup](https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup) service. 

## Running the Notebook

The file `Verified Accounts Tweeting To Fake Trump Accounts.ipynb` contains the code used to generate the visualizations in the presentation. It was run in a homebrew Python 3.8 environment on macOS 10.15.6. It has imports at the top for various libraries. To run it, you will need:
* [Jupyter](https://jupyter.org/)
* [Matplotlib](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.text.html)
* [wordcloud](https://github.com/amueller/word_cloud)
* [NLTK](https://www.nltk.org/)
* [Numpy](https://numpy.org/)
* [Tabulate](https://pypi.org/project/tabulate/)
* [Scipy](https://www.scipy.org/)

The notebook is very rough with few descriptions to cover the code. To produce the [chord diagram](https://www.data-to-viz.com/graph/chord.html) seen in slide 26, it must be run from [Jupyter Lab](https://blog.jupyter.org/jupyterlab-is-ready-for-users-5a6f039b8906) via `jupyter-lab`, not `jupyter notebook`.
