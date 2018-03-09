import numpy as np
import sys


def unpack(n,t,backpointer):
    # print backpointer
    # print t
    # print n

    i = n
    tags = []
    t=int(t)

    while(i >= 0):
        tags.append(t)
        #print backpointer[i][t]
        t = int(backpointer[i][t])
        i-=1

    tags.reverse()
    return tags


def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    #print "HIII"

    viterbi = np.zeros(shape=(N, L))
    backpointer = np.zeros(shape=(N, L))

    #initialization
    for i in range(L):
        #print "value of start :" + str(start_scores[i]) + "values of emission :" + str(emission_scores[0][i])
        viterbi[0][i] = start_scores[i]+emission_scores[0][i]


    #print viterbi

    for i in range(1,N):
        for t in range(L):
            viterbi[i][t] = -sys.maxint-1
            for t_d in range(L):
                tmp = viterbi[i-1][t_d]+trans_scores[t_d][t]
                if tmp > viterbi[i][t]:
                    viterbi[i][t] = tmp
                    backpointer[i][t] = t_d


            viterbi[i][t] = viterbi[i][t]+emission_scores[i][t]


    t_max = 0
    viterbi_max = -sys.maxint-1

    for t in range(L):
        if (viterbi[N-1][t]+end_scores[t]) > viterbi_max:
            t_max = t
            viterbi_max = (viterbi[N-1][t]+end_scores[t])

    #print viterbi
    #print backpointer

    tags = unpack(N-1,t_max,backpointer)
    s = viterbi_max


    '''
    y = []
    for i in xrange(N):
        # stupid sequence
        y.append(i % L)
    # score set to 0
    
    '''
    return (s, tags)



emission_scores = np.array([[0, 0, 0.7, 0, 0],
                            [0.4,0.1,0,0,0],
                            [0.1,0.9,0,0,0],
                            [0,0,0,1,0.1]
                            ])

trans_scores = np.array([   [0.2,0.4,0.01,0.3,0.04],
                            [0.3,0.05,0.3,0.2,0.1],
                            [0.9,0.01,0.01,0.01,0.07],
                            [0.4, 0.05, 0.4, 0.1, 0.05],
                            [0.1,0.5,0.1,0.1,0.1]])

start_scores = np.array([0.3,0.1,0.3,0.2,0.1])
end_scores = np.array([0.05,0.05,0,0,0.1])

#a,b = run_viterbi(emission_scores,trans_scores,start_scores,end_scores)

#print "score" + str(a)
#print "sequence :" + str(b)