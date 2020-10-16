#!/bin/bash

while read status_id; do
	./extract.sh $status_id
done < labelledtweet_ids.txt
