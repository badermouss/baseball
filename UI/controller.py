import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the modello, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam = None

    def handleCreaGrafo(self, e):
        anno = int(self._view._ddAnno.value)
        if anno is None:
            self._view.create_alert("Selezionare un anno prima!!")
            return
        self._model.buildGraph(anno)
        numNodi, numArchi = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito di {numNodi} nodi e da {numArchi} archi"))
        self._view._btnDettagli.disabled = False
        self._view._btnPercorso.disabled = False
        self._view.update_page()

    def handleDettagli(self, e):
        if self._selectedTeam is None:
            self._view.create_alert("Selezionare prima una squadra!!")
            return
        vicini = self._model.getSortedNeighbors(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {self._selectedTeam} "                                             f"con relativo peso dell'arco"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        if self._selectedTeam is None:
            self._view.create_alert("Selezionare prima un nodo di partenza!")
            return
        bestPath, pesoOttimo = self._model.getPercorso(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il peso ottimo del percorso è {pesoOttimo}"))
        for team in bestPath:
            self._view._txt_result.controls.append(ft.Text(f"{team[0]} -- {team[1]}"))
        self._view.update_page()

    def fillDDYear(self):
        years = self._model.getYears()
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()

    def handleDDYearSelection(self, e):
        self._view._txtOutSquadre.controls.clear()
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(teams)} squadre che "
                                                          f"hanno giocato nel {self._view._ddAnno.value}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data=t, text=t.teamCode, on_click=self.readDDTeams)
            )
        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data



