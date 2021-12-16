import urllib.request  # Netistä haettavan tietoa varten.
import json  # JSON-tiedoston lukemista varten.
import math  # Lukujen pyöristämistä varten


# Funktio hakee verkkokursseista tiedot jos ne ovat käynnissä (enabled = True)
# ja lisää ne listalle ja tulostaa ne. 
def hae_kaikki():
    pyynto = urllib.request.urlopen('https://studies.cs.helsinki.fi/stats-mock/api/courses')  # URL
    data = pyynto.read()  # Luetaan tieto ja tallennetaan se muuttujaan. 
    kurssit = json.loads(data)  # Muutetaan JSON-tiedosto ymmärrettävään muotoon ja tallennetaan se muuttujaan. 

    akt_kurssit = []  # Luodaan lista, johon tallennetaan aktiiviset kurssit tuplena.

    # Käydään luetut kurssit läpi:
    for kurssi in kurssit:  
        if kurssi['enabled']:  # Jos kurssi on käynnissä:

            # Lisätään kurssin tiedot aktiivisten kurssien listaan muodossa:
            # kurssin kokonimi, kurssin lyhenne, vuosi, tehtävien yhteismäärä.
            kurssi_tiedot = kurssi['fullName'], kurssi['name'], kurssi['year'], sum(kurssi['exercises'])
            akt_kurssit.append(kurssi_tiedot) 
        
    return akt_kurssit  # Palautetaan lista.


# Funktio hakee halutun kurssin tiedot.
def hae_kurssi(kurssi: str):
    pyynto = urllib.request.urlopen(f'https://studies.cs.helsinki.fi/stats-mock/api/courses/{kurssi}/stats')  # URL
    data = pyynto.read()  # Luetaan netistä haettu tieto ja tallennetaan se muuttujaan.
    kurssi = json.loads(data)  # Muutetaan JSON-tiedosto ymmärrettävään muotoon ja tallennetaan se muuttujaan.

    # Luodaan sanakirja, johon tallennetaan kurssin tiedot. 
    kurssitiedot = {}  
    kurssitiedot['viikkoja'] = len(kurssi)  # Viikkojen määrä on automaattisesti viikko-olioiden määrä JSON-tiedostossa.

    # Selvitetään kurssin tietoja ja tallennetaan ne sanakirjaan.
    oppilaita = 0  # Muuttujaan tallennetaan maksimiopiskelijoiden määrä.
    tuntien_summa = 0  # Muuttujaan tallennetaan tuntien yhteismäärä.
    tehtavien_summa = 0  # Muuttujaan tallennetaan tehtävien yhteismäärä. 

    # Käydään jokainen viikko-olio läpi kurssi-muuttujasta.
    for viikko in kurssi:
        # Tallennetaan oppilaita muuttujaan viikkojen maksimi opiskelijoiden määrä. 
        kurssin_oppilaat = kurssi[viikko]['students']  
        if kurssin_oppilaat > oppilaita:
            oppilaita = kurssin_oppilaat

        tuntien_summa += kurssi[viikko]['hour_total']  # Summaan lisätään kunkin viikon opintojen yhteistuntimäärä.
        tehtavien_summa += kurssi[viikko]['exercise_total']  # Summaan lisätään kunkin viikon tehtävien yhteismäärä
        
    kurssitiedot['opiskelijoita'] = oppilaita
    kurssitiedot['tunteja'] = tuntien_summa
    kurssitiedot['tunteja_keskimaarin'] = math.floor(tuntien_summa / oppilaita)  # Tunnin keskimäärin pyöristettynä alaspäin
    kurssitiedot['tehtavia'] = tehtavien_summa
    kurssitiedot['tehtavia_keskimaarin'] = math.floor(tehtavien_summa / oppilaita)

    return kurssitiedot

if __name__ == '__main__':
    hae_kurssi('docker2019')
    print(hae_kaikki())
