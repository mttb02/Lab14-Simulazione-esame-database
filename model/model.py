import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []

        self._best_path = []

    def create_graph(self):
        self._graph.clear()
        self._nodes = []

        temp_nodes = DAO.get_all_chromosomes()
        for n in temp_nodes:
            self._graph.add_node(n)
            self._nodes.append(n)

        temp_edges = DAO.get_all_edges()
        for e in temp_edges.keys():
            self._graph.add_edge(e[0], e[1], weight=temp_edges[e])


    def get_num_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_edges(self):
        return self._graph.number_of_edges()

    def get_info_edges(self):
        temp_edges = self._graph.edges
        temp_edges = sorted(temp_edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=False)
        return temp_edges[0][2]["weight"], temp_edges[-1][2]["weight"]

    def get_num_edges_soglia(self, soglia):
        temp_minori = 0
        temp_maggiori = 0
        for a in self._graph.edges(data=True):
            if a[2]["weight"] > soglia:
                temp_maggiori +=1
            else:
                temp_minori +=1
        return temp_minori, temp_maggiori

    def get_edges_maggiori(self, soglia):
        temp_edges = []
        for a in self._graph.edges(data=True):
            if a[2]["weight"] > soglia:
                temp_edges.append(a)
        return temp_edges

    def best_path(self, soglia):

        self._best_path = []
        archi_rimanenti = self.get_edges_maggiori(soglia)
        soluzione_parziale = []

        for a in archi_rimanenti:
            soluzione_parziale.append(a)
            archi_rimanenti.remove(a)
            self.ricorsione(soluzione_parziale, archi_rimanenti)
            soluzione_parziale.remove(a)
            archi_rimanenti.append(a)

        return self.calcola_punteggio(self._best_path), self._best_path


    def ricorsione(self, soluzione_parziale, archi_rimanenti):
        #Se non si sono archi "vicini" -> controlla se soluzione migliore -> esci
        archi_validi = self.get_archi_validi(soluzione_parziale[-1], archi_rimanenti)
        if len(archi_validi) == 0:
            if self.calcola_punteggio(soluzione_parziale) > self.calcola_punteggio(self._best_path):
                self._best_path = copy.deepcopy(soluzione_parziale)
            return
        for a in archi_validi:
            soluzione_parziale.append(a)
            archi_rimanenti.remove(a)
            self.ricorsione(soluzione_parziale, archi_rimanenti)
            soluzione_parziale.remove(a)
            archi_rimanenti.append(a)


    def get_archi_validi(self, arco, archi_rimanenti):
        temp_archi = []
        for a in archi_rimanenti:
            if a[0] == arco[1]:
                temp_archi.append(a)
        return temp_archi

    def calcola_punteggio(self, path):
        temp_punteggio = 0
        for a in path:
            temp_punteggio += a[2]["weight"]
        return temp_punteggio


