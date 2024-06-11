import requests
from requests.auth import HTTPBasicAuth
from calls import anagrafica

def authenticate():
    # Definisci le credenziali
    username = 'bngnnp01t44h579x'
    password = 'NinaPia.2020'

    # Definisci l'URL dell'endpoint
    url = "https://unical.esse3.cineca.it/e3rest/api/login"

    # Opzionale: aggiungi parametri alla richiesta
    params = {
        'sessionLinguaCod': 'ita',
    }

    # Esegui la richiesta GET con autenticazione BASIC
    response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)
    return response

if __name__ == "__main__":
    response = authenticate()
    anagrafica(response)