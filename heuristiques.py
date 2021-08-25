

# distance de Manhattan

def manhattan(noeudA, noeudB, D = 1):
    dx = abs(noeudA.x - noeudB.x)
    dy = abs(noeudA.y - noeudB.y)
    
    d = D * (dx + dy)
    return d


# distance diagonal (tchebychev)

def diagonal(noeudA, noeudB, D, D1):
    dx = abs(noeudA.x - noeudB.x)
    dy = abs(noeudA.y - noeudB.y)
    
    


# distance euclidienne



def euclidienne(noeudA, noeudB, D):
    dx = abs(noeudA.x - noeudB.x)
    dy = abs(noeudA.y - noeudB.y)
    
    d = D * math.sqrt(dx**2 + dy**2)
    return d