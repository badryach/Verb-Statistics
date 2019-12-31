import  InformationGenerale
def menu():
    print("Bienvenu dans le monde des verbes merci de faire un choix\n")
    print("1: Choisir un fichier\n")
    print("2 : Essayer l'application l'histoire des trois amoureux \n")
    print("3: A propos\n")
    print("3:Quiiter")



def action1():
    f = input("entrer l'adresse correct du fichier (seule format txt supporté)")
    try:
        InformationGenerale.detecterVerbe(open(str(f), "r", encoding='utf-8'))
        print("Votre fichier PDF avec le résultat est générer merci de voir le dossier racine")
    except Exception as e:
        s = str(e)
        print(s)
    x=nouvelleChoix()
    if x == "y":
        main()
    exit()

def action2():
    try:
        InformationGenerale.detecterVerbe(open("C:\\Users\\Badr\\Desktop\\amour.txt", "r", encoding='utf-8'))
        print("Votre fichier PDF avec le résultat est générer merci de voir le dossier racine")
    except Exception as e:
        s = str(e)
        print(s)
        print("Un problème est survenue, merci de choisir un nouvelle fichier de votre choix")
    x = nouvelleChoix()
    if x == "y":
        main()
    exit()


def action3():
    print("Cette application permet de donner les statistiques des verbes dans un texte ")
def action4():
    exit()
def aucun_action():
    menu()

def nouvelleChoix():
    selection2 = input("Voulez vous quitter? si oui taper y sinon taper n'importe quel caractère  \n")
    return selection2
def main():
    actions = {1: action1,2:action2,3:action3}

    r=True
    while r:
        menu()
        selection = input("Quel est votre choix:\n")
        if selection =="1" or selection =="3" or selection=="2" or selection=="4":
            choix = actions.get(int(selection), aucun_action)
        else:
            choix = actions.get(selection, aucun_action)
        choix()
        x= nouvelleChoix()
        if x == 'y':
            exit()
            r=False

if __name__ == "__main__":
    main()


