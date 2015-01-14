#!/usr/bin/python

from base import Datos

from datetime import date, timedelta
from urllib3 import connection_from_url
from bs4 import BeautifulSoup
from random import uniform
from time import sleep

from IPython import embed

db = Datos()

base_url = "http://www.loteria-nacional.gov.ar/"
http = connection_from_url(base_url, maxsize=8)
tipos = ['pri', 'mat', 'noc']


def getUrl(fecha, tipo):
    print fecha, tipo
    url = base_url + "Internet/Extractos/resultados_i.php?juego=quiniela&fechasorteo=%s&tiposorteo=%s" % (fecha.strftime("%d%m%Y"), tipo)
    return url


def dormir():
    sleep(uniform(0, 3))

fecha = date.today()
dia = timedelta(days=1)

error = 0

while True:
    print error
    print fecha, fecha.weekday()

    for t in tipos:
        print t

        dormir()
        url = getUrl(fecha, t)
        html = http.request('GET', url)
        soup = BeautifulSoup(html.data)
        html.release_conn()

        if soup.findAll('b'):
            error += 1
            continue

        error = 0

        numeros = []
        pos = 0
        for d in soup.findAll('div', {"class": "BolillaVertical"}):
            pos += 1
            numero = d.text[:5].lstrip()
            parteA = numero[:2]
            parteB = numero[2:]
            print "%s %s %s %s %s %s %s" % (fecha, fecha.weekday(), t, pos, numero, parteA, parteB)
            numeros.append([fecha, fecha.weekday(), t, pos, numero, parteA, parteB])


        i = db.quinielas.insert(values=numeros)
        i.execute()


    if error > 30:
        break

    fecha = fecha - dia
