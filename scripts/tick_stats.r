# summarize ticks and seconds
summary(ticks$ticks)
summary(ticks$seconds/3600)
summary(ticks$ticks/ticks$seconds)

plot(ticks$ticks, col=ticks$input_type)
plot(ticks$seconds, col=ticks$input_type)
plot(ticks$ticks, ticks$seconds, col=ticks$input_type)

d <- density(ticks$seconds) # returns the density data 
plot(d) # plots the results



library(ggplot2)
ggplot(ticks, aes(x =ticks, fill = input_type)) + geom_density(alpha = 0.5)
ggplot(ticks, aes(x =seconds, fill = input_type)) + geom_density(alpha = 0.5)

ggplot(ticks, aes(x =ticks/seconds, fill = input_type)) + geom_density(alpha = 0.5)

hist(ticks$ticks)
