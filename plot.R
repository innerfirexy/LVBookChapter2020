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
sd.wcount = sd(d.wcount$wordCount)

mean.ccount = mean(d.ccount$charCount)
sd.ccount = sd(d.ccount$charCount)

mean.vsize = mean(d.vsize$vocabSize)
sd.vsize = sd(d.vsize$vocabSize)

d.comb.clean  = d.comb %>%
    filter(between(wordCount, mean.wcount - 2*sd.wcount, mean.wcount + 2*sd.wcount)) %>%
    filter(between(charCount, mean.ccount - 2*sd.ccount, mean.ccount + 2*sd.ccount)) %>%
    filter(between(vocabSize, mean.vsize - 2*sd.vsize, mean.vsize + 2*sd.vsize))
d.comb.clean = data.table(d.comb.clean)
d.combm.clean = melt(d.comb.clean, id.vars = "year", variable.name = "Statistics")


### Plot
p.scatter = ggplot(d.combm.clean[year<=1950], aes(x=year, y=value)) + 
    geom_point(aes(color=Statistics, shape=Statistics)) + 
    geom_smooth(aes(color=Statistics, linetype=Statistics))

p.jitter = ggplot(d.combm.clean[year<=1950], aes(x=year, y=value)) + 
    geom_jitter(aes(color=Statistics, shape=Statistics)) + 
    geom_smooth(aes(color=Statistics, linetype=Statistics))

p.smooth = ggplot(d.combm.clean[year<=1950], aes(x=year, y=value)) + 
    geom_jitter(aes(color=Statistics, shape=Statistics)) + 
    geom_smooth(aes(color=Statistics, linetype=Statistics))