import flet as ft
from UI.view import View
from database.DAO import DAO
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        localization=self._view.dd_localization.value
        if localization is None:
            self._view.create_alert("Scegliere prima una localizzazione!")
            return
        self._view.txt_result.controls.clear()
        self._model.buildGraph(localization)
        self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {self._model.getNNodes()} nodi"
                                              f" e {self._model.getNEdges()} archi"))
        for c1, c2, peso in self._model.getEdges():
            self._view.txt_result.controls.append(ft.Text(f"{c1.GeneID} <-> {c2.GeneID}: peso {peso}"))
        self._view.update_page()

    def analyze_graph(self, e):
        if self._model.getNNodes()==0:
            self._view.create_alert("Creare prima il grafo!")
            return
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono:"))
        for c in self._model.getConnectedComponents():
            str = ""
            for nodo in c:
                str += f"{nodo.GeneID}, "
            str += f"| dimensione componente: {len(c)}"
            self._view.txt_result.controls.append(
                ft.Text(str))
        self._view.update_page()

    def handle_path(self, e):
        if self._model.getNNodes() == 0:
            self._view.create_alert("Creare prima il grafo!")
            return
        path, len, score=self._model.getBestPath()
        self._view.txt_result.controls.append(
            ft.Text(f"La sequenza più lunga di cromosomi trovata è lunga {len}"
                    f" ed ha {score} componenti connesse.\n"
                    f"Di seguito i cromosomi in ordine:"))
        str=""
        for c in path:
            str+=f"{self._model.getChromosomes(c.GeneID)}, "
        self._view.txt_result.controls.append(
                ft.Text(str))
        self._view.update_page()

    def fillDDLocalization(self):
        listaLoc=DAO.getAllLocalizations()
        listaOpt=list(map(lambda x: ft.dropdown.Option(x), listaLoc))
        self._view.dd_localization.options=listaOpt
        self._view.update_page()

