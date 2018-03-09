import string
import nltk
from nltk.tokenize import word_tokenize

#num_syllables logic
#nltk.download('punkt')

e = """
An exceedingly fat friend of mine,
When asked at what hour he'd dine,
Replied, "At eleven,     
At three, five, and seven,
And eight and a quarter past nine

"""

line = """Replied, "At eleven,"""

#['Replied', ',', '``', 'At', 'eleven', ',']

line1 = """he can't read, tirth"""

# ['he', 'can't', 'read', '.']
#e=e.strip('\n')
tp = """He "Ab"""
#print nltk.tokenize.word_tokenize(tp)

def apostrophe_tokenize(line1):
    ans = []
    i = 0
    j = 0
    while j < len(line1):
        if line1[j] not in string.ascii_letters+"'":
            if i<j:
                ans.append(line1[i:j])
                i = j
            if line1[j] in (",",".",'"'):
                ans.append(line1[j])
                i = j+1
            while i<len(line1) and line1[i]==" ":
                i = i+1
        j += 1
    if(i!=len(line1)):
        ans.append(line1[i:len(line1)])
    return ans

def guess_syllable(word):
    word = word.lower()
    num_sylla = 0
    i=0
    while i<len(word):
        if word[i] in "aeiou":
            num_sylla += 1
            i+=1
            print "Inside"
            while i < len(word) and word[i] in "aeiou":
                i+=1
        else:
            i+=1
    return num_sylla


print apostrophe_tokenize(line1)

#print guess_syllable("heaeioullookkoooppp")