import os.path
import os
import requests
from requests import get
import pyperclip
import tempfile
import hashlib
import zipfile
import shutil
from colorama import Fore, Style, init as colorama_init
import sys

def list_files(startpath): # https://stackoverflow.com/a/9728478
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def cls():  # Fonction cls/clear
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():  # Fonction pause/read
    if os.name=="nt":
        os.system("pause")
    else:
        useless=input("Appuyer sur Entrer pour continuer")


def hash_file(hashfile):  # Permet de comparer des fichiers

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(hashfile, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def listmii():  # Programme Listmii
    tmpfile = tmp+"\\listmii_temp.txt"

    # https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    original_stdout = sys.stdout  # Sauvegarde la sortie d'origine standard
    with open(tmpfile, 'w', encoding='utf-8') as f:
        sys.stdout = f # Met la sortie dans le fichier f
        print(list_files(os.getcwd())) # Liste les fichiers de la carte sd dans un fichier
        sys.stdout = original_stdout # Restaure la sortie d'origine standard

    with open(tmpfile, "r") as f: #https://stackoverflow.com/a/4710090
        lines = f.readlines()
    with open(tmpfile, "w") as f:
        for line in lines:
            if line.strip("\n") != "None":
                f.write(line)

    f = open(tmpfile, 'r', encoding='utf-8')  # Upload du fichier
    message = f.read()

    data = {
        'api_dev_key': tokenpastebin,
        'api_paste_code': message,
        'api_paste_private': '1',
        'api_option': 'paste',
        'api_paste_name': 'Listmii',
        'api_paste_expire_date': '10M',
    }

    response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    responsetest = response
    if responsetest.ok:
        pyperclip.copy(response.text)
        print("Fichier sauvegardé, merci d'envoyer ce lien pastebin", response.text,
              "(il est copié dans le presse papier)")
        pause()
    else:
        print("Merci de copier la globalité du fichier à la personne qui vous l'a demandée")
        print("Erreur :", response, response.text)
        pause()
        os.startfile(tmpfile)
        print("Une fois le fichier donné, appuyez sur une touche")
        pause()
    f.close()  # Nettoyage du fichier
    os.remove(tmpfile)


def mkdir(actualdir):
    if not os.path.isdir(actualdir):
        os.mkdir(actualdir)


def downloadfromgithub(link,output):  # fonction pour télécharger depuis Github
    # J'ai été grandement aidé par Murasaki : https://github.com/MurasakiNX
    currentdir=os.getcwd()
    os.chdir(tmp)
    request = get(link, headers={
        'Authorization': tokengithub
    }).json()[0]

    assets = request['assets']

    for asset in assets:
        file = get(asset['browser_download_url'])
        with open(asset['name'], 'wb') as f:
            f.write(file.content)
        if output:
            print(f'Le fichier {asset["name"]} a été téléchargé !')
    if zipfile.is_zipfile(asset["name"]):
        zipfile.ZipFile(asset["name"]).extractall()
        if output:
            print(f'Le fichier {asset["name"]} a été extrait !')
    os.chdir(currentdir)
    return asset["name"]


def update(): # Programme de Mise à Jour de fichier
    print("Vérification de l'installation actuelle de Luma")
    downloadfromgithub("https://api.github.com/repos/LumaTeam/Luma3DS/releases", False)
    if os.path.isfile("boot.firm"):
        if hash_file("boot.firm") == "a130c778b21c81af20f2909c6d9beb4a9a9deccc":
            print(Fore.GREEN + "Dernière version de Luma déjà installée !")
            print(Style.RESET_ALL)
            pause()
        else:
            good=False
            while not good:
                print("Version de Luma inconnue ou dépassée")
                updateluma=input("Souhaitez-vous mettre à jour Luma ? (Oui/Non) : ")
                if updateluma.lower()=="oui":
                    shutil.copyfile(tmp+"\\boot.firm", "boot.firm")
                    print(Fore.GREEN+"Luma a bien été mise à jour !")
                    print(Style.RESET_ALL)
                    pause()
                    good=True
                elif updateluma.lower()=="non":
                    print("Luma n'a pas été mis à jour")
                    pause()
                    good=True
                else:
                    cls()
                    print(Fore.RED + "Renseignez Oui ou Non")
                    print(Style.RESET_ALL)
    else:
        good=False
        while not good:
            updateluma= input("Aucun boot.firm trouvé, sans boot.firm, la console peut ne pas démarrer.\nVoulez-vous installer la dernière version de Luma ? (Oui/Non) : ")
            if updateluma.lower()=="oui":
                shutil.copyfile(tmp+"\\boot.firm", "boot.firm")
                print(Fore.GREEN+"Luma a bien été installé !")
                print(Style.RESET_ALL)
                pause()
                good=True
            elif updateluma.lower()=="non":
                print("Luma n'a pas été installé !")
                pause()
                good=True
            else:
                print(Fore.RED + "Renseignez Oui ou Non")
                print(Style.RESET_ALL)
    good=False
    while not good:
        godmode=input("Souhaitez-vous installer la dernière version de GodMode9 ? (Oui/Non) : ")
        if godmode.lower()=="oui":
            mkdir("luma")
            mkdir("luma/payloads")
            mkdir("gm9")
            mkdir("gm9/scripts")
            downloadfromgithub("https://api.github.com/repos/d0k3/GodMode9/releases", True)
            shutil.copyfile(tmp + "\\GodMode9.firm", "luma/payloads/GodMode9.firm")
            shutil.copyfile(tmp + "\\gm9/scripts/GM9Megascript.gm9", "gm9/scripts/GM9Megascript.gm9")
            print(Fore.GREEN + "Godmode9 a correctement été installé !")
            print(Style.RESET_ALL)
            pause()
            good=True
        if godmode.lower()=="non":
            good=True
        else:
            print(Fore.RED + "Renseignez Oui ou Non")
            print(Style.RESET_ALL)


def menu():  # Menu du programme
    incorrect=False
    while "1"=="1":
        cls()
        print(
            "\n _     _     _   __  __ _ _\n| |   (_)___| |_|  \/  (_|_)\n| |   | / __| __| |\/| | | |\n| |___| \__ \ |_| |  | | | |\n|_____|_|___/\__|_|  |_|_|_|\n","    - Crée par LéonLeBreton\n\n")
        choice = '0'
        while choice == '0':
            print("Merci de choisir un programme")
            print("1.ListMii")
            print("2.Update/Mise à jour")
            print("3.Quitter")
            if incorrect:
                 print(Fore.RED+"Merci d'entrer un numéro correct")
                 print(Style.RESET_ALL)
            choice = input("Merci de faire un choix (1~3): ")
            if choice == "1":
                print("")
                incorrect = False
                listmii()
            elif choice == "2":
                print("")
                incorrect = False
                update()
            elif choice == "3":
                shutil.rmtree(tmp)
                exit()
            else:
                incorrect=True


#S'exécute seulement au démarrage
def prgmboot():
    if os.name=="nt":
        letters= ["A","B","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        goodletter= []
        for i in letters:
            try:
                os.chdir(i+":/Nintendo 3ds")
                goodletter.append(i)
            except FileNotFoundError:
                pass
        if len(goodletter)==0:
            print(Fore.RED + "Aucune carte SD de 3ds détectée, branchez la carte SD puis appuyez sur Entrée")
            print(Style.RESET_ALL)
            pause()
            return "empty"
        elif len(goodletter)>=2:
            print("Plusieurs cartes SD ont été détectées :"," et ".join(goodletter))
            while True:
                goodsd=input("Merci de choisir la lettre de la carte SD que vous voulez utiliser : ")
                if not goodsd=="C":
                    try:
                        os.chdir(goodsd+":/Nintendo 3ds")
                        break
                    except FileNotFoundError:
                        cls()
                        print(Fore.RED+"Merci de choisir dans une des lettres proposées")
                        print(Style.RESET_ALL)
                else:
                    cls()
                    print(Fore.RED + "Le disque C est le disque de Windows")
                    print(Style.RESET_ALL)
            return goodsd
        else:
            return goodletter[0]
    else:
        while True:
            unix=input("Vous n'avez pas Windows NT, merci de renseigner manuellement le chemin vers votre carte SD : ")
            try:
                os.chdir(unix + ":/Nintendo 3ds")
                break
            except FileNotFoundError:
                cls()
                print(Fore.RED + "Ce chemin n'est pas celui d'une carte SD de 3ds")
                print(Style.RESET_ALL)
        return unix


colorama_init()
tmp = tempfile.gettempdir() + "\\listmii"
tokengithub = "token " + ""  # Mettre le token Github entre les guillemet
tokenpastebin = ""  # Mettre Token Pastebin entre guillemet


directory="empty"
while directory=="empty":
    directory=prgmboot()
os.chdir(directory+":/")
if os.path.exists(tmp):
    shutil.rmtree(tmp)
    os.mkdir(tmp)
else:
    os.mkdir(tmp)
menu()