# Plot Type Dictionary

Use this as a starting vocabulary. Confirm details from the PDF text, page image, user notes, or analysis context before writing a recipe.

| Plot type | Typical data shape | Required mappings | Common statistics | R packages | Python packages |
| --- | --- | --- | --- | --- | --- |
| UMAP/t-SNE embedding | one row per cell or spot with embedding columns and metadata | x, y, color, optional facet | usually descriptive; differential tests belong in companion panels | Seurat, ggplot2, scater | scanpy, matplotlib, seaborn |
| Dot plot | long table: group, feature, mean expression, percent detected | feature, group, color, size | descriptive or group-wise test if stated | Seurat, ggplot2 | scanpy, seaborn |
| Heatmap | matrix plus row/column annotations | rows, columns, fill, annotations | clustering distance/method if stated | ComplexHeatmap, pheatmap | seaborn, matplotlib, scanpy |
| Violin/box plot | long table: sample/cell, group, value | group, value, color | Wilcoxon, t-test, paired test, mixed model only if stated | ggplot2, ggpubr, rstatix | seaborn, scipy, statannotations |
| Stacked composition bar | counts/proportions by sample/group/cell type | x, fill, y proportion | chi-square, Fisher, beta-binomial, mixed model if stated | ggplot2, scProportionTest | pandas, seaborn, statsmodels |
| Volcano plot | one row per feature with log fold change and adjusted p-value | x effect, y significance, color category | method from upstream DE table | ggplot2, EnhancedVolcano | matplotlib, seaborn, adjustText |
| Enrichment bubble plot | pathway term, score, adjusted p-value, gene count | term, score, color, size | enrichment method and correction if stated | clusterProfiler, enrichplot, ggplot2 | gseapy, matplotlib, seaborn |
| Survival curve | patient-level time, event, group | time, survival, group | log-rank, Cox model if stated | survival, survminer | lifelines |
| Forest plot | term/group, effect, lower CI, upper CI | effect, interval, label | model family if stated | forestplot, ggplot2 | matplotlib, forestplot |
| Spatial feature plot | spot/cell coordinates plus expression/module score | x, y, color, optional image underlay | descriptive unless test stated | Seurat, SpatialExperiment, ggplot2 | scanpy, squidpy, matplotlib |
| Neighborhood heatmap | pairwise cell type/state enrichment matrix | row entity, column entity, fill | permutation/enrichment method if stated | ComplexHeatmap, ggplot2 | squidpy, seaborn |
| CRISPR screen rank plot | gene-level score, rank, FDR | rank, score, label/color | MAGeCK, RSA, BAGEL if stated | ggplot2 | matplotlib, seaborn |
| QC multi-metric dashboard | one row per sample/cell/library with QC metrics | sample, metric, value, threshold | descriptive thresholds, outlier flags | ggplot2, patchwork, scater | scanpy, seaborn, matplotlib |
| PCA variance/loadings | sample/cell coordinates plus variance explained or feature loadings | PC, variance, loading, group | descriptive; PERMANOVA only if stated | stats, ggplot2, factoextra | scikit-learn, scanpy, seaborn |
| Pseudotime trajectory | cell/spot rows with embedding, pseudotime and lineage | x, y, pseudotime, lineage | lineage or GAM tests if stated | slingshot, tradeSeq, monocle3 | scanpy, scvelo, cellrank |
| RNA velocity stream | embedding coordinates plus velocity vectors | x, y, dx, dy, color | descriptive velocity confidence if stated | velocyto.R, ggplot2 | scvelo, scanpy, cellrank |
| Trajectory gene heatmap | genes by ordered cells, pseudotime or branch annotations | ordered cells, genes, fill, branch | GAM/smoother or branch DE if stated | ComplexHeatmap, tradeSeq | scanpy, seaborn |
| MA plot | one row per feature with mean abundance and log fold change | mean abundance, logFC, significance | upstream DE method | DESeq2, edgeR, ggplot2 | pydeseq2, matplotlib |
| GSEA running score | ranked gene list plus running enrichment score | rank, enrichment score, hit positions | GSEA permutation/FDR if stated | fgsea, clusterProfiler | gseapy, matplotlib |
| UpSet intersection | set membership table or binary matrix | sets, intersection size, optional category | descriptive; enrichment if stated | ComplexUpset, UpSetR | upsetplot |
| Alluvial/Sankey flow | long table of entities across categorical stages | stage, category, count/entity | descriptive transition counts | ggalluvial, networkD3 | plotly, matplotlib |
| Manhattan/locus plot | variants or genomic bins with chromosomal positions and p-values | chromosome, position, p-value | GWAS/association method if stated | qqman, ggplot2 | bioinfokit, matplotlib |
| CNV profile | genomic bins or segments with log ratio/copy number | genomic position, copy number, sample | segmentation method if stated | karyoploteR, ComplexHeatmap | cnvpytor outputs, matplotlib |
| Genome browser track | genomic intervals or signal tracks | chromosome, start, end, signal | peak/call method if stated | Gviz, karyoploteR | pyGenomeTracks, pyranges |
| Circos genomic links | genomic intervals and links | genomic coordinates, link, color | descriptive or interaction test if stated | circlize | pycirclize |
| Methylation/epigenomics track | region/CpG or peak-level signal table | genomic coordinate, methylation/accessibility value | differential methylation/accessibility if stated | Gviz, DSS, methylKit | pyGenomeTracks, seaborn |
| Ligand-receptor dot plot | ligand, receptor, sender, receiver, score | pair, sender, receiver, score, p-value | permutation or database score if stated | CellChat, NicheNet | cellphonedb outputs, liana, seaborn |
| Cell communication network | nodes are cell types/pathways, edges are interaction scores | source, target, edge weight, node group | permutation/FDR if stated | CellChat, igraph, ggraph | networkx, liana, matplotlib |
| WGCNA/co-expression network | genes/modules with adjacency or module eigengenes | node, edge, module, trait correlation | module-trait correlation if stated | WGCNA, igraph, ggraph | networkx, scipy |
| Multi-omics factor loading | factor scores/loadings across samples/features/modalities | factor, loading/score, modality, group | model-specific uncertainty if stated | MOFA2, ggplot2 | mofapy2, muon, seaborn |
| Drug dose-response curve | dose and response by sample/drug | dose, response, curve group | IC50/AUC curve model if stated | drc, ggplot2 | scipy, statsmodels, seaborn |
| Calibration/reliability curve | predicted probabilities and observed outcomes | predicted bin, observed rate, count | calibration metrics if stated | yardstick, ggplot2 | scikit-learn, matplotlib |

Always record the observation unit and feature unit. For single-cell plots, separate cell-level patterns from patient/sample-level statistics.
