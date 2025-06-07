import simpy
import random
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

        self.stats = {
        'veh_passes_NS': 0,
        'veh_passes_EW': 0,
        'time_green_NS': 0,
        'time_green_EW': 0,
        'total_time': 0,
        }


        # Lancement des processus
        self.env.process(self.generateur_vehicules_NS())
        self.env.process(self.generateur_pietons_NS())
        self.env.process(self.generateur_vehicules_EW())
        self.env.process(self.generateur_pietons_EW())
        # self.env.process(self.cycle_feux_NS())
        self.env.process(self.cycle_feux())


    def generateur_vehicules_NS(self):
        while True:
            yield self.env.timeout(random.expovariate(1/5))  # un véhicule toutes ~5 sec
            self.vehicules_NS += 1
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
            self.vehicules_NS -= nb_veh_NS
            self.pietons_NS = 0
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
            self.vehicules_EW -= nb_veh_EW
            self.pietons_EW = 0
            yield self.env.timeout(duree_EW)
            print(f"[{self.env.now:.1f}s] >>> FEU ROUGE EW")
            yield self.env.timeout(3)

            #Pendant la phase NS :
            self.stats['veh_passes_NS'] += nb_veh_NS
            self.stats['time_green_NS'] += duree_NS
            self.stats['total_time'] += duree_NS + 3
            
            #Pendant la phase EW :

            self.stats['veh_passes_EW'] += nb_veh_EW
            self.stats['time_green_EW'] += duree_EW
            self.stats['total_time'] += duree_EW + 3






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

if __name__ == '__main__':
    env = simpy.Environment()
    intersection = Intersection(env)
    env.run(until=SIMULATION_DURATION)
    intersection.print_stats()
