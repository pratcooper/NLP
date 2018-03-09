import distsim
import re
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

dict_relation = {}
rel_list = []
with open("word-test.v3.txt") as f:
    for line in f:
        if line.startswith("//"):
            continue
        if line.startswith(":"):
            if len(rel_list)!=0:
                dict_relation[key]=rel_list
            key = line[2:len(line)-1]
            rel_list = []
        else:
            #li= line.split(" ")
            li = re.split('\s+', line)
            newline=li[0]+" "+li[1]+" "+li[2]+" "+li[3]
            rel_list.append(newline)
if len(rel_list) != 0:
    dict_relation[key] = rel_list
#print dict_relation['currency']

dict_final_ans={}
for k,value in dict_relation.items():
    score_list=[0,0,0]
    print k
    for line in value:
        listofwords=line.split(' ')
        first_w=listofwords[0]
        second_w=listofwords[1]
        third_w=listofwords[2]
        fourth_w=listofwords[3]

        first = word_to_vec_dict[first_w]
        second = word_to_vec_dict[second_w]
        fourth = word_to_vec_dict[fourth_w]

        ret = distsim.show_nearest(word_to_vec_dict,
                                   first - second + fourth,
                                   set([first_w, second_w, fourth_w]),
                                   distsim.cossim_dense)
        '''
        if k == 'currency':
            for i in range(10):
                print ret[i][0]
            print "-----"
        '''

        for i in range(1):
            if third_w==ret[i][0]:
                score_list[0]+=1
        for i in range(5):
            if third_w==ret[i][0]:
                score_list[1]+=1
                break
        for i in range(10):
            if third_w==ret[i][0]:
                score_list[2]+=1
                break

    #print score_list
    score_list[0] = (float(score_list[0])/ len(value))*100
    score_list[1] = (float(score_list[1])/ len(value))*100
    score_list[2] = (float(score_list[2])/ len(value))*100
    print score_list

    dict_final_ans[k]=score_list

print "Final answer"
print dict_final_ans





