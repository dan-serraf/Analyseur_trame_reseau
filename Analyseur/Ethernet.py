import copy
from Ip import *


class Ethernet :
    def __init__(self): # Notre méthode constructeur
        """Trame ethernet """
        self.adresse_mac_destination = ""
        self.adresse_mac_source = ""
        self.type = ""
        self.texte = ""
        self.data = Ip()    

    def __str__(self):
        return self.texte

def str_ethernet(reseau,ethernet) :
    if reseau.argument_main["detaille"] == True :
        return detaille(ethernet,reseau)  
    else :
        return non_detaille(ethernet,reseau)

def calcule_ethernet(reseau,nombre_trame) :
    liste = copy.deepcopy(reseau.trame)
    ethernet = Ethernet()
    
    ethernet.adresse_mac_destination = calcul_adresse_mac(liste)
    ethernet.adresse_mac_source = calcul_adresse_mac(liste[6:])
    ethernet.type = calcul_type(liste)
    ethernet.data = calcule_data(definit_type(ethernet.type),liste[14:],reseau)
    ethernet.texte = str_ethernet(reseau,ethernet)

    string = ">Trame " + str(nombre_trame) + "\n" + ethernet.__str__()
    return string

def calcul_adresse_mac(liste) :
    adresse=""

    for i in range(6) :
        adresse = adresse + str(liste[i])
        if i != 5 :
           adresse = adresse + ":"
    return adresse

def calcul_type(liste) :
    type=""
    for i in range(12,14) :
        type =  type +  str(liste[i])
    return type


def definit_type(type) :
    #types est dictionnaires qui a comme clef le type et comme valeur l'utilisation
    types = {"0800":"IPv4","0805":"X.25","0806":"ARP","8035":"RARP","8098":"Appletalk"}
    if (type in types):
        return types.get(type)
    return "Inconnu"  

def code_hexa(type):
    if type != "Inconnu" :
        return " (0x" + type +") "
    return ""

def calcule_data(type,liste,reseau) :
    if type == "IPv4" :
        return calcule_data_ip(liste,reseau)
    return "Le type n'est pas connue par l'analyseur"

def str_data(data) :
    if data != "" :
        return data.__str__()
    return data


def detaille(ethernet,reseau):
    trame = "----------------- La partie Ethernet ----------------------------- \n"
    trame = trame + "L'adresse mac de la machine source est :" +  ethernet.adresse_mac_source +".\n"
    trame = trame + "L'adresse mac de la machine destination est :" +  ethernet.adresse_mac_destination +".\n"
    trame = trame + "Le type de la trame est :" + code_hexa(ethernet.type) + " " + definit_type(ethernet.type) + ".\n\n\n"
    trame = trame + str_data(ethernet.data)  
    return trame

def non_detaille(ethernet,reseau):
    trame = ">Ethernet \n"
    trame = trame + "\tSource Adress:" +  ethernet.adresse_mac_source +".\n"
    trame = trame + "\tDestination Adress:" +  ethernet.adresse_mac_destination +".\n"
    trame = trame + "\tType:" + code_hexa(ethernet.type) + " " + definit_type(ethernet.type) + ".\n\n\n"
    trame = trame + str_data(ethernet.data)  
    return trame

