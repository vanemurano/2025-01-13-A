import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph=nx.Graph() # semplice, non orientato e pesato
        self._nodes=[]
        self._idMapGenes=dict()
        self._genes=DAO.get_all_genes()
        self._idMapClass=dict()
        for c in DAO.get_all_classifications():
            self._idMapClass[c.GeneID]=c
        self._bestPath = []
        self._bestNComp = len(self._graph.nodes)
        self._bestLen = 0

    def getAllLocalizations(self):
        return DAO.getAllLocalizations()

    def getChromosomes(self, GeneID: str):
        return DAO.getChromosomes(GeneID)

    def buildGraph(self, loc):
        self._nodes=[]
        self._graph.clear()
        for c in DAO.getAllNodesWEssential(loc):
            self._nodes.append(c)
        self._graph.add_nodes_from(self._nodes)
        for c1, c2 in DAO.getAllEdges(loc, self._idMapClass): # controllo di sicurezza sui nodi
            if c1 in self._nodes and c2 in self._nodes:
                crom1=DAO.getChromosomes(c1.GeneID)
                crom2=DAO.getChromosomes(c2.GeneID)
                if crom1!=crom2:
                    peso=crom1+crom2
                else:
                    peso=crom1
                self._graph.add_edge(c1, c2, weight=peso)

    def getConnectedComponents(self):
        componenti=list(nx.connected_components(self._graph))
        compMax=[]
        for c in componenti:
            if len(c)>1:
                compMax.append(c)
        compMax.sort(key=lambda x: len(x), reverse=True)
        return compMax

    def getBestPath(self):
        self._bestPath = []
        self._bestNComp = len(self._graph.nodes)
        self._bestLen = 0
        allNodes=[]
        for node in self._nodes:
            if node.Essential!="?":
                allNodes.append(node)
        allNodes.sort(key=lambda x: x.GeneID)
        for root in allNodes:
            rimanenti = copy.deepcopy(allNodes)
            rimanenti.remove(root)
            rimanenti = [x for x in rimanenti if x.Essential == root.Essential]
            # tutti i nodi tranne il primo che hanno lo stesso campo Essential
            self._ricorsione([root], list(rimanenti))
        return self._bestPath, self._bestLen, self._bestNComp

    def _ricorsione(self, parziale, rimanenti):
        if len (parziale) > self._bestLen:
            self._bestLen = len(parziale)
            self._bestNComp = self._getScore(parziale)
            self._bestPath = copy.deepcopy(parziale)
        if len(parziale) == self._bestLen:
            # a parità di lunghezza, minor numero di comp connesse del sottografo
            if self._getScore(parziale) < self._bestNComp:
                self._bestNComp = self._getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
        if len(rimanenti) == 0:
            return
        for n in rimanenti:
            if n.GeneID > parziale[-1].GeneID: # id dei geni strettamente crescenti
                parziale.append(n)
                rimanenti.remove(n)
                self._ricorsione(parziale, rimanenti)
                # backtracking
                parziale.pop()
                rimanenti.append(n)

    def _getScore(self, parziale):
        return nx.number_connected_components(self._graph.subgraph(parziale))

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)

    def getEdges(self):
        archi=list(self._graph.edges(data="weight"))
        archi.sort(key=lambda x: x[2])
        return archi