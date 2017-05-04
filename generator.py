import random
import time
import names

dane = open('dane.txt', 'w')

N = 2000 #ile danych
for i in range(1, N):

    #####NO
    #print >> dane, i
    #dane.write(str(i))
    ########TIMESTAMP
    t = time.time()
    #print "epoch: %d" %t

    ##########name
    name = names.get_first_name()

    #####PIN
    a = []
    for j in range(0,4):
        a.append(random.randrange(0,9))
    pin = str(a[0])+str(a[1])+str(a[2])+str(a[3])
    #pin = ''.join(str(a))

    ########MONEY
    money = random.randrange(1,100000)/100.0
    #print "Kwota : %r" %(round(money, 2))

    ########TYPE
    typ = ['income', 'outcome']
    t1 = random.randint(1,2)
    b = typ[t1-1]

    line = str(int(t)) +","+ str(i) +","+name+","+pin+","+str(money)+","+b+";"
    dane.write(line+'\n')
