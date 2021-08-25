"""
Implémentation de l'algorithme de Dijkstra
"""

## Importation des modules nécessaires

import math
import time
import datetime
import random as rd
import networkx as nx
import matplotlib.pyplot as plt


## Fonctions nécessaires pour l'exécution de Dijkstra (5 au total)

def initialisation(G, source):
    """ Fonction d'initialisation """
    INF = float("inf")
    liste_ouverte = [source]
    liste_fermee = []
    
    distances = {sommet: INF for sommet in G}
    parents = {sommet: sommet for sommet in G}
    chemin = []
    distances[source] = 0
    
    return liste_ouverte, liste_fermee, distances, parents, chemin
    

def selection_sommet_courant(liste_ouverte, distances):
    """ Fonction de sélection du sommet courant """
    sommet_courant = liste_ouverte[0]
    for k in range(0, len(liste_ouverte)):
        if distances[liste_ouverte[k]] < distances[sommet_courant]:
            sommet_courant = liste_ouverte[k]
    return sommet_courant

def successeurs_sommet_courant(G, sommet_courant):
    """ Fonction retournant les successeurs du sommet courant dans G """
    return G[sommet_courant]


def relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents):
    """ Procédure de relâchement du sommet """
    nouveau_cout = distances[sommet_courant] + s[1]
    if s[0] in liste_ouverte:
        if nouveau_cout < distances[s[0]]:
            distances[s[0]] = nouveau_cout
            parents[s[0]] = sommet_courant
    else:
        liste_ouverte.append(s[0])
        distances[s[0]] = nouveau_cout
        parents[s[0]] = sommet_courant

def construction_chemin(source, cible, liste_ouverte, parents, chemin):
    """ Fonction de construction du chemin trouvé """
    if len(liste_ouverte) == 0:
        return []
    else:
        n = cible
        while n != source:
            chemin.append(n)
            n = parents[n]
        chemin.append(source)
        chemin.reverse()
        return chemin
        
## Fonction primaire (Algorithme de Dijkstra)

def dijkstra(G, source, cible):
    """ Fonction implémentant l'algorithme de Dijkstra """
    assert source != cible
    
    # Initialisation
    liste_ouverte, liste_fermee, distances, parents, chemin = initialisation(G, source)
    while len(liste_ouverte) > 0:
        # Sélection du sommet
        sommet_courant = selection_sommet_courant(liste_ouverte, distances)
        if sommet_courant == cible:
            break
        # Transfert du sommet
        liste_ouverte.remove(sommet_courant)
        liste_fermee.append(sommet_courant)
        
        # Etape de relâchement de chaque successeur du sommet courant
        for s in successeurs_sommet_courant(G, sommet_courant):
            if s[0] in liste_fermee:
                continue # passer au suivant
                
            relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents)
            
    # renvoyer le chemin trouvé
    return construction_chemin(source, cible, liste_ouverte, parents, chemin), distances[cible]