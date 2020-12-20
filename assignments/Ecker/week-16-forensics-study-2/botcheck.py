import botometer
import json
from tqdm import tqdm

rapidapi_key = ""
twitter_app_auth = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': '',
}
filename = 'checked.json'

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


with(open('names.txt', 'r')) as f:
    accounts = f.read().splitlines()
print('Saving data to {}'.format(filename))
with (open(filename, 'w')) as o:
    json.dump(
        {key: val for key, val in tqdm(bom.check_accounts_in(accounts), total=len(accounts))},
        o,
        indent=4
    )
print('Done!')