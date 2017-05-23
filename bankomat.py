import string
import hashlib
dane = open('dane.csv')


def wczytaj_dane(linia):
    linia = string.split(linia, ',')
    epoch = linia[0]
    nr = linia[1]
    login = linia[2]
    pin = linia[3]
    kwota = float(linia[4])
    operacja = string.rstrip(linia[5], ';\n')

    return epoch, nr, login, pin, kwota, operacja



def zaszyfruj_pin(pin):
    pin256 = hashlib.sha256(str(pin))
    hex_pin = pin256.hexdigest()
    return hex_pin


# generuje raport o stanie kont wszystkich klientow po wykonaniu 100 operacji
def generuj_raport(baza, nr_operacji):
    nazwa_pliku = str(nr_operacji-100+1) + '-' + str(nr_operacji) + '.txt'
    raport = open(nazwa_pliku, 'w')
    for key in baza:
        raport.write(str(baza[key])+'\n')
    raport.close()
    print "GENERUJE RAPORT: " + nazwa_pliku


class Klient:
    def __init__(self, login, pin, stan_konta = 1000):
        self.login = login
        self.pin = zaszyfruj_pin(pin)
        self.stan_konta = stan_konta
        self.proby_logowania = 0
        self.konto_zablokowane = False

    #__str__ wywoluje sie przy uzyciu print Klient
    def __str__(self):
        return "%s,%r;" % (self.login, self.stan_konta)

    def zmien_stan_konta(self,kwota,operacja):
        if operacja == 'income':
            self.stan_konta += kwota
        elif operacja == 'outcome':
            if self.stan_konta >= kwota:
                self.stan_konta -= kwota
            else:
                pass
                #print "za malo srodkow na koncie"
        else:
             print "niepoprawna operacja"

def logowanie(login, pin):
    if zaszyfruj_pin(pin) == baza[login].pin and not baza[login].konto_zablokowane:
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
        return True
    else:
        #print "Przekroczono limit uzytkownikow"
        return False


baza = {}
liczba_operacji = 0


#glowna petla progrmau
for line in dane:
    epoch, nr, login, pin, kwota, operacja = wczytaj_dane(line);
    #print login, operacja, kwota

    if login in baza:
        if logowanie(login, pin):
            baza[login].zmien_stan_konta(kwota,operacja)
            liczba_operacji += 1
        else:
            # niepoprawne logowanie
            liczba_operacji += 1
    else:
        if nowy_klient(login, pin):
            baza[login].zmien_stan_konta(kwota,operacja)
            liczba_operacji += 1
        else:
            # za duzo klientow w bazie
            liczba_operacji += 1


    #print liczba_operacji, login, operacja, kwota

    if liczba_operacji % 100 == 0:
        generuj_raport(baza, liczba_operacji)


dane.close()
