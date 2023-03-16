from graph import Graph
from main import kruskal,new_get_power


def truck_from_file(filename):
    L=[]
    with open(filename, "r") as file:
        nb_truck=map(int, file.readline().split())
        for _ in range (nb_truck):
            power,cost=map(int, file.readline().split())
            L.append((power,cost))
    return L

def routes_from_file(filename):
    L=[]
    with open(filename, "r") as file:
        nb_trajet=map(int, file.readline().split())
        for _ in range (nb_trajet):
            src,dest,profit=map(int, file.readline().split())
            L.append([(src,dest),profit])
    return L

def power_path(filename):
    with open(filename, "r") as file:
        L=file.read().splitlines()
    return L

'''
On créé une fonction qui créé une liste de camions mise à jour, ne contenant pas les camions "inutiles".
On peut considérer un camion comme inutile lorsqu'il a une puissance inférieure ou égale à la puissance 
d'un camion existant mais un coût supérieur à ce même camion.
'''
def tri_camion(camions):
    c=camions[-1][1]
    p=camions[-1][0]
    new_list=[(p,c)]
    for power, cost in reversed(camions):
        if power<=p and cost<c:
            new_list.insert((power,cost))
        c=cost
        p=power
    return new_list


def best_camion(routes,camions,puissances_min):
    d={}
    for k in range (len(routes)):
        profit=routes[k][1]
        src,dest=routes[k][0]
        power=puissances_min[k]
        p,c= False, max([camions[k][1] for k in range (len(camions))])
        for k in range len(camions):
            if camions[k][0]>=power and camions[0][1]<c:
                p=camion[k][0]
                c=camions[0][1]
        if p!=False:
            utility=profit-c
            d[(src,dest)]=(p,c,utility)
    return d

            
                









