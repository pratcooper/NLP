import distsim


word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
#cali = word_to_vec_dict['california']

for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['dance'], set(['dance']), distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))