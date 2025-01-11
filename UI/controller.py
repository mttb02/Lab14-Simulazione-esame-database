import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):

        self._model.create_graph()

        self._view.txt_result.controls.clear()

        temp_numero_vertici = self._model.get_num_nodes()
        temp_numero_archi = self._model.get_num_edges()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici {temp_numero_vertici} Numero di archi {temp_numero_archi}"))

        temp_arco_min, temp_arco_max = self._model.get_info_edges()
        self._view.txt_result.controls.append(ft.Text(f"Informazioni sui pesi degli archi - valore minimo {temp_arco_min} e valore massimo {temp_arco_max}"))

        self._view.btn_countedges.disabled = False
        self._view.btn_search.disabled = False

        self._view.update_page()


    def handle_countedges(self, e):
        temp_soglia = self._view.txt_name.value
        try:
            temp_soglia = float(temp_soglia)
        except ValueError:
            self._view.create_alert("Inserire un valore soglia numerico")
            return

        temp_arco_min, temp_arco_max = self._model.get_info_edges()
        if (temp_soglia > temp_arco_max) or (temp_soglia < temp_arco_min):
            self._view.create_alert(f"Il valore soglia deve essere tra {temp_arco_min} e {temp_arco_max}")
            return

        num_minori, num_maggiori = self._model.get_num_edges_soglia(temp_soglia)

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso maggiore della soglia: {num_maggiori}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso minore della soglia: {num_minori}"))

        self._view.update_page()

    def handle_search(self, e):
        temp_soglia = self._view.txt_name.value
        try:
            temp_soglia = float(temp_soglia)
        except ValueError:
            self._view.create_alert("Inserire un valore soglia numerico")
            return

        temp_arco_min, temp_arco_max = self._model.get_info_edges()
        if (temp_soglia > temp_arco_max) or (temp_soglia < temp_arco_min):
            self._view.create_alert(f"Il valore soglia deve essere tra {temp_arco_min} e {temp_arco_max}")
            return

        temp_punteggio, temp_vertici = self._model.best_path(temp_soglia)

        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {temp_punteggio}"))
        for a in temp_vertici:
            self._view.txt_result3.controls.append(ft.Text(f"{a[0]} --> {a[1]}: {a[2]["weight"]}"))

        self._view.update_page()



