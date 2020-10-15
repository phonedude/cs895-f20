#!/bin/bash

status_id=$1
MYURL='https://twitter.com/realDonaldTrump/status/'$status_id

curl -s https://web.archive.org/cdx/search/cdx?url=$MYURL | awk -F" " '$5=="200" && $7> 40000 {print}' | cut -d" " -f2 > URMs$status_id


while read DT; do
	#echo $DT
	URM='https://web.archive.org/web/'$DT'/'$MYURL
	curl -s $URM > temp$status_id.html
	eng=$(grep 'class="ProfileTweet-actionCount" data-tweet-stat-count=' temp$status_id.html| head -3| cut -d'"' -f4 | tr '\n' ' ' )
	#TL=$(grep 'Tombstone-label' temp$status_id.html| wc -l)
	echo $DT' '$eng >> engage$status_id
	if test -z "$eng"; then
		break
	fi	
	grep ^'" data-tweet-id=' temp$status_id.html >> replies$status_id

done < URMs$status_id

rm -r temp*
rm -r URMs*