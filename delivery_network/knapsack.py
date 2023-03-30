from graph import Graph
from main import kruskal,new_get_power


B=25*10**9

def truck_from_file(filename): # Fonction permettant d'ouvrir les fichiers trucks
    L=[]
    with open(filename, "r") as file:
        nb_truck=map(int, file.readline().split())
        nb_truck0=list(nb_truck)[0]
        for _ in range (nb_truck0):
            power,cost=map(int, file.readline().split())
            L.append((power,cost))
    return L

def routes_from_file(filename): # Fonction permettant d'ouvrir les fichiers routes.in  
    L=[]
    with open(filename, "r") as file:
        nb_trajet=map(int, file.readline().split())
        for _ in range (list(nb_trajet)[0]):
            src,dest,profit=map(int, file.readline().split())
            L.append([(src,dest),profit])
    return L

def power_path(filename): # Fonction permettant d'ouvrir les fichiers routes.out
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
            new_list.insert(0,(power,cost))
        c=cost
        p=power
    return new_list

'''
On définit une fonction qui renvoie pour un fichier "routes" le dictionnaire qui associe aux trajets
effectuables par au moins l'un des camion, la puissance, le cout et l'utilité du camion qui maximise 
cette dernière. Elle prend en argument la liste des camions, la liste des trajets et la liste des 
puissances minimales nécessaires pour effectuer ces trajets. 
'''

def best_camion(routes,camions,puissances_min):
    #d={}
    L=[]
    for k in range (len(routes)):
        profit=routes[k][1]
        src,dest=routes[k][0]
        power=puissances_min[k]
        p,c= False, max([camions[k][1] for k in range (len(camions))])
        for j in range (len(camions)):
            print(type(camions[j][0]))
            print(type(power))
            if camions[j][0]>=power and camions[j][1]<c:
                p=camions[j][0]
                c=camions[j][1]
        if p!=False: #Si l'on a trouvé au moins un camion pouvant parcourir le trajet 
            #d[(src,dest)]=(p,c,profit)
            res=profit/c
            L.append([(src, dest),p,c,profit,res])
    return L

def knapsack (routes, camions, puissances_min):
    income=B
    Buy={camions[k][0]:[0] for k in range (len(camions))}
    profit=0
    L=best_camion(routes, camions, puissances_min)
    new_L=sorted(L, key=lambda x:x[4], reverse=True)
    stop=False
    k=0
    while stop!=True:
        src, dest=new_L[k][0]
        pow=new_L[k][1]
        cost=new_L[k][2]
        earn=new_L[k][3]
        if income-cost>=0:
            Buy[pow].append((src, dest))
            Buy[pow][0]+=1
            profit+=earn-cost
            income-=cost
            k+=1
        if income-cost<0:
            k+=1
        if k==len(new_L):
            stop=True
    return Buy, profit

def final_knapsack(truckname,routename1,routename2):
    camions1=truck_from_file(truckname)
    routes=routes_from_file(routename1)
    powers=power_path(routename2)
    camions2=tri_camion(camions1)
    buy, profit=knapsack(routes, camions2, powers)
    return buy, profit 

'''Tests de l'algorithme naïf'''
truckname=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\trucks.0.in"
routename1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.2.in"
routename2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.2.out"

print(final_knapsack(truckname, routename1, routename2))
            
                









