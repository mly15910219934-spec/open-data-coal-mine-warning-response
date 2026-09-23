args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("Usage: Rscript redraw_fig3.R <output.tif> <preview.png>")

output_tif <- args[[1]]
preview_png <- args[[2]]
dir.create(dirname(output_tif), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(preview_png), recursive = TRUE, showWarnings = FALSE)
grDevices::windowsFonts(Arial = grDevices::windowsFont("Arial"))

# Figure contract:
# Core conclusion: the P-W-D-A-V-F sequence retains six ordered response-chain elements.
# Evidence logic: one box per element and directional arrows showing the closed loop.
# Archetype: schematic-led composite with a single schematic panel.
# Export: 2250 x 669 px, 300 dpi, RGB, LZW TIFF, Arial text, no internal figure title.
# Review risk: terminology drift only; no data, coding value, or sequence may change.

draw_box <- function(x0, x1, y0, y1, number, title, detail, border, fill, number_fill,
                     title_cex = 0.94, detail_cex = 0.72) {
  rect(x0, y0, x1, y1, col = fill, border = border, lwd = 1.15)
  sq_x0 <- x0 + 0.018
  sq_x1 <- x0 + 0.051
  sq_y1 <- y1 - 0.052
  sq_y0 <- sq_y1 - 0.115
  rect(sq_x0, sq_y0, sq_x1, sq_y1, col = number_fill, border = border, lwd = 0.7)
  text((sq_x0 + sq_x1) / 2, (sq_y0 + sq_y1) / 2, labels = number,
       col = "white", cex = 0.94, font = 2, family = "Arial")

  text_x <- x0 + 0.069
  title_y <- y1 - 0.105
  if (length(title) == 1) {
    text(text_x, title_y, labels = title, adj = c(0, 0.5), cex = title_cex,
         font = 2, family = "Arial", col = "black")
    detail_y <- y1 - 0.245
  } else {
    text(text_x, title_y + 0.022, labels = title[[1]], adj = c(0, 0.5), cex = title_cex,
         font = 2, family = "Arial", col = "black")
    text(text_x, title_y - 0.052, labels = title[[2]], adj = c(0, 0.5), cex = title_cex,
         font = 2, family = "Arial", col = "black")
    detail_y <- y1 - 0.275
  }
  for (i in seq_along(detail)) {
    text(text_x, detail_y - (i - 1) * 0.068, labels = detail[[i]], adj = c(0, 0.5),
         cex = detail_cex, family = "Arial", col = "black")
  }
}

draw_figure <- function() {
  par(mar = c(0, 0, 0, 0), xaxs = "i", yaxs = "i", family = "Arial")
  plot.new()
  plot.window(xlim = c(0, 1), ylim = c(0, 1), asp = NA)

  blue <- "#245781"
  green <- "#4F7C56"
  teal <- "#2B7F83"
  orange <- "#C94F16"
  pale_blue <- "#F5F8FB"
  pale_peach <- "#FAEEE9"

  boxes <- list(
    p = c(0.003, 0.278, 0.575, 0.995),
    w = c(0.365, 0.638, 0.575, 0.995),
    d = c(0.725, 0.998, 0.575, 0.995),
    f = c(0.003, 0.278, 0.005, 0.425),
    v = c(0.365, 0.638, 0.005, 0.425),
    a = c(0.725, 0.998, 0.005, 0.425)
  )

  draw_box(boxes$p[1], boxes$p[2], boxes$p[3], boxes$p[4], "1", "Perception input",
           c("sensors, video analytics,", "continuous monitoring"), blue, pale_blue, blue)
  draw_box(boxes$w[1], boxes$w[2], boxes$w[3], boxes$w[4], "2", "Warning interpretation",
           c("data fusion, risk grading,", "warning release"), green, pale_peach, orange,
           title_cex = 0.89)
  draw_box(boxes$d[1], boxes$d[2], boxes$d[3], boxes$d[4], "3", "Task dispatch",
           c("work order, responsible", "party, deadline"), teal, pale_peach, orange)
  draw_box(boxes$a[1], boxes$a[2], boxes$a[3], boxes$a[4], "4",
           c("Response or", "mitigation action"),
           c("ventilation, power cut-off,", "evacuation, equipment control"), teal, pale_peach, orange,
           title_cex = 0.82, detail_cex = 0.67)
  draw_box(boxes$v[1], boxes$v[2], boxes$v[3], boxes$v[4], "5", "Verification or closure",
           c("acceptance check, closure", "record, residual-risk check"), blue, pale_blue, blue,
           title_cex = 0.82, detail_cex = 0.68)
  draw_box(boxes$f[1], boxes$f[2], boxes$f[3], boxes$f[4], "6", "Feedback update",
           c("rule revision;", "model/workflow update"), blue, pale_blue, blue)

  arrow_col <- "#000000"
  arrows(0.278, 0.785, 0.365, 0.785, length = 0.055, angle = 28, lwd = 1.6, col = arrow_col)
  arrows(0.638, 0.785, 0.725, 0.785, length = 0.055, angle = 28, lwd = 1.6, col = arrow_col)
  arrows(0.862, 0.575, 0.862, 0.425, length = 0.055, angle = 28, lwd = 1.6, col = arrow_col)
  arrows(0.725, 0.215, 0.638, 0.215, length = 0.055, angle = 28, lwd = 1.6, col = arrow_col)
  arrows(0.365, 0.215, 0.278, 0.215, length = 0.055, angle = 28, lwd = 1.6, col = arrow_col)
  arrows(0.1405, 0.425, 0.1405, 0.575, length = 0.055, angle = 28, lwd = 1.45,
         lty = 2, col = arrow_col)
}

grDevices::tiff(output_tif, width = 2250, height = 669, units = "px", res = 300,
                compression = "lzw", type = "windows", bg = "white", pointsize = 10)
draw_figure()
dev.off()

grDevices::png(preview_png, width = 2250, height = 669, units = "px", res = 300,
               type = "windows", bg = "white", pointsize = 10)
draw_figure()
dev.off()

message("Wrote: ", output_tif)
message("Preview: ", preview_png)
