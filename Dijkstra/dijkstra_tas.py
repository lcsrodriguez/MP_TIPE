import heapq


def initialisation_tas(G, source):
    """ Fonction d'initialisation """
    INF = float("inf")
    liste_ouverte = []
    liste_fermee = []
    
    distances = {sommet: INF for sommet in G}
    parents = {sommet: sommet for sommet in G}
    chemin = []
    distances[source] = 0
    
    heapq.heappush(liste_ouverte, (distances[source], source))
    
    return liste_ouverte, liste_fermee, distances, parents, chemin
    

def selection_sommet_courant_tas(liste_ouverte, distances):
    """ Fonction de sélection du sommet courant """
    return heapq.heappop(liste_ouverte)

def successeurs_sommet_courant_tas(G, sommet_courant):
    """ Fonction retournant les successeurs du sommet courant dans G """
    return G[sommet_courant]


def relachement_sommet_tas(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents):
    """ Procédure de relâchement du sommet """
    nouveau_cout = distances[sommet_courant] + s[1]
    if s[0] in liste_ouverte:
        if nouveau_cout < distances[s[0]]:
            distances[s[0]] = nouveau_cout
            parents[s[0]] = sommet_courant
    else:
        distances[s[0]] = nouveau_cout
        parents[s[0]] = sommet_courant
        heapq.heappush(liste_ouverte, (distances[s[0]], s[0]))

def construction_chemin_tas(source, cible, liste_ouverte, parents, chemin):
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

def dijkstra_tas(G, source, cible):
    """ Fonction implémentant l'algorithme de Dijkstra """
    assert source != cible
    
    # Initialisation
    liste_ouverte, liste_fermee, distances, parents, chemin = initialisation_tas(G, source)
    while len(liste_ouverte) > 0:
        # Sélection du sommet
        sommet_courant = selection_sommet_courant_tas(liste_ouverte, distances)[1]
        if sommet_courant == cible:
            break
        # Transfert du sommet
        liste_fermee.append(sommet_courant)
        
        # Etape de relâchement de chaque successeur du sommet courant
        for s in successeurs_sommet_courant_tas(G, sommet_courant):
            if s[0] in liste_fermee:
                continue # passer au suivant
                
            relachement_sommet_tas(sommet_courant, s, liste_ouverte, liste_fermee, distances, parents)
            
    # renvoyer le chemin trouvé
    return construction_chemin_tas(source, cible, liste_ouverte, parents, chemin), distances[cible]
