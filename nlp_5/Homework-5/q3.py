#!/usr/bin/env python
import distsim

# you may have to replace this line if it is too slow 
word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below
print(distsim.show_nearest(word_to_ccdict, word_to_ccdict['california'],set(['california']),distsim.cossim_sparse))

print(distsim.show_nearest(word_to_ccdict, word_to_ccdict['doctors'],set(['doctors']),distsim.cossim_sparse))

print(distsim.show_nearest(word_to_ccdict, word_to_ccdict['small'],set(['small']),distsim.cossim_sparse))

print(distsim.show_nearest(word_to_ccdict, word_to_ccdict['draw'],set(['draw']),distsim.cossim_sparse))

print(distsim.show_nearest(word_to_ccdict, word_to_ccdict['month'],set(['month']),distsim.cossim_sparse))

print(distsim.show_nearest(word_to_ccdict, word_to_ccdict['france'],set(['france']),distsim.cossim_sparse))

###Answer examples
distsim.show_nearest(word_to_ccdict, word_to_ccdict['jack'],set(['jack']),distsim.cossim_sparse)
