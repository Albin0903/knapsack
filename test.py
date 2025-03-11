import random
import math

# on peut implémenter la solution linéaire si on a du temps 

def lire_fichier(fichier):
    with open(fichier, 'r') as f:
        liste_items = []
        data = False
        max_capacity = None
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith('MAX_CAPACITY:'):
                max_capacity = int(ligne.split()[1])
            elif ligne.startswith('DATA [id profit weight]:'):
                data = True
                continue
            if data and ligne:
                liste_items.append([int(x) for x in ligne.split()])
    return max_capacity, liste_items

def calculer_poids_total(liste_items, solution):
    return sum(liste_items[i][2] for i in range(len(liste_items)) if solution[i] == 1)

def calculer_profit_total(liste_items, solution): # fonction à minimiser 
    return (-sum(liste_items[i][1] for i in range(len(liste_items)) if solution[i] == 1))

def verifier_solution(liste_items, solution, max_capacity): # contrainte à respecter
    return calculer_poids_total(liste_items, solution) <= max_capacity

def generer_solution_aleatoire(liste_items):
    return [random.randint(0, 1) for _ in range(len(liste_items))]

def generer_solution_ratio(liste_items):
    solution = [0] * len(liste_items)
    for i in range(3):
        solution[i] = 1
    return solution

def generer_voisin(solution): # voisinage de la solution -> changer un bit de la solution
    index = random.randint(0, len(solution) - 1)
    solution[index] = 1 if solution[index] == 0 else 0
    return solution

def accepter_solution_moins_bonne(delta, temperature):
    proba = math.exp(-delta / temperature)
    return random.random() < proba

def sort_items(liste_items):
    return sorted(liste_items, key=lambda x: x[1] / x[2], reverse=True)

def recuit_simule(liste_items, max_capacity, max_iter, temperature_initiale, alpha):
    solution = [0] * len(liste_items)
    meilleur_solution = solution[:]
    for i in range(max_iter):
        temperature = temperature_initiale / (1 + alpha * i)
        voisin = generer_voisin(solution[:])
        if not verifier_solution(liste_items, voisin, max_capacity):
            continue
        delta = calculer_profit_total(liste_items, voisin) - calculer_profit_total(liste_items, solution)
        # print("Delta:", delta)
        if delta < 0 or accepter_solution_moins_bonne(delta, temperature):
            solution = voisin
            # print("Solution:", solution)
            # print("Poids total:", calculer_poids_total(liste_items, solution))
            # print("Profit total:", (-calculer_profit_total(liste_items, solution)))
            # print("Temperature:", temperature)
            # print()
            if calculer_profit_total(liste_items, solution) < calculer_profit_total(liste_items, meilleur_solution):
                meilleur_solution = solution[:]
    return meilleur_solution

def main():
    max_capacity, liste_items = lire_fichier('pi-12-100-1000-001.kna') # fichier à lire
    # pi-12-100-1000-001.kna
    # pi-12-1000-1000-001.kna
    # pi-12-10000-1000-001.kna
    # pi-13-100-1000-001.kna
    # pi-13-1000-1000-001.kna
    # pi-13-10000-1000-001.kna
    # pi-15-100-1000-001.kna
    # pi-15-1000-1000-001.kna
    # pi-15-10000-1000-001.kna
    print("MAX_CAPACITY:", max_capacity)
    # print("Liste des items (id, profit, weight):")
    liste_items = sort_items(liste_items) # trier les items par rapport à leur ratio profit/poids
    # for item in liste_items:
    #     print(item)
    # print()
    solution = recuit_simule(liste_items, max_capacity, 10000, 10000, 0.01)
    print("\nSolution finale:", solution)
    print("Poids total:", calculer_poids_total(liste_items, solution))
    print("Profit total:", (-calculer_profit_total(liste_items, solution)))
    # afficher les id des items sélectionnés
    print("Items sélectionnés:", [liste_items[i][0] for i in range(len(liste_items)) if solution[i] == 1])

if __name__ == '__main__':
    main()
