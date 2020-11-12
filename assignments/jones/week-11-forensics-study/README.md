# Spikes in 8chan Boards: the View from Web Archives

8chan has been connected to numerous incidents of violence. This is an analysis of 8chan boards to see if there is are spikes in activity around these events.

## File listing

This repository consists of the following files:
* `Spikes in 8chan Boards.pptx` - the in-class presentation of this work
* `timemaps/8ch-pol-timemap.json` - Memgator's TimeMap for 8chan's /pol/ board
* `timemaps/8ch.net-timemap.json` - Memgator's TimeMap for the 8chan boards page
* `timemaps/8chan.co-boards-timemap.json` - Memgator's TimeMap for the 8chan.co boards page (not used)
* `scripts/compute_board_rank.py` - script for extracting data from the 8chan boards page mementos, used to create `generated-data/boards-gendata-with-japanese.tar.gz`
* `scripts/download_8chan.co_boards_mementos.py` - script for downloading all mementos from the 8chan.co boards page (not used)
* `scripts/download_8kun_boards_mementos.py` - script for downloading all mementos from the 8ch.net boards page using `8ch.net-timemap.json` as input
* `scripts/download_8kun_pol_mementos.py` - script for downloading all mememntos from the /pol/ board using `8ch-pol-timemap.json` as input
* `scripts/remove-boilerplate_8kun_pol_mementos.py` - script for removing boilerplate from the /pol/ board mementos, used to create the data in `pol-mementos-noboilerplate.tar.gz`
* `generated-data/boards-gendata-with-japanese.tar.gz` - generated data from `scripts/compute_board_rank.py`
* `generated-data/pol-mementos-noboilerplate.tar.gz` - /pol/ boards with boilerplate removed
* `notebooks/8chan Boards Analysis-Final.ipynb` - analysis of different boards and events, some of which made it into `Spikes in 8chan Boards.pptx`
* `notebooks/Analysis of pol.ipynb` - analysis of the /pol/ board text overlap with Jaccard distance

## Running the Notebook

The files in `notebook` contain the code used to generate the visualizations used in the presentation. It was run in a homebrew Python 3.8 environment on macOS 10.15.7. It has imports for various libraires. To run them, you will need:
* [Jupyter](https://jupyter.org/)
* [Matplotlib](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.text.html)
* [distance](https://pypi.org/project/Distance/) (for Jaccard)
* [NLTK](https://www.nltk.org/)
* [Numpy](https://numpy.org/)
* [Pandas](https://pandas.pydata.org/)
