import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph= nx.DiGraph()
        self._idMapA= {}


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
