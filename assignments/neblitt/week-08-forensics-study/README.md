# Examining the news media’s treatment of the COVID-19 death milestones

Upon encountering a tweet that suggested that the news media gave the 200,000 deaths milestone a diminished treatment from the 100,000 milestones, I decided to investigate if this was true.

## Workflow

1. Determined news sources to examine - equal number of left, center, and right based on a list from ["365 Dots in 2019: Quantifying Attention of News Sources"](https://arxiv.org/abs/2003.09989)

2. Determined when we reached 100,000 deaths and 200,000 deaths. Used data from 
Johns Hopkins University COVID-19 Dashboard and CDC COVID-19 Data Tracker. Used archive.is and Wayback Machine.

3. Inspected the captures from the Wayback Machine for each of the news sources near the dates determined in Step 2 to find the first occurrence of a milestone story. Results are in the `logs` folder

4. Identified and ranked the parts of the captures found. Consulted ["Measuring News Similarity Across Ten U.S. News Sites"](https://arxiv.org/abs/1806.09082) for ideas.

5. Treated the captures like search engine result pages and calculated Mean Reciprocal Rank (MRR), precision, and Normalized Discounted Cumulative Gain (nDCG) for each capture. Calculated MRR and precision by hand. Used a Jupyter notebook for nDCG (`Notebooks`). Instructions for using [sklearn.metrics.ndcg_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html).

