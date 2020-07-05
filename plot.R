require(ggplot2)
require(data.table)
require(dplyr)


### Read data
# word count per year
d.wcount = fread("wikisource_chn_word_count_year.csv")

# char count per year
d.ccount = fread("wikisource_chn_cc_year.csv")

# vocab size per year
d.vsize = fread("wikisource_chn_vocab_size_year.csv")

# combine
d.comb = cbind(d.wcount, d.ccount$charCount, d.vsize$vocabSize) %>%
    rename(charCount = V2, vocabSize = V3)

d.combm = melt(d.comb, id.vars = "year", variable.name = "Statistics")


# deal with outliers
mean.wcount = mean(d.wcount$wordCount)
sd.wccount = sd(d.wcount$wordCount)



### Scatterplot
p.scatter = ggplot(d.combm[year<=1980], aes(x=year, y=value)) + 
    geom_point(aes(color=Statistics, shape=Statistics)) + 
    geom_smooth(aes(color=Statistics, linetype=Statistics))