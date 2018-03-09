# import the fst module
import fst
# import the string module
import string
# Dene a list of all vowels for convenience
vowels = ['a', 'e', 'i', 'o', 'u']
# Instantiate an FST object with some name
f = fst.FST('devowelizer')
# All we need is a single state ...
f.add_state('1')
# and this same state is the initial and the nal state
f.initial_state = '1'
f.set_final('1')
# Now, we need to add an arc for each letter; if the letter is a vowel
# then the transition outputs nothing but otherwise it outputs the same
# letter that it consumed.
for letter in string.ascii_lowercase:
    if letter in vowels:
        _ = f.add_arc('1', '1', (letter), ())
    else:
        _ = f.add_arc('1', '1', (letter), (letter))
# Evaluate it on some example words
print ''.join(f.transduce(['v', 'o', 'w', 'e', 'l']))
print ''.join(f.transduce('e x c e p t i o n'.split()))
print ''.join(f.transduce('c o n s o n a n t'.split()))

print f.transduce(['a','w'])

from fsmutils import composechars
S = "vowels"
output = composechars(S, f, f, f)

print output

from fsmutils import trace
trace(f, S)


# Add the rest of the arcs
f1 = fst.FST('new')
# All we need is a single state ...
f1.add_state('start')
f1.add_state('next')
# and this same state is the initial and the nal state
f1.initial_state = 'start'
f1.set_final('next')

cnt = 0
for letter in string.ascii_lowercase:
    if cnt == 0:
        f1.add_arc('start', 'next', (letter), (letter))
    else:
        cnt=cnt+1
        if letter in "aeiouhwy":
            f1.add_arc('start', 'next', (letter), ())
        else:
            if letter in "bfpv":
                f1.add_arc('start', 'next', (letter), (1))
            elif letter in "cgjkxsxz":
                f1.add_arc('start', 'next', (letter), (2))
            elif letter in "dt":
                f1.add_arc('start', 'next', (letter), (3))
            elif letter in "mn":
                f1.add_arc('start', 'next', (letter), (5))
            elif letter == 'r':
                f1.add_arc('start', 'next', (letter), (6))
            elif letter == 'l':
                f1.add_arc('start', 'next', (letter), (4))



print f1.transduce("Resnik")
