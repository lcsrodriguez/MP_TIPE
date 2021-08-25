"""
Implémentation algorithme A* général
(sans pondération)
"""

# importation des fonctions générales
from tipe_fonctions_a_etoile import *

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

def relachement_sommet(voisin, sommet_courant, cible, liste_ouverte, liste_fermee, f_h):
    """ Procédure de relâchement du sommet """
    new_g = voisin.parent.g
    new_h = f_h(cible, voisin)
    new_f = new_g + new_h
    
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
##

##
def algorithme_a_etoile(G, s, c, f_v, f_h):
    """
    Description:
    
    
    Entrée:
        G   : grille (objet de type Grille)
        s   : noeud source (objet de type Noeud)
        c   : noeud cible (objet  de type Noeud)
        f_v : fonction de voisinage
        f_h : fonction heuristique (distance couran -> cible)
    
    Sortie:
        chemin : itinéraire choisi
        l      : nbre d'intermédiaires
        omega  : coût total de l'itinéraire
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
                
            relachement_sommet(voisin, sommet_courant, cible, liste_ouverte, liste_fermee, f_h)
        
    return construction_chemin(source, cible, liste_ouverte, chemin)


## Algorithme A*
def a_etoile(G, s, c):
    """
    Fonction appliquant l'algorithme A* à une grille G
    en partant d'un noeud de départ s pour arriver à un noeud d'arrivée c
    
    Entrées:
        G: grille (objet de type Grille)
        s: noeud de départ (objet de type Noeud)
        c: noeud d'arrivée (objet de type Noeud)
        f_v: fonction de voisinages
        f_h: fonction heuristique de h
    
    Sortie:
        CHEMIN_FINAL: chemin final
        l: nbre de sommets empruntés par CHEMIN_FINAL
        d: 
    """

    # Déclaration des variables
    LISTE_OUVERTE = []
    LISTE_FERMEE  = []
    
    CHEMIN_FINAL = []
    
    source = s
    cible = c
    
    CURRENT = source
    LISTE_OUVERTE.append(source)
    
    # Tant que LISTE_OUVERTE n'est pas vide
    while len(LISTE_OUVERTE) > 0:
        CURRENT = getCurrentNode(LISTE_OUVERTE)
        if CURRENT == cible:
            break
        
        LISTE_OUVERTE.remove(CURRENT)
        LISTE_FERMEE.append(CURRENT)
        
        voisins_CURRENT = G.voisinage_8directions(CURRENT)
        
        for voisin in voisins_CURRENT:
            if voisin in LISTE_FERMEE or voisin.empruntable == 0:
                continue
            
            new_g = voisin.parent.g
            new_h = heuristique_euclidienne(cible, voisin)
            new_f = new_g + new_h
            
            if voisin in LISTE_OUVERTE:
                if new_g < voisin.g:
                    voisin.parent = CURRENT
                    voisin.g = new_g
                    voisin.h = new_h
                    voisin.f = new_f
            else:
                LISTE_OUVERTE.append(voisin)
                voisin.parent = CURRENT
                voisin.g = new_g
                voisin.h = new_h
                voisin.f = new_f
    
    if len(LISTE_OUVERTE) == 0:
        return CHEMIN_FINAL
    
    n = cible
    while n != source:
        CHEMIN_FINAL.append(n)
        n = n.parent
    CHEMIN_FINAL.append(source)
    CHEMIN_FINAL.reverse()
    return CHEMIN_FINAL