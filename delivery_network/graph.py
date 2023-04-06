class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges=[]
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
    
#Fonction prenant en argument un trajet (src, dest) à effectuer et la puissance power d'un camion,
#renvoyant si le camion peut effectuer le trajet et, si c'est le cas, un chemin. 

    def get_path_with_power(self, src, dest, power):
        verif={node:False for node in self.nodes} #dictionnaire indiquant les noeuds visités ou non, 
        #afin d'éviter, par exemple de faire des aller-retours entre deux noeuds.
        verif[src]=True

        def path(node, chemin):
            if node==dest:  #condition d'arrêt: si l'on est arrivé à destination, on retourne le chemin
                return chemin
            list_nghbr=self.graph[node]
            for voisin in list_nghbr:   #on parcourt les voisins du noeud
                nghbr=voisin[0]
                if voisin[1]<=power and not verif[nghbr]: #si le camion a une puissance suffisante pour
                    #traverser l'arête et que le voisin n'a pas déjà été visité
                    verif[nghbr]=True
                    chemin.append(nghbr)    #on ajoute le voisin au chemin car il convient
                    return path(nghbr,chemin)   #on réapplique la fonction à ce nouveau noeud sur lequel
                #le camion se trouve
                if voisin==self.graph[node] and chemin[-1]!=src:    #condition si jamais le camion arrive
                    #dans un cul-de-sac
                    verif[nghbr]=True
                    chemin.pop()
                    return path(chemin[-1],chemin)
            return None
        
        return path(src,[src])
    
    '''
Complexité de l'algorithme: cf compte rendu.
    '''

    '''
Détermination des composantes connexes d'un graphe:
On écrit une fonction récursive permettant de déterminer la composante connexe dans laquelle se trouve 
un noeud: tant qu'un noeud a des voisins et que ces derniers n'ont pas été visités, on les ajoute à
la composante connexe et l'on réeffectue la fonction sur chacun d'eux. La fonction s'arrête lorsque
tous les noeuds ont été visités.
    ''' 
    def connected_components(self):
        connected_components=[]
        vnodes={node:False for node in self.nodes}  #marqueur pour savoir si un noeud a déjà été visité
        
        def component(node):
            C=[node]    #liste représentant une composante connexe
            for list_nghbr in self.graph[node]:
                nghbr=list_nghbr[0]
                if not vnodes[nghbr]:
                    vnodes[nghbr]=True
                    C+=component(nghbr)
            return C
        
        for node in self.nodes:
            if not vnodes[node]:
                connected_components.append(component(node))
        return connected_components

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
#Détermination de la puissance minimale nécessaire pour effectuer un trajet (src, dest) par dichotomie
#à l'aide de la fonction get_path_with_power.
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        g=0
        d=1
        eps=0.5

        def rechdicho(g,d): #fonction de recherhce dichotomique de la puissance
            if abs(g-d)<=eps:
                if d-int(d)<0.5:    #on conditionne pour renvoyer un entier et non un flottant
                    return self.get_path_with_power(src,dest,d),int(d)
                else:  
                    return self.get_path_with_power(src,dest,d),int(d)+1   
            while abs(g-d)>eps:
                m=(d+g)/2
                if self.get_path_with_power(src,dest,m)!=None:
                    d=m
                else:
                    g=m
                print(g,d)
        aretes=self.edges
        g=min([aretes[k][2] for k in range (len(aretes))])
        d=max([aretes[k][2] for k in range (len(aretes))])

        return rechdicho(g,d)
    
    '''
Complexité de l'algorithme:cf compte rendu.
'''


def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
                g.edges.append(edge)
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
                g.edges.append(edge)
            else:
                raise Exception("Format incorrect")
    return g
