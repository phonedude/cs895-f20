import botometer
import sys

accounts=open(sys.argv[1],'r').read().splitlines()


rapidapi_key = "7b06a0d6d4msh1a47b6d7478303ep1a20e8jsn85ea0902a712"
twitter_app_auth = {
    'consumer_key': 'IV4FVfxacULjFvMR12EgpIxII',
    'consumer_secret': 'z8E4N1XpxmonZ3ki4aYehNk20ERLUGkKdrMKPOsiqXL9PsZ6Po',
    'access_token': '264861144-6xgQhZNtSpOkTKNR6QBavbojpohl9DN89XZYrfXv',
    'access_token_secret': 'I2kQRkS2Pip3B49CtCNNvQ6bN4EYfmcMKFYhfgFuKV8Ct',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
# result = bom.check_account('@Jamierodr14')
# score= result["display_scores"]["english"]["overall"]
# print(score)
#print(type(result))
#Check a single account by id
#result = bom.check_account(1548959833)
#print(result)
# Check a sequence of accounts
#accounts = ['@clayadavis', '@onurvarol', '@jabawack']
for screen_name, result in bom.check_accounts_in(accounts):
	try:
		score = result['cap']['english']
		#score = result["display_scores"]["english"]["overall"]
		out=f'{screen_name}\t{score}'
		print(out)
	except:
		continue
    # Do stuff with `screen_name` and `result`