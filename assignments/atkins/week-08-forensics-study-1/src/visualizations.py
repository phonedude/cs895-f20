import pandas as pd
import seaborn as sns
import csv
import json
from data_collection import slugify

# Globals
sns.set_theme(style="darkgrid")


def draw_alive_status():
    data = pd.read_csv("../data/sample_alive.csv", header=None)
    data.fillna(0, inplace=True)


    print(data.head())
    # plot = sns.displot(data=data.rename(columns=lambda x: str(x)), x="3", col="3", kde=True)
    plot = sns.countplot(x="3", data=data.rename(columns=lambda x: str(x)))
    plot.set(xlabel='Status Code', ylabel='Count', title="Live Web Statuses")
    fig = plot.get_figure()
    fig.savefig("../slides/alive.png")



def draw_tweet_coverage():
    """
    docstring
    """
    # chart.set_xticklabels(rotation=65, horizontalalignment='right')
    print()


def draw_tweet_bar_chart(slug):
    """
    docstring
    """
    print()


def draw_timemap_coverage(slug):
    df = None
    with open("../data/timemaps/" + slug + ".json") as f:
        js = json.load(f)
        mementos = js.get("mementos", {}).get("list", [])
        orig = js.get("original_uri")
        df = pd.io.json.json_normalize([{
            "original_uri": orig,
            "mementos": mementos
        }], 'mementos', ['original_uri'])
        df['datetime'] =  pd.to_datetime(df['datetime'], format='%Y-%m-%dT%H:%M:%SZ')
        df['original_uri'].value_counts()
        # df = pd.read_json(f)
        df



if __name__ == "__main__":
    draw_alive_status()
    # with open("../data/sample_alive.csv") as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         domain = row[0]
    #         urir = row[1]
    #         final_urir = row[2]
    #         status_code = row[3]
    #         draw_timemap_coverage(slugify(domain))
