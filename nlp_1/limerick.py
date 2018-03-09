#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import string
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

#cmu_dict= nltk.corpus.cmudict.dict()
digits = re.compile('\d')
def has_digits(d):
    return bool(digits.search(d))


scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        #cmu_dict = self._pronunciations

    def num_syllables(self,word):
        word = word.lower()
        # If syllable not found in dict , return 1
        default_ans =  1
        if (word not in self._pronunciations):
            return default_ans
        else:
            pronun = self._pronunciations[word]
            num_syl = 1
            res = 100000
            for item in pronun:
                item = str(item)
                num_syl = sum(c.isdigit() for c in item)
                if (num_syl < res):
                    res = num_syl
            return res

    def rhymes(self,a, b):
        a = a.lower()
        b = b.lower()

        # calculate the normalized lists for each word-1
        if (a not in self._pronunciations or b not in self._pronunciations):
            return False

        vowels = ["A", "E", "I", "O", "U"]
        word1_pronounce = self._pronunciations[a]
        word2_pronounce = self._pronunciations[b]

        normalized_list1 = []
        for list in word1_pronounce:
            for item in list:
                if item[0] in vowels:
                    new_start_index = list.index(item)
                    normalized_list1.append(list[new_start_index:])
                    break

        result_normal_list = []

        normalized_list2 = []
        for list in word2_pronounce:
            for item in list:
                if item[0] in vowels:
                    new_start_index = list.index(item)
                    normalized_list2.append(list[new_start_index:])
                    break

        # Check two normalized lists for rhyme conditions
        '''
        size = no of sounds remaining in word prononciation after normalization.
        if size of both words equal 
        	then remaining sound should be equal.
        else 
        	smaller word sound should be suffix of larger. 
        '''

        for elem1 in normalized_list1:
            for elem2 in normalized_list2:
                size1 = len(elem1)
                size2 = len(elem2)
                # smaller word sound should be suffix of larger.
                if size1 == size2:
                    if str(elem1) == str(elem2):
                        return True
                elif (size1 > size2):
                    suffix = str(elem2)[1:]
                    if str(elem1).endswith(suffix):
                        return True
                elif (size1 < size2):
                    suffix = str(elem1)[1:]
                    if str(elem2).endswith(suffix):
                        return True

        return False

    def is_limerick(self, text):
        # rule 1 number of lines should be = 5
        lines = text.splitlines()

        #if (len(lines) != 5):
        #   return False
        #print lines

        list_of_tokelized_lines = []

        cnt = 0
        for line in lines:
            list_of_tokelized_lines.append(word_tokenize(lines[cnt]))
            cnt = cnt + 1

        #print 'token 1 : '
        #print list_of_tokelized_lines
        list_of_tokelized_lines = [x for x in list_of_tokelized_lines if x != []]

        #print 'token 2 : '
        #print list_of_tokelized_lines

        if (len(list_of_tokelized_lines) != 5):
            return False

        num_syl_in_lines = []

        for line in list_of_tokelized_lines:
            tot_syl = 0

            for word in line:
                if (word not in string.punctuation):
                    ans = self.num_syllables(word)
                    tot_syl = tot_syl + ans

            # if any line has  < 4 syllables then return false

            if (4 > tot_syl):
                return False

            num_syl_in_lines.append(tot_syl)

        syl_1 = num_syl_in_lines[0]
        syl_2 = num_syl_in_lines[1]
        syl_3 = num_syl_in_lines[2]
        syl_4 = num_syl_in_lines[3]
        syl_5 = num_syl_in_lines[4]

        if (not (abs(syl_3 - syl_4) <= 2)):
            return False

        if (not (abs(syl_1 - syl_2) <= 2 and abs(syl_1 - syl_5) <= 2 and abs(syl_2 - syl_5) <= 2)):
            return False

        min_A_syl = min(syl_1, syl_2, syl_5)

        if (min_A_syl < syl_4 or min_A_syl < syl_3):
            return False

        listlastwords = []
        last_word_compare_list = []

        for line in list_of_tokelized_lines:
            # comma case
            last_elem = line[-1]
            if (last_elem in string.punctuation):
                second_last_elem = line[-2]
                listlastwords.append(second_last_elem)
            else:
                listlastwords.append(last_elem)


        lastword_A1 = listlastwords[0]
        lastword_A2 = listlastwords[1]
        lastword_B3 = listlastwords[2]
        lastword_B4 = listlastwords[3]
        lastword_A5 = listlastwords[4]

        if (not (self.rhymes(lastword_B3, lastword_B4))) or (not (self.rhymes(lastword_A1, lastword_A2) and self.rhymes(lastword_A2, lastword_A5) and self.rhymes(lastword_A1,
                                                                                                  lastword_A5))):
            return False

        listA = []
        listA.append(lastword_A1)
        listA.append(lastword_A2)
        listA.append(lastword_A5)

        listB = []
        listB.append(lastword_B3)
        listB.append(lastword_B4)

        flag = 0

        for each1 in listB:
            for each2 in listA:
                if self.rhymes(each1, each2):
                    flag = 1


        if flag == 1:
            return False


        #if control reached here means , is_limerick is true :)
        return True

    def apostrophe_tokenize(self, line1):
        ans = []
        i = 0
        j = 0
        while j < len(line1):
            if line1[j] not in string.ascii_letters + "'":
                if i < j:
                    ans.append(line1[i:j])
                    i = j
                if line1[j] in (",", ".", '"'):
                    ans.append(line1[j])
                    i = j + 1
                while i < len(line1) and line1[i] == " ":
                    i = i + 1
            j += 1
        if (i != len(line1)):
            ans.append(line1[i:len(line1)])
        return ans

    def guess_syllable(self, word):
        word = word.lower()
        num_sylla = 0
        i = 0
        while i < len(word):
            if word[i] in "aeiou":
                num_sylla += 1
                i += 1
                #print "Inside"
                while i < len(word) and word[i] in "aeiou":
                    i += 1
            else:
                i += 1
        return num_sylla


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
