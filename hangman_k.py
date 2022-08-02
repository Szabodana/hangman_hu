from posixpath import split
import requests as req
from bs4 import BeautifulSoup as b
import re
import string as st
import unidecode as u 
import time as t
import random as r
#megadott URL alapján végigkeresi a HTMLben az "a" tageket
#speciális karatkereket, 
def get_lista(x):
    szolista=list()
    parse = req.get(x).text
    soup = b(parse, 'html.parser')
    for szo in soup.findAll('a'):
        stringg = szo.text
        szavak = stringg.lower().split()
        for darab_szo in szavak:
            s=darab_szo.strip().rstrip(st.punctuation)
            if szam_check(s) is False and len(s)>=5 and len(s)<8 and "-" not in s:
                #latin_s=u.unidecode(s)
                szolista.append(s)
    print(len(szolista), "találat")
    return szolista

def szo_talalat_check(titkos_szo, tippelt_betu):
    check=False
    for i in titkos_szo:
        if i == tippelt_betu:
            check=True
    if check is True:
        return True
    else:
        return False

def uj_jatek():
    jatek="x"
    while jatek.lower()!="igen" and jatek.lower()!= "nem":
        jatek=input("Szeretnéd újraindítani a játékot? \nIgen/Nem: ")
        print("Hibás input, Igen/Nem")
    if jatek.lower() == "igen":
        print("Új játék kezdve!")
        fo_jatek()
    else:
        print("Játék befejezve :(")
        quit()

#Ha van szám a stringben akkor True, ha nincs akkor False
def szam_check(str):
    return any(x.isdigit() for x in str)

def titkos_szo_kereso():
    url=input("Először add meg az URL-t ami alapján a szót kiválasztom:")
    try:
        print(f"{url} kiválasztva.") 
        return r.choice(get_lista(url))
    except:
        print("Helytelen URL vagy Beautifulsoup valamiért tracebacket dobott :(\n")
        fo_jatek()

def check(titkos_szo, eddig_tippelt_betuk, tippelt_betu): 
    stat = '' 
    talalat = 0     
    for betu in titkos_szo: 
        if betu in eddig_tippelt_betuk: 
            stat += betu 
        else: 
            stat += '_'
        if betu == tippelt_betu: 
            talalat += 1        
    if talalat > 1: 
        print(talalat)
    return stat

def fo_jatek():
    eddig_tippelt_betuk = []
    tippek_szama = 0 #len(eddig_tippelt_betuk) vagy ez külön?
    titkos_szo=titkos_szo_kereso()
    fordulok_szama=len(titkos_szo)
    print("Próbálkozási lehetőségek: ", fordulok_szama)
    while tippek_szama < fordulok_szama:
        print("Eddig tippelt betűk:", eddig_tippelt_betuk )
        tippelt_betu = input("Betű tipp: ") 
        if szam_check(tippelt_betu) is False and len(tippelt_betu) == 1:
            if tippelt_betu in eddig_tippelt_betuk:
                print(f"{tippelt_betu}-t már próbáltad!")
            elif szo_talalat_check(titkos_szo, tippelt_betu) is True:
                print("Talált!")
                eddig_tippelt_betuk.append(tippelt_betu)
            else:
                eddig_tippelt_betuk.append(tippelt_betu)
                tippek_szama+=1
            result = check(titkos_szo, eddig_tippelt_betuk, tippelt_betu)
            if result == titkos_szo:
                print(titkos_szo)
                print(f"Gratulálok, nyertél! A megoldás <<<{titkos_szo}>>> volt!")
                uj_jatek()
            else:
                print("\n",result)
                print(f"Hátralévő tippek száma: {fordulok_szama-tippek_szama}!")
        else: 
            print("Hiba! Egyszerre csak egy betűt írhatsz be!" )
    print("Túl sok próbálkozás, játék vége!")
    print(f"A helyes válasz {titkos_szo} volt!")
    uj_jatek()
fo_jatek()