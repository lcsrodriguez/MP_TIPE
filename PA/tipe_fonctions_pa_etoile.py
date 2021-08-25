"""
Implémentation des fonctions nécessaires à l'algorithme PA*
(avec pondération)
"""

## Importation des modules nécessaires
import math
import datetime
import time
import os
import random
import matplotlib as mpl
import matplotlib.pyplot as plt

#mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#mpl.rc("text", usetex=True)

## Fonctions générales

def affiche(M):
    """ Affichage propre d'une matrice """
    for ligne in M:
        print(ligne)

def bernoulli(p):
    """ Loi de Bernoulli de param p """
    if random.random() < p:
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

def heuristique_tchebychev(noeudA, noeudB):
    Ax, Ay = noeudA.x, noeudA.y
    Bx, By = noeudB.x, noeudB.y
    
    dist = max(abs(Bx - Ax), abs(By - Ay))
    return dist

def heuristique_euclidienne(noeudA, noeudB):
    """ Fonction heuristique retournant la distance d'euclidienne entre 2 objets de type noeud """
    Ax, Ay = noeudA.x, noeudA.y
    Bx, By = noeudB.x, noeudB.y

    dist = (Bx - Ax)**2 + (By - Ay)**2
    return math.sqrt(dist)              # attention aux flottants


## Classes nécessaires (classes Noeud et Grille)

class Noeud:
    def __init__(self, x, y, w):
        """ Méthode de construction d'une instance Noeud """
        self.x = x                              # abscisse de la case
        self.y = y                              # ordonnée de la case
        self.w = w                              # pondération de la case
        self.empruntable = 0                    # booléen indiquant s'il s'agit d'un obstacle ou non
        
        if self.w != -1:
            self.empruntable = 1
        
        self.g = 0                              # coût g (distance source - noeud)
        self.h = 0                              # coût h (distance noeud - cible)
        self.f = 0                              # coût f = g + h
        self.parent = self                      # parent du noeud (initialisé à lui-même)

    def __str__(self):
        """ Méthode de représentation du Noeud """
        return "Noeud ({},{})".format(self.x, self.y)
    
class Grille:
    def __init__(self, n, p = 0.8, wmin = 1, wmax = 100):
        """ Méthode de construction 
        - N: largeur de la grille
        - p: probabilité d'avoir une case empruntable 
        """
        self.n = n                  # nombre de lignes
        self.p = p                  # probabilité d'avoir un obstacle
        self.wmin = wmin            # borne inférieure 
        self.wmax = wmax
        
        # Création de la grille 
        self.grille = [[None for j in range(self.n)] for i in range(self.n)]
        
        # Remplissage de la grille
        for i in range(self.n):
            for j in range(self.n):
                if bernoulli(self.p):
                    self.grille[i][j] = Noeud(i, j, random.randint(self.wmin, self.wmax))
                else:
                    self.grille[i][j] = Noeud(i, j, -1)
    
    def selection_source_cible(self):
        """ Fonction sélectionnant 2 cases (source et cible) pour une simulation """
        b = False
        while not b:
            xs, xc = random.sample(range(self.n), 2)
            ys, yc = random.sample(range(self.n), 2)
            
            if self.grille[ys][xs].empruntable or self.grille[yc][xc].empruntable:
                b = True

        self.s = (xs, ys)
        self.c = (xc, yc)
    
    def voisinage_4directions(self, noeud):
        """ Méthode retournant le voisinage d'un noeud suivant un système NSEO """
        noeud_x = noeud.x
        noeud_y = noeud.y
        
        voisins = []
        
        X = noeud_x - 1
        Y = noeud_y
        if (X >= 0 and X < self.n) and (Y >= 0 and Y < self.n):
            voisins.append(self.grille[X][Y])
        
        X = noeud_x + 1
        Y = noeud_y
        if (X >= 0 and X < self.n) and (Y >= 0 and Y < self.n):
            voisins.append(self.grille[X][Y])
                    
        X = noeud_x
        Y = noeud_y - 1
        if (X >= 0 and X < self.n) and (Y >= 0 and Y < self.n):
            voisins.append(self.grille[X][Y])
                    
        X = noeud_x
        Y = noeud_y + 1
        if (X >= 0 and X < self.n) and (Y >= 0 and Y < self.n):
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
                
                if (X >= 0 and X < self.n) and (Y >= 0 and Y < self.n):
                    voisins.append(self.grille[X][Y])
        return voisins