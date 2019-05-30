# Non parameric ANOVA with interaction
# Adam Hornsby, UCL Love Lab
# load in the rfit package
# install.packages('Rfit', repos = "http://cran.r-project.org")
library('Rfit')

args = commandArgs(trailingOnly=TRUE)

# Useful article: https://journal.r-project.org/archive/2016/RJ-2016-027/RJ-2016-027.pdf
# And: https://journal.r-project.org/archive/2012-2/RJournal_2012-2_Kloke+McKean.pdf

# library(car)
# read in the data
data = read.csv(args[1], header = TRUE)

# print the shape of the data
print(c('The shape of the dataset is: ', dim(data)))

# perform a normality test on the target variable
# i.e. shapiro-wilk test
data$SLIDER_P_DIR <- as.numeric(data$SLIDER_P_DIR)
shap = shapiro.test(data$SLIDER_P_DIR)
print(c('The results of the Shapiro-Wilk test: ', shap))

# format affiliation and vote as factors (2 levels)
data$VOTE_CONTRO_DIR <- as.factor(data$VOTE_CONTRO_DIR)
data$AFFILIATION <- as.factor(data$AFFILIATION)

# run a fligner-killeen test for homogoneity of variances
flig = fligner.test(SLIDER_P_DIR~interaction(VOTE_CONTRO_DIR, AFFILIATION), data=data)
print(c('The results of the Fligner-Killeen test', flig))

# run a Levene's test
#lev = leveneTest(SLIDER_P_DIR~VOTE_CONTRO_DIR*AFFILIATION, data=data)
# print(c('The results of the Levenes test', lev))
# run a non-parametric ANOVA
fit <- raov(SLIDER_P_DIR ~ VOTE_CONTRO_DIR + AFFILIATION, data=data)

# print(c('The results of the non-parametric ANOVA: ', fit$fit))
# fit
print(attributes(fit))
print(fit)

# calculate a qqplot
png(paste(args[2], 'qqplot.png', sep = "/"))
plot(qqnorm(residuals(fit)))
dev.off()

# create a two way interaction plot
png(paste(args[2], 'interaction.png', sep = "/"))
interaction.plot(data$VOTE_CONTRO_DIR, data$AFFILIATION, data$SLIDER_P_DIR)
dev.off()