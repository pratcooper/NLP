import re

word = "lilac+ing"

#traffic+ing  = trafficking

#(ruleLHS, ruleRHS)  = ("(.+)e\+([^ei].*)", "\\1e\\2")
(ruleLHS, ruleRHS)  = ("(.*)([aeiou])c\+(ed|ing)", "\\1\\2ck\\3")

word = re.sub("^" + ruleLHS + "$", ruleRHS, word)

word = re.sub("\+","", word)

print word