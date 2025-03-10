from ortools.sat.python import cp_model


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
   
    # 1) Lecture des données
    max_capacity, liste_items = lire_fichier(fichier)
    n = len(liste_items)

    # 2) Création du modèle
    model = cp_model.CpModel()

    # 3) Définition des variables binaires x_i (1 si l'item i est pris, 0 sinon)
    x = []
    for i in range(n):
        x.append(model.NewBoolVar(f"x_{i}"))

    # 4) Contraintes : somme(weight_i * x_i) <= max_capacity
    model.Add(
        sum(liste_items[i][2] * x[i] for i in range(n)) <= max_capacity
    )

    # 5) Fonction objectif : Maximize sum(profit_i * x_i)
    model.Maximize(
        sum(liste_items[i][1] * x[i] for i in range(n))
    )

    # 6) Résolution
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 7) Affichage des résultats
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution trouvée !")
        print(f"Profit total = {solver.ObjectiveValue()}")

        poids_total = 0
        items_selectionnes = []
        for i in range(n):
            if solver.Value(x[i]) == 1:
                idx_item = liste_items[i][0]
                profit_item = liste_items[i][1]
                weight_item = liste_items[i][2]
                items_selectionnes.append(idx_item)
                poids_total += weight_item

        print(f"Poids total = {poids_total}")
        print(f"Items sélectionnés (IDs) = {items_selectionnes}")
    else:
        print("Pas de solution faisable ou le modèle n'est pas satisfaisable.")

if __name__ == "__main__":
    # Exemple : fichier .kna ou .txt au format attendu
    fichier_test = "pi-15-10000-1000-001.kna"
    solve_knapsack_cp_sat(fichier_test)
