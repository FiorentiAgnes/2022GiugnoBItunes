import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph= nx.DiGraph()
        self._idMapA= {}
        self._path = []

    #def getPath(...):

        # inizializza parziale
        # imposta record migliore
        # chiama _ricorsione
        # return record migliore

    #def _ricorsione(...):

        # 1. CONTROLLO TERMINAZIONE
        # se ultimo nodo == destinazione:
        # aggiorna record migliore se necessario

        # 2. ESPLORAZIONE VICINI
        # per ogni vicino:
        # se (condizione 1) e (condizione 2):
        # append()
        # ricorsione()
        # pop()

    def getPath(self, id1, id2, soglia):
        album1 = self._idMapA[int(id1)]
        album2 = self._idMapA[int(id2)]
        parziale = [album1]
        bilancio = self.calcolaBilancio(album1)
        self._ricorsione(parziale, album2, bilancio, soglia)
        return self._path

    def _ricorsione(self, parziale, target, bilancio, soglia):
        if parziale[-1] == target:
            if len(parziale) > len(self._path):
                self._path = list(parziale)
        nodo_corrente = parziale[-1]
        for vicino in self._graph.neighbors(nodo_corrente):
            if vicino not in parziale:
                if self._graph[nodo_corrente][vicino]['weight'] >= soglia:
                    if self.calcolaBilancio(vicino) > bilancio:
                        parziale.append(vicino)
                        self._ricorsione(parziale, target, bilancio, soglia)
                        parziale.pop()

    def calcolaBilancio(self, source):
        in_d = self._graph.in_degree(source, weight='weight')
        out_d = self._graph.out_degree(source, weight='weight')
        bilancio = in_d - out_d
        return bilancio


    def buildGraph(self, n):
        self._graph.clear()

        nodes = DAO.getAllNodes(n)
        self._graph.add_nodes_from(nodes)
        for a in nodes:
            self._idMapA[a.AlbumId] = a
        allEdges = DAO.getAllEdges(n, self._idMapA)
        for e in allEdges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        return self._graph.nodes

    def getAdiacenzePerBilancio(self, a):
        listaVicini = []
        for n in self._graph.successors(a):
            bilancio = 0
            for e in self._graph.out_edges(n, data=True):
                bilancio -= e[2]["weight"]
            for e in self._graph.in_edges(n, data=True):
                bilancio += e[2]["weight"]
            listaVicini.append([n, bilancio])
        listaVicini.sort(key=lambda x: x[1], reverse=True)
        return listaVicini
