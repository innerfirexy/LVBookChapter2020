require(data.table)
require(ggplot2)
require(stringr)
require(dplyr)


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
#        word   ch1norm yearGroup wordLen
#     1:   之 28.129229    group1       1
#     2:   於 11.115711    group1       1
#     3:   而 16.235857    group1       1
#     4:   也  8.862605    group1       1
#     5:   曰 13.906273    group1       1
#    ---                                 
# 41681:   麋  2.734783    group9       1
# 41682:   醺  1.279642    group9       1
# 41683:   邏  2.876110    group9       1
# 41684:   澈  3.893485    group9       1
# 41685:   盏  2.256299    group9       1

dt.cnorms.len2
#         word  ch1norm  ch2norm yearGroup wordLen
#      1: 天下 23.96513 21.61901    group1       2
#      2: 不可 26.82893 22.53408    group1       2
#      3: 陛下 17.01623 21.61901    group1       2
#      4: 不能 26.82893 14.28710    group1       2
#      5: 朝廷 15.75091 10.10425    group1       2
#     ---                                         
# 204001: 愛君 17.50762 20.02632    group9       2
# 204002: 生机 27.26549 18.91319    group9       2
# 204003: 款式 22.72212 16.66585    group9       2
# 204004: 一源 32.20609 16.20178    group9       2
# 204005: 權行 34.42167 26.81774    group9       2

dt.cnorms.len3
#          word  ch1norm  ch2norm  ch3norm yearGroup wordLen
#     1: 会计师 15.99137 39.22816 12.60471    group1       3
#     2: 樞密院 22.75516 19.16593 24.49895    group1       3
#     3: 士大夫 25.67350 13.60612 18.40463    group1       3
#     4: 王安石 21.71546 16.20210 14.84477    group1       3
#     5: 軍節度 24.94672 16.82806 14.45265    group1       3
#    ---                                                    
# 17257: 礦產地 13.88551 25.06489 33.67128    group9       3
# 17258: 中國全 28.47364 42.91333 21.68737    group9       3
# 17259: 財產及 13.94514 25.06489 24.43055    group9       3
# 17260: 無所見 27.01165 26.82688 24.19416    group9       3
# 17261: 李春發 21.22027 16.42271 23.56733    group9       3

dt.cnorms.len4
#           word   ch1norm   ch2norm   ch3norm   ch4norm yearGroup wordLen
#    1: 审计工作 23.428506 39.228156 11.753285 15.614833    group1       4
#    2: 御史中丞 22.344590 19.690056 22.197392 17.340880    group1       4
#    3: 太皇太后 24.517013 23.607018 24.517013 16.962977    group1       4
#    4: 财务报表 13.370693 29.131133 24.108787 10.614163    group1       4
#    5: 审计报告 23.428506 39.228156 24.108787  8.898856    group1       4
#   ---                                                                   
# 3558: 萬壽聖節 28.604260  6.221004 17.741363 13.270659    group9       4
# 3559: 歐美學者 16.936803 17.120091 37.948945 34.235868    group9       4
# 3560: 夙兴夜寐  3.377830  8.413206 25.092624 10.818650    group9       4
# 3561: 公平交易 24.483013 17.402820 21.561293 16.307971    group9       4
# 3562: 崇壽禪院  8.975205  6.221004  9.443777 31.548748    group9       4


###
# Compute mean character norm
dt.cnorms.len1[, meanCharNorm := ch1norm][]
dt.cnorms.len2[, meanCharNorm := (ch1norm + ch2norm) / 2][]
dt.cnorms.len3[, meanCharNorm := (ch1norm + ch2norm + ch3norm) / 3][]
dt.cnorms.len4[, meanCharNorm := (ch1norm + ch2norm + ch3norm + ch4norm) / 4][]


###
# Models