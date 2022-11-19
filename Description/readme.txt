Analyseur de Protocoles Réseau ‘Offline’ en Python
Dan SERRAF et Melissa MOHELLEBI
17/12/2020

###1/ Introduction:

	Cet analyseur est utilisé pour étudier le trafic envoyé sur un réseau déjà capturé.
	Il comprend :
		- Ethernet (Couche 2)
		- IP (Couche 3)
		- TCP (Couche 4)
		- HTTP (Couche 7)
	L'approche utilisé est similaire à celle de Wirshark lorsque on vas dans le panneau  ‘analyse des entêtes de message’(<https://fr.wikipedia.org/wiki/Wireshark>).


###2/ Architecture:

		# Le fichier ValideFichier.py nous permet de tester la validité du fichier et d'ignorer les commentaires.

		# La Class Reseau nous permet de manipuler le fichier .txt où se trouve notre trame à étudier.

		# La Class TCP permet d'extraire toutes les informations qui concerneTCP. 
		  Elle contient les fonctions qui permettent de calculer chaque champs de ce protocole.

		# La Class IP permet d'extraire toutes les information qui concerne IP. 
		  Elle contient les fonctions qui permettent de calculer chaque champs de ce protocole.

		# La Class Ethernet permet d'extraire toutes les information qui concerne Ethernet.
		  Elle contient les fonctions qui permettent de calculer chaque champs de ce protocole.
 
		# Le fichier main.py récupère les informations saisies par l'utilisateur.
		Puis si les informations saisies par l'utilisateur sont valides, il va faire appelle a la fonction qui va nettoyer la trame et tester ca validiter.
		Si la trame contient des erreures de formations alors le fichier retourne un fichier texte d'erreur qui indique les différents problème a résoudre.
		Si la trame est valide, elle va faire appelle a l'analyseur et retourne alors l'analyse de la trame.
		

###3/ Structure du code 
	*Fonctions de nettoyage et validation fichier:
		#convert_fichier_ligne(nom_fichier): teste la validité du fichier contenant les trames

		#enleve_ligne_commentaire(fichier): enlève tout les lignes qui sont entièrement des commentaires
		#enleve_commentaire(liste,reseau): enlève les commentaires entrelacer ou en fin de ligne

		#detaille(objet): fonction d'affichage détaillé des divers champs de l'objet (avec option -d)
		#non_detaille(objet):fonction d'affichage non détaillé des divers champs de l'objet (sans option -d)

		#valide_offset(offset,reseau) : verifier que l'offset est valide
		--> verifie qu'elle est bien hexadécimal
		--> verifie que la taille minimal de l'offset est atteinte
		--> verifie que la taille maximal de l'offser n'est pas dépasser
		--> verifei que l'offset courant pointe vers l'octet courant ...

		#test_hexadecimal(x,reseau) : verifie qu'un caractere est bien en hexadécimal

	*Fonctions d'analyse:
		#calcule_ethernet(reseau,nombre_trame) : analyse la trame et détermine si le protocole est est IP ou autre puis renvoi une chaine de caractères qui comporte l'adresse mac source et destination, le type et les données.
		
		#calcule_data_ip(liste,reseau): analyse la séquence IP et détermine sa version, l'IHL, le TOS, détermine la longueur total, calcule le fragment offset et l'identification, calcule le cheksum, determine l'adresse source et destination, calcule la taille des options et du padding et pour finir les données.

		#calcule_data_tcp(liste,reseau): analyse la séquence TCP si elle existe et calcule à l'aide de fonctions déjà implémentées le nombre d'octets étudiés les options et leurs tailles calcule les données de http et le renvois sous forme de chaine de caractère qu'on utiliseras ensuite pour l'affichage des résultats.

		#*calcule_entete_http(liste) : analyse l'entete http si elle existe 			#*calcule_corp_http(liste) : analyse et la séquence http si elle existe et renvoi une liste contenant les octets étudiés 
		#*convert_list_to_http(entete,corp): convertie les données récoltées dans les deux fonctions précédentes en une chaine de carractères ainsi elle renvoi le message d'analyse de HTTP		

 
		#***# les fonctions déclarées au dessus utilisent toutes des sous fonctions pour faciliter le calcule de chacun de leurs champs


