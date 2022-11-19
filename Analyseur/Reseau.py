class Reseau :
    def __init__(self): # Notre méthode constructeur
        """Objet contenant plusieurs parametre utile pour valider le fichier contenant les trames."""
        self.index_courant = 0
        self.offset_courant = 0
        self.taille_lire = 0
        self.ligne_courant = 1
        self.valide_courant = True
        self.nombre_trame = 0
        self.trame_total = []
        self.trame = []
        self.erreur = []
        self.argument_main = {}
        self.texte = ""


def texte_afficher(reseau) :
    if fichier_erreur(reseau):
        return assemble_texte(reseau.erreur)

    return reseau.texte

def fichier_erreur(reseau):
    return reseau.erreur != []

def assemble_texte(liste):
    resultat = ""
    for i in liste :
        resultat = resultat + i
    return resultat

def argument_general_to_dict(args):
    dict = {}
    dict["detaille"] = args.detaille
    dict["nom_fichier"] = args.nom_fichier
    dict["sauvegarde"] = args.sauvegarde

    return dict