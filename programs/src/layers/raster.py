import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import rasterio as rio
from rasterio.crs import CRS

from src.layers import state

try:
    from pyproj import CRS as PyprojCRS
except ImportError:
    PyprojCRS = None


def extract_epsg(
    crs: Optional[CRS],
    min_confidence: int = 25,
    allow_authority_fallback: bool = True,
) -> Optional[int]:
    if crs is None:
        return None

    try:
        epsg = crs.to_epsg()
        if epsg is not None:
            return int(epsg)
    except Exception:
        pass

    if PyprojCRS is not None:
        try:
            p_crs = PyprojCRS.from_wkt(crs.to_wkt())
            epsg = p_crs.to_epsg(min_confidence=min_confidence)
            if epsg is not None:
                return int(epsg)
        except Exception:
            pass

    if allow_authority_fallback:
        wkt = crs.to_wkt()
        matches = re.findall(r'(?:AUTHORITY|ID)\["EPSG","?(\d+)"?\]', wkt)
        if matches:
            candidate = int(matches[-1])
            try:
                if CRS.from_epsg(candidate).is_valid:
                    return candidate
            except Exception:
                pass

    return None

@dataclass
class RasterLayer:
    id: int
    name: str
    array: np.ndarray  # kształt (wysokość, szerokość, kanały)
    profile: rio.profiles.Profile
    epsg: Optional[int] = None

    @staticmethod
    def read_raster(path: str | Path, name: Optional[str] = None) -> "RasterLayer":
        path = Path(path)
        layer_name = name if name else path.stem

        with rio.open(path) as src:
            # rasterio zwraca (kanały, wysokość, szerokość)
            raster_arr = src.read()
            raster_profile = src.profile.copy()
            epsg = extract_epsg(src.crs)

            # Jeśli udało się rozpoznać EPSG, ujednolicamy CRS w profilu
            if epsg is not None:
                raster_profile["crs"] = CRS.from_epsg(epsg)

        raster_arr_hwc = np.moveaxis(raster_arr, 0, -1)
        height, width, channels = raster_arr_hwc.shape

        raster = RasterLayer(
            id=state.layer_id,
            name=layer_name,
            array=raster_arr_hwc,
            profile=raster_profile,
            epsg=epsg
        )

        state.layers_dict[raster.name] = raster

        crs_label = f"EPSG:{epsg}" if epsg is not None else (
            raster_profile["crs"].to_string() if raster_profile.get("crs") else pd.NA
        )

        raster_row = {
            "id": state.layer_id,
            "nazwa": raster.name,
            "wysokość": height,
            "szerokość": width,
            "crs": crs_label,
            "liczba kanałów": channels,
        }
        state.layers_table.loc[len(state.layers_table)] = raster_row
        state.layer_id += 1

        return raster

    def save(self, output_path: str | Path) -> None:
        output_path = Path(output_path)

        arr_to_write = np.moveaxis(self.array, -1, 0)

        profile = self.profile.copy()
        profile.update(
            height=arr_to_write.shape[1],
            width=arr_to_write.shape[2],
            count=arr_to_write.shape[0],
            dtype=arr_to_write.dtype,
        )
        if self.epsg is not None:
            profile["crs"] = CRS.from_epsg(self.epsg)

        with rio.open(output_path, "w", **profile) as dst:
            dst.write(arr_to_write)
