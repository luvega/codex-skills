# Minimal ggplot2 theme helpers for biomedical figures.

nature_bio_size_inches <- function(width_class = c("single", "double", "extended-data"), height = NULL) {
  width_class <- match.arg(width_class)
  width_mm <- switch(width_class, single = 89, double = 183, "extended-data" = 180)
  max_height_mm <- 170
  width_in <- width_mm / 25.4
  height_in <- if (is.null(height)) min(width_in * 0.75, max_height_mm / 25.4) else height
  if (height_in > max_height_mm / 25.4) {
    stop("Height exceeds Nature 170 mm maximum.")
  }
  c(width = width_in, height = height_in)
}

theme_nature_bio <- function(base_size = 7, base_family = "Arial") {
  if (base_size < 5 || base_size > 7) {
    warning("Nature body text should usually be 5-7 pt.")
  }
  ggplot2::theme_classic(base_size = base_size, base_family = base_family) +
    ggplot2::theme(
      axis.line = ggplot2::element_line(linewidth = 0.35, colour = "black"),
      axis.ticks = ggplot2::element_line(linewidth = 0.35, colour = "black"),
      axis.text = ggplot2::element_text(size = base_size - 1, colour = "black"),
      axis.title = ggplot2::element_text(size = base_size, colour = "black"),
      strip.background = ggplot2::element_blank(),
      strip.text = ggplot2::element_text(size = base_size, colour = "black"),
      legend.title = ggplot2::element_text(size = base_size - 1),
      legend.text = ggplot2::element_text(size = base_size - 1),
      legend.key.size = grid::unit(0.32, "cm"),
      plot.title = ggplot2::element_text(size = base_size, face = "bold", hjust = 0),
      plot.background = ggplot2::element_rect(fill = "white", colour = NA),
      panel.background = ggplot2::element_rect(fill = "white", colour = NA)
    )
}

save_nature_bio_plot <- function(plot, filename_base, width_class = c("single", "double", "extended-data"), height = NULL, dpi = 450) {
  width_class <- match.arg(width_class)
  size <- nature_bio_size_inches(width_class = width_class, height = height)
  ggplot2::ggsave(paste0(filename_base, ".pdf"), plot = plot, width = size[["width"]], height = size[["height"]], units = "in", bg = "white", device = grDevices::cairo_pdf)
  ggplot2::ggsave(paste0(filename_base, ".svg"), plot = plot, width = size[["width"]], height = size[["height"]], units = "in", bg = "white")
  ggplot2::ggsave(paste0(filename_base, ".png"), plot = plot, width = size[["width"]], height = size[["height"]], units = "in", dpi = dpi, bg = "white")
}
