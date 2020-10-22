import sys
import twitter
import jsonlines
import pprint

pp = pprint.PrettyPrinter(indent=4)

inputfile = sys.argv[1]
credentials_file = sys.argv[2]
outputfile = sys.argv[3]

accountids = []
credentials = {}

with open(inputfile) as f:

    for line in f:
        line = line.strip()
        accountids.append( int(line.split('\t')[0]) )

if len(accountids) > 100:
    print("only doing batches of 100")
    sys.exit(255)

with open(credentials_file) as f:

    for line in f:

        line = line.strip()
        key, value = line.split(':')
        credentials[key] = value.strip()

# for debugging
# pp.pprint(accountids)

api = twitter.Api(consumer_key=credentials['consumer_key'],
                  consumer_secret=credentials['consumer_secret'],
                  access_token_key=credentials['access_token'],
                  access_token_secret=credentials['access_token_secret']
                  )

userdata = api.UsersLookup(user_id=accountids, return_json=True)

with jsonlines.open(outputfile, 'w') as f:
    f.write_all(userdata)
