library("ggplot2", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")

# plot scatter and fit model to data

# read data
dat = cos_sim

# plot
plot(
  dat, 
  frame.plot=FALSE, # don't show frame
  col = plot_colors[1], # color to use
  ann=FALSE, # don't use the automatic annotation/label of axes
  axes=TRUE) # don't use the automatic axes numbering

dat["it"] = 10*dat["it"]

dat$it_log = log(dat$it)
model1=lm(rms~it_log, data=dat)
plot(model1)

model2=lm(rms~it_log+I(it_log^2), data=dat)

anova(model1, model2)
dat$fit = fitted(model2)

model3 = glm(rms~it_log, family = e
setEPS()
postscript("rmsdiff-it-log-log.eps")
# ggplot
ggplot(dat, aes(x=it,y=rms)) + 
  geom_point(color="#999999") +
  #stat_smooth(method = 'nls', formula = 'y~a*x^b', start = list(a = 80444,b=0.012),se=FALSE,size=2,color='#333333') +
  #stat_smooth(method = 'lm', start = list(a = 80444,b=0.012),se=FALSE,size=2,color='#333333') +
  geom_line(aes(x=it, y=fit)) +
  guides(color = guide_legend(override.aes = list(alpha = 1))) + # override alpha on legend
  #theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black")) +
  theme(axis.title.x = element_text(size=14),
          axis.text.x  = element_text(size=12,color="#000000")) +
  theme(axis.title.y = element_text(size=14),
        axis.text.y  = element_text(size=12,color="#000000")) +
  scale_x_log10("Iteration") +
  scale_y_continuous("RMS difference")
  #ylab("RMS difference") + xlab("Iteration")
  # ggtitle("")

dev.off()