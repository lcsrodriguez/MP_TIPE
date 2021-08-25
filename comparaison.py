"""
Etude comparative des différentes solutions


- Dijkstra (FPLI)
- Dijkstra (FPLS)
- Dijkstra (FPTR)


"""

from files_priorite import *
import random
import time
import matplotlib.pyplot as plt
plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = True

# Fonctions nécessaires
def successeurs_sommet_courant(G, sommet_courant):
    """ Fonction retournant les successeurs du sommet courant dans G """
    return G[sommet_courant]

def construction_chemin(source, cible, liste_ouverte, parents, chemin):
    """ Fonction de construction du chemin trouvé """
    if liste_ouverte.taille() == 0:             ###
        return []
    else:
        n = cible
        while n != source:
            chemin.append(n)
            n = parents[n]
        chemin.append(source)
        chemin.reverse()
        return chemin
        
##

        # Dijkstra (FPLI)
##

# Fonctions principales
def FPLI_initialisation(G, source):
    """ Fonction d'initialisation """
    INF = float("inf")
    liste_ouverte = FPLI()
    liste_fermee = []
    
    distances = {sommet: INF for sommet in G}
    parents = {sommet: sommet for sommet in G}
    chemin = []
    
    distances[source] = 0
    liste_ouverte.filer(source, distances)  ###
    return liste_ouverte, liste_fermee, distances, parents, chemin

def FPLI_selection_sommet_courant(liste_ouverte, distances):
    """ Fonction de sélection du sommet courant """
    return liste_ouverte.defiler()          ###

def FPLI_relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents):
    """ Procédure de relâchement du sommet """
    nouveau_cout = distances[sommet_courant] + s[1]
    if s[0] in liste_ouverte.file:
        if nouveau_cout < distances[s[0]]:
            distances[s[0]] = nouveau_cout
            parents[s[0]] = sommet_courant
    else:
        
        distances[s[0]] = nouveau_cout
        parents[s[0]] = sommet_courant
        liste_ouverte.filer(s[0], distances)        ###

        
# Fonction primaire (Algorithme de Dijkstra)
def dijkstra_FPLI(G, source, cible):
    """ Fonction implémentant l'algorithme de Dijkstra """
    assert source != cible
    
    # Initialisation
    liste_ouverte, liste_fermee, distances, parents, chemin = FPLI_initialisation(G, source)
    while not liste_ouverte.estVide():              ###
        # Sélection du sommet
        sommet_courant = FPLI_selection_sommet_courant(liste_ouverte, distances)
        if sommet_courant == cible:
            break
        # Transfert du sommet
                                    
        liste_fermee.append(sommet_courant)
        
        # Etape de relâchement de chaque successeur du sommet courant
        for s in successeurs_sommet_courant(G, sommet_courant):
            if s[0] in liste_fermee:
                continue # passer au suivant
                
            FPLI_relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents)
    # renvoyer le chemin trouvé
    return construction_chemin(source, cible, liste_ouverte, parents, chemin), distances[cible]

##

        # Dijkstra (FPLS)
## 

# Fonctions principales
def FPLS_initialisation(G, source):
    """ Fonction d'initialisation """
    INF = float("inf")
    liste_ouverte = FPLS()
    liste_fermee = []
    
    distances = {sommet: INF for sommet in G}
    parents = {sommet: sommet for sommet in G}
    chemin = []
    
    distances[source] = 0
    liste_ouverte.filer(source)  ###
    return liste_ouverte, liste_fermee, distances, parents, chemin

def FPLS_selection_sommet_courant(liste_ouverte, distances):
    """ Fonction de sélection du sommet courant """
    return liste_ouverte.defiler(distances)          ###

def FPLS_relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents):
    """ Procédure de relâchement du sommet """
    nouveau_cout = distances[sommet_courant] + s[1]
    if s[0] in liste_ouverte.file:
        if nouveau_cout < distances[s[0]]:
            distances[s[0]] = nouveau_cout
            parents[s[0]] = sommet_courant
    else:
        
        distances[s[0]] = nouveau_cout
        parents[s[0]] = sommet_courant
        liste_ouverte.filer(s[0])        ###

# Fonction primaire (Algorithme de Dijkstra)
def dijkstra_FPLS(G, source, cible):
    """ Fonction implémentant l'algorithme de Dijkstra """
    assert source != cible
    
    # Initialisation
    liste_ouverte, liste_fermee, distances, parents, chemin = FPLS_initialisation(G, source)
    while not liste_ouverte.estVide():              ###
        # Sélection du sommet
        sommet_courant = FPLS_selection_sommet_courant(liste_ouverte, distances)
        if sommet_courant == cible:
            break
        # Transfert du sommet
                                    
        liste_fermee.append(sommet_courant)
        
        # Etape de relâchement de chaque successeur du sommet courant
        for s in successeurs_sommet_courant(G, sommet_courant):
            if s[0] in liste_fermee:
                continue # passer au suivant
                
            FPLS_relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents)
    # renvoyer le chemin trouvé
    return construction_chemin(source, cible, liste_ouverte, parents, chemin), distances[cible]

##

        # Dijkstra (FPTR)
## 

# Fonctions principales
def FPTR_initialisation(G, source):
    """ Fonction d'initialisation """
    INF = float("inf")
    liste_ouverte = FPTR()
    liste_fermee = []
    
    distances = {sommet: INF for sommet in G}
    parents = {sommet: sommet for sommet in G}
    chemin = []
    
    distances[source] = 0
    liste_ouverte.filer(source, distances)  ###
    return liste_ouverte, liste_fermee, distances, parents, chemin

def FPTR_selection_sommet_courant(liste_ouverte):
    """ Fonction de sélection du sommet courant """
    return liste_ouverte.defiler()          ###

def FPTR_relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents):
    """ Procédure de relâchement du sommet """
    nouveau_cout = distances[sommet_courant] + s[1]
    b = False
    for i in range(liste_ouverte.taille()):
        if s[0] == liste_ouverte.file[i][1]:
            b = True
    if b:
        if nouveau_cout < distances[s[0]]:
            distances[s[0]] = nouveau_cout
            parents[s[0]] = sommet_courant
    else:
        
        distances[s[0]] = nouveau_cout
        parents[s[0]] = sommet_courant
        liste_ouverte.filer(s[0], distances)        ###

        
# Fonction primaire (Algorithme de Dijkstra)
def dijkstra_FPTR(G, source, cible):
    """ Fonction implémentant l'algorithme de Dijkstra """
    assert source != cible
    
    # Initialisation
    liste_ouverte, liste_fermee, distances, parents, chemin = FPTR_initialisation(G, source)
    while not liste_ouverte.estVide():              ###
        # Sélection du sommet
        sommet_courant = FPTR_selection_sommet_courant(liste_ouverte)
        if sommet_courant == cible:
            break
        # Transfert du sommet
                                    
        liste_fermee.append(sommet_courant)
        
        # Etape de relâchement de chaque successeur du sommet courant
        for s in successeurs_sommet_courant(G, sommet_courant):
            if s[0] in liste_fermee:
                continue # passer au suivant
                
            FPTR_relachement_sommet(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents)
    # renvoyer le chemin trouvé
    return construction_chemin(source, cible, liste_ouverte, parents, chemin), distances[cible]


##

        # Dijkstra TEST
## 


G = {
    "1": [("2", 7), ("3", 9), ("4", 14)],
    "2": [("3", 10),("4", 15)],
    "3": [("4", 11), ("5", 2)],
    "4": [("5", 6)],
    "5": [("3", 9)],
    "6": []
}

print(dijkstra_FPLI(G, "1", "6"))




##
def bernoulli(p):
    """ Loi de Bernoulli de param p """
    if random.random() < p:
        return 1
    else:
        return 0

def creation_graphe(n, p, dmax = 10, wmin = 0, wmax = 100):
    """
    n : nombre de sommets
    p : probabilité d'avoir un arc
    dmax : degré maximal des sommets
    wmin : poids minimal des flux
    wmax : poids maximal des flux
    """
    G = {}
    V = [k for k in range(n)]
    
    for k in range(n):
        k = str(k)
        G[k] = []
        for i in range(dmax):
            if bernoulli(p):
                s = random.randint(0, n-1)
                c = random.randint(wmin, wmax)
                G[k].append((str(s), c))    # (sommet, coût)
    return G, V
    
G, V = creation_graphe(5000, 0.8, dmax= 4)

##
def test_performances_dijkstra(Tn, p, dmax = 4, wmin = 0, wmax = 50):
    
    T_FPLI, T_FPLS, T_FPTR = [], [], []
    
    for n in Tn:
        print(n)
        G, V = creation_graphe(n, p, dmax, wmin, wmax)
        s, c = random.sample(range(1, n-1), 2)
        s, c = str(s), str(c)
        # FPLI
        debut = time.clock()
        FPLI = dijkstra_FPLI(G, s, c)
        T_FPLI.append(time.clock() - debut)
        
        # FPLS
        debut = time.clock()
        FPLS = dijkstra_FPLS(G, s, c)
        T_FPLS.append(time.clock() - debut)
        
        # FPTR
        debut = time.clock()
        FPTR = dijkstra_FPTR(G, s, c)
        T_FPTR.append(time.clock() - debut)
        
    plt.scatter(Tn, T_FPLI, label="FPLI", c="blue", s=10)
    plt.scatter(Tn, T_FPLS, label="FPLS", c="red", s=10)
    plt.scatter(Tn, T_FPTR, label="FPTR", c="green", s=10)
    plt.xlabel("Nombre de noeuds (n)")
    plt.ylabel("Temps (en sec)")
    plt.legend()
    plt.show()
    
A = [k for k in range(5, 50, 1)]

test_performances_dijkstra(A, 0.9)