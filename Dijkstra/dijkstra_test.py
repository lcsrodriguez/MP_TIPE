from dijkstra import *
from dijkstra_tas import *
## Fonctions génératrices de graphes

def bernoulli(p):
    """ Loi de Bernoulli de param p """
    if rd.random() < p:
        return 1
    else:
        return 0

def creation_graphe(n, p, dmax = 10, wmin = 0, wmax = 100):
    G = {}
    V = []
    
    H = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            V.append((i,j))
            H.add_node((i,j), pos=(i,j), label=str(i)+str(j))
    
    for k in V:
        G[k] = []
        for i in range(dmax):
            if bernoulli(p):
                s = rd.choice(V)
                c = rd.randint(wmin, wmax)
                G[k].append((s, c))    # (sommet, coût)
                H.add_edge(k, s, weight = c)
    
    return G, H, V

def affichage_graphe_console(G):
    for s in G:
        print(s, ":", G[s]) 
    



def affichage_graphe(H, source, cible):
    pos = nx.get_node_attributes(H, 'pos')
    labels = nx.get_node_attributes(H, 'label')
    weights = nx.get_edge_attributes(H, 'weight')
    
    # Détermination des chemins
    debut = time.clock()
    chemin = dijkstra(G, source, cible)[0]
    duree = time.clock() - debut
    
    print(chemin)
    
    chemin.remove(source)
    chemin.remove(cible)
    chemin_arcs = list(zip(chemin, chemin[1:]))
    # Couleurs des arcs
    couleurs_arcs = ['magenta' if arc in chemin_arcs else 'black' for arc in H.edges()]
    
    # Couleurs des noeuds
    couleurs_noeuds = []
    for n in H.nodes():
        if n in chemin:
            couleurs_noeuds.append("magenta")
        elif n == source:
            couleurs_noeuds.append("limegreen")
        elif n == cible:
            couleurs_noeuds.append("red")
        else:
            couleurs_noeuds.append("lightskyblue")
    
    
    # Afficher les noeuds
    nodes = nx.draw_networkx_nodes(H, pos, with_labels=False, node_color=couleurs_noeuds, node_size =400)
    nodes.set_edgecolor('k')
    
    # Afficher les arcs
    nx.draw_networkx_edges(H, pos, arrowsize=12, edge_color=couleurs_arcs)
    
    # Afficher les étiquettes des arcs
    #x.draw_networkx_edge_labels(G, pos, edge_labels= arcs_poids)

    # Afficher les étiquettes des sommets
    nx.draw_networkx_labels(H,pos,labels,font_size=8, font_color="w", font_weight='normal')
    
    plt.axis("off")
    """
    plt.title("Algorithme de Dijkstra\n $n$ = "+str(int(math.sqrt(len(H.nodes)))))
    plt.title("RODRIGUEZ\nMP (TIPE)", loc="left")
    #plt.title("$d$ ="+str(duree), loc="right")
    
    plt.text(int(math.sqrt(len(H.nodes)))/2 - 1/2, -1.5, "NON DEFINITIF - NON EXPLOITABLE\nNE PAS DIFFUSER", 
    color="r", 
    horizontalalignment = 'center', 
    verticalalignment = 'center',
    bbox=dict(boxstyle="square",
                   ec=(1., 0, 0),
                   fc=(1., 1.0, 1.0),))
    """
    FICHIER = "simulations/sim" + datetime.datetime.now().strftime("%d-%m-%y %H-%M")+".png"
    
    plt.savefig(FICHIER, dpi=1000)
    plt.show()
    
## 

            # TEST #
## 

N = 20      # N^2 = nbre de sommets
p = 0.2     # probabilité d'avoir un arc entre 2 sommets


dmax = 10   # degré maximal de chaque noeud
wmin = 0    # valeur minimale de valuation
wmax = 100  # valeur maximale de valuation

# Création du graphe
G, H, V = creation_graphe(N, p, dmax, wmin, wmax)

# Détermination aléatoire de la source et de la cible
source, cible = (0, 0), (0, 0)
while source == cible:
    source = rd.choice(V)
    cible = rd.choice(V)

# Affichage de la source
print(source, cible)

# Affichage du 

affichage_graphe(H, source, cible)





## Test des performances






n = 10**4
ns = [k for k in range(10, n, 10)]


T_liste = []
T_tas = []

for k in ns:
    N = 20      # N^2 = nbre de sommets
    p = 0.3     # probabilité d'avoir un arc entre 2 sommets
    dmax = 10   # degré maximal de chaque noeud
    wmin = 0    # valeur minimale de valuation
    wmax = 100  # valeur maximale de valuation
    
    # Création du graphe
    G, H, V = creation_graphe(N, p, dmax, wmin, wmax)
    print(k)
    
    source, cible = (0, 0), (0, 0)
    while source == cible:
        source = rd.choice(V)
        cible = rd.choice(V)
    
    
    debut_liste = time.clock()
    chemin = dijkstra(G, source, cible)[0]
    duree_liste = time.clock() - debut_liste
    T_liste.append(duree_liste)
    
    debut_tas = time.clock()
    chemin = dijkstra_tas(G, source, cible)[0]
    duree_tas = time.clock() - debut_tas
    T_tas.append(duree_tas)
    
    ##

plt.scatter(ns, T_liste, s=20, facecolors='none', edgecolors='b', label="solution avec liste")
plt.scatter(ns, T_tas, s=20, facecolors='none', edgecolors='r', label="solution avec tas")

T_lim = [0.02 for k in ns]
plt.plot(ns, T_lim, 'g-', lw=1)

plt.title("Etude comparative de la solution")
plt.xlabel("Nombre de sommets : $n$")
plt.ylim(0, 0.5*max(max(T_liste, T_tas)))
plt.ylabel("Temps d'exécution (en sec)")
plt.legend(loc="upper right")
plt.show()


