# R and Python Package Map

| Plot family | R packages | Python packages | Notes |
| --- | --- | --- | --- |
| UMAP/t-SNE embedding | Seurat, ggplot2, scater | scanpy, matplotlib, seaborn | Keep descriptive visualization separate from patient-level tests. |
| Dot plot | Seurat, ggplot2 | scanpy, seaborn, matplotlib | Requires mean/score and percent-detected or fraction columns. |
| Heatmap | ComplexHeatmap, circlize, pheatmap | seaborn, matplotlib, scanpy | Record scaling, clustering, and annotation rules. |
| Violin/box/jitter | ggplot2, ggpubr, rstatix | seaborn, scipy, statannotations | Use sample-level values for biological inference when applicable. |
| Stacked composition bar | ggplot2, dplyr, tidyr | pandas, seaborn, matplotlib | Record denominator and normalization rule. |
| Volcano | ggplot2, ggrepel, EnhancedVolcano | pandas, matplotlib, seaborn, adjustText | Upstream DE method should come from input table. |
| Enrichment | clusterProfiler, enrichplot, ggplot2 | gseapy, pandas, matplotlib, seaborn | Record gene universe and correction if known. |
| Survival | survival, survminer | lifelines, matplotlib | Requires time, event, and group columns. |
| Forest plot | ggplot2, forestplot | matplotlib, forestplot | Requires effect, lower CI, upper CI, and label columns. |
| Spatial expression | Seurat, SpatialExperiment, ggplot2 | scanpy, squidpy, matplotlib | Record coordinate system and image background use. |
| TCR/BCR clonotype | immunarch, scRepertoire, ggplot2 | scirpy, pandas, seaborn | Record clone definition and repertoire metric. |
| CRISPR screen | ggplot2, ggrepel | pandas, matplotlib, seaborn | Record score direction and FDR threshold. |
| Drug response | ggplot2, drc | pandas, scipy, seaborn | Record dose unit, response metric, and curve model. |
| QC dashboard | ggplot2, patchwork, scater, MultiQC outputs | pandas, seaborn, scanpy, matplotlib | Keep thresholds and exclusion rules explicit. |
| PCA/loadings | stats, ggplot2, factoextra | scikit-learn, scanpy, seaborn | Record scaling, variance explained and feature-loading sign. |
| Pseudotime trajectory | slingshot, tradeSeq, monocle3, ggplot2 | scanpy, scvelo, cellrank, seaborn | Record root state and lineage assignment rule. |
| RNA velocity | velocyto.R, ggplot2 | scvelo, scanpy, cellrank | Record velocity layer and confidence/latent-time source. |
| Trajectory heatmap | ComplexHeatmap, tradeSeq, monocle3 | scanpy, seaborn, scipy | Record ordering, branch and smoothing model. |
| MA plot | DESeq2, edgeR, ggplot2, ggrepel | pydeseq2, pandas, matplotlib | Use upstream DE table; do not recompute silently. |
| GSEA running score | fgsea, clusterProfiler, ggplot2 | gseapy, matplotlib | Record ranked list, gene-set database and FDR. |
| UpSet/intersections | ComplexUpset, UpSetR | upsetplot, pandas, matplotlib | Prefer over Venn for more than three sets. |
| Alluvial/Sankey | ggalluvial, networkD3, ggplot2 | plotly, matplotlib, pandas | Record denominator and transition identity. |
| Manhattan/locus | qqman, ggplot2, ggrepel | bioinfokit, pandas, matplotlib | Record genome build and association method. |
| CNV profile | karyoploteR, ComplexHeatmap, ggplot2 | cnvpytor outputs, pandas, matplotlib | Record segmentation and chromosome ordering. |
| Genome browser track | Gviz, karyoploteR, rtracklayer | pyGenomeTracks, pyranges | Record genome build, track scale and interval source. |
| Circos links | circlize, ComplexHeatmap | pycirclize, pandas | Use only when genomic coordinates matter. |
| Methylation/epigenomics | methylKit, DSS, Gviz, ggplot2 | pyGenomeTracks, pyranges, seaborn | Record CpG/region definition and differential method. |
| Ligand-receptor dot plot | CellChat, NicheNet, ggplot2 | liana, cellphonedb outputs, seaborn | Record sender, receiver, database and scoring method. |
| Communication network | CellChat, igraph, ggraph | networkx, liana, matplotlib | Record edge threshold and FDR if available. |
| WGCNA/network | WGCNA, igraph, ggraph | networkx, scipy, pandas | Record adjacency, module detection and trait correlation. |
| Multi-omics factors | MOFA2, ggplot2, ComplexHeatmap | mofapy2, muon, seaborn | Record modality, factor orientation and normalization. |
| Perturbation embedding | Seurat, ggplot2, scater | scanpy, scvi-tools outputs, seaborn | Separate visual embedding from replicate-level inference. |
| Calibration curve | yardstick, ggplot2 | scikit-learn, matplotlib | Record binning rule, metric and outcome definition. |
