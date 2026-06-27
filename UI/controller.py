import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        n = self._view._txt_n.value
        try:
            nInt = int(n)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore deve essere un intero positivo", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._model.buildGraph(n)
        self.fillDDAlbum()
        self._view.txt_result.controls.append(ft.Text("Grafo creato corretto", color="green"))
        nodi, archi= self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Num nodi:{nodi}, Num archi: {archi}", color="blue"))

        self._view.update_page()

    def fillDDAlbum(self):
        self._view._dd_album.options.clear()
        album = self._model.getAllNodes()
        for a in album:
            self._view._dd_album.options.append(ft.dropdown.Option(key=a.AlbumId, text=a.Title))
        self._view.update_page()

    def handleBilancio(self, e):
        if self._view._dd_album.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un album", color="red"))
            self._view.update_page()
            return

        id_album = int(self._view._dd_album.value)
        album_selezionato = self._model._idMapA[id_album]
        vicini = self._model.getAdiacenzePerBilancio(album_selezionato)
        self._view.txt_result.controls.clear()
        for v in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} -> Bilancio: {v[1]}"))
        self._view.update_page()

    def handlePercorso(self):
        pass