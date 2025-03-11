from ortools.sat.python import cp_model # type: ignore
import time

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

def solve_knapsack_cp_sat(fichier):
    max_capacity, liste_items = lire_fichier(fichier)
    n = len(liste_items)

    model = cp_model.CpModel()

    x = []
    for i in range(n): # on crée une variable binaire pour chaque item : x_i = 1 si l'item i est pris, 0 sinon
        x.append(model.NewBoolVar(f"x_{i}"))

    model.Add(
        sum(liste_items[i][2] * x[i] for i in range(n)) <= max_capacity # fonction contrainte : somme des poids des items sélectionnés <= max_capacity
    )

    model.Maximize(
        sum(liste_items[i][1] * x[i] for i in range(n)) # fonction objectif : somme des profits des items sélectionnés
    )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution trouvée !")
        print(f"Profit total = {solver.ObjectiveValue()}")
        poids_total = 0
        items_selectionnes = []
        for i in range(n):
            if solver.Value(x[i]) == 1:
                idx_item = liste_items[i][0]
                weight_item = liste_items[i][2]
                items_selectionnes.append(idx_item)
                poids_total += weight_item

        print(f"Poids total = {poids_total}")
        print(f"Items sélectionnés (IDs) = {items_selectionnes}")
    else:
        print("Pas de solution.")

if __name__ == "__main__":
    fichier_test = "pi-15-10000-1000-001.kna"
    start_time = time.time()
    solve_knapsack_cp_sat(fichier_test)
    execution_time = time.time() - start_time
    print(f"Temps d'exécution : {execution_time} secondes")
