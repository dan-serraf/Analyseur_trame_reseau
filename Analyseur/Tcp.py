import copy

class Tcp :
    def __init__(self): # Notre méthode constructeur
        """Tcp """
        self.port_source = ""
        self.port_dest = ""
        self.sequence_number = ""
        self.acknowledgment_number = ""
        self.thl = ""
        self.reserved = ""
        self.drapeau = [] #Drapeau
        self.window = ""
        self.checksum=""
        self.urgent_pointeur=""
        self.option=""
        self.taille_option = 0
        self.padding=""
        self.data=""
        self.texte = ""

    def __str__(self):
        return self.texte

    
def str_tcp(reseau,tcp) :
    if reseau.argument_main["detaille"] == True :
        return detaille(tcp)  
    else :
        return non_detaille(tcp)



def calcule_data_tcp(liste,reseau):
    liste2 = copy.deepcopy(liste)
    tcp = Tcp()
    tcp.port_source = calcule_port_source(liste2)
    tcp.port_dest = calcule_port_dest(liste2[2:])
    tcp.sequence_number = calcule_sequence_number(liste2[4:])
    tcp.acknowledgment_number = calcule_acknowledgment_number(liste2[8:])
    tcp.thl = calcule_thl(liste2[12:])
    tcp.reserved = calcule_reserved(liste2[12:])
    tcp.drapeau = calcule_drapeau(liste2[12:])
    tcp.window = calcule_window(liste2[14:])
    tcp.checksum = calcule_checksum(liste2[16:])
    tcp.urgent_pointeur = calcule_urgent_pointeur(liste2[18:])
    tcp.option = calcule_option(tcp.thl)
    tcp.taille_option = calcule_taille_option(tcp.thl)
    tcp.padding = calcule_padding(tcp.taille_option)
    tcp.data = calcule_data_http(liste2[ (20 + tcp.taille_option + tcp.padding) :],reseau)
    tcp.texte = str_tcp(reseau,tcp)
    return tcp

def calcule_port_source(liste):
    return int(asssemble_octet(liste,2),16)

def calcule_port_dest(liste):
    return int(asssemble_octet(liste,2),16)

def calcule_sequence_number(liste):
    sequence_number =""
    for i in range(4) :
        sequence_number = sequence_number + str(liste[i])
    return int(sequence_number,16)

def calcule_acknowledgment_number(liste):
    acknowledgment_number =""
    for i in range(4) :
        acknowledgment_number = acknowledgment_number + str(liste[i])

    return int(acknowledgment_number,16)

def calcule_thl(liste):
    #Attention lors de l'interpretation il faut faire le resultat * 4 octets pour avoir taille de l'entete d'Ip
    return str(int(liste[0][0],16))

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
        liste.insert(2,'0')

    return liste

def calcule_reserved(liste):
    flag1 = bin(int(liste[0][1],16))
    flag2 = bin(int(liste[1][0],16))
    flags1 = string_to_list(flag1) #passe de string a liste pour inserer des bits de rembourages
    flags1 = insert_bit_rembourages(flags1)
    flags2 = string_to_list(flag2) #passe de string a liste pour inserer des bits de rembourages
    flags2 = insert_bit_rembourages(flags2)
    resultat = concatener_liste(flags1[2:],flags2[2:])#enleve les 0b
    return definit_reserved(resultat)


def calcule_drapeau(liste):
    flag1 = bin(int(liste[1][0],16))
    flag2 = bin(int(liste[1][1],16))
    flags1 = string_to_list(flag1) #passe de string a liste pour inserer des bits de rembourages
    flags1 = insert_bit_rembourages(flags1)
    flags2 = string_to_list(flag2) #passe de string a liste pour inserer des bits de rembourages
    flags2 = insert_bit_rembourages(flags2)
    resultat = concatener_liste(flags1[2:],flags2[2:])#on enleve les 0b
    return definit_drapeau(resultat)

def definit_drapeau(liste):
    resultat = ""
    #Il commence au 2eme bits car les deux premiers font partie de reserved
    for i in range(2,8): #drapeau sont sur 6 bits                   
        resultat = resultat + str(liste[i])
    return resultat

def decrit_drapeau(liste):
    #initialisation d'un tableau de 6 cases vides
    resultat = ["","","","","",""]

    if liste[0] == '1' :
        resultat[0] = "\tURG = 1 : La trame est prioritaire .\n"
    else :
        resultat[0] = "\tURG = 0 : La trame est non prioritaire .\n"

    if liste[1] == '1' :
        resultat[1] = "\tACK = 1 : Le numero d acquitement est valide .\n"
    else :
        resultat[1] = "\tACK = 0 : Le numero d acquitement est non valide .\n"
    
    if liste[2] == '1' :
        resultat[2] = "\tPSH = 1 : Il faut push cette trame .\n"
    else :
        resultat[2] = "\tPSH = 0 : Il ne faut pas push cette trame .\n"

    if liste[3] == '1' :
        resultat[3] = "\tRST = 1 : Il faut reinitialiser la connexion car elle devenue incoherente .\n"
    else :
        resultat[3] = "\tRST = 0 : On a pas besoin de reinitialiser la connexion .\n"
    
    if liste[4] == '1' :
        resultat[4] = "\tSYN = 1 : On est en phase d etablissement de connexion .\n"
    else :
        resultat[4] = "\tSYN = 0 : On n est pas en phase d etablissement de connexion .\n"

    if liste[5] == '1' :
        resultat[5] = "\tFIN = 1 : On libere la connexion .\n"
    else :
        resultat[5] = "\tFIN = 0 : On ne libere pas la connexion .\n"
    
    return resultat

def decrit_drapeau_non_detaille(liste):
    #initialisation d'un tableau de 6 cases vides
    resultat = ["","","","","",""]

    if liste[0] == '1' :
        resultat[0] = "\tFlags:\t\tURG = 1\n"
    else :
        resultat[0] = "\t\tURG = 0\n"

    if liste[1] == '1' :
        resultat[1] = "\t\tACK = 1\n"
    else :
        resultat[1] = "\t\tACK = 0\n"
    
    if liste[2] == '1' :
        resultat[2] = "\t\tPSH = 1\n"
    else :
        resultat[2] = "\t\tPSH = 0\n"

    if liste[3] == '1' :
        resultat[3] = "\t\tRST = 1\n"
    else :
        resultat[3] = "\t\tRST = 0\n"
    
    if liste[4] == '1' :
        resultat[4] = "\t\tSYN = 1\n"
    else :
        resultat[4] = "\t\tSYN = 0\n"

    if liste[5] == '1' :
        resultat[5] = "\t\tFIN = 1\n"
    else :
        resultat[5] = "\t\tFIN = 0\n"
    
    return resultat
    

def concatener_liste(liste1,liste2):
    for i in liste2:
        liste1.append(i)
    return liste1
    
def definit_reserved(liste):
    resultat = ""
    for i in range(0,6): #reserver est sur 6 bits
        resultat = resultat + str(liste[i])
    return resultat

def calcule_window(liste):
    return int(asssemble_octet(liste,2),16)

def calcule_checksum(liste):
    return asssemble_octet(liste,2)

def calcule_urgent_pointeur(liste):
    return asssemble_octet(liste,2)

def calcule_option(thl) :
    return (int(thl)- 5) * 4 

def calcule_taille_option(thl) :
    return (int(thl)- 5) * 4 

def calcule_padding(taille_option) :
    # nombre d'octet de padding est multiple de 4octets pour completer une ligne
    return taille_option % 4 

def calcule_data_http(liste,reseau) :
    
    
    entete,index_liste = calcule_entete_http(liste)
    corp = calcule_corp_http(liste[index_liste:])
    return convert_list_to_http(entete,corp,reseau)

def condition_fin_corp(liste,i):
    #Test qu'il y a bien encore 1 éléments a lire
    return ( len(liste) - i ) > 1 

def condition_fin_entete(liste,i):
    #Test qu'il y a bien encore 4 éléments a lire
    if len(liste) - i >= 4 :
        liste[i] = liste[i].lower() #convertit minuscule
        liste[i+1] = liste[i+1].lower()
        liste[i+2] = liste[i+2].lower()
        liste[i+3] = liste[i+3].lower()
        return liste[i] == "0d" and liste[i+1] == "0a" and liste[i+2] == "0d" and liste[i+3] == "0a" 
    return True

def convert_hexa_to_string(hexa):
    code_ascii = int(hexa,16)
    return chr(code_ascii) 

def valide_http(liste) :
    
    liste_resultat = []
    if len(liste) >= 4 :
        
        temp_str = ""
        for i in range(4):
            temp_str = temp_str + liste[i] 
            temp_str = temp_str.lower()
            #Si la methode est post on traite normalement
            if temp_str == "post" :
                
                return liste
            #Si la methode est differente alors on prends on compte uniquement l'entete http
        i = 0
       
        while not condition_fin_entete(liste,i)  :
            liste_resultat.append(liste[i])
            i+=1
        
        liste_resultat.append("0d")
        liste_resultat.append("0a")
        liste_resultat.append("0d")
        liste_resultat.append("0a")

    return liste_resultat  


def calcule_entete_http(liste) :
    i = 0
    #resultat est une liste[liste[str]] ou chaque liste corresponds a une ligne
    #chaque ligne est composer de mot
    resultat = []
    temp_str = ""
    temp_list = []
    
    
    liste = valide_http(liste)

    while not condition_fin_entete(liste,i):
        liste[i] = liste[i].lower() #convertit minuscule
        liste[i+1] = liste[i+1].lower()
       
        if liste[i] == "20": #code ascii espace
            temp_str = temp_str + " "
            temp_list.append(temp_str)
            temp_str = ""

        elif liste[i] == "0a" and liste[i+1] != "0a" : #code ascii retour a la ligne ne pas ajouter saut de ligne
            i+= 1
            continue

        elif liste[i] == "0d" and liste[i+1] == "0a" : #code ascii retour a la ligne et retour chariot
            temp_list.append(temp_str)
            resultat.append(temp_list)
            temp_str = ""
            temp_list = []
            
        else :
            temp_str = temp_str + convert_hexa_to_string(liste[i])

        
        i += 1 
    
    i+= 4 #On ajoute le 0x0d 0x0a 0x0d 0x0a qui indiquent la fin de l'entete
    #On ajoute le dernier mot a notre ligne
    temp_list.append(temp_str)
    #On ajoute la derniere ligne au resultat
    resultat.append(temp_list)
    return resultat,i

def calcule_corp_http(liste) :
    i = 0
    #resultat est une liste[liste[str]] ou chaque liste corresponds a une ligne
    #chaque ligne est composer de mot
    resultat = []
    temp_str = ""
    temp_list = []


    while condition_fin_corp(liste,i):
        liste[i] = liste[i].lower() #convertit minuscule
        liste[i+1] = liste[i+1].lower()
    
        if liste[i] == "20": #code ascii espace
            temp_str = temp_str + " "
            temp_list.append(temp_str)
            temp_str = ""
        
        elif liste[i] == "0d" and liste[i+1] == "0a" : #code ascii retour a la ligne et retour chariot
            temp_list.append(temp_str)
            resultat.append(temp_list)
            temp_str = ""
            temp_list = []
        
        else :
            temp_str = temp_str + convert_hexa_to_string(liste[i])

        i += 1 

    return resultat

def convert_list_to_http(entete,corp,reseau):
    http = ""
    temp = ""
    #print("aaa")
    #print(len(entete))
    if len(entete) > 1 : #Entete non vide
        if reseau.argument_main["detaille"] == True :
            http = detaille_http(entete,corp,reseau)
        else :
            http = non_detaille_http(entete,corp,reseau)
    
    return http

def detaille_http(entete,corp,reseau):
    http = "----------------- La partie Http ----------------------------- \n"
    http = http + "Entete \n"
    for ligne in entete :
        temp = ""
        for mot in ligne :
            temp = temp + mot 
        temp = "\t" + temp
        http = http + temp + "\n"
    
    if len(corp) > 0 :
        http = http + "Corps \n"
        for ligne in corp :
            temp = ""
            for mot in ligne :
                temp = temp + mot 
            temp = "\t" + temp
            http = http + temp + "\n"
    
    return http

def non_detaille_http(entete,corp,reseau):
    http = ">Http \n"
    http = http + "\t>Entete \n"
    for ligne in entete :
        temp = ""
        for mot in ligne :
            temp = temp + mot 
        temp = "\t\t" + temp
        http = http + temp + "\n"
    
    if len(corp) > 0 :
        http = http + "Corps \n"
        for ligne in corp :
            temp = ""
            for mot in ligne :
                temp = temp + mot 
            temp = "\t\t" + temp
            http = http + temp + "\n"
    
    return http


def int_to_hexa_to_str(variable):
    return  " (" + str(hex(int(variable))) + ") "

def hexa_to_int_str(variable):
    return " (" + str(int(variable,16)) + ") "


def detaille(Tcp):
    tcp = "----------------- La partie Tcp ----------------------------- \n"
    tcp = tcp + "Le port source est :" +  str(Tcp.port_source) + int_to_hexa_to_str(Tcp.port_source) + ".\n"
    tcp = tcp + "Le port destination est :" +  str(Tcp.port_dest)+ int_to_hexa_to_str(Tcp.port_dest) +".\n"
    tcp = tcp + "Le numero de sequence est :" + str(Tcp.sequence_number) + int_to_hexa_to_str(Tcp.sequence_number) + ".\n"
    tcp = tcp + "Le numero d'acquittement est :" + str(Tcp.acknowledgment_number) + int_to_hexa_to_str(Tcp.acknowledgment_number) + ".\n"
    tcp = tcp + "La taille de l'entete est :" + Tcp.thl +" octets "+ int_to_hexa_to_str(Tcp.thl) +".\n"
    tcp = tcp + "La partie reserve pour usage futur est :" + Tcp.reserved + ".\n"
    tcp = tcp + list_to_string(decrit_drapeau(Tcp.drapeau))
    tcp = tcp + "La taille de la fenetre est :" + str(Tcp.window)+" octets " + int_to_hexa_to_str(Tcp.window) + ".\n"
    tcp = tcp + "Le checksum est :" + "0x" +Tcp.checksum + hexa_to_int_str(Tcp.checksum)+ ".\n"
    tcp = tcp + "Les poiteurs de donnees urgentes sont :" + Tcp.urgent_pointeur + ".\n"
    tcp = tcp + "La taille des options est :" + str(Tcp.option) + int_to_hexa_to_str(Tcp.option)+ ".\n"
    tcp = tcp + "La partie remplissage est :" + str(Tcp.padding) + ".\n\n\n"
    tcp = tcp + Tcp.data 
    return tcp

def non_detaille(Tcp):
    tcp = ">Transmission Control Protocol\n"
    tcp = tcp + "\tSource Port :" +  str(Tcp.port_source) + int_to_hexa_to_str(Tcp.port_source) + ".\n"
    tcp = tcp + "\tDestination Port :" +  str(Tcp.port_dest)+ int_to_hexa_to_str(Tcp.port_dest) +".\n"
    tcp = tcp + "\tSequence Number :" + str(Tcp.sequence_number) + int_to_hexa_to_str(Tcp.sequence_number) + ".\n"
    tcp = tcp + "\tAcknowledgment Number :" + str(Tcp.acknowledgment_number) + int_to_hexa_to_str(Tcp.acknowledgment_number) + ".\n"
    tcp = tcp + "\tHeader Length :" + Tcp.thl +" octets "+ int_to_hexa_to_str(Tcp.thl) +".\n"
    tcp = tcp + "\tReserved:" + Tcp.reserved + ".\n"
    tcp = tcp + list_to_string(decrit_drapeau_non_detaille(Tcp.drapeau))
    tcp = tcp + "\tWindow :" + str(Tcp.window)+" octets " + int_to_hexa_to_str(Tcp.window) + ".\n"
    tcp = tcp + "\tChecksum :" + "0x" +Tcp.checksum + hexa_to_int_str(Tcp.checksum)+ ".\n"
    tcp = tcp + "\tUrgent Pointer :" + Tcp.urgent_pointeur + ".\n"
    tcp = tcp + "\tOption Length :" + str(Tcp.option) + int_to_hexa_to_str(Tcp.option)+ ".\n"
    tcp = tcp + "\tRembourrage Length :" + str(Tcp.padding) + ".\n\n\n"
    tcp = tcp + Tcp.data 
    return tcp
    