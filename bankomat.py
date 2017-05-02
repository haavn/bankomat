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
        self.proby_logowania = 0
        self.konto_zablokowane = False

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

def logowanie(login, pin):
    if pin == baza[login].pin and not baza[login].konto_zablokowane:
        baza[login].proby_logowania = 0
        return True
    else:
        baza[login].proby_logowania += 1
        if not baza[login].konto_zablokowane:
            print "Niepoprawny pin"
        if baza[login].proby_logowania >= 3:
            baza[login].konto_zablokowane = True
            print "Konto zablokowane, skontaktuj sie z bankiem"
        return False

def nowy_klient(login, pin):
    if len(baza) < 100:
        baza[login] = Klient(login,pin)
    else:
        print "Przekroczono limit uzytkownikow"

baza = {}

for line in dane:
    nr, epoch, login, pin, kwota, operacja = wczytaj_dane(line);
    print login, operacja, kwota
    if login in baza:
        if logowanie(login, pin):
            baza[login].zmien_stan_konta(kwota,operacja)
    else:
        nowy_klient(login, pin)
        baza[login].zmien_stan_konta(kwota,operacja)

dane.close()


for key in baza:
    print baza[key]
print baza
