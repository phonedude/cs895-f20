import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(rc={'figure.figsize':(20,20)})
sns.set_theme(style='darkgrid')


def get_hist(data, type=None):
    if type is 'cap':
        sns.displot(data, kind='kde', bw_adjust=0.5)
        plt.title('Overall Complete Automation Probability')
        plt.savefig('cap.png', bbox_inches='tight')
    elif type is 'types':
        sns.displot(data)
        plt.title('Overall Complete Automation Probability')
    elif type is 'overall_scores':
        sns.displot(data, kind='kde', bw_adjust=0.25)
        plt.title('Overall Score')
    else:
        print('please use type=<cap, types, overall_scores>')
        return
    plt.xticks(rotation=45)
    plt.savefig('{}.png'.format(type), bbox_inches='tight')


with open('hashed.json') as f:
    accounts = json.load(f)

scores = []
types = []
display_scores = []
df = pd.DataFrame.from_dict(accounts).T

for account in accounts:
    if 'error' not in accounts[account].keys():
        if accounts[account]['user']['majority_lang'] is 'en':
            scores.append(accounts[account]['cap']['english'])
            if accounts[account]['cap']['english'] > 0.75:
                for type in accounts[account]['display_scores']['english']:
                    if type != 'overall':
                        if accounts[account]['display_scores']['english'][type] > 3:
                            types.append(type)
            display_scores = df['display_scores']['english']['overall']
        else:
            scores.append(accounts[account]['cap']['universal'])
            if accounts[account]['cap']['unverisal'] > 0.75:
                for type in accounts[account]['display_scores']['universal']:
                    if type != 'overall':
                        if accounts[account]['display_scores']['universal'][type] > 3:
                            types.append(type)
            display_scores = df['display_scores']['universal']['overall']
get_hist(scores, type='cap')
get_hist(types, type='types')
get_hist(display_scores, type='overall_scores')

