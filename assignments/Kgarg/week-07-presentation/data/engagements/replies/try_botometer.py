import botometer
import sys

accounts=open(sys.argv[1],'r').read().splitlines()


rapidapi_key = "8cce39894bmshd0dd52aa2f81053p1a8f4bjsn0a3ed51c5118"
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
#result = bom.check_account('@clayadavis')

#Check a single account by id
#result = bom.check_account(1548959833)
#print(result)
# Check a sequence of accounts
#accounts = ['@clayadavis', '@onurvarol', '@jabawack']
for screen_name, result in bom.check_accounts_in(accounts):
	print(result)
    # Do stuff with `screen_name` and `result`