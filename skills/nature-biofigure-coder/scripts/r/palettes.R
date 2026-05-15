# Semantic palette helpers for biomedical figures.

nature_bio_palettes <- function() {
  list(
    cell_type = c(
      T_cell = "#4E79A7",
      CD8_T_cell = "#2F5597",
      Treg = "#6A51A3",
      NK_cell = "#1B9E77",
      B_cell = "#E69F00",
      Plasma_cell = "#F28E2B",
      Myeloid = "#8C564B",
      Macrophage = "#A05A2C",
      Dendritic_cell = "#59A14F",
      Fibroblast = "#7F7F7F",
      CAF = "#6B6B6B",
      Tumor = "#B2182B",
      Epithelial = "#D62728",
      Endothelial = "#1F9AC9",
      Pericyte = "#76B7B2",
      Mast_cell = "#B07AA1"
    ),
    clinical_response = c(
      Responder = "#2C7BB6",
      Non_responder = "#D7191C",
      Stable_disease = "#FDB863",
      Progressive_disease = "#B2182B",
      Complete_response = "#1A9850",
      Partial_response = "#66BD63"
    ),
    directional = c(up = "#B2182B", down = "#2166AC", neutral = "#BDBDBD"),
    nature_accessible = c(
      Black = "#000000",
      Orange = "#E69F00",
      Sky_blue = "#56B4E9",
      Bluish_green = "#009E73",
      Yellow = "#F0E442",
      Blue = "#0072B2",
      Vermillion = "#D55E00",
      Reddish_purple = "#CC79A7"
    ),
    fluorescence_accessible = c(
      magenta = "#CC79A7",
      green = "#009E73",
      turquoise = "#56B4E9",
      white_overlap = "#FFFFFF"
    )
  )
}

scale_color_nature_bio <- function(values, ...) {
  ggplot2::scale_color_manual(values = values, ...)
}

scale_fill_nature_bio <- function(values, ...) {
  ggplot2::scale_fill_manual(values = values, ...)
}
