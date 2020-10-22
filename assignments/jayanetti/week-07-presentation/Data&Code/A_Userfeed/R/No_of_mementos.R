data = Final_data
freq <- table(data$mementos)
df <- as.data.frame(freq)

No_of_mementos$...1 <- factor(No_of_mementos$...1, levels = No_of_mementos$...1)
p <- ggplot(No_of_mementos, aes(No_of_mementos$...1, No_of_mementos$...2)) + geom_bar(stat="identity", colour = "#cd5c5c", , fill="#cd5c5c")+
  xlab("Number of Mementos") + ylab("Frequency") + labs (caption = "Based on data from MemGator") +
  ggtitle("Distribution of Number of Mementos for the Individual Posts", subtitle = "68.33% posts have 0 mementos!" ) +
  theme( plot.title = element_text(size = 30, face = "bold", colour = "#555555" ), plot.subtitle = element_text(size = 20, face = "bold", colour = "#555555" ) ) +
  scale_y_continuous(limits = c(0, 1200), expand = c(0,0), breaks = c(100,200,300,400,500,600,700,800,900,1000,1100,1200)) +
  scale_x_discrete(labels = c("0", "1", "2", "3", "4", "5", "6", "7", "8",  "9", "10","11-100", "101-200",  "201-300","301-400" ,"401-500", "501-600", "601-700", "701-800")) +                
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line = element_line(colour = "black"), axis.text.x = element_text( size = 12), axis.text.y  = element_text(size = 15), axis.title=element_text(size=25,face="bold"))

p



hist(data$mementos)
library("ggplot2")
#breaks = c(0,1,2,3,4,5,6,7,8,9,10,110,210,310,410,510,610,710,810)
breaks = c(0,1,2,3,4,5,6,7,8,9,10,210,410,610,810)
ggplot(data, aes(mementos)) +
  geom_histogram(aes(y=..density..),
                 color="black", fill="grey40", breaks=breaks) +
  scale_x_continuous(breaks=breaks)

barplot(No_of_mementos$...2)
