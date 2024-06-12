import os
import sys
import api_client
import getpass

def clear_screen():
    # Funzione per pulire lo schermo del terminale
    os.system('clear')

def print_menu(options, header="Menu"):
    print(f"+{'-' * 50}+")
    print(f"|{header.center(50)}|")
    print(f"+{'-' * 50}+")
    for i, option in enumerate(options, 1):
        print(f"| {i}. {option.ljust(46)}|")
    print(f"+{'-' * 50}+")

def login():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    print('\nLogin in corso...')
    return api_client.UnicalApiClient(username, password)

def main():
    client = None
    user_info = {}

    while True:
        clear_screen()
        if client is None:
            print_menu(["Login", "Esci"], header="Benvenuto!")
            choice = input("Scegli un opzione: ")
            if choice == '1':
                client = login()
                client.authenticate()
                #client.populate()
                user_info = client.anagrafica()
                clear_screen()
            elif choice == '2':
                sys.exit(0)
            else:
                print("Scelta non valida, riprovare.")
                continue
        else:
            username = user_info['firstName']
            options = [
                "Stampa anagrafica",
                "Lista Insegnamenti",
                "Lista appelli prenotati",
                "Lista appelli disponibili",
                "Visualizza Medie",
                "Chiudi"
            ]
            if user_info['sex'] == 'F':
                print_menu(options, header=f"Benvenuta, {username}")
            else:
                print_menu(options, header=f"Benvenuto, {username}")
            choice = input("Scegli un opzione: ")

            if choice == '1':
                clear_screen()
                client.print_user_info(user_info)
                input("\nPremi invio per ritornare al menù principale...")
            elif choice == '2':
                clear_screen()
                client.get_attivita_per_appelli()
                input("\nPremi invio per ritornare al menù principale...")
            elif choice == '3':
                clear_screen()
                client.get_appelli_prenotati()
                #print(appelli_prenotati)
                input("\nPremi invio per ritornare al menù principale...")
            elif choice == '4':
                clear_screen()
                ins = input("Scrivi il nome completo dell'insegnamento: ")
                ins = ins.upper()
                client.appello(client.insegnamenti[ins])
                input("\nPremi invio per ritornare al menù principale...")
            elif choice == '5':
                clear_screen()
                client.medieC()
                #print(medie)
                input("\nPremi invio per ritornare al menù principale...")
            elif choice == '6':
                clear_screen()
                client = None
            else:
                print("Scelta non valida, riprovare.")
                continue

if __name__ == "__main__":
    main()