fname = "hyp1-hyp2-ref"
fw1 = open('train-ref35k', 'w')
fw3 = open('test-ref15k', 'w')
cnt = 0
with open(fname) as f1:
    content = f1.readlines()
    for i in range(35000):
        fw1.write(content[i])
    for i in range(35000,50000):
        fw3.write(content[i])


fname = "dev.answers"
fw2 = open('train-answers35k', 'w')
fw4 = open('test-answers15k', 'w')
with open(fname) as f2:
    content = f2.readlines()
    for i in range(35000):
        fw2.write(content[i])
    for i in range(35000,50000):
        fw4.write(content[i])