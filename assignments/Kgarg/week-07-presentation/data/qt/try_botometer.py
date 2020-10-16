import botometer
import sys

accounts=open(sys.argv[1],'r').read().splitlines()


rapidapi_key = ""
twitter_app_auth = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': '',
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
