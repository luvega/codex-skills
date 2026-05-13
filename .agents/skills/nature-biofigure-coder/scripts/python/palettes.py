"""Semantic palette helpers for biomedical figures."""

CELL_TYPE = {
    "T_cell": "#4E79A7",
    "CD8_T_cell": "#2F5597",
    "Treg": "#6A51A3",
    "NK_cell": "#1B9E77",
    "B_cell": "#E69F00",
    "Plasma_cell": "#F28E2B",
    "Myeloid": "#8C564B",
    "Macrophage": "#A05A2C",
    "Dendritic_cell": "#59A14F",
    "Fibroblast": "#7F7F7F",
    "CAF": "#6B6B6B",
    "Tumor": "#B2182B",
    "Epithelial": "#D62728",
    "Endothelial": "#1F9AC9",
    "Pericyte": "#76B7B2",
    "Mast_cell": "#B07AA1",
}

CLINICAL_RESPONSE = {
    "Responder": "#2C7BB6",
    "Non_responder": "#D7191C",
    "Stable_disease": "#FDB863",
    "Progressive_disease": "#B2182B",
    "Complete_response": "#1A9850",
    "Partial_response": "#66BD63",
}

DIRECTIONAL = {
    "up": "#B2182B",
    "down": "#2166AC",
    "neutral": "#BDBDBD",
}

CATEGORICAL_FALLBACK = [
    "#4E79A7",
    "#F28E2B",
    "#59A14F",
    "#E15759",
    "#76B7B2",
    "#EDC948",
    "#B07AA1",
    "#9C755F",
    "#BAB0AC",
]

NATURE_ACCESSIBLE = {
    "Black": "#000000",
    "Orange": "#E69F00",
    "Sky_blue": "#56B4E9",
    "Bluish_green": "#009E73",
    "Yellow": "#F0E442",
    "Blue": "#0072B2",
    "Vermillion": "#D55E00",
    "Reddish_purple": "#CC79A7",
}

FLUORESCENCE_ACCESSIBLE = {
    "magenta": "#CC79A7",
    "green": "#009E73",
    "turquoise": "#56B4E9",
    "white_overlap": "#FFFFFF",
}


def palette(name: str) -> dict[str, str] | list[str]:
    palettes = {
        "cell_type": CELL_TYPE,
        "clinical_response": CLINICAL_RESPONSE,
        "directional": DIRECTIONAL,
        "categorical_fallback": CATEGORICAL_FALLBACK,
        "nature_accessible": NATURE_ACCESSIBLE,
        "fluorescence_accessible": FLUORESCENCE_ACCESSIBLE,
    }
    if name not in palettes:
        raise KeyError(f"Unknown palette: {name}")
    return palettes[name]
