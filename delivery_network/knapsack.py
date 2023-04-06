from graph import Graph
from main import kruskal,new_get_power
import numpy as np
import random as rd 

'''Budget'''

B=25*(10**9)

''' Fonctions permettant d'ouvrir les fichiers dont nous aurons besoin'''

# Fonction permettant d'ouvrir les fichiers trucks
def truck_from_file(filename): 
    L=[]
    with open(filename, "r") as file:
        nb_truck=map(int, file.readline().split())
        nb_truck0=list(nb_truck)[0]
        for _ in range (nb_truck0):
            power,cost=map(int, file.readline().split())
            L.append((power,cost))
    return L

# Fonction permettant d'ouvrir les fichiers routes.in 
def routes_from_file(filename):  
    L=[]
    with open(filename, "r") as file:
        nb_trajet=map(int, file.readline().split())
        for _ in range (list(nb_trajet)[0]):
            src,dest,profit=map(int, file.readline().split())
            L.append([(src,dest),profit])
    return L

# Fonction permettant d'ouvrir les fichiers routes.out
def power_path(filename): 
    with open(filename, "r") as file:
        L=file.read().splitlines()
        L0=[int(L[k]) for k in range (len(L))]
    return L0

''' Fichiers routes.in et .out et camions'''

truckfile0=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\trucks.0.in"
truckfile1=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\trucks.1.in"
truckfile2=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\trucks.2.in"

routename1in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.1.in"
routename1out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.1 (1).out"

routename2in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.2.in"
routename2out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.2.out"

routename3in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.3.in"
routename3out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.3.out"

routename4in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.4.in"
routename4out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.4.out"

routename5in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.5.in"
routename5out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.5.out"

routename6in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.6.in"
routename6out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.6.out"

routename7in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.7.in"
routename7out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.7.out"

routename8in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.8.in"
routename8out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.8.out"

routename9in=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.9.in"
routename9out=r"C:\Users\auran\OneDrive\Documents\ensae\1A\Projet de programmation\ensae-prog23v2\input\routes.9.out"

''' Résolution du problème'''

#Fonction créant une liste de camions de laquelle ont été retirés les camions inutiles.

def tri_camion(camions):
    c=camions[-1][1]
    p=camions[-1][0]
    new_list=[(p,c)]
    for power, cost in reversed(camions): #les camions dans les fichiers sont classés par ordre de puissance croissant
        if power<=p and cost<c: # on garde le camion tant que pour une puissance inférieure ou égale, son coût est strictement inférieur
            new_list.insert(0,(power,cost))
        c=cost
        p=power
    return new_list

#Fonction renvoyant une liste des couples trajet-camion optimaux lorsqu'au moins un camion peut effectuer
#le trajet.

def best_camion(routes,camions,puissances_min):
    '''
    Prend en argument: liste des routes, camions et puissances minimales
    Renvoie: liste des couples trajet-camion optimaux
    '''
    L=[]
    for k in range (len(routes)):
        profit=routes[k][1]
        src,dest=routes[k][0]
        power=puissances_min[k]
        p,c= False, max([camions[k][1] for k in range (len(camions))])
        for j in range (len(camions)):
            if camions[j][0]>=power and camions[j][1]<c:
                power=camions[j][0]
                p=camions[j][0]
                c=camions[j][1]
        if p!=False: #Si l'on a trouvé au moins un camion pouvant parcourir le trajet 
            res=profit/c
            L.append([(src, dest),p,c,profit,res])
    return L


''' Implémentation de l'algorithme glouton'''

def knapsack (routes, camions, puissances_min):
    income=B
    Buy={camions[k][0]:[0] for k in range (len(camions))} # Dictionnaire qui a chaque camion associe la quantité à acheter et les trajets à effectuer
    profit=0
    L=best_camion(routes, camions, puissances_min)
    new_L=sorted(L, key=lambda x:x[4], reverse=True)
    #new_L=sorted(L, key=lambda x:x[3], reverse=True)
    stop=False # Variable indiquant quand on dépasse le budget
    k=1
    while stop!=True:
        src, dest=new_L[k][0]
        pow=new_L[k][1]
        cost=new_L[k][2]
        earn=new_L[k][3]
        if income-cost>=0:
            Buy[pow].append((src, dest))
            Buy[pow][0]+=1
            #profit+=(earn-cost)
            profit+=earn
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
#print(final_knapsack(truckfile2, routename8in, routename8out))
#print(final_knapsack(truckfile1, routename4in, routename4out))
#print(final_knapsack(truckfile0, routename4in, routename4out))
#print(final_knapsack(truckfile2, routename9in, routename9out))
#print(final_knapsack(truckfile0, routename2in, routename2out))
#print(final_knapsack(truckfile0, routename1in, routename1out))
#print(final_knapsack(truckfile1, routename9in, routename9out))

''' Implémentation de la méthode de programmation dynamique'''

def dynamic_prog(routes, camions, powers):
    L=best_camion(routes, camions, powers)
    n=len(L)
    table=[[0 for i in range (B+1)] for j in range (n+1)]
    for i in range (n+1):
        for j in range (B+1):
            cost=L[i-1][2]
            earn=L[i-1][3]
            profit=earn
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


''' Implémentation d'une solution inspirée par les algorithmes génétiques'''

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
    stop=False
    k=0
    while stop!=True:
        if genome[k]==1:
            c=cost+L[k][2]
            if c<=budget:
                cost=c
                profit+=L[k][3]
        k+=1
        if k==len(L):
            stop=True
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

#Fonction de mutation d'un génome
def mutation(genome, proba, val):
    for k in range (val):
        i=rd.randint(0,len(genome)-1)
        if rd.random()<proba:
            genome[i]=abs(genome[i]-1)
    return genome

#Fonction résumant les étapes de la sélection naturelle
def evolution(L, N, budget):
    proba=0.5
    length=len(L)
    population=generate_population(N,length) #création d'une population
    while np.max([fitness(L,genome,budget) for genome in population])==0:
        population=generate_population(N,length)
        print('encore')
    for k in range (1000):
        population_sorted=sorted(population, key=lambda genome: fitness(L,genome,budget), reverse=True)
        selected=population_sorted[:2] #sélection des deux meilleurs individus
        ind_a,ind_b=crossover(selected[0], selected[1]) #croisement
        ind_c, ind_d=mutation(ind_a,proba,1), mutation(ind_b,proba,1) #mutation 
        selected+=[ind_a,ind_b,ind_c,ind_d]
        population=selected
        print(k)
    population=sorted(population,key=lambda genome:fitness(L,genome, budget), reverse=True)
    return population

def results(fileroute,filetrucks,filepowers,budget,N=10):
    routes=routes_from_file(fileroute)
    trucks=truck_from_file(filetrucks)
    powers=power_path(filepowers)
    L=best_camion(routes,trucks,powers)
    print(len(L))
    best_pop=evolution(L,N,budget)
    best_ind=best_pop[0]
    Buy={}
    profit=fitness(L,best_ind,budget)
    if profit!=0:
        for i,l in enumerate(L):
            if best_ind[i]==1:
                src,dest=l[0]
                if l[1] not in Buy.keys():
                    Buy[l[1]]=[1,(src,dest)]
                else:
                    Buy[l[1]][0]+=1
                    Buy[l[1]].append((src,dest))
    return Buy,profit 

#print(results(routename1in,truckfile1,routename1out,B,N=10))
#print(results(routename9in, truckfile1, routename9out,B,N=10))
#print(results(routename4in,truckfile0, routename4out,B,N=10))
#print(results(routename2in,truckfile1,routename2out,B,N=10))
#print(results(routename8in,truckfile2,routename8out,B,N=10))
print(results(routename3in,truckfile2,routename3out,B,N=10))