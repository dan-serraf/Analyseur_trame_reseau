from Reseau import *
from Ethernet import *
from ValideFichier import *
import argparse


#Création objet parser
parser = argparse.ArgumentParser()
#On définit les différentes variables : les noms de variables, les types et les descriptions
#commande : python3 main.py --help 
parser.add_argument("nom_fichier",type=str,help="Saisir le chemin du nom de fichier texte qui contient la trame.")
parser.add_argument("sauvegarde",type=str,help="Saisir le nom du fichier qui contiendra les informations.")
parser.add_argument("-d", "--detaille", action="store_true",help="Détaille les informations")

args = parser.parse_args()
reseau=convert_fichier_ligne(args.nom_fichier)
reseau.argument_main = argument_general_to_dict(args)

#Si le fichier ne contient pas d'erreur
if not fichier_erreur(reseau):
    resultat = ""
    
    nombre_trame = 1
    for trame in reseau.trame_total :
        #Ont traite la trame
        t = calcule_ethernet(reseau,nombre_trame)
        resultat = resultat + t
        nombre_trame += 1
    
    reseau.texte = resultat
    
texte = texte_afficher(reseau)

fichier = open(args.sauvegarde, "w")
fichier.write(texte)
fichier.close()