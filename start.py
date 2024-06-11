import requests
from requests.auth import HTTPBasicAuth

def parse_response(response):
    """Parsa la risposta JSON e restituisce un dizionario leggibile."""
    if response.status_code == 200:
        data = response.json()
        result = {
            'user': {
                'firstName': data.get('user', {}).get('firstName', ''),
                'lastName': data.get('user', {}).get('lastName', ''),
                #'email': data.get('user', {}).get('email', ''),
                'codFis': data.get('user', {}).get('codFis', ""),
            },
            'auth_token': data.get('authToken', ''),
            'jwt': data.get('jwt', ''),
            'exp_pwd': data.get('expPwd', False)
        }
        return result
    elif response.status_code == 300:
        return "Multipli profili disponibili, specifica un profilo."
    elif response.status_code == 401:
        return "Credenziali non valide."
    else:
        return f"Errore: {response.status_code}"

# Definisci le credenziali
username = 'bngnnp01t44h579x'
password = 'NinaPia.2020'

# Definisci l'URL dell'endpoint
url = "https://unical.esse3.cineca.it/e3rest/api/login"

# Opzionale: aggiungi parametri alla richiesta
params = {
    'sessionLinguaCod': 'ita',
    #'optionalFields': 'ALL'
}

# Esegui la richiesta GET con autenticazione BASIC
response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)

# Controlla la risposta e parsala
result = parse_response(response)
#print(result.get('user'))
print(response.json())