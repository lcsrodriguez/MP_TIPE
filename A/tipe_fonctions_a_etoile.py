"""
Implémentation des fonctions nécessaires aux algorithmes A* et PA*
(avec et sans pondération)
"""

## Importation des modules nécessaires
import math
import datetime
import time
import os
import random as rd
import matplotlib as mpl
import matplotlib.pyplot as plt

## Fonctions générales

def affiche(M):
    """ Affichage propre d'une matrice """
    for ligne in M:
        print(ligne)

def bernoulli(p):
    """ Loi de Bernoulli de param p """
    if rd.random() < p:
        return 1
    else:
        return 0

## Heuristiques utilisées

def heuristique_manhattan(noeudA, noeudB):
    """ Fonction heuristique retournant la distance de Manhattan entre 2 objets de type noeud """
    Ax, Ay = noeudA.x, noeudA.y
    Bx, By = noeudB.x, noeudB.y
    
    dist = abs(Bx - Ax) + abs(By - Ay)
    return dist

def heuristique_euclidienne(noeudA, noeudB):
    """ Fonction heuristique retournant la distance d'euclidienne entre 2 objets de type noeud """
    Ax, Ay = noeudA.x, noeudA.y
    Bx, By = noeudB.x, noeudB.y

    dist = (Bx - Ax)**2 + (By - Ay)**2
    return math.sqrt(dist)              # attention aux flottants


## Classes nécessaires (classes Noeud et Grille)

class Noeud:
    def __init__(self, x, y, empruntable):
        """ Méthode de construction d'une instance Noeud """
        self.x = x                              # abscisse de la case
        self.y = y                              # ordonnée de la case
        self.empruntable = empruntable          # booléen indiquant s'il s'agit d'un obstacle ou non
        self.g = 0                              # coût g (distance source - noeud)
        self.h = 0                              # coût h (distance noeud - cible)
        self.f = 0                              # coût f = g + h
        self.parent = self                      # parent du noeud (initialisé à lui-même)

    def __str__(self):
        """ Méthode de représentation du Noeud """
        return "Noeud ({},{})".format(self.x, self.y)
    
class Grille:
    def __init__(self, N, p):
        """ Méthode de construction 
        - N: largeur de la grille
        - p: probabilité d'avoir une case empruntable 
        """
        self.N = N
        self.p = p
        self.grille = [[None for j in range(self.N)] for i in range(self.N)] # création de la grille vide
        
        for i in range(self.N):
            for j in range(self.N):
                self.grille[i][j] = Noeud(i, j, bernoulli(self.p))           # remplissage de la grille
    
    def voisinage_4directions(self, noeud):
        """ Méthode retournant le voisinage d'un noeud suivant un système NSEO """
        noeud_x = noeud.x
        noeud_y = noeud.y
        
        voisins = []
        
        X = noeud_x - 1
        Y = noeud_y
        if (X >= 0 and X < self.N) and (Y >= 0 and Y < self.N):
            voisins.append(self.grille[X][Y])
        
        X = noeud_x + 1
        Y = noeud_y
        if (X >= 0 and X < self.N) and (Y >= 0 and Y < self.N):
            voisins.append(self.grille[X][Y])
                    
        X = noeud_x
        Y = noeud_y - 1
        if (X >= 0 and X < self.N) and (Y >= 0 and Y < self.N):
            voisins.append(self.grille[X][Y])
                    
        X = noeud_x
        Y = noeud_y + 1
        if (X >= 0 and X < self.N) and (Y >= 0 and Y < self.N):
            voisins.append(self.grille[X][Y])
        return voisins
        

    def voisinage_8directions(self, noeud):
        """ Méthode retournant le voisinage d'un noeud suivant un système N-NE-E-SE-S-SO-O-NO """
        noeud_x = noeud.x
        noeud_y = noeud.y
        
        voisins = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                X = noeud_x + x
                Y = noeud_y + y
                if (X >= 0 and X < self.N) and (Y >= 0 and Y < self.N):
                    voisins.append(self.grille[X][Y])
        return voisins