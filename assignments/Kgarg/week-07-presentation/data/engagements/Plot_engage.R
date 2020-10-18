

library(readr)
library(ggplot2)
library(reshape2)

  df <- read_table2("RA/895/labeled_trump_tweets/engagements/engage1313449844413992961", 
                   col_types=cols(Time=col_datetime(format = "%Y%m%d%H%M%S")))
  
  
  meltdf <- melt(df,id="Time")

  ggplot(meltdf,aes(x=Time,y=value,colour=variable,group=variable)) + 
    geom_line(size=1)+
    ylab("Engagements") +
    theme(legend.title=element_blank())+
    theme(legend.position="top") +
    theme(axis.line = element_line(color = 'black'),
          panel.background = element_blank()) +
    ggtitle("Engagements with Trump's covid-19 misinfo tweet before label")
