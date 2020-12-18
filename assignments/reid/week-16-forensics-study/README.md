# Finding JennaMarbles’s Deleted/Private YouTube Videos
## Slides
https://docs.google.com/presentation/d/1AJHyH-hjWOVtUBr7FdMpziA7Y3YHNK8_FOT-P9-mrJs/edit?usp=sharing

## Dataset
known_video_URLs.txt: Videos from the live YouTube account.
videoSection_URI-Rs.txt: The URIs used to get the URI-Ms for the video section.
checkpoint_ExtractVideoURI-Rs.txt: Used if the ExtractURLs_archived_account.py program did not finish going through all of the URI-Ms on the first execution.
Slow_Loading_Webpages.txt: Archived video sections that took too long to load will be stored here.
privated_videos_Uri-Rs.txt: The URI-Rs for the private / deleted YouTube videos.
    
privated_videos_Uri-Ms.txt: The URI-Ms for the private / deleted YouTube videos.
categorized_privated_videos_Uri-Ms.txt: Each URI-R is at the beginning of a section of URI-Ms that should belong to the same video. There are some exceptions, so check for the 'v' parameter.
1-100_privated_videos_Uri-Ms.txt: Similar to categorized_privated_videos_Uri-Ms, except the videos are numbered and the first 100 videos are in this file.
101-200_privated_videos_Uri-Ms.txt: Similar to categorized_privated_videos_Uri-Ms, except the videos are numbered and the second set of 100 videos are in this file.
201-300_privated_videos_Uri-Ms.txt: Similar to categorized_privated_videos_Uri-Ms, except the videos are numbered and the third set of 100 videos are in this file.

## Scripts
ChromeDrivers: The web drivers used by the scripts.
ExtractURLs_live_account.py:  Gets the YouTube video URLs from a channel. I did not automate the scrolling, so this script requires the user to scroll the web page that is displayed.
ExtractURLs_archived_account.py: Gets the URI-Rs for the privated / deleted videos, when given a list of video section URI-Rs.
ExtractVideoURI-Ms.py: Gets the URI-Ms for the privated / deleted videos when given a list of video URI-Rs.

