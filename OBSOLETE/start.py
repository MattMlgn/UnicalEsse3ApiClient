import requests
from requests.auth import HTTPBasicAuth
from utils import anagrafica


# Definisci le credenziali
username = 'bngnnp01t44h579x'
password = 'NinaPia.2020'

# Definisci l'URL dell'endpoint
url = "https://unical.esse3.cineca.it/e3rest/api"

def authenticate():
    ### FUNZIONE DI LOGIN + OTTENIMENTO ANAGRAFICA ###

    # Opzionale: aggiungi parametri alla richiesta
    params = {
        'sessionLinguaCod': 'ita',
    }

    # Esegui la richiesta GET con autenticazione BASIC
    response = requests.get(url+"/login", auth=HTTPBasicAuth(username, password), params=params)
    return response

def get_attivita_per_appelli():
    ### LISTA DEGLI INSEGNAMENTI PER CUI GLI APPELLI SONO SBLOCCATI ###
    # Opzionale: aggiungi parametri alla richiesta
    params = {
        'start': 0,
        'limit': 50,
        'order': '+dataInizio'
    }

    # Esegui la richiesta GET con autenticazione BASIC
    response = requests.get(url+"/calesa-service-v1/appelli/10224/16077/9/iscritti/249287", auth=HTTPBasicAuth(username, password), params=params)
    print()

    # Verifica la risposta
    if response.status_code == 200:
        appelli = response.json()
        """for appello in appelli:
            print(f"Anno: {appello['aaOffId']}")
            print(f"Id Appello: {appello['adDefAppId']}")
            print(f"Nome Appello: {appello['adDes']}")
            print(f"Id Corso di Studio: {appello['cdsDefAppId']}")
            print()  # Linea vuota per separare i record"""
        print(appelli)
    else:
        print(f"Errore: {response.status_code}")
        print(response.text)

def appello(adId):

    ### LISTA DI APPELLI PRENOTABILI E FUTURI DATO INSEGNAMENTO###

    cdsId = 10224  # ID del corso di studio
    # Parametri opzionali
    params = {
        'q': 'APPELLI_PRENOTABILI_E_FUTURI',  # Filtra per appelli prenotabili
        'start': 0,
        'limit': 50,
        'order': '+dataInizio',
        #'aaCalId' : 2024
    }

    # Effettua la richiesta GET
    response = requests.get(f"{url}/calesa-service-v1/appelli/{cdsId}/{adId}/", auth=HTTPBasicAuth(username, password), params=params)

    # Verifica la risposta
    if response.status_code == 200:
        appelli = response.json()
        for appello in appelli:
            print(f"Insegnamento: {appello['adDes']}")
            print(f"Corso di Studio: {appello['cdsDes']}")
            print(f"Data Fine Iscrizioni: {appello['dataFineIscr'].split()[0]}")
            print(f"Data Appello: {appello['dataInizioApp'].split()[0]}")
            print(f"Data Inizio Iscrizioni: {appello['dataInizioIscr'].split()[0]}")
            print(f"Descrizione: {appello['desApp']}")
            print(f"Iscritti: {appello['numIscritti']}")
            print(f"Presidente Commissione d'Esame: {appello['presidenteNome']} {appello['presidenteCognome']}")
            print(f"Tipo Esame: {appello['tipoGestAppDes']}")
            print()  # Linea vuota per separare i record
    else:
        print(f"Errore: {response.status_code}")
        print(response.text)

def get_appelli_prenotati(matId,adsceId):
    ### APPELLI PRENOTATI ###
    
    params = {

    }
    # Esegui la richiesta GET con autenticazione BASIC
    #response = requests.get(f"{url}/libretto-service-v2/libretti/{matId}/righe/{adsceId}/prenotazioni", auth=HTTPBasicAuth(username, password))
    #response = requests.get(f"{url}/libretto-service-v2/libretti/{matId}/righe", auth=HTTPBasicAuth(username, password))


    # Verifica la risposta
    if response.status_code == 200:
        appelli = response.json()
        """for appello in appelli:
            print(f"Id Appello: {appello['adId']}")
            print(f"Data Prenotazione: {appello['dataIns']}")
            print(f"Data Appello: {appello['dataEsa']}")
            print()  # Linea vuota per separare i record"""
        print(appelli)
    else:
        print(f"Errore: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    #anagrafica(authenticate())
    get_attivita_per_appelli()
    #appello(9142)
    #get_appelli_prenotati(401817,9218232)
    #pass