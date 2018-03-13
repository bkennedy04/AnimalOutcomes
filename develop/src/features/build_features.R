library(tidyr)
library(dplyr)
library(dummies)
library(lubridate)
library(nnet)
library(caret)


read_in_data <- function(path){
  train <- read.csv(paste(path,"/external/train.csv",sep = ''), strip.white = TRUE, na.strings=c("","NA"))
  test <- read.csv(paste(path,"/external/test.csv", sep = ''), strip.white = TRUE, na.strings=c("","NA"))
  train$Train <- rep(1) #to keep track of training and testing set
  test$Train <- rep(0)
  colnames(test)[1] <- "AnimalID" #rename ID column in test to match train ID column
  test$AnimalID <- as.character(test$AnimalID)
  df <- bind_rows(train, test)
  
  return(df)
}

data_cleansing <- function(df){
  
  #Create hasName feature
  hasName <- rep(NA, nrow(df))
  for(animal in 1:nrow(df)){
    if(is.na(df[animal, 2])){hasName[animal] <- 0}
    else{hasName[animal] <- 1}
  }
  df <- cbind(df, hasName)
  
  
  #split age into number and time unit column
  df <- separate(df, AgeuponOutcome, c("value", "timeunit"), sep = " ", fill = "right")
  
  #Convert age to same units (weeks)
  df$value <- as.numeric(df$value)
  df$ageWeeks <- NA
  for(animal in 1:nrow(df)){
    if((df[animal, "timeunit"] == 'year'| df[animal, "timeunit"] == 'years') & !is.na(df[animal, "timeunit"])){
      df[animal, "ageWeeks"] <- round(df[animal, "value"] * 52, 2)
    }
    else if((df[animal, "timeunit"] == 'month'| df[animal, "timeunit"] == 'months') & !is.na(df[animal, "timeunit"])){
      df[animal, "ageWeeks"] <- round(df[animal, "value"] * 4, 2) 
    }
    else if((df[animal, "timeunit"] == 'day'| df[animal, "timeunit"] == 'days') & !is.na(df[animal, "timeunit"])){
      df[animal, "ageWeeks"] <- round(df[animal, "value"] /7, 2)
    }
    else{
      df[animal, "ageWeeks"] <- round(df[animal, "value"], 2)
    }
  }
  
  #impute missing ages with mean 
  df$ageWeeks = ifelse(is.na(df$ageWeeks), mean(df$ageWeeks, na.rm = T), df$ageWeeks)
  
  #Create AnimalType dummy variables (can use just 1 in modeling as isCat or isDog)
  df <- cbind(df, dummy(df$AnimalType, sep = "_"))
  df$isDog <- df$df_Dog
  
  #Create isMix variable from Breed
  df$Breed <- as.character(df$Breed)
  df$isMix <- as.numeric(grepl("Mix", df$Breed, ignore.case = TRUE)) #may need to add in pattern for /
  
  #convert DateTime into DateTime
  df$DateTime <- strptime(x = as.character(df$DateTime), format = "%Y-%m-%d %H:%M:%S")
  
  #Extract datetime information
  df$year <- year(df$DateTime)
  df$month <- month(df$DateTime)
  df$weekday <- weekdays(df$DateTime)
  df$hourOfDay <- hour(df$DateTime)
  
  #Create isFixed variable 
  toMatch <- c("Neutered", "Spayed")
  matches <- sapply(toMatch, grepl, df$SexuponOutcome, ignore.case=TRUE)
  df$isFixed <- as.numeric(apply(matches, 1, any))
  
  #Create gender variable
  df <- separate(df, SexuponOutcome, c("fixed", "gender"), sep = " ", fill = "left")
  df$gender <- as.factor(df$gender)
  
  #Delete rows where gender = NA (only 1 obs. in df set)
  df <- df[!(is.na(df$gender)), ]
  
  #Look at top occuring breeds
  breeds <- as.data.frame(table(df$Breed))
  breeds <- breeds[order(-breeds$Freq),]
  row.names(breeds) <- NULL
  topbreeds <- breeds$Var1[1:30] #top 50 breeds
  df$newBreed <- (ifelse(df$Breed %in% topbreeds, df$Breed, "Other"))
  
  #Look at top colors
  colors <- as.data.frame(table(df$Color))
  colors <- colors[order(-colors$Freq),]
  row.names(colors) <- NULL
  topcolors <- colors[1:30, "Var1"] #top 50 colors
  df$newColor <- ifelse(df$Color %in% topcolors, df$Color, "Other")
  
  return(df)
}

output_final <- function(df){
  final <- c("AnimalID","OutcomeType", "hasName", "ageWeeks", "isDog", "isMix", "month", "weekday", "hourOfDay", "isFixed", "gender", "newBreed", "newColor", "Train")
  
  finaldf <- df[, colnames(df) %in% final]
  finaldf$hasName <- as.factor(finaldf$hasName)
  finaldf$isDog <- as.factor(finaldf$isDog)
  finaldf$isMix <- as.factor(finaldf$isMix)
  finaldf$isFixed <- as.factor(finaldf$isFixed)
  finaldf$weekday <- as.factor(finaldf$weekday)
  finaldf$newBreed <- as.factor(finaldf$newBreed)
  finaldf$newColor <- as.factor(finaldf$newColor)
  
  #split back into train and test sets
  final_train <- finaldf[finaldf$Train == 1, ]
  final_test <- finaldf[finaldf$Train == 0, ]
  
  
  features <- c("OutcomeType", "hasName", "ageWeeks", "isDog", "isMix", "month", "weekday", "hourOfDay", "isFixed", "gender", "newBreed", "newColor")
  trainset <- final_train[, colnames(final_train) %in% features]
  testset <- final_test[, colnames(final_test) %in% features]
  
  write.csv(trainset, file = paste(path,"/processed/trainset.csv", sep = ''), row.names = FALSE)
  write.csv(testset, file = paste(path,"/processed/testset.csv", sep = ''), row.names = FALSE)
}

path <- "../../data"
df <- read_in_data(path)
df <- data_cleansing(df)
output_final(df)
