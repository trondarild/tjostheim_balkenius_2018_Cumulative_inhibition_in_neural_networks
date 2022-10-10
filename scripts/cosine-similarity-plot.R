###
library(mgcv)
library(ggplot2)
library(scales)
#plot(cos_sim_crp)
df0 <- read.csv("~/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/scripts/cos_sim_crp.csv")
df0 = df0[3:nrow(df0),]
#df1 <- read.csv("~/Code/ikaros/ik-t-tst/Source/UserModules/Models/CSOM-paper/scripts/cos_sim_crp_first350.csv")
#df1 = df1[3:nrow(df1),]
df = df0 #rbind(df1, df0)
#df = cos_sim_crp#[1:300,] #rms.diff.orig.constr# read.csv('~/Downloads/rms-diff-orig-constr.csv')
df$expit = df$it*5
df$it = log10(df$expit)

# create subsets for thinning
s1 = sample(1:300, 300, replace=FALSE)
s2 = sample(301:3000, 500, replace=FALSE)
s3 = sample(3001:30000, 500, replace=FALSE)
s4 = sample(30001:99990, 500, replace=FALSE)
subs = c(s1, s2, s3, s4)
df = df[subs,]
#a = df$it
#b = df$rms

# plot(a, b)
# plot(log(a), log(b))
# plot(a, log(b))
# plot(log(a), b)
# 
#plot(a, b, type = 'l')



# see http://www.fromthebottomoftheheap.net/2014/05/09/modelling-seasonal-data-with-gam/

#mod = gam(rms~s(it), data=df)
#plot(mod)

mod1 = gamm(rms ~ s(it), data = df)
#plot(mod1$lme)
#plot(mod1$gam)

# residual autocorrelation?
#layout(matrix(1:2, ncol = 2))
#acf(resid(mod1$lme), lag.max = 36, main = "ACF")
#pacf(resid(mod1$lme), lag.max = 36, main = "pACF")
#layout(1)

# correlated errors
#mod2 = gamm(rms ~ s(it), correlation = corARMA(form = ~ it, p = 1), data = df)
#plot(mod2$gam)
# mod3 = gamm(rms ~ s(it), correlation = corARMA(form = ~ it, p = 2), data = df)
#anova(mod1$lme, mod2$lme)

mod_chosen = mod1

#layout(matrix(1:2, ncol = 2))
#res = resid(mod_chosen$lme, type = "normalized")
#acf(res, lag.max = 36, main = "ACF - AR(2) errors")
#pacf(res, lag.max = 36, main = "pACF- AR(2) errors")
#layout(1)

f = predict(mod_chosen$gam, df, se.fit=T)
df$fit = f$fit
df$se = f$se.fit


mult_format <- function() {
  #function(x) format(10^x,digits = 4) 
  function(x) format(10**x, digits=1, scientific=FALSE) 
}


setEPS()
postscript("cosinesimil.eps", width = 7, height = 7)
point <- format_format(big.mark = " ", decimal.mark = ",", scientific = FALSE)
ggplot(df, aes(x = it, y = rms)) + 
  geom_point(col = 'gray70', alpha = 1) +
    geom_line(aes(x = it, y = fit)) +
  geom_hline(yintercept=0.83) + # add text - noise
  geom_text(aes(4.2, 0.83, label = "Noise", vjust = -1)) +
  geom_hline(yintercept=1.0) +
  geom_ribbon(aes(x = it, ymin = fit - 2 * se, ymax = fit + 2 * se), fill = 'gray20', alpha = 1) +
  ylab("Cosine similarity") + xlab("Iteration") +
  theme_bw() +
  theme(text = element_text(size=20)) +
  scale_x_continuous( labels = mult_format() ) 
  #scale_x_continuous(breaks = scales::trans_breaks("log10", function(x) 10**x),
  #                 labels = format(10**x, digits=1))# scales::comma_format(digits=1)) #+ trans_format("log10", scales::math_format(.x)) 
  #scale_y_continuous(breaks = scales::trans_breaks("log10", function(x) 10^x),
  #                   labels = scales::comma_format(digits=1)) + #scales::trans_format("log10", scales::math_format(.x)))+
  #annotation_logticks(scaled = FALSE)
dev.off()




