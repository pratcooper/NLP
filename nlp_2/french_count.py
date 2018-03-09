import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():

    f = FST('french')

    f.add_state('start')

    #states
    f.add_state('dig1zero')
    f.add_state('dig2zero')
    f.add_state('f_dig3')
    f.add_state('dig2_one')
    f.add_state('state5')
    f.add_state('state6')
    f.add_state('dig2_two')
    f.add_state('dig2_three')
    f.add_state('dig2_four')
    f.add_state('dig2_five')
    f.add_state('dig2_six')
    f.add_state('dig2_sev')
    f.add_state('dig2_eig')
    f.add_state('dig2_nine')
    f.add_state('dig1_nzero')
    f.add_state('sec_last')
    f.add_state('last')
    f.add_state('p1')
    f.add_state('p2')
    f.add_state('p3')

    f.initial_state = 'start'
    f.set_final('start')
    f.set_final('f_dig3')
    f.set_final('state5')
    f.set_final('state6')
    f.set_final('dig2_two')
    f.set_final('dig2_three')
    f.set_final('dig2_four')
    f.set_final('dig2_five')
    f.set_final('dig2_six')
    f.set_final('dig2_sev')
    f.set_final('dig2_eig')
    f.set_final('dig2_nine')
    f.set_final('last')
    f.set_final('p1')
    f.set_final('p2')
    f.set_final('p3')
    f.set_final('sec_last')

    # case for 09X
    f.add_arc('dig1zero', 'dig2_nine', '9', ())
    f.add_arc('dig2_nine', 'dig2_nine', '0', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]] + [kFRENCH_TRANS[10]])
    for k in range(1, 7):
        f.add_arc('dig2_nine', 'dig2_nine', str(k), [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]] + [kFRENCH_TRANS[k + 10]])
    for k in range(7, 10):
        f.add_arc('dig2_nine', 'dig2_nine', str(k), [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]] + [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[k]])

    # case for 08X
    f.add_arc('dig1zero', 'dig2_eig', '8', ())
    f.add_arc('dig2_eig', 'dig2_eig', '0', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])
    for j in range(1, 10):
        f.add_arc('dig2_eig', 'dig2_eig', str(j), [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]] + [kFRENCH_TRANS[j]])

    # case for 07X
    f.add_arc('dig1zero', 'dig2_sev', '7', ())
    f.add_arc('dig2_sev', 'dig2_sev', '0', [kFRENCH_TRANS[60]] + [kFRENCH_TRANS[10]])
    f.add_arc('dig2_sev', 'dig2_sev', '1', [kFRENCH_TRANS[60]] + [kFRENCH_AND] + [kFRENCH_TRANS[11]])
    for k in range(2, 7):
        f.add_arc('dig2_sev', 'dig2_sev', str(k), [kFRENCH_TRANS[60]] + [kFRENCH_TRANS[k + 10]])
    for k in range(7, 10):
        f.add_arc('dig2_sev', 'dig2_sev', str(k), [kFRENCH_TRANS[60]] + [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[k]])

    #00X case in french
    f.add_arc('start', 'dig1zero', '0', ())
    f.add_arc('dig1zero', 'dig2zero', '0', ())
    for ii in range(10):
        f.add_arc('dig2zero', 'f_dig3', [str(ii)], [kFRENCH_TRANS[ii]])

    #case for 02X
    f.add_arc('dig1zero', 'dig2_two', '2', ())
    f.add_arc('dig2_two', 'dig2_two', '0', [kFRENCH_TRANS[20]])
    f.add_arc('dig2_two', 'dig2_two', '1', [kFRENCH_TRANS[20]] + [kFRENCH_AND] + [kFRENCH_TRANS[1]])
    for j in range(2, 10):
        f.add_arc('dig2_two', 'dig2_two', str(j), [kFRENCH_TRANS[20]] + [kFRENCH_TRANS[j]])

    #01X case
    f.add_arc('dig1zero', 'dig2_one', '1', ())
    for j in range(7):
        f.add_arc('dig2_one', 'state5', [str(j)], [kFRENCH_TRANS[j + 10]])
    for j in range(7, 10):
        f.add_arc('dig2_one', 'state6', [str(j)], [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[j]])

    # case for 04X
    f.add_arc('dig1zero', 'dig2_four', '4', ())
    f.add_arc('dig2_four', 'dig2_four', '0', [kFRENCH_TRANS[40]])
    f.add_arc('dig2_four', 'dig2_four', '1', [kFRENCH_TRANS[40]] + [kFRENCH_AND] + [kFRENCH_TRANS[1]])
    for j in range(2, 10):
        f.add_arc('dig2_four', 'dig2_four', str(j), [kFRENCH_TRANS[40]] + [kFRENCH_TRANS[j]])

    # case for 03X
    f.add_arc('dig1zero', 'dig2_three', '3', ())
    f.add_arc('dig2_three', 'dig2_three', '0', [kFRENCH_TRANS[30]])
    f.add_arc('dig2_three', 'dig2_three', '1', [kFRENCH_TRANS[30]] + [kFRENCH_AND] + [kFRENCH_TRANS[1]])
    for j in range(2, 10):
        f.add_arc('dig2_three', 'dig2_three', str(j), [kFRENCH_TRANS[30]] + [kFRENCH_TRANS[j]])

    # case for 05X
    f.add_arc('dig1zero', 'dig2_five', '5', ())
    f.add_arc('dig2_five', 'dig2_five', '0', [kFRENCH_TRANS[50]])
    f.add_arc('dig2_five', 'dig2_five', '1', [kFRENCH_TRANS[50]] + [kFRENCH_AND] + [kFRENCH_TRANS[1]])
    for k in range(2, 10):
        f.add_arc('dig2_five', 'dig2_five', str(k), [kFRENCH_TRANS[50]] + [kFRENCH_TRANS[k]])

    # case for 06X
    f.add_arc('dig1zero', 'dig2_six', '6', ())
    f.add_arc('dig2_six', 'dig2_six', '0', [kFRENCH_TRANS[60]])
    f.add_arc('dig2_six', 'dig2_six', '1', [kFRENCH_TRANS[60]] + [kFRENCH_AND] + [kFRENCH_TRANS[1]])
    for k in range(2, 10):
        f.add_arc('dig2_six', 'dig2_six', str(k), [kFRENCH_TRANS[60]] + [kFRENCH_TRANS[k]])

    f.add_arc('start', 'dig1_nzero', '1', [kFRENCH_TRANS[100]])
    for j in range(2, 10):
        f.add_arc('start', 'dig1_nzero', str(j), [kFRENCH_TRANS[j]] + [kFRENCH_TRANS[100]])

    for i in range(1, 10):
        f.add_arc('sec_last', 'sec_last', str(i), [kFRENCH_TRANS[i]])

    f.add_arc('dig1_nzero', 'dig2_six', '6', ())
    f.add_arc('dig1_nzero', 'dig2_sev', '7', ())
    f.add_arc('dig1_nzero', 'dig2_eig', '8', ())
    f.add_arc('dig1_nzero', 'dig2_nine', '9', ())
    f.add_arc('dig1_nzero', 'sec_last', '0', ())
    f.add_arc('dig1_nzero', 'dig2_one', '1', ())
    f.add_arc('dig1_nzero', 'dig2_two', '2', ())
    f.add_arc('dig1_nzero', 'dig2_three', '3', ())
    f.add_arc('dig1_nzero', 'dig2_four', '4', ())
    f.add_arc('dig1_nzero', 'dig2_five', '5', ())
    f.add_arc('sec_last', 'last', '0', ())

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
