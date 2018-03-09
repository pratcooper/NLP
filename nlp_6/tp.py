import pickle
import os
import io

fav_color = {}

cwd = os.getcwd()
for filename in os.listdir(cwd + "/data/lexicon/"):
    with open(cwd + "/data/lexicon/"+filename, "r") as ins:
        array_set = set()
        for line in ins:
            line = line.strip()
            for word in line.split(" "):
                word = word.rstrip()
                array_set.add(word)
	fav_color[str(filename)] = array_set


pickle.dump(fav_color, open("save.p", "wb"))


favorite_color = pickle.load(open( "save.p", "rb" ))