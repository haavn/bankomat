import string
dane = open('dane.txt')


def wczytaj_dane(linia):
    linia = string.split(linia, ',')
    nr = linia[0]
    epoch = linia[1]
    login = linia[2]
    pin = linia[3]
    kwota = float(linia[4])
    operacja = string.rstrip(linia[5], ';\n')

    return nr, epoch, login, pin, kwota, operacja

class Klient:
    def __init__(self, login, pin, stan_konta = 0):
        self.login = login
        self.pin = pin
        self.stan_konta = stan_konta

    #__str__ wywoluje sie przy uzyciu print Klient
    def __str__(self):
        return "Login: %s; pin: %s; stan konta: %r;" % (self.login,self.pin,self.stan_konta)

    def zmien_stan_konta(self,kwota,operacja):
        if operacja == 'income':
            self.stan_konta += kwota
        elif operacja == 'outcome':
            if self.stan_konta >= kwota:
                self.stan_konta -= kwota
            else:
                print "za malo srodkow na koncie"
        else:
             print "niepoprawna operacja"


baza = {}

for line in dane:
    nr, epoch, login, pin, kwota, operacja = wczytaj_dane(line);
    print login, operacja, kwota
    if login in baza:
        if pin == baza[login].pin:
            baza[login].zmien_stan_konta(kwota,operacja)
        else:
            print "Niepoprawny pin"
    else:
        baza[login] = Klient(login,pin)
        baza[login].zmien_stan_konta(kwota,operacja)
dane.close()


for key in baza:
    print baza[key]
print baza
