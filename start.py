import requests
from requests.auth import HTTPBasicAuth
from utils import anagrafica

# Definisci le credenziali
username = 'bngnnp01t44h579x'
password = 'NinaPia.2020'

# Definisci l'URL dell'endpoint
url = "https://unical.esse3.cineca.it/e3rest/api"

def authenticate():

    # Opzionale: aggiungi parametri alla richiesta
    params = {
        'sessionLinguaCod': 'ita',
    }

    # Esegui la richiesta GET con autenticazione BASIC
    response = requests.get(url+"/login", auth=HTTPBasicAuth(username, password), params=params)
    return response

def get_attivita_per_appelli():

    # Opzionale: aggiungi parametri alla richiesta
    params = {
        'start': 0,
        'limit': 50,
        'order': '+dataInizio'
    }

    # Esegui la richiesta GET con autenticazione BASIC
    response = requests.get(url+"/calesa-service-v1/appelli", auth=HTTPBasicAuth(username, password), params=params)

    # Verifica la risposta
    if response.status_code == 200:
        appelli = response.json()
        #for appello in appelli:
            #print(f"Data: {appello['dataInizio']}, Descrizione: {appello['descrizione']}")
        print(appelli)
    else:
        print(f"Errore: {response.status_code}")
        print(response.text)
        
if __name__ == "__main__":
    #anagrafica(authenticate())
    #get_attivita_per_appelli()
    pass