"""
Implémentation algorithme PA*
(avec pondération)
"""

# Importation des fonctions générales
from tipe_fonctions_pa_etoile import *

def initialisation(G, source):
    """ Fonction d'initialisation """
    liste_ouverte = [source]
    liste_fermee = []
    chemin = []
    
    sommet_courant = source
    
    return liste_ouverte, liste_fermee, chemin, sommet_courant

def selection_sommet_courant(liste_ouverte):
    """ Fonction de sélection du sommet courant """
    sommet_courant = liste_ouverte[0]
    
    for k in range(0, len(liste_ouverte)):
        if liste_ouverte[k].f < sommet_courant.f:
            sommet_courant = liste_ouverte[k]
    return sommet_courant

def successeurs_sommet_courant_4_directions(G, sommet_courant):
    """ Fonction retournant les successeurs du sommet courant dans G """
    return G.voisinage_4directions(sommet_courant)
    
def successeurs_sommet_courant_8_directions(G, sommet_courant):
    """ Fonction retournant les successeurs du sommet courant dans G """
    return G.voisinage_8directions(sommet_courant)

def relachement_sommet(alpha, voisin, sommet_courant, cible, liste_ouverte, liste_fermee, f_h):
    """ Procédure de relâchement du sommet """
    new_g = voisin.parent.g
    new_h = f_h(cible, voisin)
    new_f = new_g + new_h + alpha * voisin.w        # implémentation des pondérations
    
    if voisin in liste_ouverte:
        if new_g < voisin.g:
            voisin.parent = sommet_courant
            voisin.g = new_g
            voisin.h = new_h
            voisin.f = new_f
    else:
        liste_ouverte.append(voisin)
        voisin.parent = sommet_courant
        voisin.g = new_g
        voisin.h = new_h
        voisin.f = new_f
    
def construction_chemin(source, cible, liste_ouverte, chemin):
    """" Fonction de construction du chemin trouvé """
    if len(liste_ouverte) == 0:
        return chemin
    
    n = cible
    while n != source:
        chemin.append(n)
        n = n.parent
    chemin.append(source)
    chemin.reverse()
    
    return chemin

## Algorithme principal

def algorithme_pa_etoile(G, s, c, f_v, f_h, alpha = 1):
    """
    Description:
    
    
    Entrée:
        G       : grille (objet de type Grille)
        s       : noeud source (objet de type Noeud)
        c       : noeud cible (objet  de type Noeud)
        f_v     : fonction de voisinage
        f_h     : fonction heuristique (distance courant -> cible)
        alpha   : coefficient d'amplification des pondérations
    
    Sortie:
        chemin : itinéraire choisi
    """
    source, cible = s, c
    assert source != cible
    
    
    # Initialisation
    liste_ouverte, liste_fermee, chemin, sommet_courant = initialisation(G, source)
    
    # Bouclage du processus
    while len(liste_ouverte) > 0:
        # Sélection du sommet courant
        sommet_courant = selection_sommet_courant(liste_ouverte)
        if sommet_courant == cible:
            break
        
        # Transfert du sommet courant
        liste_ouverte.remove(sommet_courant)
        liste_fermee.append(sommet_courant)
        
        # Etape de relâchement
        for voisin in f_v(G, sommet_courant):
            if voisin in liste_fermee or voisin.empruntable == 0:
                continue
                
            relachement_sommet(alpha, voisin, sommet_courant, cible, liste_ouverte, liste_fermee, f_h)
        
    return construction_chemin(source, cible, liste_ouverte, chemin)