import json
import requests
from pprint import pprint
import time
from datetime import datetime

while True:
    try:
        Numero_Crypto = int(input("Di quante crypto vuoi analizzare i dati? "))
    except ValueError:
        print("ERRORE: Digitare un numero intero maggiore o uguale a 20.")

        continue

    if Numero_Crypto<20:
        print("ERRORE: Digitare un numero intero maggiore o uguale a 20.")

        continue

    else:

        break

class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': Numero_Crypto,
            'convert': 'USD'
        }

        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '45b7dcfa-3a54-46e0-975f-8cbd84b42e20'
        }

        self.orders = []

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers,
                         params=self.params).json()
        return r['data']


GetDataBot = Bot()

Currencies = GetDataBot.fetchCurrenciesData()


# Ricercare la cryptovaluta con maggior volume di scambio registrato nelle ultime 24 ore:
Max_Volume_Currency = None
for Currency in Currencies:
    if not Max_Volume_Currency or Currency['quote']['USD']['volume_24h'] > Max_Volume_Currency['quote']['USD']['volume_24h']:
        Max_Volume_Currency = Currency
print()
print(
    f"La criptovaluta con il volume maggiore (in $) delle ultime 24 ore è: {Max_Volume_Currency['name']}")
print()

# Individuare le migliori 10 e le peggiori 10 cryptovalute in base alla variazione percentuale registrata nelle ultime 24 ore.


# Peggiori 10 in base al numero iniziale di crypto esaminate (numero)


Sorted_Currencies = sorted(
    Currencies, key=lambda i: i['quote']['USD']['percent_change_24h'])
Worst_10 = []
Counter = 0
while Counter <= 9:
    Worst_10.append(Sorted_Currencies[Counter]['name'])
    Counter += 1
print(
    f"Le peggiori 10 cryptovalute in termini di variazione percentuale sono: \n {Worst_10}")
print()

# Migliori 10 in base al numero iniziale di crypto esaminate (numero)


Best_10 = []
Counter = (Numero_Crypto - 1)
while Counter >= (Numero_Crypto - 10):
    Best_10.append(Sorted_Currencies[Counter]['name'])
    Counter -= 1
print(
    f"Le migliori 10 cryptovalute in termini di variazione percentuale sono: \n {Best_10}")
print()


# Quanti $ sono necessari per acquistare una unità di ciascuna delle migliori 20 cryptovalute secondo la classifica coinmarketcap:

Total_Cost = 0
n = 0

for Currency in Currencies:
    if n <= 20:
        Total_Cost += Currency['quote']['USD']['price']
        n += 1
print(
    f"Per acquistare una unità di ognuna delle prime 20 cryptovalute proposte dalla classifica di Coinmarketcap occorrono: {round(Total_Cost,2)} dollari")
print()


# Quanti $ sono necessari per acquistare una unità delle cryptovalute che hanno registrato un volume > di 76 milioni nelle ultime 24 ore:

Total_Amount = 0
for Currency in Currencies:
    if Currency['quote']['USD']['volume_24h'] > 76000000:
        Total_Amount += Currency['quote']['USD']['price']
print(
    f"Per acquistare una unità di ognuna delle cryptovalute proposte dalla classifica di Coinmarketcap che hanno registrato un volume maggiore di 76 milioni nelle ultime 24 ore occorrono: {round(Total_Amount,2)} dollari")
print()

# La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute il giorno prima
# (ipotizzando che la classifca non sia cambiata)

Total_Today = Total_Cost
Total_Yesterday = 0
Price_Yesterday = []
Change_In_Price = 0
Percent_Change_In_Price = 0
n = 0

for Currency in Currencies:
    if n <= 20:
        Price_Yesterday.append(Currency['quote']['USD']['price'] / (
            1 + (Currency['quote']['USD']['percent_change_24h'] / 100)))
        Total_Yesterday += Price_Yesterday[n]
        n += 1

Change_In_Price = Total_Today - Total_Yesterday
Percent_Change_In_Price = round(Change_In_Price * 100 / Total_Yesterday, 2)

if Percent_Change_In_Price > 0:
    print(
        f"Se ieri si fossero acquistate n. 1 unità di ciascuna delle prime 20 criptovalute secondo la classifica proposta da Coinmarketcap oggi si sarebbe registrata una variazione percentuale positiva pari al {Percent_Change_In_Price}%")
else:
    print(
        f"Se ieri si fossero acquistate n. 1 unità di ciascuna delle prime 20 criptovalute secondo la classifica proposta da Coinmarketcap oggi si sarebbe registrata una variazione percentuale negativa pari al {Percent_Change_In_Price}%")

print()

Result = {
    "Criptovaluta_Maggior_Volume_24h": Max_Volume_Currency['name'],
    "Peggiori_10_Criptovalute": Worst_10,
    "Migliori_10_Criptovalute": Best_10,
    "Costo_Totale_20_Crypto": round(Total_Cost, 2),
    "Costo_Totale_Crypto_Vol_76M": round(Total_Amount, 2),
    "Variazione_Percentuale_Portafoglio_Ieri": Percent_Change_In_Price
}

today = datetime.now().strftime("%Y_%m_%d-%I.%M.%S_%p")
filename = today + '.json'  # use the file extension .json
with open(filename, 'w') as file_object:  # w opens the file in write mode
    # json.dump() function to store the set of data in .json file
    json.dump(Result, file_object, indent=4)

    print()
