"""
Implémentation files de priorité


4 solutions (classe Python)
- FPLI()        :   Coût majoritaire sur l'insertion dans la file de priorité   (liste chaînée)
- FPLS()      :   Coût majoritaire sur la sélection/suppression dans la file de priorité      (liste chaînée)
- FPTR()     :   Implémentation avec le module heapq utilisant un tas binaire
- FPTH()      :   Implémentation "maison" utilisant un tas binaire


ATTENTION DEPENDANCE

Les classes ci-dessous utilisent un dictionnaires des distances implémenté dans Dijkstra


"""
# Importation des modules nécessaires
import heapq

## FPLI

class FPLI:
    def __init__(self):
        self.file = []
        
    def taille(self):
        return len(self.file)
    
    def estVide(self):
        return self.taille() == 0
    
    def filer(self, sommet, distances):
        # si la file est vide, on met l'élément au début
        if self.estVide():
            self.file.append(sommet)
        else:
            # pour chaque élément de la file
            for k in range(self.taille()):
                # si la distance source - sommet  est supérieure à la distance source - sommet k
                if distances[sommet] >= distances[self.file[k]]:
                    # si l'élément est le dernier
                    if k == self.taille() - 1:
                        self.file.insert(k + 1, sommet) # on insére l'élément
                    else:
                        continue # on passe au suivant
                else:
                    self.file.insert(k, sommet) # on insére l'élément
    
    def defiler(self):
        try:
            return self.file.pop(0)
        except IndexError:
            return "Erreur"

## FPLS

class FPLS:
    def __init__(self):
        self.file = []
        
    def taille(self):
        return len(self.file)
    
    def estVide(self):
        return self.taille() == 0
        
    def filer(self, sommet):
        self.file.append(sommet)
        
    def defiler(self, distances):
        minSommet = self.file[0]
        minIndex = 0
        minDistance = distances[minSommet]
        
        for i in range(self.taille()):
            sommet = self.file[i]
            distance = distances[sommet]
            
            if minDistance >= distance:
                minSommet = sommet
                minIndex = i
                minDistance = distances[minSommet]
        m = minSommet
        
        self.file.remove(minSommet)
        return m

## FPTR

class FPTR:
    def __init__(self):
        self.file = []
    
    def taille(self):
        return len(self.file)
    
    def estVide(self):
        return self.taille() == 0
    
    def filer(self, sommet, distances):
        distance = distances[sommet]
        heapq.heappush(self.file, (distance, sommet))
    
    def defiler(self):
        try:
            sommet = heapq.heappop(self.file)
            return sommet[1]
        except IndexError:
            return "Erreur"

## FPTH


# Fonctions préliminaires
def gauche(i):
    """ Fonction renvoyant l'indice du fils gauche de i """
    return 2*i + 1

def droite(i):
    """ Fonction renvoyant l'indice du fils droit de i """
    return 2*(i + 1)

def pere(i):
    """ Fonction renvoyant l'indice du père de i """
    return (i - 1)//2

def estTas(T):
    """ Fonction booléenne vérifiant si T est un tas		 """
    n = len(T)
    for i in range(1, n):
        if T[pere(i)] < T[i]:
            return False
    return True
    
# Algorithme principal
def maxi(T, i, lim):
    """ 
    Fonction retournant l'indice (inférieur à lim) de la plus grande des 3 valeurs 
    entre T[i], T[gauche(i)] et T[droite(i)]
    """
    n = len(T)
    assert i >= 0
    assert i < lim
    assert lim <= n
    
    i_max = i
    
    g = gauche(i)
    d = droite(i)
    
    if g < lim and T[g][1] > T[i_max][1]:
        i_max = g
    if d < lim and T[d][1] > T[i_max][1]:
        i_max = d
    
    return i_max
    
def echange_elements(T, a, b):
    """ Fonction d'échange de 2 éléments dans le tas """
    temp = T[a]
    T[a] = T[b]
    T[b] = temp

def entasserRecursif(T, i, lim):
    """ Fonction d'entassement (récursif) """
    i_max = maxi(T, i, lim)
    if i_max != i:
        echange_elements(T, i, i_max)
        entasserRecursif(T, i_max, lim)

def entasserInteratif(T, i, lim):
    """ Fonction d'entassement (itératif) """
    i_max = maxi(T, i, lim)
    
    while i_max != i:
        echange_elements(T, i, i_max)
        i = i_max
        i_max = maxi(T, i, lim)
        
def construireTas(T):
    """ Fonction de construction d'un tas """
    for i in range((len(T) - 1)//2, -1, -1):
        entasserInteratif(T, i, len(T))
     
def trierTas(T):
    """ Fonction de triage par tas """
    for i in range(len(T) - 1, 0, -1):
        echange_elements(T, 0, i)
        entasserInteratif(T, 0, i)


class FPTH:
    def __init__(self, T):
        self.T = T
    
    def trier(self):
        construireTas(T)
        trierTas(T)
        return T
    
    def defiler(self):
        try:
            return T.pop(0)
        except IndexError:
            return "Erreur"
        
## Test classe FPTH
"""
T = [(2, 25), (1, 10), (5, 200), (3, 45), (4, 30)]
print("Ancien T :", T, "\n")
U = FPTH(T)
print("Après traitement : ", U)"""