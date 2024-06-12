import requests
from requests.auth import HTTPBasicAuth

def get_key_from_value(dizionario, valore):
    for chiave, valore_corrente in dizionario.items():
        if valore_corrente == valore:
            return chiave
    return None

class UnicalApiClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://unical.esse3.cineca.it/e3rest/api"
        self.matId = 0
        self.insegnamenti = {}
        self.cdsId = 0
        self.medie = {}

    def authenticate(self):
        url = f"{self.base_url}/login"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            self.auth_data = response.json()
            self.matId = self.auth_data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('matId', '')
            self.populate()
            return self.auth_data
        else:
            response.raise_for_status()

    def populate(self):
        url = f"{self.base_url}/calesa-service-v1/appelli"
        params = {
            'start': 0,
            'limit': 50,
            'order': '+dataInizio'
        }
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), params=params)
        if response.status_code == 200:
            appelli = response.json()
            self.cdsId = appelli[0]['cdsDefAppId']
            for appello in appelli:
                self.insegnamenti[appello['adDes']] = appello['adDefAppId']
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)

        url = f"{self.base_url}/libretto-service-v2/libretti/{self.matId}/medie"
        response = requests.get(url, auth=HTTPBasicAuth(self.username,self.password))
        if response.status_code == 200:
            risultati = response.json()
            print(risultati)
            for risultato in risultati:
                base = risultato.get('base', 'N/A')
                media = risultato.get('media', 'N/A')
                tipoMediaCod = risultato.get('tipoMediaCod', {}).get('value', 'N/A')
                if base == 30 and tipoMediaCod == 'P':
                    self.medie['voti'] = media
                if base == 110 and tipoMediaCod == 'P':
                    self.medie['baseL'] = media
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)

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
        #self.print_user_info(user_info)
        return user_info

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
        for nome_appello, id_appello in self.insegnamenti.items():
            print(f"Nome Insegnamento: {nome_appello}")
            print(f"Id Appello: {id_appello}")
            print()  # Linea vuota per separare i record

    def appello(self, adId):
        params = {
            'q': 'APPELLI_PRENOTABILI_E_FUTURI',
            'start': 0,
            'limit': 50,
            'order': '+dataInizio'
        }
        url = f"{self.base_url}/calesa-service-v1/appelli/{self.cdsId}/{adId}/"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), params=params)
        if response.status_code == 200:
            appelli = response.json()
            for appello in appelli:
                print(f"Insegnamento: {appello['adDes']}")
                print(f"Corso di Studio: {appello['cdsDes']}")
                print(f"Data Inizio Iscrizioni: {appello['dataInizioIscr'].split()[0]}")
                print(f"Data Fine Iscrizioni: {appello['dataFineIscr'].split()[0]}")
                print(f"Data Esame: {appello['dataInizioApp'].split()[0]}")
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
                print(f"Nome Insegnamento: {get_key_from_value(self.insegnamenti, appello['adId'])}")
                print(f"Data Prenotazione: {appello['dataIns']}")
                print(f"Data Appello: {appello['dataEsa']}")
                print(f"Peso: {int(appello['pesoAd'])} cfu")
                print()  # Linea vuota per separare i record
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)

    def medieC(self):
        url = f"{self.base_url}/libretto-service-v2/libretti/{self.matId}/medie"
        response = requests.get(url, auth=HTTPBasicAuth(self.username,self.password))
        print(f"Media Ponderata Voti: {self.medie['voti']}\nMedia Base Laurea Ponderata: {self.medie['baseL']}")
        if response.status_code == 200:
            risultati = response.json()
            for risultato in risultati:
                base = risultato.get('base', 'N/A')
                media = risultato.get('media', 'N/A')
                tipoMediaCod = risultato.get('tipoMediaCod', {}).get('value', 'N/A')
                
                if base == 30 and tipoMediaCod == 'A':
                    print(f"Media Aritmetica Voti: {media}")
                if base == 110 and tipoMediaCod == 'A':
                    print(f"Media Base Laurea Aritmetica: {media}")

                ### FUNZIONE CALCOLO VARIAZIONE MEDIA  ###
            """if(input("Vuoi simulare un nuovo voto? S/N: ")) == 'S':
                nuovoV = int(input("\nInserisci il voto: "))
                cfu = int(input("\nInserisci i crediti: "))
                cfuT = int(input("\nI tuoi cfu totali attuali: "))
                print("La nuova media voti sarà: ", round(((self.medie['voti']*cfuT)+(nuovoV+cfu))/(cfuT+cfu),2))"""
            
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    client = UnicalApiClient('bngnnp01t44h579x', 'NinaPia.2020')  # Imposta credenziali
    client.authenticate()  # Esegue l'autenticazione e popola i dati
    # Le seguenti chiamate stampano i dati già popolati
    #client.anagrafica()  # Stampa l'anagrafica
    #client.get_attivita_per_appelli()  # Stampa la lista degli insegnamenti per cui gli appelli sono sbloccati
    #print(client.insegnamenti)
    #client.appello(client.insegnamenti["LINGUA E TRADUZIONE INGLESE I - PRIMA LINGUA DI SPECIALIZZAZIONE"])  # Stampa la lista di appelli prenotabili e futuri dato l'insegnamento
    #client.get_appelli_prenotati()  # Stampa gli appelli prenotati
    client.medieC() # Stampa le medie
    