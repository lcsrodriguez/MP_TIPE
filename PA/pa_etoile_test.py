from pa_etoile import *
from tipe_fonctions_pa_etoile import *



"""
2 fonctions

- test_graphique()      : créé et enregistre une simulation aléaloire entière
- test_perf()           : créé et compare l'algo pour différentes tailles de grilles (évolution temporelle)
- test_etats_noeuds()   : créé et retourne le ratio de sommets explorés, non explorés et obstacles
- test_perf_fcts()      : évolution du temps en fonction de la taille et des fonctions (heuristiques et voisinages) utilisées


"""
def lancement_simulation(N, p = 0.8, wmin = 1, wmax = 100, f_v = 8, f_h = "m", alpha = 1):
    """
    Entrées:
        - N: largeur de la grille
        - p: probabilité d'avoir un obstacle
        - wmin: borne minimale des valuations
        - wmax: borne maximale des valuations
        - f_v: fonction de voisinage
        - f_h: fonction de valuation
        - alpha: coefficient d'influence des valuations sur la prise de décision
    
    """
    
    # Création de la grille
    G  = Grille(N, p, wmin, wmax)
    
    # Sélection de la source et de la cible
    G.selection_source_cible()
    source = G.s
    cible = G.c
    
    # Création du dossier
    dt = datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")
    
    DOSSIER = "simulations/sim" + dt +" N = "+str(N)+" p = "+str(p)+" wmin = "+str(wmin)+" wmax = "+str(wmax)+" f_v = "+str(f_v)+" f_h = "+str(f_h)+" alpha = "+str(alpha)
    
    try:
        os.mkdir(DOSSIER)
    except:
        os.mkdir(DOSSIER + "1")
    
    # Création et remplissage préliminaire de la grille pour l'affichage
    M = [[4.5 for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if G.grille[i][j].empruntable == 0:
                M[i][j] = float("nan")
    M[source[0]][source[1]] = 0.5
    M[cible[0]][cible[1]] = 1.5
    
    s = G.grille[source[0]][source[1]]
    c = G.grille[cible[0]][cible[1]]
    

    # Exécution de l'algorithme A* sur la grille
    debut = time.clock()
    a = algorithme_pa_etoile(G, s, c,
    successeurs_sommet_courant_8_directions, 
    heuristique_euclidienne, 
    alpha = 0.2)
    duree = time.clock() - debut
    
    # Formatage et création de l'image (plt)
    
    chemin = [(n.x,n.y) for n in a]
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    cmap = mpl.colors.ListedColormap(['#1bc700', 'red', 'blue', 'yellow', 'white', 'magenta', 'black'])
    cmap.set_bad(color='black')
    boundaries = [0, 1, 2, 3, 4, 5, 6, 7]
    norm = mpl.colors.BoundaryNorm(boundaries, cmap.N, clip=True)

    
    # on dessine la grille
    
    for x in range(0, N + 1):
        ax.axhline(x, lw=2, color='gray', zorder=5)
        ax.axvline(x, lw=2, color='gray', zorder=5)
    
    for k in range(0, len(chemin)-1):
        if (chemin[k][0],chemin[k][1]) != source and (chemin[k][0],chemin[k][1]) != cible:
            M[chemin[k][0]][chemin[k][1]] = 2.5
        voisins_k = [(n.x, n.y) for n in G.voisinage_8directions(G.grille[chemin[k][0]][chemin[k][1]]) if n.empruntable == 1]
        for v in voisins_k:
            if v != chemin[k-1] and v != source and v != cible:
                M[v[0]][v[1]] = 3.5
        
        im = plt.imshow(M, interpolation='none', cmap=cmap, extent=[0, N, 0, N], zorder=2, norm=norm)
        

        # Titre (en haut de la figure)
        plt.title("$N$ = "+str(N)+" - $d$ = "+ str(round(duree, 5)) + " - (ALL DIR. - Euclidienne)")
        
        """
        xlab = "N : "+ str(N) + "\t p : " + str(p) + "\t" + "$f_v$ : " + str(f_v) + "\t$f_h$ : "+str(f_h) + "\talpha : " + str(alpha) + "\n s : "+ dt + "\n d : " + str(duree)
        
        plt.xlabel(xlab)"""
        FICHIER = DOSSIER + "/" + "grille_"+str(k)
        ax.axis("off")
        """
        plt.text(N/2, -N/6, str(duree), color="g", 
        horizontalalignment = 'center', 
        verticalalignment = 'center')
        """
        """
        plt.text(N/2, (-3*N)/7, "NON DEFINITIF - NON EXPLOITABLE\nNE PAS DIFFUSER", 
        color="r", 
        horizontalalignment = 'center', 
        verticalalignment = 'center',
        bbox=dict(boxstyle="square",
                    ec=(1., 0, 0),
                    fc=(1., 1.0, 1.0),))
        """
        plt.savefig(FICHIER) #, quality=80) #;, pad_inches=5)
    
    plt.show()
    
   
lancement_simulation(30)


##

def test_perf(T, p):
    n = len(T)
    Yt, Yc = [], []
    for N in T:
        G = Grille(N, p)
        print(N)
        # Sélection de la source et de la cible
        source, cible = (0, 0), (0, 0)
        while source == cible or (G.grille[source[0]][source[1]].empruntable == 0 or G.grille[cible[0]][cible[1]].empruntable == 0):
            source = tuple(random.sample(range(0, N), 2))
            cible = tuple(random.sample(range(0, N), 2))
        
        s = G.grille[source[0]][source[1]]
        c = G.grille[cible[0]][cible[1]]
        
        # Exécution de l'algorithme A* sur la grille
        debut_t = time.time()
        debut_c = time.clock()
        a = algorithme_pa_etoile(G, s, c, successeurs_sommet_courant_8_directions, heuristique_manhattan)
        duree_c = time.clock() - debut_c
        duree_t = time.time() - debut_t
        
        Yc.append(duree_c)
        Yt.append(duree_t)
    

    plt.scatter(T, Yc, color='red',s=7, marker="o")
    plt.xlabel("Largeur d'une '")
    plt.show()
    
    
A = [k for k in range(5, 100, 20)]

test_perf(A, 0.9)

##

def test_etats_noeuds(N, p):
    G = Grille(N, p)
    
    Y = []
    
    nbre_obstacles = 0
    for i in G.grille:
        for j in i:
            if j.empruntable == 0:
                nbre_obstacles += 1
    
    
    # Sélection de la source et de la cible
    source, cible = (0, 0), (0, 0)
    while source == cible or (G.grille[source[0]][source[1]].empruntable == 0 or G.grille[cible[0]][cible[1]].empruntable == 0):
        source = tuple(random.sample(range(0, N), 2))
        cible = tuple(random.sample(range(0, N), 2))
    
    s = G.grille[source[0]][source[1]]
    c = G.grille[cible[0]][cible[1]]
    
    # Exécution de l'algorithme A* sur la grille
    chemin = algorithme_a_etoile(G, s, c, successeurs_sommet_courant_8_directions, heuristique_manhattan)
    chemin = [(n.x,n.y) for n in chemin]
    l = len(chemin) - 2
    
    nbre_explores = l
    for k in range(0, len(chemin)-1):
        voisins_k = [(n.x, n.y) for n in G.voisinage_8directions(G.grille[chemin[k][0]][chemin[k][1]]) if n.empruntable == 1]
        for v in voisins_k:
            if v != chemin[k-1] and v != source and v != cible:
                nbre_explores += 1
                
    X = [k for k in range(l)]
    return N**2, nbre_obstacles, nbre_explores

##

def test_perf_fcts(Tn, p):
    n = len(Tn)

    YM4, YM8, YE4, YE8, Ym = [], [], [], [], []
    
    for N in Tn:
        # Création de la grille
        print(N)
        G = Grille(N, p)
        
        source, cible = (0, 0), (0, 0)
        while source == cible or (G.grille[source[0]][source[1]].empruntable == 0 or G.grille[cible[0]][cible[1]].empruntable == 0):
            source = tuple(random.sample(range(0, N), 2))
            cible = tuple(random.sample(range(0, N), 2))
        
        s = G.grille[source[0]][source[1]]
        c = G.grille[cible[0]][cible[1]]
        
        # Manhattan - 4
        debut = time.clock()
        a = algorithme_a_etoile(G, s, c, successeurs_sommet_courant_4_directions, heuristique_manhattan)
        duree = time.clock() - debut
        m = duree
        YM4.append(duree)
        
        # Manhattan - 8
        debut = time.clock()
        a = algorithme_a_etoile(G, s, c, successeurs_sommet_courant_8_directions, heuristique_manhattan)
        duree = time.clock() - debut
        m += duree
        YM8.append(duree)
    
        # Euclidienne - 4
        debut = time.clock()
        a = algorithme_a_etoile(G, s, c, successeurs_sommet_courant_4_directions, heuristique_euclidienne)
        duree = time.clock() - debut
        m += duree
        YE4.append(duree)
        
        # Euclidienne - 8
        debut = time.clock()
        a = algorithme_a_etoile(G, s, c, successeurs_sommet_courant_8_directions, heuristique_euclidienne)
        duree = time.clock() - debut
        m += duree
        Ym.append(m/4)
        YE8.append(duree)
    plt.clf()
    plt.plot(Tn, YM4, "ro-", label="Manhattan (4 dir.)", linestyle='dashed', linewidth=1, markersize=3)
    plt.plot(Tn, YM8, "go-", label="Manhattan (8 dir.)", linestyle='dashed', linewidth=1, markersize=3)
    plt.plot(Tn, YE4, "bo-", label="Euclidienne (4 dir.)", linestyle='dashed', linewidth=1, markersize=3)
    plt.plot(Tn, YE8, "co-", label="Euclidienne (8 dir.)", linestyle='dashed', linewidth=1, markersize=3)
    plt.plot(Tn, Ym, "mo-", label="Moyenne", markersize=3)
    plt.legend()
    plt.xlabel("$N$ (largeur de la grille)")
    plt.ylabel("Temps (en sec)")
    plt.title("Etude comparative des différentes méthodes de l'algorithme A*")
    plt.show()
    
    return YM4, YM8, YE4, YE8

A = [k for k in range(5, 500, 10)]

resultats = test_perf_fcts(A, 0.9)