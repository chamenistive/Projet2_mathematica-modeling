
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl 
import matplotlib.pyplot as plt


#creons les univers de discours : c'est la plage de valeurs 
#possibles pour chaque variable.
#Il crée les fonctions d'appartenance à l'aide de fuzz.trimf, 
# c'est-à-dire des triangles définissant les zones « floues ».



# creations des univers (la modelissation des 4 vois nor sud est ouest)
dv = ctrl.Antecedent(np.arange (0, 51, 1), 'densite_vehicule')
pa = ctrl.Antecedent(np.arange (0, 11, 1), 'densite_pietons')
dfv = ctrl.Consequent(np.arange (0, 61, 1), 'duree_feux_vert')  # Fixed: removed 's' to match usage

# definition des fonction d'apprenntissage pour DV (densite_vehicule)
dv['faible'] = fuzz.trimf(dv.universe, [0, 0, 15])
dv['moyenne'] = fuzz.trimf(dv.universe, [10, 25, 40])
dv['eleve'] = fuzz.trimf(dv.universe, [30, 50, 50])


#fonction d'apprenntissage pour PA (pietons) - Fixed ranges to match universe
pa['aucun'] = fuzz.trimf(pa.universe, [0, 0, 2])
pa['quelques'] = fuzz.trimf(pa.universe, [1, 5, 8])      # Fixed: adjusted to universe range
pa['beaucoup'] = fuzz.trimf(pa.universe, [6, 10, 10])    # Fixed: adjusted to universe range


#fonction d'apprenntissage pour dfv (duree feux vert)
dfv['court'] = fuzz.trimf(dfv.universe, [0, 0, 20])
dfv['normal'] = fuzz.trimf(dfv.universe, [15, 30, 45])
dfv['long'] = fuzz.trimf(dfv.universe, [40, 60, 60])



# AJouts des regles flou

regles = [
    ctrl.Rule(dv['faible'] & pa['aucun'], dfv['court']),      # Fixed: removed spaces
    ctrl.Rule(dv['faible'] & pa['quelques'], dfv['normal']),
    ctrl.Rule(dv['faible'] & pa['beaucoup'], dfv['normal']),


    ctrl.Rule(dv['moyenne'] & pa['aucun'], dfv['normal']),
    ctrl.Rule(dv['moyenne'] & pa['quelques'], dfv['normal']),
    ctrl.Rule(dv['moyenne'] & pa['beaucoup'], dfv['long']),


    ctrl.Rule(dv['eleve'] & pa['aucun'], dfv['long']),
    ctrl.Rule(dv['eleve'] & pa['quelques'], dfv['long']),
    ctrl.Rule(dv['eleve'] & pa['beaucoup'], dfv['long']),


]


# Création du système de contrôle flou
controle_dfv = ctrl.ControlSystem(regles)
simulateur_dfv = ctrl.ControlSystemSimulation(controle_dfv)




# # Optionnel : style graphique
# plt.style.use('seaborn-v0_8')

# # Visualisation de la densité de véhicules
# dv.view()
# plt.title("Densité de Véhicules (DV)")
# plt.show()

# # Visualisation du nombre de piétons
# pa.view()
# plt.title("Nombre de Piétons (PA)")
# plt.show()

# # Visualisation de la durée du feu vert
# dfv.view()
# plt.title("Durée du Feu Vert (DFV)")
# plt.show()





# Exemple de simulation manuelle
# Cas : 30 véhicules détectés + 6 piétons en attente

simulateur_dfv.input['densite_vehicule'] = 10
simulateur_dfv.input['densite_pietons'] = 1

# Calcul de la sortie
simulateur_dfv.compute()

# Résultat
print("Available output keys:", list(simulateur_dfv.output.keys()))
print(f"Durée conseillée du feu vert : {simulateur_dfv.output['duree_feux_vert']:.2f} secondes")  # Fixed: removed 's'

# Affichage graphique de la décision
dfv.view(simulateur_dfv)
plt.title("Sortie : Durée du Feu Vert recommandée")
plt.show()