def parse_response(response):
    """Parsa la risposta JSON e restituisce un dizionario leggibile."""
    if response.status_code == 200:
        data = response.json()
        result = {
            'user': {
                'firstName': data.get('user', {}).get('firstName', ''),
                'lastName': data.get('user', {}).get('lastName', ''),
                'codFis': data.get('user', {}).get('codFis', ""),
                'grpDes': data.get('user', {}).get('grpDes', ""),
                'sex': data.get('user', {}).get('sex', ""),
                'cdsDes': data.get('user', {}).get('trattiCarriera', [{}])[0].get('cdsDes', ''),
                'cdsId': data.get('user', {}).get('trattiCarriera', [{}])[0].get('cdsId', ''),
                'aaIscrId': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('aaIscrId', ''),
                'aaOrdId': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('aaOrdId', ''),
                'annoCorso': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('annoCorso', ''),
                'durataAnni': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('durataAnni', ''),
                'tipoCorsoCod': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('tipoCorsoCod', ''),
                'ultimoAnnoFlg': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('ultimoAnnoFlg', ''),
                'matricola': data.get('user', {}).get('trattiCarriera', [{}])[0].get('matricola', ''),
                'matId': data.get('user', {}).get('trattiCarriera', [{}])[0].get('dettaglioTratto', {}).get('matId', ''),
                'staMatDes': data.get('user', {}).get('trattiCarriera', [{}])[0].get('staMatDes', ''),
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

def print_user_info(user):
    """
    Stampa i dati dell'utente in modo ordinato e leggibile.
    """
    ultimo_anno = 'Si' if user.get('ultimoAnnoFlg', 0) == 1 else 'No'
    
    print(f"Nome: {user.get('firstName', '')}")
    print(f"Cognome: {user.get('lastName', '')}")
    print(f"Codice Fiscale: {user.get('codFis', '')}")
    print(f"Gruppo: {user.get('grpDes', '')}")
    print(f"Sesso: {user.get('sex', '')}")
    print(f"Corso di Studi: {user.get('cdsDes', '')}")
    print(f"ID Corso di Studi: {user.get('cdsId', '')}")
    print(f"Anno di Iscrizione: {user.get('aaIscrId', '')}")
    print(f"Anno Ordinamento: {user.get('aaOrdId', '')}")
    print(f"Anno di Corso: {user.get('annoCorso', '')}")
    print(f"Durata Legale: {user.get('durataAnni', '')}")
    print(f"Tipo di Corso: {user.get('tipoCorsoCod', '')}")
    print(f"Ultimo Anno: {ultimo_anno}")
    print(f"Matricola: {user.get('matricola', '')}")
    print(f"Id Matricola: {user.get('matId', '')}")
    print(f"Stato della Matricola: {user.get('staMatDes', '')}")

def anagrafica(response):
    result = parse_response(response)
    if isinstance(result, dict) and "user" in result:
        print_user_info(result["user"])
    else:
        print(result)