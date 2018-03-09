#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
king = word_to_vec_dict['usa']
man = word_to_vec_dict['dollar']
woman = word_to_vec_dict['won']
ret = distsim.show_nearest(word_to_vec_dict,
                           king-man+woman,
                           set(['usa','dollar','won']),
                           distsim.cossim_dense)
print("usa : dollar :: {} : won".format(ret[0][0]))
