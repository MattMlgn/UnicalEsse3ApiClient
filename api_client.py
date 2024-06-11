import requests
from requests.auth import HTTPBasicAuth

class UnicalApiClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://unical.esse3.cineca.it/e3rest/api"
        self.matId = 0
        self.insegnamenti = {}

    def authenticate(self):
        url = f"{self.base_url}/login"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            self.auth_data = response.json()
            self.matId = self.auth_data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('matId', '')
            return self.auth_data
        else:
            response.raise_for_status()

    def anagrafica(self):
        data = self.auth_data.get('user', {})
        user_info = {
            'firstName': data.get('firstName', ''),
            'lastName': data.get('lastName', ''),
            'codFis': data.get('codFis', ""),
            'grpDes': data.get('grpDes', ""),
            'sex': data.get('sex', ""),
            'cdsDes': data.get('trattiCarriera', [{}])[0].get('cdsDes', ''),
            'cdsId': data.get('trattiCarriera', [{}])[0].get('cdsId', ''),
            'aaIscrId': data.get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('aaIscrId', ''),
            'aaOrdId': data.get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('aaOrdId', ''),
            'annoCorso': data.get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('annoCorso', ''),
            'durataAnni': data.get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('durataAnni', ''),
            'tipoCorsoCod': data.get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('tipoCorsoCod', ''),
            'ultimoAnnoFlg': data.get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('ultimoAnnoFlg', ''),
            'matricola': data.get('trattiCarriera', [{}])[0].get('matricola', ''),
            'staMatDes': data.get('trattiCarriera', [{}])[0].get('staMatDes', ''),
        }
        self.print_user_info(user_info)

    def print_user_info(self, user):
        ultimo_anno = 'Si' if user.get('ultimoAnnoFlg', 0) == 1 else 'No'
        print(f"Nome: {user['firstName']}")
        print(f"Cognome: {user['lastName']}")
        print(f"Codice Fiscale: {user['codFis']}")
        print(f"Gruppo: {user['grpDes']}")
        print(f"Sesso: {user['sex']}")
        print(f"Corso di Studi: {user['cdsDes']}")
        print(f"ID Corso di Studi: {user['cdsId']}")
        print(f"Anno di Iscrizione: {user['aaIscrId']}")
        print(f"Anno Ordinamento: {user['aaOrdId']}")
        print(f"Anno di Corso: {user['annoCorso']}")
        print(f"Durata Legale: {user['durataAnni']}")
        print(f"Tipo di Corso: {user['tipoCorsoCod']}")
        print(f"Ultimo Anno: {ultimo_anno}")
        print(f"Matricola: {user['matricola']}")
        print(f"Id Matricola: {self.matId}")
        print(f"Stato della Matricola: {user['staMatDes']}")

    def get_attivita_per_appelli(self):
        url = f"{self.base_url}/calesa-service-v1/appelli"
        params = {
            'start': 0,
            'limit': 50,
            'order': '+dataInizio'
        }
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), params=params)
        if response.status_code == 200:
            appelli = response.json()
            for appello in appelli:
                print(f"Anno: {appello['aaOffId']}")
                print(f"Id Appello: {appello['adDefAppId']}")
                print(f"Nome Appello: {appello['adDes']}")
                print(f"Id Corso di Studio: {appello['cdsDefAppId']}")
                print()  # Linea vuota per separare i record
                self.insegnamenti[appello['adDes']] = appello['adDefAppId']
  
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)
        

    def appello(self, adId):
        cdsId = 10224  # ID del corso di studio
        # Parametri opzionali
        params = {
            'q': 'APPELLI_PRENOTABILI_E_FUTURI',  # Filtra per appelli prenotabili
            'start': 0,
            'limit': 50,
            'order': '+dataInizio',
            #'aaCalId' : 2024
        }
        url = f"{self.base_url}/calesa-service-v1/appelli/{cdsId}/{adId}/"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), params=params)
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

    def get_appelli_prenotati(self):
        url = f"{self.base_url}/calesa-service-v1/prenotazioni/{self.matId}"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            appelli = response.json()
            for appello in appelli:
                print(f"Id Appello: {appello['adId']}")
                print(f"Data Prenotazione: {appello['dataIns']}")
                print(f"Data Appello: {appello['dataEsa']}")
                print()  # Linea vuota per separare i record
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    
    client = UnicalApiClient('bngnnp01t44h579x', 'NinaPia.2020') #Imposta credenziali
    client.authenticate() # Esegue l'autenticazione
    #client.anagrafica() # Stampa l'anagrafica
    #client.get_attivita_per_appelli()  ### LISTA DEGLI INSEGNAMENTI PER CUI GLI APPELLI SONO SBLOCCATI ###
    #client.appello(client.insegnamenti["DIDATTICA DELLE LINGUE"]) ### LISTA DI APPELLI PRENOTABILI E FUTURI DATO INSEGNAMENTO###
    #client.get_appelli_prenotati() ### APPELLI PRENOTATI ###
