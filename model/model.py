import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self._lista_rifugi = []
        self._dizionario_rifugi = {}
        self.lista_nodi = []

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        self._dizionario_rifugi.clear()

        self._lista_rifugi = DAO.readAllrifugi()  # Leggo tutti i rifugi dal DAO
        # Ciclo sui rifugi per aggiungerli al grafo e popolare il dizionario
        for rifugio in self._lista_rifugi:
            self._dizionario_rifugi[rifugio.id] = rifugio
        # prendo solo le connessioni valide
        connessioni = DAO.readAllConnessioniFinoAnno(year)

        # Ciclo su tutte le coppie di hub  per creare archi
        for c in connessioni:
            # Recupero i due rifugi usando il dizionario
            rifugio1 = self._dizionario_rifugi[c.id_rifugio1]
            rifugio2 = self._dizionario_rifugi[c.id_rifugio2]
            difficolta = c.difficolta.lower().strip()

            self.G.add_node(rifugio1)
            self.G.add_node(rifugio2)
            distanza =float(c.distanza)

            if difficolta=="facile":
                fattore=1
            elif difficolta=="media":
                fattore= 1.5
            elif difficolta == "difficile":
                fattore=2
            peso_arco= distanza*fattore
            # Aggiungo l’arco
            self.G.add_edge(rifugio1, rifugio2,peso=peso_arco)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        #return nx.min_weight_matching(self.G,weight="peso"), nx.max_weight_matching(self.G,weight="peso")
        pesi = nx.get_edge_attributes(self.G, "peso").values()
        return min(pesi), max(pesi)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        pesi = nx.get_edge_attributes(self.G, "peso")  # dizionario {(u,v): peso}
        minori = 0
        maggiori = 0
        for peso in pesi.values():  # itero sui valori, non sulle chiavi
            if peso < soglia:
                minori += 1
            elif peso > soglia:
                maggiori += 1

        return minori, maggiori






    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def cammino_minimo(self,soglia):

            # Filtro archi con peso maggiore di soglia
            valid_edges = [(u, v, d) for u, v, d in self.G.edges(data=True) if d["peso"] > soglia]
            if not valid_edges:
                return None, []  # Nessun arco valido

            # Creo sotto-grafo con archi validi
            H = nx.Graph()
            H.add_edges_from(valid_edges)

            # Per ogni nodo calcolo Dijkstra verso tutti gli altri
            for nodo in H.nodes:
                lunghezze, paths = nx.single_source_dijkstra(H, nodo, weight="peso")
                for target, percorso in paths.items():
                    if len(percorso) >= 3:  # almeno 2 archi (3 nodi)
                        return lunghezze[target], percorso  # restituisco il primo percorso valido trovato

            # Nessun percorso valido trovato
            return None, []

    # METODO 2: ricorsione
    # Creo sotto-grafo con archi validi
    # H = nx.Graph()
    # for u, v, d in self.G.edges(data=True):
    #     if d["peso"] > soglia:
    #         H.add_edge(u, v, peso=d["peso"])    Aggiungo solo gli archi validi (peso maggiore di soglia)
    #
    # if H.number_of_edges() == 0:
    #     return None, []                         Se non ci sono archi validi, non esiste alcun percorso
    #
    # # Funzione ricorsiva per trovare un percorso valido
    # def dfs(percorso, visitati):                 Funzione ricorsiva DFS per trovare un percorso valido
    #     ultimo = percorso[-1]                    Prendo l'ultimo nodo del percorso corrente
    #     for vicino in H.neighbors(ultimo):       Controllo tutti i vicini del nodo corrente
    #         if vicino not in visitati:
    #             nuovo_percorso = percorso + [vicino]       aggoiungo il vicino
    #             nuovo_visitati = visitati | {vicino}       aggiorno i nodi visitati
    #             if len(nuovo_percorso) >= 3:               almeno 2 archi
    #                 return nuovo_percorso                 primo percorso valido trovato
    #             risultato = dfs(nuovo_percorso, nuovo_visitati)    Altrimenti continuo la ricerca ricorsivamente
    #             if risultato:                                      se valido lo restituisco
    #                 return risultato
    #     return None
    #
    # # Provo DFS partendo da ogni nodo
    # for nodo in H.nodes:
    #     percorso = dfs([nodo], {nodo})
    #     if percorso:
    #          Calcolo il costo totale del percorso sommando i pesi degli archi
    #         costo = sum(H[percorso[i]][percorso[i + 1]]["peso"] for i in range(len(percorso) - 1))
    #         return costo, percorso
    #
    # # Nessun percorso valido trovato
    # return None, []








