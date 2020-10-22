library(tidyverse)
library(ggplot2)
library(scales)

### Tags ### 
tags <- read.csv("../data/sample.csv", header = FALSE)

# tag stats
tags <- tags %>%
  select(c(V1, V2, V3, V4)) %>%
  gather(CO, TAG, V2:V4)

tags <- tags %>% 
  group_by(TAG) %>%
  summarize(no_rows = length(TAG)) %>%
  arrange(desc(no_rows))


### Timemaps & CDX Main data ###
tmd <- read.csv("../data/timemaps_small.csv", header = TRUE)
cdx <- read.csv("../data/cdx_counts.csv", header = TRUE) %>%
  rename(cdx_count = count)

# Archive diversity
tmd %>% count(archive) %>% arrange(desc(n))

# CDX & Memento Distribution
tmd <- tmd %>% 
  left_join(cdx, by = "domain") 

tmd_dist <- tmd %>%
  group_by(domain, cdx_count) %>%
  count(domain) %>%
  rename(memento_count = n)

# Correlations
ggplot(tmd_dist, mapping = aes(x=log10(memento_count), y=log10(cdx_count))) +
  geom_point() +
  geom_smooth() +
  labs(x='Memento Count', y='CDX Count')

# Memento count
ggplot(tmd_dist, aes(x=reorder(domain,-memento_count), y=memento_count)) + 
  geom_bar(stat="identity") + 
  labs(x='Domain', y='Memento Count') +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# CDX count
ggplot(tmd_dist, aes(x=reorder(domain,-memento_count), y=cdx_count)) + 
  geom_bar(stat="identity") + 
  labs(x='Domain', y='CDX Count') +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  scale_y_continuous(labels = unit_format(unit = "M", scale = 1e-6))


### Tweets Main data ###
dt <- read.csv("../data/tweets_small.csv", header = TRUE)
dt <- dt %>%
  mutate(date = as.Date(date, "%Y-%m-%d", tz = "America/New_York"))

# How many URIs total there are
count(distinct(dt, domain))

##### TWEETS ####
# Count number of times a URL appears
most_tweets <- dt %>%
  group_by(domain) %>%
  filter(date > "2019-12-31") %>%
  group_by(domain) %>%
  count() %>%
  arrange(desc(n))

ggplot(most_tweets, aes(x=reorder(domain,n), y=n)) + 
  geom_bar(stat="identity") +
  # labs(title="Domains with most Tweets 2020") +
  xlab("Domain") +
  ylab("Count") + 
  coord_flip() + 
  theme_classic()

##### TWEET USERS ####
# Which users make up a percentage of the tweets
user_tweets <- dt %>%
  group_by(username) %>%
  count() %>%
  arrange(desc(n)) %>%
  mutate(percentage = n/length(dt$id))

# Binning users into count ranges
labels <- c("[0-1)", "[2-6)", "[6-10)", "[10-100)", "[100-1000)", "[1000-Inf)")
user_tweets <- user_tweets %>% 
  mutate( x_bins = cut(n, breaks = c(-Inf,1,6,10,100,1000,Inf), labels=labels))

ggplot(user_tweets, aes(x=x_bins)) +
  geom_bar(fill="seagreen4",color="white",alpha=0.9) + 
  stat_count(geom="text", aes(label=..count..), vjust=-0.5) +
  labs(x='User Tweet Counts Buckets', y='Count') +
  theme_minimal() 

# group domains & usernames
domain_totals <- dt %>% count(domain)
user_tweets <- dt %>% 
  count(username, domain) %>%
  # mutate(percent = count(domain)) %>%
  # mutate(percent = n / ) %>%
  arrange(username, n) %>%
  rename(twitter_username = username)
  

##### DOMAINS ####
# Filters on domain count
# top <- distinct(dt, domain) %>%
#   head(50)
# top <- dt %>%
#   filter(domain %in% top$domain) %>%
#   filter(date > "2019-12-31")
# 
# bottom <-distinct(dt, domain) %>%
#   tail(47)
# bottom <- dt %>% 
#   count(domain) %>%
#   # filter(domain %in% bottom$domain) %>%
#   arrange(desc(n)) %>%
#   filter(date > "2019-12-31")

# Heatmaps
# ggplot(top, aes(x=date, y=domain)) + 
#   geom_tile()
# 
# ggplot(bottom, aes(x=date, y=domain)) + 
#   geom_tile()

hmap_2020 <- dt %>% 
  filter(date > "2019-12-31") %>%
  add_count(domain)

ggplot(hmap_2020, aes(x=date, y=reorder(domain,n))) +
  geom_tile() +
  theme_classic() + 
  labs(x='Date', y='Domain')
