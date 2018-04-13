#DPLYR library example

#dataset<-read.csv('D:/Study/Machine_Learning/Libraries/dplyr/sampledata.csv')
library(dplyr)
library(downloader)
url <- "https://raw.githubusercontent.com/genomicsclass/dagdata/master/inst/extdata/msleep_ggplot2.csv"
filename <- "msleep_ggplot2.csv"
if (!file.exists(filename)) download(url,filename)
msleep <- read.csv("msleep_ggplot2.csv")
head(msleep)

str(msleep)

summary(msleep)

sleepData <- select(msleep, name, sleep_total)
head(sleepData)

#select command 
select(msleep,genus,order)
select(msleep,name:awake)
select(msleep,-name)


#filter command
filter(msleep,order=="Carnivora",bodywt<=20.0)

# Pipe(%>%) Operator
msleep%>%
  select(order)%>%
  head

#mutate command
msleep%>%
  mutate(col1=bodywt*2)
