from src.layers import state
from src.menu_operations.read_raster import active_layer_windows


def close_raster(layer_id):
    if layer_id is None:
        return False

    row = state.layers_table.loc[state.layers_table["id"] == layer_id]
    if row.empty:
        return False

    name = row.iloc[0]["nazwa"]
    state.layers_dict.pop(name, None)
    state.layers_table = state.layers_table[
        state.layers_table["id"] != layer_id
    ].reset_index(drop=True)

    for callback in list(active_layer_windows):
        try:
            callback()
        except Exception:
            active_layer_windows.remove(callback)

    return True
