import random

def lire_fichier(fichier):
    with open(fichier, 'r') as f:
        liste_items = []
        data_section = False
        max_capacity = None
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith('MAX_CAPACITY:'):
                max_capacity = int(ligne.split()[1])
            elif ligne.startswith('DATA [id profit weight]:'):
                data_section = True
            elif data_section and ligne:
                parts = ligne.split()
                if len(parts) == 3:
                    idx = int(parts[0])
                    profit = int(parts[1])
                    weight = int(parts[2])
                    liste_items.append((idx, profit, weight))
    return max_capacity, liste_items

def generer_solution_aleatoire(n):
    """Génère aléatoirement un vecteur binaire de taille n."""
    return [random.randint(0, 1) for _ in range(n)]

def calculer_poids_total(liste_items, solution):
    """Calcule la somme des poids des items sélectionnés."""
    return sum(liste_items[i][2] for i in range(len(solution)) if solution[i] == 1)

def calculer_profit_total(liste_items, solution):
    """Calcule le profit total des items sélectionnés."""
    return sum(liste_items[i][1] for i in range(len(solution)) if solution[i] == 1)

def fitness(liste_items, solution, max_capacity):
    """
    Renvoie la fitness d'une solution.
    - Si la capacité est dépassée, on applique une pénalité.
    - Sinon, c'est simplement le profit total.
    """
    poids = calculer_poids_total(liste_items, solution)
    profit = calculer_profit_total(liste_items, solution)
    if poids > max_capacity:
        # Pénalité : on soustrait une partie du dépassement au profit
        return profit - 10_000 * (poids - max_capacity)
    else:
        return profit

def selection_tournoi(population, fitnesses, k=2):
    """
    Sélection par tournoi :
    - On choisit aléatoirement k individus, on prend le meilleur en termes de fitness.
    - On renvoie l'indice du vainqueur.
    """
    participants = random.sample(range(len(population)), k)
    best_idx = participants[0]
    best_fit = fitnesses[best_idx]
    for idx in participants[1:]:
        if fitnesses[idx] > best_fit:
            best_idx = idx
            best_fit = fitnesses[idx]
    return best_idx

def crossover_1point(parent1, parent2):
    """
    Croisement 1-point : on coupe les gènes en un point choisi aléatoirement
    et on échange les segments.
    """
    n = len(parent1)
    point = random.randint(1, n-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutation_flip(child, prob_mut=0.01):
    """
    Mutation : on parcourt chaque bit,
    et on le flip avec une probabilité prob_mut.
    """
    for i in range(len(child)):
        if random.random() < prob_mut:
            child[i] = 1 - child[i]
    return child

def algogen_knapsack(liste_items, max_capacity,
                     pop_size=50,
                     max_gen=100,
                     pcross=0.8,
                     pmut=0.01,
                     tournament_k=2):
    """
    Algorithme génétique classique pour le Knapsack 0-1.
    :param liste_items: liste de (id, profit, weight)
    :param max_capacity: capacité max du sac
    :param pop_size: taille de la population
    :param max_gen: nombre de générations
    :param pcross: probabilité de crossover
    :param pmut: probabilité de mutation (flip)
    :param tournament_k: taille du tournoi pour la sélection
    :return: (best_solution, best_fitness)
    """

    n = len(liste_items)

    # --- 1) Initialisation de la population ---
    population = [generer_solution_aleatoire(n) for _ in range(pop_size)]
    
    # Calcul des fitness initiaux
    fitnesses = [fitness(liste_items, sol, max_capacity) for sol in population]

    best_global_sol = None
    best_global_fit = float('-inf')

    # Mise à jour du meilleur global initial
    for i, fit in enumerate(fitnesses):
        if fit > best_global_fit:
            best_global_fit = fit
            best_global_sol = population[i][:]

    # --- 2) Boucle génétique principale ---
    for gen in range(max_gen):
        new_population = []

        # Tant qu'on n'a pas une population complète...
        while len(new_population) < pop_size:
            # --- a) Sélection de deux parents par tournoi ---
            idx1 = selection_tournoi(population, fitnesses, tournament_k)
            idx2 = selection_tournoi(population, fitnesses, tournament_k)
            parent1 = population[idx1]
            parent2 = population[idx2]

            # --- b) Crossover (avec probabilité pcross) ---
            if random.random() < pcross:
                child1, child2 = crossover_1point(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            # --- c) Mutation ---
            child1 = mutation_flip(child1, pmut)
            child2 = mutation_flip(child2, pmut)

            # On ajoute les enfants à la nouvelle population
            new_population.append(child1)
            if len(new_population) < pop_size:  # évite de dépasser pop_size
                new_population.append(child2)

        # --- d) Remplacement : on remplace l'ancienne pop par la nouvelle ---
        population = new_population
        
        # Recalculer les fitness
        fitnesses = [fitness(liste_items, sol, max_capacity) for sol in population]

        # --- e) Mettre à jour le meilleur global ---
        for i, fit in enumerate(fitnesses):
            if fit > best_global_fit:
                best_global_fit = fit
                best_global_sol = population[i][:]

    return best_global_sol, best_global_fit

# ---------------------------------------------------------------------
# Exemple d'utilisation si on exécute ce script directement :
if __name__ == '__main__':
    # Exemple : à adapter selon le nom du fichier
    fichier_test = "pi-12-100-1000-001.kna"
    max_capacity, liste_items = lire_fichier(fichier_test)

    best_sol, best_fit = algogen_knapsack(
        liste_items,
        max_capacity,
        pop_size=50,      # taille de la population
        max_gen=200,      # nombre de générations
        pcross=0.8,       # probabilité de crossover
        pmut=0.01,        # probabilité de mutation
        tournament_k=3    # taille de tournoi (sélection)
    )

    print("Meilleure fitness obtenue:", best_fit)
    print("Solution (vecteur binaire) :", best_sol)
    poids_total = sum(liste_items[i][2] for i, bit in enumerate(best_sol) if bit == 1)
    profit_total = sum(liste_items[i][1] for i, bit in enumerate(best_sol) if bit == 1)
    print("Poids total:", poids_total, "/", max_capacity)
    print("Profit total:", profit_total)

    # IDs des items sélectionnés
    selected_ids = [liste_items[i][0] for i, bit in enumerate(best_sol) if bit == 1]
    print("Items sélectionnés (ID):", selected_ids)
