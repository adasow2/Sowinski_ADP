import pandas as pd

layer_id = 0

layers_table = pd.DataFrame({
    'id': [],
    'nazwa': [],
    'wysokość': [],
    'szerokość': [],
    'crs': [],
    'liczba kanałów': []
})

layers_dict = {}


def get_layer(layer_id):
    row = layers_table.loc[layers_table["id"] == layer_id]
    if row.empty:
        return None
    return layers_dict.get(row.iloc[0]["nazwa"])
