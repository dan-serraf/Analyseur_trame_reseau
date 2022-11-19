import copy
from Tcp import * 

class Ip :
    def __init__(self): # Notre méthode constructeur
        """Ip """

        self.version = ""
        self.ihl = ""
        self.tos = ""
        self.total_length = ""
        self.identification =""
        self.flag = []
        self.fragment_offset=""
        self.ttl = 0
        self.protocol = ""
        self.header_checksum=""
        self.adress_source=""
        self.adress_dest=""
        self.taille_option = 0
        self.option=""
        self.padding=0
        self.data= Tcp()
        self.texte = ""

    def __str__(self):
        return self.texte

def str_ip(reseau,ip) :
    if reseau.argument_main["detaille"] == True :
        return detaille(ip)  
    else :
        return non_detaille(ip)

def calcule_data_ip(liste,reseau):
    liste2 = copy.deepcopy(liste)
    ip = Ip()
    ip.version = calcule_version_ip(liste2)
    ip.ihl = calcule_ihl(liste2)
    ip.tos = calcule_tos(liste2[1:])
    ip.total_length = calcule_total_length(liste2[2:])
    ip.identification = calcule_identification(liste2[4:])
    ip.flag = calcule_flag(liste2[6:])
    ip.fragment_offset = calcule_fragment_offset(liste2[6:])
    ip.ttl = calcule_ttl(liste2[8:])
    ip.protocol = calcule_protocol(liste2[9:])
    ip.header_checksum = calcule_header_checksum(liste2[10:])
    ip.adress_source = calcule_adress_ip(liste2[12:])
    ip.adress_dest = calcule_adress_ip(liste2[16:])
    ip.taille_option = calcule_taille_option(ip.ihl)
    ip.padding = calcule_taille_padding(ip.taille_option)
    ip.option = calcule_option(liste2[20:],ip.taille_option)
    ip.data = calcule_data(ip.protocol,liste[20 + ip.taille_option:],reseau)
    ip.texte = str_ip(reseau,ip)
    return ip


def calcule_version_ip(liste):
    return str(int(liste[0][0],16))

def calcule_ihl(liste):
    #Attention lors de l'interpretation il faut faire le resultat * 4 octets pour avoir taille de l'entete d'Ip
    return str(int(liste[0][1],16))

def calcule_tos(liste):
    return str(int(liste[1],16))

def calcule_total_length(liste) :
    total = ""
    for i in range(2) :
        total = total + liste[i]
    return str(int(total,16))

def calcule_identification(liste):
    return asssemble_octet(liste,2)

def string_to_list(string):
    liste = []
    for i in string :
        liste.append(i)
    return liste

def list_to_string(liste):
    string = ""
    for i in liste:
        string = string + i
    return string

def asssemble_octet(liste,nombre):
    string=""
    k = 0
    for i in liste :
        if k == nombre :
            break
        string = string + i
        k+=1
    return string

def insert_bit_rembourages(liste) :
    while (len(liste)< 6) : #4 bits + 2 car commence par 0b
        liste.insert(2,0)
    return liste

def calcule_flag(liste) :
    flag = bin(int(liste[0][0],16))
    flags = string_to_list(flag) #passe de string a liste pour inserer des bits de rembourages
    flags = insert_bit_rembourages(flags)
    return [flags[2],flags[3],flags[4]]

def definit_flag(flag):
    flag[0] = "Flags : \nBits reserver a 0 .\n"
    if flag[1] == '1' :
        flag[1] = "\tDf = 1 : Interdiction de fragmenter. \n"
    else :
        flag[1] = "\tDf = 0 : Fragmentation autoriser. \n"

    if flag[2] == '1' :
        flag[2] = "\tMf = 1 : Le fragment courant est suivi d'un autre fragment. \n"
    else :
        flag[2] = "\tMf = 0 : Le fragment courant n'est pas suivi d'un autre fragment. \n"

    return flag

def definit_flag_not_verbiose(flag):
    flag[0] = "\tFlags : \n\t\tBits reserver = 0 .\n"
    if flag[1] == '1' :
        flag[1] = "\t\tDf = 1\n"
    else :
        flag[1] = "\t\tDf = 0\n"

    if flag[2] == '1' :
        flag[2] = "\t\tMf = 1\n"
    else :
        flag[2] = "\t\tMf = 0\n"

    return flag
     
def calcule_fragment_offset(liste) :
    # nombre octets / 8
    string = asssemble_octet(liste,2)
    string = bin(int(string,16))
    liste2 = string_to_list(string) #passe de string a liste pour inserer des bits de rembourages
    liste2 = insert_bit_rembourages(liste2)
    return definit_fragment_offset(liste2[5:]) #5 car on ignore les 2 premieres cases 0b puis on ignore les 3 prochaines cases car flag

def definit_fragment_offset(liste):
    string = list_to_string(liste)
    offset = int(string,2)#base 2
    return int(offset/8) #Pour avoir l'offset


def calcule_ttl(liste) :
    return str(int(liste[0],16))

def definit_protocol(valeur) :
    if valeur == 6 :
        return "TCP"
    return "Autre"


def calcule_protocol(liste) :
   return int(liste[0],16)

def definit_header_checksum(liste) :
    return "calcul_header_checksum"

def calcule_header_checksum(liste) :
    total = ""
    for i in range(2) :
        total = total + liste[i]
    return total
    #return str(int(total,16)) 

def calcule_adress_ip(liste) :
    adresse_ip =""
    for i in range(4) :
        adresse_ip = adresse_ip + str(int(liste[i],16))
        if i != 3 :
            adresse_ip = adresse_ip + "."
    return adresse_ip

def calcule_option(liste,longeur_option) :
    if longeur_option > 0 :
        return "\tCes option n'ont pas ete prit en compte par notre analyseur."
    return ""

def calcule_taille_option(ihl) :
    return ( int(ihl) * 4 ) - 20  # taille entete - min = taille option

def calcule_taille_padding(taille_option):
    return 60 - taille_option - 20 # max - taille_option - taille entete= taille_padding

def calcule_data(type,liste,reseau):
    return calcule_data_tcp(liste,reseau)

def str_data(data) :
    if data != "" :
        return  data.__str__()
    return data


def int_to_hexa_to_str(variable):
    return  " (" + str(hex(int(variable))) + ") "

def hexa_to_int_str(variable):
    return " (" + str(int(variable,16)) + ") "

def detaille(Ip):
    ip = "----------------- La partie IP ----------------------------- \n"
    ip = ip + "La version est :" + int_to_hexa_to_str(Ip.version) +  Ip.version +".\n"
    ip = ip + "La longeur de l'entete est :" + int_to_hexa_to_str(Ip.ihl) +  str(int(Ip.ihl)*4) +".\n"
    ip = ip + "Le TOS est :" + int_to_hexa_to_str(Ip.tos) + Ip.tos + ".\n"
    ip = ip + "La longeur total est :" + int_to_hexa_to_str(Ip.total_length) + Ip.total_length + ".\n"
    ip = ip + "L'identification est :" +hexa_to_int_str(Ip.identification) + "0x" +Ip.identification + ".\n"
    ip = ip + asssemble_octet( definit_flag(Ip.flag) , 3 ) 
    ip = ip + "La position du fragement est :" + int_to_hexa_to_str(Ip.fragment_offset) + str(Ip.fragment_offset) + ".\n"
    ip = ip + "Le TTL est :" + int_to_hexa_to_str(Ip.ttl) + str(Ip.ttl) + ".\n"
    ip = ip + "Le Protocole est :" + int_to_hexa_to_str(Ip.protocol) + str(Ip.protocol )+ ".\n"
    ip = ip + "Le cheksum est :" + hexa_to_int_str(Ip.header_checksum) +  "0x" + Ip.header_checksum + ".\n"
    ip = ip + "L'adresse source Internet est :" + Ip.adress_source + ".\n"
    ip = ip + "L'adresse destinataire Internet est :" + Ip.adress_dest + ".\n"
    ip = ip + "La taille de l'option est :" +  int_to_hexa_to_str(Ip.taille_option) + str(Ip.taille_option) + ".\n"
    ip = ip + "Le rembourrage est :" + int_to_hexa_to_str(Ip.taille_option) + str(Ip.padding) + ".\n"
    ip = ip + Ip.option + "\n\n\n"
    ip = ip + str_data(Ip.data)  
    return ip


def non_detaille(Ip):
    ip = ">Internet Protocol \n"
    ip = ip + "\tVersion:" + int_to_hexa_to_str(Ip.version) +  Ip.version +".\n"
    ip = ip + "\tHeader Length:" + int_to_hexa_to_str(Ip.ihl) +  str(int(Ip.ihl)*4) +".\n"
    ip = ip + "\tTOS:" + int_to_hexa_to_str(Ip.tos) + Ip.tos + ".\n"
    ip = ip + "\tTotal Length:" + int_to_hexa_to_str(Ip.total_length) + Ip.total_length + ".\n"
    ip = ip + "\tIdentification:" +hexa_to_int_str(Ip.identification) + "0x" +Ip.identification + ".\n"
    ip = ip + asssemble_octet( definit_flag_not_verbiose(Ip.flag) , 3 ) 
    ip = ip + "\tFragment Offset:" + int_to_hexa_to_str(Ip.fragment_offset) + str(Ip.fragment_offset) + ".\n"
    ip = ip + "\tTTL:" + int_to_hexa_to_str(Ip.ttl) + str(Ip.ttl) + ".\n"
    ip = ip + "\tProtocole:" + int_to_hexa_to_str(Ip.protocol) + str(Ip.protocol )+ ".\n"
    ip = ip + "\tHeader Cheksum:" + hexa_to_int_str(Ip.header_checksum) + "0x" + Ip.header_checksum + ".\n"
    ip = ip + "\tSource Adresse:" + Ip.adress_source + ".\n"
    ip = ip + "\tDestinataire Adresse :" + Ip.adress_dest + ".\n"
    ip = ip + "\tOption Length:" +  int_to_hexa_to_str(Ip.taille_option) + str(Ip.taille_option) + ".\n"
    ip = ip + "\tRembourrage Length:" + int_to_hexa_to_str(Ip.taille_option) + str(Ip.padding) + ".\n"
    ip = ip + Ip.option + "\n\n\n"
    ip = ip + str_data(Ip.data)  

    return ip