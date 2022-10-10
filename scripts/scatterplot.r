# read error files
files <- list.files(path="./tmp", pattern="error_C2_COIL_C1_alpha=0.0001_C1_rf_size=7_C1_rf_inc=1_C1_som_size=4_C2_alpha=0.0001_C2_rf_size=7_C2_rf_inc=1_C2_som_size=4_61-162.out_dec", full.names=T, recursive=FALSE)
lapply(files, function(x) {
  print(x)
  t <- read.table(x, header=T) # load file
  # apply function
  title = x
  # write to file
  colnames(t)[1] <- "time"
  colnames(t)[2] <- "error"
  plt = ggplot(t,aes(x=time,y=error)) + 
    geom_point(alpha = 0.01) +
    ggtitle(title) +
    guides(color = guide_legend(override.aes = list(alpha = 1)))
  #print(plt)
  png(file=paste(x, ".png", sep=""), width=600)
  print(plt)
  dev.off()
  
  #TODO add all data to same dataframe with data as separate columns - 
})

# TODO
# extract median and avg etc from each, put into table