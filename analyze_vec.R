require(data.table)
require(ggplot2)
require(stringr)


dt.cc = fread("wikisource_chn_cc_year.csv")

p = ggplot(dt.cc[year<=1875], aes(x=year, y=charCount)) + geom_jitter()
ggsave("cc_year.pdf", plot=p, width=8, height = 4)


###
# Read word vector norms
rootFolder = "./data/group_year_span/100years_cutoff1951"
groups = Sys.glob(file.path(rootFolder,"group*"))
hyperParams = "cbow1_size300_cwetype1"

dt.wnorms = data.table()
for (grp in groups) {
    data.file = Sys.glob(file.path(grp, str_c("wordvec_", hyperParams, "*wordnorms.csv")))
    dt = fread(data.file)
    dt$yearGroup = basename(grp)
    dt.wnorms = rbindlist(list(dt.wnorms, dt))
}

##
# Character norms with word len = 1, 2, 3, 4
wordLen = 1
dt.cnorms.len1 = data.table()

for (grp in groups) {
    data.file = Sys.glob(file.path(grp, str_c("charvec_", hyperParams, "*charnorms_len", wordLen, ".csv")))
    dt = fread(data.file, skip = 1)
    dt$yearGroup = basename(grp)
    dt.cnorms.len1 = rbindlist(list(dt.cnorms.len1, dt))
}
dt.cnorms.len1$wordLen = 1