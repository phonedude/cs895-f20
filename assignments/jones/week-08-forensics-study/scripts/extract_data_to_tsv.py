import sys
import jsonlines

inputfile = sys.argv[1]
outputfile = sys.argv[2]
target = sys.argv[3]


out = open(outputfile, 'w')

out.write(
    "{}\t{}\t{}\t{}\t{}\t{}\n".format(
        "created-at",
        "username",
        "user_id",
        "replies_count",
        "retweets_count",
        "likes_count"
    )
)

with jsonlines.open(inputfile) as f:

    for obj in f:

        if '@' + target.lower() in obj['tweet'].lower():

            tweet_time = obj['created_at']
            account_name = obj['username']
            account_id = obj['user_id']
            replies = obj['replies_count']
            retweets = obj['retweets_count']
            likes = obj['likes_count']

            out.write(
                "{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    tweet_time,
                    account_name,
                    account_id,
                    replies,
                    retweets,
                    likes
                )
            )

        else:
            print('@' + target + " not in tweet: {}".format(obj['tweet']))
