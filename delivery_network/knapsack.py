from graph import Graph
from main import kruskal,new_get_power
import numpy as np
import random as rd 


B=25*(10**3)
# B=25*10**9

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
        L0=[int(L[k]) for k in range (len(L))]
    return L0

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
        #print(profit)
        src,dest=routes[k][0]
        power=puissances_min[k]
        p,c= False, max([camions[k][1] for k in range (len(camions))])
        for j in range (len(camions)):
            if camions[j][0]>=power and camions[j][1]<c:
                power=camions[j][0]
                p=camions[j][0]
                c=camions[j][1]
        if p!=False: #Si l'on a trouvé au moins un camion pouvant parcourir le trajet 
            #d[(src,dest)]=(p,c,profit)
            res=profit/c
            L.append([(src, dest),p,c,profit,res])
    return L

''' Implementation of the greedy algorithm'''

def knapsack (routes, camions, puissances_min):
    income=B
    Buy={camions[k][0]:[0] for k in range (len(camions))}
    profit=0
    L=best_camion(routes, camions, puissances_min)
    new_L=sorted(L, key=lambda x:x[4], reverse=True)
    print(new_L)
    stop=False
    k=1
    while stop!=True:
        src, dest=new_L[k][0]
        pow=new_L[k][1]
        cost=new_L[k][2]
        earn=new_L[k][3]
        if income-cost>=0 and earn-cost>0:
            Buy[pow].append((src, dest))
            Buy[pow][0]+=1
            profit+=(earn-cost)
            income-=cost
            k+=1
        if income-cost<0 or earn-cost<0:
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
truckname=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\trucks.2.in"
routename1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.1.in"
routename2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.1 (1).out"

#print(final_knapsack(truckname, routename1, routename2))
camions1=truck_from_file(truckname)
routename11=routes_from_file(routename1)
powers=power_path(routename2)              
#print(best_camion(routename11,camions1,powers))
#print(knapsack(routename11, camions1, powers))

''' Implementation of the dynamic algorithm'''

def dynamic_prog(routes, camions, powers):
    L=best_camion(routes, camions, powers)
    n=len(L)
    table=[[0 for i in range (B+1)] for j in range (n+1)]
    for i in range (n+1):
        for j in range (B+1):
            cost=L[i-1][2]
            earn=L[i-1][3]
            profit=earn-cost
            if i==0 or j==0:
                table[i][j]=0
            elif cost<=j:
                table[i][j]=max(profit+table[i-1][j-cost], table[i-1][j])
            else:
                table[i][j]=table[i-1][j]
            print(i,j)
    return table[n][B]

def knapsack2(fileroute,filetruck, filepowers):
    truck0=truck_from_file(filetruck)
    trucks=tri_camion(truck0)
    routes=routes_from_file(fileroute)
    powers=power_path(filepowers)
    return dynamic_prog(routes, trucks, powers)


#print(knapsack2(routename1,truckname,routename2))

''' Implementation of a solution inspired by the genetic algorithms'''

#Fonction générant un génome de taille length=len(best_camions(routes, camions, puissances)). Obtenir la
#valeur 1 (resp.0) au i-ème indice, signifie que l'on choisi l'association camion-trajet de best_camions[i]
#(resp. on ne la choisit pas).

def generate_genome(length):
    return rd.choices([0,1], k=length)

def generate_population(N, length):
    return [generate_genome(length) for k in range (N)]

#Fonction déterminant pour chaque génome le profit pouvant être réalisé et retournant par défaut 0 si
#l'achat des camions nécessaires dépasse le budget.
def fitness(L, genome, budget):
    cost=0
    profit=0
    for i, l in enumerate(L):
        if genome[i]==1:
            cost+=l[2]
            profit+=(l[3]-l[2])
            if cost>budget:
                return 0
    return profit

#Sélection d'une paire de génomes ayant presque sûrement les meilleurs profits parmi la population de départ.
#Cela équivaut à la sélection des meilleurs individus pour la reproduction.
def selection_pair(population, L, budget):
    return rd.choices(population, weights=[fitness(L,genome,budget) for genome in population], k=2)

#Croisement des individus sélectionnés pour obtenir un nouveau génome
def crossover(gen1,gen2):
    if len(gen1)<2:
        return gen1,gen2
    r=rd.randint(0,len(gen1)-1)
    return np.concatenate((gen1[:r],gen2[r:])), np.concatenate((gen1[r:],gen2[:r]))

def mutation(genome, proba, val):
    for k in range (val):
        i=rd.randint(0,len(genome)-1)
        if rd.random()<proba:
            genome[i]=abs(genome[i]-1)
    return genome

def evolution(L, N, budget):
    proba=0.5
    length=len(L)
    population=generate_population(N,length)
    for k in range (1000):
        population_sorted=sorted(population, key=lambda genome: fitness(L,genome,budget), reverse=True)
        selected=population_sorted[:2]
        ind_a,ind_b=crossover(selected[0], selected[1])
        ind_c, ind_d=mutation(ind_a,proba,1), mutation(ind_b,proba,1)
        selected+=[ind_a,ind_b,ind_c,ind_d]
        population=selected
    population=sorted(population,key=lambda genome:fitness(L,genome, budget), reverse=True)
    return population

def results(fileroute,filetrucks,filepowers,budget,N=10):
    routes=routes_from_file(fileroute)
    trucks=truck_from_file(filetrucks)
    powers=power_path(filepowers)
    L=best_camion(routes,trucks,powers)
    best_pop=evolution(L,N,budget)
    best_ind=best_pop[0]
    Buy={}
    for i,l in enumerate(L):
        if best_ind[i]==1:
            src,dest=l[0]
            if l[1] not in Buy.keys():
                Buy[l[1]]=[1,(src,dest)]
            else:
                Buy[l[1]][0]+=1
                Buy[l[1]].append((src,dest))
    profit=fitness(L,best_ind,budget)
    return Buy,profit 

print(results(routename1,truckname,routename2,B,N=10))

