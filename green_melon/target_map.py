"""Map class names to class IDs."""

GREEN_MELON: dict[str, int] = {"broadleaf": 0, "grass": 1, "maize": 2}

WEEDMAIZE: dict[str, int] = {
    # Maize (crop)
    "ZEAMX": GREEN_MELON["maize"],
    "ZEAMX_V1": GREEN_MELON["maize"],
    "ZEAMX_V3": GREEN_MELON["maize"],
    "ZEAMX_V4": GREEN_MELON["maize"],
    # Grass weeds (monocots)
    "CYPRO": GREEN_MELON["grass"],
    "CYPRO_max": GREEN_MELON["grass"],
    "CYPRO_min": GREEN_MELON["grass"],
    "ECHCG": GREEN_MELON["grass"],
    "ECHCG_V1": GREEN_MELON["grass"],
    "ECHCG_V2": GREEN_MELON["grass"],
    "ECHCG_Ve": GREEN_MELON["grass"],
    # Broadleaf weeds (dicots)
    "SOLNI": GREEN_MELON["broadleaf"],
    "SOLNI_V1": GREEN_MELON["broadleaf"],
    "SOLNI_V2": GREEN_MELON["broadleaf"],
    "SOLNI_Vc": GREEN_MELON["broadleaf"],
    # Background (hard negatives - not detection targets)
    "NC": -1,  # or "background"
    "OE": -1,
    "POROL": -1,
}
