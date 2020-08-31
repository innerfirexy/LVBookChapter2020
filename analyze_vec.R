require(data.table)
require(ggplot2)
require(stringr)
require(dplyr)
require(patchwork)


# dt.cc = fread("wikisource_chn_cc_year.csv")
# p = ggplot(dt.cc[year<=1875], aes(x=year, y=charCount)) + geom_jitter()
# ggsave("cc_year.pdf", plot=p, width=8, height = 4)


###
# Read word vector norms
rootFolder = "./data/group_year_span/100years_cutoff1951"
groups = Sys.glob(file.path(rootFolder,"group*"))
# hyperParams = "cbow1_size300_cwetype1"
hyperParams = "cbow1_size300_cwetype1_data_shuf_sample"
# hyperParams = "cbow0_size300_cwetype1_data_shuf_sample"


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
dt.cnorms.len1$wordLen = wordLen
dt.cnorms.len1 = rename(dt.cnorms.len1, word = V1, ch1norm = V2)

wordLen = 2
dt.cnorms.len2 = data.table()
for (grp in groups) {
    data.file = Sys.glob(file.path(grp, str_c("charvec_", hyperParams, "*charnorms_len", wordLen, ".csv")))
    dt = fread(data.file, skip = 1)
    dt$yearGroup = basename(grp)
    dt.cnorms.len2 = rbindlist(list(dt.cnorms.len2, dt))
}
dt.cnorms.len2$wordLen = wordLen 
dt.cnorms.len2 = rename(dt.cnorms.len2, word = V1, ch1norm = V2, ch2norm = V3)

wordLen = 3
dt.cnorms.len3 = data.table()
for (grp in groups) {
    data.file = Sys.glob(file.path(grp, str_c("charvec_", hyperParams, "*charnorms_len", wordLen, ".csv")))
    dt = fread(data.file, skip = 1)
    dt$yearGroup = basename(grp)
    dt.cnorms.len3 = rbindlist(list(dt.cnorms.len3, dt))
}
dt.cnorms.len3$wordLen = wordLen 
dt.cnorms.len3 = rename(dt.cnorms.len3, word = V1, ch1norm = V2, ch2norm = V3, ch3norm = V4)

wordLen = 4
dt.cnorms.len4 = data.table()
for (grp in groups) {
    data.file = Sys.glob(file.path(grp, str_c("charvec_", hyperParams, "*charnorms_len", wordLen, ".csv")))
    dt = fread(data.file, skip = 1)
    dt$yearGroup = basename(grp)
    dt.cnorms.len4 = rbindlist(list(dt.cnorms.len4, dt))
}
dt.cnorms.len4$wordLen = wordLen 
dt.cnorms.len4 = rename(dt.cnorms.len4, word = V1, ch1norm = V2, ch2norm = V3, ch3norm = V4, ch4norm = V5)


###
# print
dt.cnorms.len1

dt.cnorms.len2

dt.cnorms.len3

dt.cnorms.len4


###
# Compute mean character norm
dt.cnorms.len1[, meanCharNorm := ch1norm][]
dt.cnorms.len2[, meanCharNorm := (ch1norm + ch2norm) / 2][]
dt.cnorms.len3[, meanCharNorm := (ch1norm + ch2norm + ch3norm) / 3][]
dt.cnorms.len4[, meanCharNorm := (ch1norm + ch2norm + ch3norm + ch4norm) / 4][]


###
# combine `meanCharNorm` column with the `norm` column in dt.wnorms
combineNormCols = function(dt.cnorms, dt.wnorms) {
    setkey(dt.cnorms, word, yearGroup)
    setkey(dt.wnorms, word, yearGroup)
    dt.combined = dt.cnorms[dt.wnorms, nomatch = 0]
    setnames(dt.combined, old = "norm", new = "wordNorm")
    dt.combined
}

dt.wcnorms.len1 = combineNormCols(dt.cnorms.len1, dt.wnorms)
dt.wcnorms.len2 = combineNormCols(dt.cnorms.len2, dt.wnorms)
dt.wcnorms.len3 = combineNormCols(dt.cnorms.len3, dt.wnorms)
dt.wcnorms.len4 = combineNormCols(dt.cnorms.len4, dt.wnorms)

# Add norm ration column
# charRatio = meanCharNorm / (meanCharNorm + wordNorm)
dt.wcnorms.len1[, charRatio := meanCharNorm / (meanCharNorm + wordNorm)]
dt.wcnorms.len2[, charRatio := meanCharNorm / (meanCharNorm + wordNorm)]
dt.wcnorms.len3[, charRatio := meanCharNorm / (meanCharNorm + wordNorm)]
dt.wcnorms.len4[, charRatio := meanCharNorm / (meanCharNorm + wordNorm)]


###
# Plot
p.len1 = ggplot(dt.wcnorms.len1, aes(x = yearGroup, y = charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange") + 
    theme_bw()

p.len2 = ggplot(dt.wcnorms.len2, aes(x = yearGroup, y = charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange") + 
    theme_bw()

p.len3 = ggplot(dt.wcnorms.len3, aes(x = yearGroup, y = charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange") + 
    theme_bw()

p.len4 = ggplot(dt.wcnorms.len4, aes(x = yearGroup, y = charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange") + 
    theme_bw()


###
# Find the common vocabulary between groups
commonVocab = function(dt.cnorms) {
    vocab = c()
    for (i in 1:9) {
        grp = stringr::str_interp("group${i}")
        subvocab = unique(dt.cnorms[yearGroup == grp]$word)
        if (i == 1) {
            vocab = subvocab
        } else {
            vocab = intersect(vocab, subvocab)
        }
    }
    vocab
}

cv.len1 = commonVocab(dt.cnorms.len1)
length(cv.len1) # 
length(unique(dt.cnorms.len1$word)) # 

cv.len2 = commonVocab(dt.cnorms.len2)
length(cv.len2) # 
length(unique(dt.cnorms.len2$word)) # 

cv.len3 = commonVocab(dt.cnorms.len3)
length(cv.len3) # 
length(unique(dt.cnorms.len3$word)) # 

cv.len4 = commonVocab(dt.cnorms.len4)
length(cv.len4) # 
length(unique(dt.cnorms.len4$word)) # 

cv.allLens <- c(cv.len1, cv.len2, cv.len3, cv.len4)

dt.wcnorms.len1$yearGroupInt <- as.integer(str_sub(dt.wcnorms.len1$yearGroup, start=6))
dt.wcnorms.len2$yearGroupInt <- as.integer(str_sub(dt.wcnorms.len2$yearGroup, start=6))
dt.wcnorms.len3$yearGroupInt <- as.integer(str_sub(dt.wcnorms.len3$yearGroup, start=6))
dt.wcnorms.len4$yearGroupInt <- as.integer(str_sub(dt.wcnorms.len4$yearGroup, start=6))


gg_color_hue <- function(n) {
    hues = seq(15, 375, length = n + 1)
    hcl(h = hues, l = 65, c = 100)[1:n]
}
FOUR_COLORS <- gg_color_hue(4)


###
# Plot with common vocabulary only
p.len1.cv = ggplot(dt.wcnorms.len1[word %in% cv.len1], aes(x = yearGroupInt, y = 1 - charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange", color=FOUR_COLORS[1]) + 
    geom_smooth(method = 'lm', linetype='dotted', color=FOUR_COLORS[1]) + 
    scale_x_discrete(limits=1:9) + 
    labs(y = "Semantic weight Omega", x = "Year group", title = "Word length = 1") + 
    theme_bw()
ggsave('Omega_yeargroup_len1_commonVocab.pdf', plot=p.len1.cv, width=5, height = 4)

p.len2.cv = ggplot(dt.wcnorms.len2[word %in% cv.len2], aes(x = yearGroupInt, y = 1 - charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange", color=FOUR_COLORS[2]) + 
    geom_smooth(method = 'lm', linetype='dotted', color=FOUR_COLORS[2]) + 
    scale_x_discrete(limits=1:9) + 
    labs(y = "Semantic weight Omega", x = "Year group", title = "Word length = 2") + 
    theme_bw()
ggsave('Omega_yeargroup_len2_commonVocab.pdf', plot=p.len2.cv, width=5, height = 4)

p.len3.cv = ggplot(dt.wcnorms.len3[word %in% cv.len3], aes(x = yearGroupInt, y = 1 - charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange", color=FOUR_COLORS[3]) + 
    geom_smooth(method = 'lm', linetype='dotted', color=FOUR_COLORS[3]) + 
    scale_x_discrete(limits=1:9) + 
    labs(y = "Semantic weight Omega", x = "Year group", title = "Word length = 3") + 
    theme_bw()
ggsave('Omega_yeargroup_len3_commonVocab.pdf', plot=p.len3.cv, width=5, height = 4)

p.len4.cv = ggplot(dt.wcnorms.len4[word %in% cv.len4], aes(x = yearGroupInt, y = 1 - charRatio)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange", color=FOUR_COLORS[4]) + 
    geom_smooth(method = 'lm', linetype='dotted', color=FOUR_COLORS[4]) + 
    scale_x_discrete(limits=1:9) + 
    labs(y = "Semantic weight Omega", x = "Year group", title = "Word length = 4") + 
    theme_bw()
ggsave('Omega_yeargroup_len4_commonVocab.pdf', plot=p.len4.cv, width=5, height = 4)


p.allLens.cv <- p.len1.cv | p.len2.cv | p.len3.cv | p.len4.cv
ggsave("Omega_yeargroup_alllens_commonVocab.pdf", plot=p.allLens.cv, width=16, height = 4)

p.allLens.cv <- (p.len1.cv | p.len2.cv) / (p.len3.cv | p.len4.cv)
ggsave("Omega_yeargroup_alllens_commonVocab_2by2.pdf", plot=p.allLens.cv, width=8, height = 8)


# combine all lens
dt.wcnorms.allLens <- rbindlist(list(
    dt.wcnorms.len1[, .(word, yearGroup, wordLen, charRatio)],
    dt.wcnorms.len2[, .(word, yearGroup, wordLen, charRatio)],
    dt.wcnorms.len3[, .(word, yearGroup, wordLen, charRatio)],
    dt.wcnorms.len4[, .(word, yearGroup, wordLen, charRatio)]
))
dt.wcnorms.allLens[, Omega := 1 - charRatio]

p.allLens.cv <- ggplot(dt.wcnorms.allLens[word %in% cv.allLens], aes(x = yearGroup, y = Omega)) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange", aes(color=as.factor(wordLen))) + 
    theme_bw()
ggsave("Omega_yeargroup_alllens_commonVocab.pdf", plot=p.allLens.cv, width=6, height=4)
# 区分不明显

p.allLens.cv <- ggplot(dt.wcnorms.allLens[word %in% cv.allLens], aes(x = yearGroup, y = Omega)) + 
    facet_grid(~ wordLen, scales = "free_y", shrink = FALSE) + 
    stat_summary(fun = mean, fun.data = mean_cl_boot, geom = "pointrange", aes(color=as.factor(wordLen))) + 
    theme_bw()
ggsave("Omega_yeargroup_alllens_commonVocab.pdf", plot=p.allLens.cv, width=10, height=3)


###
# Models