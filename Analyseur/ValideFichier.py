from Reseau import *
import copy

def convert_fichier_ligne(nom_fichier):
    reseau = Reseau()
    try :
        f=open(nom_fichier,"r")
        fichier2 = fichier_to_liste(f)
        fichier = enleve_ligne_commentaire(fichier2) #enleve ligne de commentaire entre les trame
       
        longeur = len(fichier)
  
        for ligne in range(longeur) :
            
            reseau.valide_courant = True
            l = fichier[ligne].split()
            l = enleve_commentaire(l,reseau) #enleve les commentaires
            reseau.taille_lire = taille_lecture(fichier,ligne,l)
            
            test_ligne(l,reseau)
            reseau.ligne_courant += 1
        
        test_longeur_fichier_min_trame1(reseau)
        f.close()
    except FileNotFoundError :
        reseau.erreur.append("Erreur le chemin saisie ne possede pas le fichier " + nom_fichier + " .\n")

    except :
        reseau.erreur.append("Erreur ouverture du fichier.\n")
    
    return reseau

def enleve_ligne_commentaire(fichier):
    fic = []
    for ligne in range(len(fichier)) :
        
        lis = fichier[ligne].split()
       
        if len(lis) > 0 :
            if est_un_hexadecimal(lis) == True:
                fichier[ligne] = modifie_liste(lis,lis[0][2:])
                fic.append(fichier[ligne])
                continue

            #Verifie que la chaine n'est pas un commentaire
            if test_commentaire(lis[0],None) == False :
                continue
            
            #Verifie que la chaine est bien en hexa
            if  test_chaine_code_hexa(lis[0],None) == False  :
                continue

            fic.append(fichier[ligne])

    return fic

def est_un_hexadecimal(chaine):
    if chaine[0][0:2] == "0x":
        return True
    return False

def modifie_liste(liste,valeur):
    #modifie offset
    liste[0] = valeur
    espace = " "
    return espace.join(liste)



def taille_lecture(fichier,index,liste_courante):
    #Si le fichier contient une ligne ou
    #Si on arrive a la fin de fichier 
    l1 = fichier[index].split()
  
    if (index  == 0 and len(fichier) == 0) or (index + 1 >= len(fichier)) :
        return len(liste_courante) # ont lit alors la taille de la ligne courante 

    l2 = fichier[index+1].split()
    #Si la ligne suivante est une nouvelle trame
    if int(l2[0],16) == 0 :
        return len(liste_courante)  # ont lit alors la taille de la ligne courante 

    #Sinon on regarde le nombre d'octet a lire en regarde la taille de l'offset de la ligne suivante
    return int(l2[0],16) - int(l1[0],16)  + 1
    
def fichier_to_liste(fichier):
    liste = []
    for i in fichier :
        liste.append(i)  
    return liste

def enleve_commentaire(liste,reseau) :
    l = [liste[0]]
    for i in range(1,len(liste)) :
        if test_longeur_chaine_deux_octet(liste[i],reseau) == False :
           continue

        if test_chaine_code_hexa(liste[i],reseau) == False :
            continue
        
        l.append(liste[i])
    
    return l

def test_ligne(liste,reseau) :
    if reseau.taille_lire < len(liste) :
        liste = liste[:reseau.taille_lire]

    if reseau.taille_lire > len(liste) :
        reseau.erreur.append("Erreur ligne : " + str(reseau.ligne_courant) + ".\n")
        reseau.erreur.append("Erreur ligne : le nombre d'octets a lire ne corresponds pas a l'offset.\n")
    
    if len(liste) <= 0 : #Test ligne non vide
        return False
    #Valider une ligne = valider offset + reste ligne
    if valide_offset(liste[0],reseau) == False :
        return False
     
    if valide_composition_trame(liste,reseau) == False :
        return False
    
    return True

def test_chaine_code_hexa(chaine,reseau) :
    #Verifie que la chaine est bien en hexa
    for i in range(len(chaine)) :
        #Test chaque caractere
        if test_hexadecimal(chaine[i],reseau) == False :
            return False
    return True

def test_commentaire(chaine,reseau):
    #Verifie que la chaine est bien en hexa
    for i in range(len(chaine)) :
        #Test chaque caractere
        if test_hexadecimal(chaine[i],reseau) == False :
            return False
    return True

def valide_offset(offset,reseau) :
    #Verifie que la chaine n'est pas un commentaire
    if test_commentaire(offset,reseau) == False :
        return False

    #Verifie que la chaine est bien en hexa
    if  test_chaine_code_hexa(offset,reseau) == False :
        return False
    
    #Verifie que la valeur maximum n'est pas depasse
    if test_valeur_offset(offset) == False :
        return False
    
    #Verifie que l'offset courant pointe bien vers le bon octet courant
    if test_offset_courant(offset,reseau) == False :
        return False
    
    return True   

def test_longeur_fichier_min_trame1(reseau):
    if reseau.nombre_trame == 1 :
        #Test le cas ou le fichier contient une seul trame et la trame est inferieur a la taille minimum
        if len(reseau.trame) < 60 :
                
            reseau.erreur.append("Erreur ligne : " + str(reseau.ligne_courant) + ".\n")
            reseau.erreur.append("Erreur la trame numero " + str(reseau.nombre_trame) + " est trop petite.\n")
            reseau.erreur.append("Sa taille est " + str(len(reseau.trame)) + " alors que la taille minimum est 60 octets.\n")

            for i in range(len(reseau.trame)) :
                reseau.trame.pop()
        
        reseau.trame_total.append(reseau.trame)
    return reseau

def test_offset_courant(offset,reseau) :
    #nouvelle trame
    if int(offset,16) == 0 :
        reseau.nombre_trame += 1
   
    #Ici on ajoute les trames , lorsqu'il y en a plus de deux
    if int(offset,16) == 0 and reseau.nombre_trame > 1:
        reseau.trame_total.append(reseau.trame)
        reseau.trame = []
    
    #nouvelle trame et notre fichier contient plus de 1 trame
    if int(offset,16) == 0 and reseau.nombre_trame > 1:
        #taille min trame 
        if reseau.offset_courant < 60 :
            
            reseau.erreur.append("Erreur ligne : " + str(reseau.ligne_courant) + ".\n")
            reseau.erreur.append("Erreur la trame numero " + str(reseau.nombre_trame) + " est trop petite.\n")
            reseau.erreur.append("Sa taille est " + str(len(reseau.trame) )+ " alors que la taille minimum est 60 octet.\n")

            for i in range(len(reseau.trame)) :
                reseau.trame.pop()
            
        reseau.offset_courant = 0
        return True
    
    #Trame n'indique pas la bonne position
    if int(offset,16) != reseau.offset_courant :
        reseau.erreur.append("Erreur ligne : " + str(reseau.ligne_courant) + ".\n")
        reseau.erreur.append("Erreur l'offset " +  str(int(offset,16)) + " ne correspond pas avec la position courante " + str(reseau.offset_courant) + ".\n")
        return False

    return True 

def test_valeur_offset(offset) :
    #taille max trame
    #valeur prise annexe td 6 sans preambule et crc
    return int(offset,16) >= 0 and int(offset,16) <= 1514       
#### TEST OFFSET ####

def valide_composition_trame(liste,reseau) :
    #Verifie que la longeur de la ligne est valide
    for i in range(1,len(liste)) :
        reseau.trame.append(liste[i])
        reseau.index_courant += 1
        reseau.offset_courant += 1
    return True 


def test_longeur_chaine_deux_octet(offset,reseau) :
    #Test qu'il est bien sur 2bits
    #On ignore et on passe a la ligne suivant
    if len(offset) != 2 :
        return False 

    #Il est bien sur 2 bits
    return True
    
def test_hexadecimal(x,reseau):
    """Test qu'un caractere est bien en hexadecimal.
       Permet de savoir si un debut de ligne n'est pas un offset alors on ignore la ligne"""
    try :
        return int(x,16) >= 0 and int(x,16) <= 15

    except :
        return False
