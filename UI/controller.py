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
        self._view._dd_album2.options.clear()
        album = self._model.getAllNodes()
        for a in album:
            self._view._dd_album.options.append(ft.dropdown.Option(key=a.AlbumId, text=a.Title))
            self._view._dd_album2.options.append(ft.dropdown.Option(key=a.AlbumId, text=a.Title))
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

    def handlePercorso(self, e):
        self._view.txt_result.controls.clear()
        id1 = self._view._dd_album.value
        id2 = self._view._dd_album2.value
        if id1 is None or id2 is None:
            self._view.create_alert("Seleziona entrambi gli album")
            return
        if id1 == id2:
            self._view.create_alert("L'album di partenza e di arrivo devono essere diversi")
            return
        soglia = self._view._txt_soglia.value
        if soglia == "":
            self._view.create_alert("Seleziona soglia")
            return
        try:
            x = float(soglia)
        except ValueError:
            self._view.create_alert("Seleziona soglia numerica")
            return
        path = self._model.getPath(id1, id2, x)
        if path is None or len(path) <= 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Non esiste nessun cammino tra i due album che rispetti i criteri indicati.")
            )
        for a in path:
            self._view.txt_result.controls.append(ft.Text(f"{a}"))
        self._view.update_page()