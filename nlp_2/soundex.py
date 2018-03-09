from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    #f1.add_state('next')
    f1.add_state('grp0')
    f1.add_state('grp1')
    f1.add_state('grp2')
    f1.add_state('grp3')
    f1.add_state('grp4')
    f1.add_state('grp5')
    f1.add_state('grp6')
    f1.initial_state = 'start'

    # Set all the final states
    #f1.set_final('next')
    f1.set_final('grp0')
    f1.set_final('grp1')
    f1.set_final('grp2')
    f1.set_final('grp3')
    f1.set_final('grp4')
    f1.set_final('grp5')
    f1.set_final('grp6')

    # Add the rest of the arcs
    for letter in string.ascii_lowercase:
        #f1.add_arc('start', 'next', (letter), (letter)) # do we need to move this to end ????
        '''
        if letter in "aeiouhwy":
            f1.add_arc('next', 'next', (letter), ())
            f1.add_arc('grp1', 'grp1', (letter), ())
            f1.add_arc('grp2', 'grp2', (letter), ())
            f1.add_arc('grp3', 'grp3', (letter), ())
            f1.add_arc('grp4', 'grp4', (letter), ())
            f1.add_arc('grp5', 'grp5', (letter), ())
            f1.add_arc('grp6', 'grp6', (letter), ())
        if letter in "bfpv":
            f1.add_arc('next', 'grp1', (letter), ('1'))
            f1.add_arc('grp1', 'grp1', (letter), ())
            f1.add_arc('grp2', 'grp1', (letter), ('1'))
            f1.add_arc('grp3', 'grp1', (letter), ('1'))
            f1.add_arc('grp4', 'grp1', (letter), ('1'))
            f1.add_arc('grp5', 'grp1', (letter), ('1'))
            f1.add_arc('grp6', 'grp1', (letter), ('1'))
        if letter in "cgjkqsxz":
            f1.add_arc('next', 'grp2', (letter), ('2'))
            f1.add_arc('grp1', 'grp2', (letter), ('2'))
            f1.add_arc('grp2', 'grp2', (letter), ())
            f1.add_arc('grp3', 'grp2', (letter), ('2'))
            f1.add_arc('grp4', 'grp2', (letter), ('2'))
            f1.add_arc('grp5', 'grp2', (letter), ('2'))
            f1.add_arc('grp6', 'grp2', (letter), ('2'))
        if letter in "dt":
            f1.add_arc('next', 'grp3', (letter), ('3'))
            f1.add_arc('grp1', 'grp3', (letter), ('3'))
            f1.add_arc('grp2', 'grp3', (letter), ('3'))
            f1.add_arc('grp3', 'grp3', (letter), ())
            f1.add_arc('grp4', 'grp3', (letter), ('3'))
            f1.add_arc('grp5', 'grp3', (letter), ('3'))
            f1.add_arc('grp6', 'grp3', (letter), ('3'))
        if letter in "l":
            f1.add_arc('next', 'grp4', (letter), ('4'))
            f1.add_arc('grp1', 'grp4', (letter), ('4'))
            f1.add_arc('grp2', 'grp4', (letter), ('4'))
            f1.add_arc('grp3', 'grp4', (letter), ('4'))
            f1.add_arc('grp4', 'grp4', (letter), ())
            f1.add_arc('grp5', 'grp4', (letter), ('4'))
            f1.add_arc('grp6', 'grp4', (letter), ('4'))
        if letter in "mn":
            f1.add_arc('next', 'grp5', (letter), ('5'))
            f1.add_arc('grp1', 'grp5', (letter), ('5'))
            f1.add_arc('grp2', 'grp5', (letter), ('5'))
            f1.add_arc('grp3', 'grp5', (letter), ('5'))
            f1.add_arc('grp4', 'grp5', (letter), ('5'))
            f1.add_arc('grp5', 'grp5', (letter), ())
            f1.add_arc('grp6', 'grp5', (letter), ('5'))
        if letter in "r":
            f1.add_arc('next', 'grp6', (letter), ('6'))
            f1.add_arc('grp1', 'grp6', (letter), ('6'))
            f1.add_arc('grp2', 'grp6', (letter), ('6'))
            f1.add_arc('grp3', 'grp6', (letter), ('6'))
            f1.add_arc('grp4', 'grp6', (letter), ('6'))
            f1.add_arc('grp5', 'grp6', (letter), ('6'))
            f1.add_arc('grp6', 'grp6', (letter), ())
        f1.add_arc('start', 'next', (letter), (letter))
        '''
        if letter in "aeiouhwy":
            f1.add_arc('start', 'grp0', (letter), (letter))
            f1.add_arc('grp0', 'grp0', (letter), ())
            f1.add_arc('grp1', 'grp0', (letter), ())
            f1.add_arc('grp2', 'grp0', (letter), ())
            f1.add_arc('grp3', 'grp0', (letter), ())
            f1.add_arc('grp4', 'grp0', (letter), ())
            f1.add_arc('grp5', 'grp0', (letter), ())
            f1.add_arc('grp6', 'grp0', (letter), ())
        if letter in "bfpv":
            f1.add_arc('start', 'grp1', (letter), (letter))
            f1.add_arc('grp0', 'grp1', (letter), ('1'))
            f1.add_arc('grp1', 'grp1', (letter), ())
            f1.add_arc('grp2', 'grp1', (letter), ('1'))
            f1.add_arc('grp3', 'grp1', (letter), ('1'))
            f1.add_arc('grp4', 'grp1', (letter), ('1'))
            f1.add_arc('grp5', 'grp1', (letter), ('1'))
            f1.add_arc('grp6', 'grp1', (letter), ('1'))
        if letter in "cgjkqsxz":
            f1.add_arc('start', 'grp2', (letter), (letter))
            f1.add_arc('grp0', 'grp2', (letter), ('2'))
            f1.add_arc('grp1', 'grp2', (letter), ('2'))
            f1.add_arc('grp2', 'grp2', (letter), ())
            f1.add_arc('grp3', 'grp2', (letter), ('2'))
            f1.add_arc('grp4', 'grp2', (letter), ('2'))
            f1.add_arc('grp5', 'grp2', (letter), ('2'))
            f1.add_arc('grp6', 'grp2', (letter), ('2'))
        if letter in "dt":
            f1.add_arc('start', 'grp3', (letter), (letter))
            f1.add_arc('grp0', 'grp3', (letter), ('3'))
            f1.add_arc('grp1', 'grp3', (letter), ('3'))
            f1.add_arc('grp2', 'grp3', (letter), ('3'))
            f1.add_arc('grp3', 'grp3', (letter), ())
            f1.add_arc('grp4', 'grp3', (letter), ('3'))
            f1.add_arc('grp5', 'grp3', (letter), ('3'))
            f1.add_arc('grp6', 'grp3', (letter), ('3'))
        if letter in "l":
            f1.add_arc('start', 'grp4', (letter), (letter))
            f1.add_arc('grp0', 'grp4', (letter), ('4'))
            f1.add_arc('grp1', 'grp4', (letter), ('4'))
            f1.add_arc('grp2', 'grp4', (letter), ('4'))
            f1.add_arc('grp3', 'grp4', (letter), ('4'))
            f1.add_arc('grp4', 'grp4', (letter), ())
            f1.add_arc('grp5', 'grp4', (letter), ('4'))
            f1.add_arc('grp6', 'grp4', (letter), ('4'))
        if letter in "mn":
            f1.add_arc('start', 'grp5', (letter), (letter))
            f1.add_arc('grp0', 'grp5', (letter), ('5'))
            f1.add_arc('grp1', 'grp5', (letter), ('5'))
            f1.add_arc('grp2', 'grp5', (letter), ('5'))
            f1.add_arc('grp3', 'grp5', (letter), ('5'))
            f1.add_arc('grp4', 'grp5', (letter), ('5'))
            f1.add_arc('grp5', 'grp5', (letter), ())
            f1.add_arc('grp6', 'grp5', (letter), ('5'))
        if letter in "r":
            f1.add_arc('start', 'grp6', (letter), (letter))
            f1.add_arc('grp0', 'grp6', (letter), ('6'))
            f1.add_arc('grp1', 'grp6', (letter), ('6'))
            f1.add_arc('grp2', 'grp6', (letter), ('6'))
            f1.add_arc('grp3', 'grp6', (letter), ('6'))
            f1.add_arc('grp4', 'grp6', (letter), ('6'))
            f1.add_arc('grp5', 'grp6', (letter), ('6'))
            f1.add_arc('grp6', 'grp6', (letter), ())

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('start1')
    f2.add_state('char')
    f2.add_state('dig1')
    f2.add_state('dig2')
    f2.add_state('dig3')
    f2.initial_state = 'start1'
    f2.set_final('char')
    f2.set_final('dig1')
    f2.set_final('dig2')
    f2.set_final('dig3')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('start1', 'char', (letter), (letter))
        f2.add_arc('char', 'dig1', (letter), (letter))
        f2.add_arc('dig1', 'dig2', (letter), (letter))
        f2.add_arc('dig2', 'dig3', (letter), (letter))
        f2.add_arc('dig3', 'dig3', (letter), ())

    for n in range(10):
        f2.add_arc('start1', 'dig1', (str(n)), (str(n)))
        f2.add_arc('char', 'dig1', (str(n)), (str(n)))
        f2.add_arc('dig1', 'dig2', (str(n)), (str(n)))
        f2.add_arc('dig2', 'dig3', (str(n)), (str(n)))
        f2.add_arc('dig3', 'dig3', (str(n)), ())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')
    f3.add_state('start2')
    f3.add_state('char2')
    f3.add_state('dig1')
    f3.add_state('dig2')
    f3.add_state('dig3')

    f3.initial_state = 'start2'
    f3.set_final('dig3')

    f3.add_arc('char2', 'dig1', (), ('0'))
    f3.add_arc('dig1', 'dig2', (), ('0'))
    f3.add_arc('dig2', 'dig3', (), ('0'))

    for letter in string.letters:
        f3.add_arc('start2', 'char2', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('start2', 'dig1', (str(number)), (str(number)))
        f3.add_arc('char2', 'dig1', (str(number)), (str(number)))
        f3.add_arc('dig1', 'dig2', (str(number)), (str(number)))
        f3.add_arc('dig2', 'dig3', (str(number)), (str(number)))
        f3.add_arc('dig3', 'dig3', (str(number)), ())

    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
