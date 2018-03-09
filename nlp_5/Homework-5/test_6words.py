#!/usr/bin/env python
import distsim
word_to_ccdict = distsim.load_contexts("nytcounts.4k")
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['dance'], set(['dance']), distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))