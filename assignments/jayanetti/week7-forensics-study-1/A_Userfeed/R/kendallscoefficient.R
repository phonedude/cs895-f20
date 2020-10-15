rank = ranking
a = unclass(cor.test(as.numeric(rank$rank_likes), as.numeric(rank$rank_mementos), method="kendall"))
print(a)

b = unclass(cor.test(as.numeric(rank$rank_comments), as.numeric(rank$rank_mementos), method="kendall"))
print(b)

c = unclass(cor.test(as.numeric(rank$rank_likes), as.numeric(rank$rank_comments), method="kendall"))
print(c)

d = unclass(cor.test(as.numeric(rank$rank_engagement), as.numeric(rank$rank_mementos), method="kendall"))
print(d)
