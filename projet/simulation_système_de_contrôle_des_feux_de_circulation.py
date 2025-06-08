# import simpy
# import random
# from système_de_contrôle_des_feux_de_circulation import simulateur_dfv  # on importe notre contrôleur flou

# # Paramètres de simulation
# SIMULATION_DURATION = 300  # en secondes

# class Intersection:
#     def __init__(self, env):
#         self.env = env
#         self.vehicules_NS = 0
#         self.pietons_NS = 0
#         self.vehicules_EW = 0
#         self.pietons_EW = 0

#         self.stats = {
#         'veh_passes_NS': 0,
#         'veh_passes_EW': 0,
#         'time_green_NS': 0,
#         'time_green_EW': 0,
#         'total_time': 0,
#         }


#         # Lancement des processus
#         self.env.process(self.generateur_vehicules_NS())
#         self.env.process(self.generateur_pietons_NS())
#         self.env.process(self.generateur_vehicules_EW())
#         self.env.process(self.generateur_pietons_EW())
#         # self.env.process(self.cycle_feux_NS())
#         self.env.process(self.cycle_feux())


#     def generateur_vehicules_NS(self):
#         while True:
#             yield self.env.timeout(random.expovariate(1/5))  # un véhicule toutes ~5 sec
#             self.vehicules_NS += 1
#             self.arriv_NS.append(self.env.now)
#             print(f"[{self.env.now:.1f}s] Véhicule arrivé (NS) - Total : {self.vehicules_NS}")

#     def generateur_pietons_NS(self):
#         while True:
#             yield self.env.timeout(random.expovariate(1/15))  # un piéton toutes ~15 sec
#             self.pietons_NS += 1
#             print(f"[{self.env.now:.1f}s] Piéton détecté (NS) - Total : {self.pietons_NS}")


#     def generateur_vehicules_EW(self):
#         while True:
#             yield self.env.timeout(random.expovariate(1/7))  
#             self.vehicules_EW += 1
#             self.arriv_EW.append(self.env.now)
#             print(f"[{self.env.now:.1f}s] Véhicule arrivé (EW) - Total : {self.vehicules_EW}")

    
#     def generateur_pietons_EW(self):
#         while True:
#             yield self.env.timeout(random.expovariate(1/20))
#             self.pietons_EW += 1
#             print(f"[{self.env.now:.1f}s] Piéton détecté (EW) - Total : {self.pietons_EW}")



#     def cycle_feux(self):
#         while True:
#             # === Phase NS ===
#             simulateur_dfv.input['densite_vehicule'] = min(self.vehicules_NS, 50)
#             simulateur_dfv.input['densite_pietons'] = min(self.pietons_NS, 10)
#             simulateur_dfv.compute()
#             duree_NS = simulateur_dfv.output['duree_feux_vert']

#             print(f"\n[{self.env.now:.1f}s] ===> FEU VERT NS : {duree_NS:.2f} sec (DV={self.vehicules_NS}, PA={self.pietons_NS})")
#             nb_veh_NS = min(self.vehicules_NS, int(duree_NS // 2))
#             self.vehicules_NS -= nb_veh_NS
#             self.pietons_NS = 0
#             yield self.env.timeout(duree_NS)
#             print(f"[{self.env.now:.1f}s] >>> FEU ROUGE NS")
#             yield self.env.timeout(3)

#             # === Phase EW ===
#             simulateur_dfv.input['densite_vehicule'] = min(self.vehicules_EW, 50)
#             simulateur_dfv.input['densite_pietons'] = min(self.pietons_EW, 10)
#             simulateur_dfv.compute()
#             duree_EW = simulateur_dfv.output['duree_feux_vert']

#             print(f"\n[{self.env.now:.1f}s] ===> FEU VERT EW : {duree_EW:.2f} sec (DV={self.vehicules_EW}, PA={self.pietons_EW})")
#             nb_veh_EW = min(self.vehicules_EW, int(duree_EW // 2))
#             self.vehicules_EW -= nb_veh_EW
#             self.pietons_EW = 0
#             yield self.env.timeout(duree_EW)
#             print(f"[{self.env.now:.1f}s] >>> FEU ROUGE EW")
#             yield self.env.timeout(3)

#             #Pendant la phase NS :
#             self.stats['veh_passes_NS'] += nb_veh_NS
#             self.stats['time_green_NS'] += duree_NS
#             self.stats['total_time'] += duree_NS + 3
            
#             #Pendant la phase EW :

#             self.stats['veh_passes_EW'] += nb_veh_EW
#             self.stats['time_green_EW'] += duree_EW
#             self.stats['total_time'] += duree_EW + 3






# def print_stats(self):
#     print("\n========= STATISTIQUES DE SIMULATION =========")
#     total_veh = self.stats['veh_passes_NS'] + self.stats['veh_passes_EW']
#     print(f"Véhicules passés (NS) : {self.stats['veh_passes_NS']}")
#     print(f"Véhicules passés (EW) : {self.stats['veh_passes_EW']}")
#     print(f"Total véhicules passés : {total_veh}")
    
#     print(f"Temps vert (NS) : {self.stats['time_green_NS']:.1f}s")
#     print(f"Temps vert (EW) : {self.stats['time_green_EW']:.1f}s")
#     print(f"Temps total simulé : {self.stats['total_time']:.1f}s")

#     if self.stats['total_time'] > 0:
#         taux_utilisation = 100 * (self.stats['time_green_NS'] + self.stats['time_green_EW']) / self.stats['total_time']
#         print(f"Taux d’utilisation des feux verts : {taux_utilisation:.1f}%")

# if __name__ == '__main__':
#     env = simpy.Environment()
#     intersection = Intersection(env)
#     env.run(until=SIMULATION_DURATION)
#     intersection.print_stats()

import simpy
import random
# import matplotlib.pyplot as plt
from système_de_contrôle_des_feux_de_circulation import simulateur_dfv  # on importe notre contrôleur flou

# Paramètres de simulation
SIMULATION_DURATION = 300  # en secondes

class Intersection:
    def __init__(self, env):
        self.env = env
        self.vehicules_NS = 0
        self.pietons_NS = 0
        self.vehicules_EW = 0
        self.pietons_EW = 0

        # Statistiques
        self.stats = {
            'veh_passes_NS': 0,
            'veh_passes_EW': 0,
            'time_green_NS': 0,
            'time_green_EW': 0,
            'total_time': 0,
        }
        
        #historique
        
        self.historique = {
            'temps': [],
            'file_NS': [],
            'file_EW': [],
            'attente_NS': [],
            'attente_EW': [],
        }

        


        # Listes d'arrivée pour calcul du temps d'attente
        self.arriv_NS = []
        self.arriv_EW = []
        self.attente_totale_NS = 0
        self.attente_totale_EW = 0

        # Lancement des processus
        self.env.process(self.generateur_vehicules_NS())
        self.env.process(self.generateur_pietons_NS())
        self.env.process(self.generateur_vehicules_EW())
        self.env.process(self.generateur_pietons_EW())
        self.env.process(self.cycle_feux())

    def generateur_vehicules_NS(self):
        while True:
            yield self.env.timeout(random.expovariate(1/5))  # un véhicule toutes ~5 sec
            self.vehicules_NS += 1
            self.arriv_NS.append(self.env.now)
            print(f"[{self.env.now:.1f}s] Véhicule arrivé (NS) - Total : {self.vehicules_NS}")

    def generateur_pietons_NS(self):
        while True:
            yield self.env.timeout(random.expovariate(1/15))  # un piéton toutes ~15 sec
            self.pietons_NS += 1
            print(f"[{self.env.now:.1f}s] Piéton détecté (NS) - Total : {self.pietons_NS}")

    def generateur_vehicules_EW(self):
        while True:
            yield self.env.timeout(random.expovariate(1/7))  
            self.vehicules_EW += 1
            self.arriv_EW.append(self.env.now)
            print(f"[{self.env.now:.1f}s] Véhicule arrivé (EW) - Total : {self.vehicules_EW}")

    def generateur_pietons_EW(self):
        while True:
            yield self.env.timeout(random.expovariate(1/20))
            self.pietons_EW += 1
            print(f"[{self.env.now:.1f}s] Piéton détecté (EW) - Total : {self.pietons_EW}")

    def cycle_feux(self):
        while True:
            # === Phase NS ===
            simulateur_dfv.input['densite_vehicule'] = min(self.vehicules_NS, 50)
            simulateur_dfv.input['densite_pietons'] = min(self.pietons_NS, 10)
            simulateur_dfv.compute()
            duree_NS = simulateur_dfv.output['duree_feux_vert']

            print(f"\n[{self.env.now:.1f}s] ===> FEU VERT NS : {duree_NS:.2f} sec (DV={self.vehicules_NS}, PA={self.pietons_NS})")

            nb_veh_NS = min(self.vehicules_NS, int(duree_NS // 2))
            for _ in range(nb_veh_NS):
                if self.arriv_NS:
                    arrivee = self.arriv_NS.pop(0)
                    attente = self.env.now - arrivee
                    self.attente_totale_NS += attente

            self.vehicules_NS -= nb_veh_NS
            self.pietons_NS = 0
            self.stats['veh_passes_NS'] += nb_veh_NS
            self.stats['time_green_NS'] += duree_NS
            self.stats['total_time'] += duree_NS + 3

            #enregistrment d'etat a chaque cycle

            self.historique['temps'].append(self.env.now)
            self.historique['file_NS'].append(self.vehicules_NS)
            self.historique['file_EW'].append(self.vehicules_EW)

            # Ajouter attente moyenne instantanée simulée (approximative)
            moy_NS = (self.attente_totale_NS / self.stats['veh_passes_NS']) if self.stats['veh_passes_NS'] else 0
            moy_EW = (self.attente_totale_EW / self.stats['veh_passes_EW']) if self.stats['veh_passes_EW'] else 0
            self.historique['attente_NS'].append(moy_NS)
            self.historique['attente_EW'].append(moy_EW)

            yield self.env.timeout(duree_NS)
            print(f"[{self.env.now:.1f}s] >>> FEU ROUGE NS")
            yield self.env.timeout(3)

            # === Phase EW ===
            simulateur_dfv.input['densite_vehicule'] = min(self.vehicules_EW, 50)
            simulateur_dfv.input['densite_pietons'] = min(self.pietons_EW, 10)
            simulateur_dfv.compute()
            duree_EW = simulateur_dfv.output['duree_feux_vert']

            print(f"\n[{self.env.now:.1f}s] ===> FEU VERT EW : {duree_EW:.2f} sec (DV={self.vehicules_EW}, PA={self.pietons_EW})")

            nb_veh_EW = min(self.vehicules_EW, int(duree_EW // 2))
            for _ in range(nb_veh_EW):
                if self.arriv_EW:
                    arrivee = self.arriv_EW.pop(0)
                    attente = self.env.now - arrivee
                    self.attente_totale_EW += attente

            self.vehicules_EW -= nb_veh_EW
            self.pietons_EW = 0
            self.stats['veh_passes_EW'] += nb_veh_EW
            self.stats['time_green_EW'] += duree_EW
            self.stats['total_time'] += duree_EW + 3

            yield self.env.timeout(duree_EW)
            print(f"[{self.env.now:.1f}s] >>> FEU ROUGE EW")
            yield self.env.timeout(3)


    def plot_stats(self):
        import matplotlib.pyplot as plt
        t = self.historique['temps']
        file_ns = self.historique['file_NS']
        file_ew = self.historique['file_EW']
        att_ns = self.historique['attente_NS']
        att_ew = self.historique['attente_EW']

        plt.figure(figsize=(12, 5))

        # Graphique des files d’attente
        plt.subplot(1, 2, 1)
        plt.plot(t, file_ns, label="File NS", color="blue")
        plt.plot(t, file_ew, label="File EW", color="orange")
        plt.xlabel("Temps (s)")
        plt.ylabel("Nombre de véhicules")
        plt.title("Évolution des files d’attente")
        plt.legend()

        # Graphique du temps d’attente
        plt.subplot(1, 2, 2)
        plt.plot(t, att_ns, label="Attente moyenne NS", linestyle='--', color="green")
        plt.plot(t, att_ew, label="Attente moyenne EW", linestyle='--', color="red")
        plt.xlabel("Temps (s)")
        plt.ylabel("Attente moyenne (s)")
        plt.title("Temps d’attente moyen par direction")
        plt.legend()

        plt.tight_layout()
        plt.show()

    def print_stats(self):
        print("\n========= STATISTIQUES DE SIMULATION =========")
        total_veh = self.stats['veh_passes_NS'] + self.stats['veh_passes_EW']
        print(f"Véhicules passés (NS) : {self.stats['veh_passes_NS']}")
        print(f"Véhicules passés (EW) : {self.stats['veh_passes_EW']}")
        print(f"Total véhicules passés : {total_veh}")
            
        print(f"Temps vert (NS) : {self.stats['time_green_NS']:.1f}s")
        print(f"Temps vert (EW) : {self.stats['time_green_EW']:.1f}s")
        print(f"Temps total simulé : {self.stats['total_time']:.1f}s")

        if self.stats['total_time'] > 0:
            taux_utilisation = 100 * (self.stats['time_green_NS'] + self.stats['time_green_EW']) / self.stats['total_time']
            print(f"Taux d’utilisation des feux verts : {taux_utilisation:.1f}%")

        if self.stats['veh_passes_NS'] > 0:
            moyenne_NS = self.attente_totale_NS / self.stats['veh_passes_NS']
        else:
            moyenne_NS = 0

        if self.stats['veh_passes_EW'] > 0:
            moyenne_EW = self.attente_totale_EW / self.stats['veh_passes_EW']
        else:
            moyenne_EW = 0

        print(f"Temps d’attente moyen (NS) : {moyenne_NS:.1f} sec")
        print(f"Temps d’attente moyen (EW) : {moyenne_EW:.1f} sec")

    def export_rapport(self, filename="rapport_simulation.txt"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("========= RAPPORT DE SIMULATION =========\n\n")
            total_veh = self.stats['veh_passes_NS'] + self.stats['veh_passes_EW']
            f.write(f"🕒 Durée simulée          : {self.stats['total_time']:.1f} s\n")
            f.write(f"🚗 Véhicules passés (NS)  : {self.stats['veh_passes_NS']}\n")
            f.write(f"🚗 Véhicules passés (EW)  : {self.stats['veh_passes_EW']}\n")
            f.write(f"🚦 Total véhicules passés : {total_veh}\n\n")

            f.write(f"🟩 Temps vert (NS)        : {self.stats['time_green_NS']:.1f} s\n")
            f.write(f"🟧 Temps vert (EW)        : {self.stats['time_green_EW']:.1f} s\n")

            if self.stats['total_time'] > 0:
                taux_utilisation = 100 * (self.stats['time_green_NS'] + self.stats['time_green_EW']) / self.stats['total_time']
            else:
                taux_utilisation = 0.0
            f.write(f"📊 Taux utilisation feux  : {taux_utilisation:.1f} %\n\n")

            # Temps d’attente moyens
            moyenne_NS = self.attente_totale_NS / self.stats['veh_passes_NS'] if self.stats['veh_passes_NS'] > 0 else 0
            moyenne_EW = self.attente_totale_EW / self.stats['veh_passes_EW'] if self.stats['veh_passes_EW'] > 0 else 0

            f.write(f"⏱️ Temps attente moyen (NS) : {moyenne_NS:.1f} s\n")
            f.write(f"⏱️ Temps attente moyen (EW) : {moyenne_EW:.1f} s\n")
            f.write("\n=========================================\n")
            print(f"\n📄 Rapport sauvegardé dans : {filename}")


# Exécution principale
if __name__ == '__main__':
    env = simpy.Environment()
    intersection = Intersection(env)
    env.run(until=SIMULATION_DURATION)
    intersection.print_stats()
    intersection.plot_stats()
    intersection.export_rapport()