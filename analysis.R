require(data.table)
require(ggplot2)


dt.cc = fread("wikisource_chn_cc_year.csv")

p = ggplot(dt.cc[year<=1875], aes(x=year, y=charCount)) + geom_jitter()
ggsave("cc_year.pdf", plot=p, width=8, height = 4)