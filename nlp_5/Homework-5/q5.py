#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['california'],set(['california']),distsim.cossim_dense))

print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['doctors'],set(['doctors']),distsim.cossim_dense))

print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['small'],set(['small']),distsim.cossim_dense))

print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['draw'],set(['draw']),distsim.cossim_dense))

print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['month'],set(['month']),distsim.cossim_dense))

print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['france'],set(['france']),distsim.cossim_dense))

###Answer examples
print(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['jack'],set(['jack']),distsim.cossim_dense))
