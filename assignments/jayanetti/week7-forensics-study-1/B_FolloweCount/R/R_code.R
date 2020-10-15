install.packages("ggplot2")
install.packages("scales")
library(ggplot2)
library(scales)


d = DateTimeVsFollowers
d$...1 <- as.Date(d$...1, format = '%a, %d %b %Y %H:%M:%S')
sorted <- d[order(d$...1),]
data = na.omit(sorted)
#plot(data$...1, data$...2,main="Follower Growth: Katy Perry Account", xlab="Year", ylab="Number of Followers (million)")

colnames(data) <- c("date", "followers")

p <-ggplot(data, aes(x=date, y=followers)) + 
  geom_line(size =1, colour = "grey") + 
  geom_point(size =2, colour = "#E5310C") +
  labs(  x="Month, Year", y="Number of Followers (million)", caption = "Based on data collected through web archives") +
  ggtitle("Follower Count Growth") +
  scale_x_date(date_labels = "%b, %Y", breaks = breaks_pretty(30))+
  theme(axis.text.x = element_text(angle=90, vjust = 0.5, size = 15), axis.text.y = element_text(size = 15), axis.title=element_text(size=20,face="bold"), plot.title = element_text(size = 30, face = "bold", colour = "#555555" ))+ 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line = element_line(colour = "black"))

p
