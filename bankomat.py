import string
import hashlib
import time


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

    def zmien_stan_konta_2(self,kwota,operacja):
        if operacja == 'income':
            self.stan_konta += kwota
            return time.time()
        elif operacja == 'outcome':
            if self.stan_konta >= kwota:
                self.stan_konta -= kwota
                return time.time()
            else:              
                print "za malo srodkow na koncie"
                return 0
        else:
            print "niepoprawna operacja"
            return 0

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

###bez numeru
def wczytaj_dane(linia):
    linia = string.split(linia, ',')
    epoch = linia[0]
    login = linia[1]
    pin = linia[2]
    kwota = float(linia[3])
    operacja = string.rstrip(linia[4], ';\n')

    return epoch, login, pin, kwota, operacja



def wczytaj_historie(baza):
    liczba_operacji = 0
    historia_transakcji = open('baza_transakcji.txt') 
    for line in historia_transakcji:
        epoch, login, pin, kwota, operacja = wczytaj_dane(line);
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


    historia_transakcji.close()


baza = {}
liczba_operacji = 0

print "WYBIERZ TRYB PRACY BANKOMATU"
print "TRYB TESTOWY -> WYBIERZ 1"
print "TRYB KLIENTA -> WYBIERZ 2"
tryb_pracy = int(raw_input("> "))

if tryb_pracy == 1:
    dane = open('dane.csv')
    print "START TESTOW"
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

elif tryb_pracy == 2:

    wczytaj_historie(baza)
    historia_transakcji = open('baza_transakcji.txt', 'a')

    while(True):
        wyjscie = False
        while(wyjscie==False):
            wyswietl_stan_konta = True
            login = raw_input("Wpisz login: ")
            pin = raw_input("Wpisz PIN (4 cyfry): ")

            if login in baza:
                if logowanie(login, pin):
                    print "\nLogowanie poprawne, teraz wpisz kwote oraz rodzaj operacji (income, outcome)\n"
                    zalogowany = True
                    kwota = int(raw_input("Kwota: "))
                    operacja = raw_input("Operacja: ")
                    epoch = baza[login].zmien_stan_konta_2(kwota,operacja)
                    ###jesli epoch != 0 znaczy ze transakcja sie udala i wpisujemy ja do historii
                    if epoch != 0:
                        linia = str(int(epoch)) +","+login+","+pin+","+str(kwota)+","+operacja+";"
                        historia_transakcji.write(linia+'\n')

                    liczba_operacji += 1
                else:
                    wyswietl_stan_konta = False
                    # niepoprawne logowanie
                    liczba_operacji += 1
                    break
            else:
                if nowy_klient(login, pin):
                    print "\nKonto dodane do bazy klientow. Teraz wpisz kwote oraz rodzaj operacji (income, outcome)\n"
                    zalogowany = True
                    kwota = int(raw_input("Kwota: "))
                    operacja = raw_input("Operacja: ")
                    epoch = baza[login].zmien_stan_konta_2(kwota,operacja)
                    if epoch != 0:
                        linia = str(int(epoch)) +","+login+","+pin+","+str(kwota)+","+operacja+";"
                        historia_transakcji.write(linia+'\n')
                    liczba_operacji += 1
                else:
                    # za duzo klientow w bazie
                    liczba_operacji += 1
            

            if liczba_operacji % 100 == 0:
                generuj_raport(baza, liczba_operacji)

            if wyswietl_stan_konta == True:
                print "\nStan konta po operacji: \n", baza[login].stan_konta

            print "\nJesli chcesz sie wylogowac wpisz 1, jesli nie wpisz 2"
            b = int(raw_input("> "))
            if b == 1:
                zalogowany = False

            while(zalogowany == True):
                print "\nTeraz wpisz kwote oraz rodzaj operacji (income, outcome)\n"
                kwota = int(raw_input("Kwota: "))/1.0
                operacja = raw_input("Operacja: ")
                epoch = baza[login].zmien_stan_konta_2(kwota,operacja)
                if epoch != 0:
                        linia = str(int(epoch)) +","+login+","+pin+","+str(kwota)+","+operacja+";"
                        historia_transakcji.write(linia+'\n')
                liczba_operacji += 1
                print "\nStan konta po operacji: \n", baza[login].stan_konta
                print "\nJesli chcesz sie wylogowac wpisz 1, jesli nie wpisz 2"
                b = int(raw_input("> "))
                if b == 1:
                    zalogowany = False


            print "\nAby zakonczyc dzialanie bankomatu wpisz 1, jesli nie wpisz 2"
            a = int(raw_input("> "))
            if a == 1:
                wyjscie = True

            print "Zostales wylogowany."

        if wyjscie == True:
            break    

    historia_transakcji.close()
