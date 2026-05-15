# Bioinformatics Plot Type Atlas

Use this atlas to choose a plot family before generating R or Python code. Prefer an existing family over inventing a new one. If a plot combines multiple families, generate a multi-panel contract and keep the data table for each panel separate.

## Coverage Map

| Family | Use When | Representative Recipes |
| --- | --- | --- |
| QC and EDA | Library quality, feature counts, mapping rates, batch overview, PCA variance | `qc_multi_metric_dashboard`, `pca_variance_loadings` |
| Single-cell embedding | Cell states, batches, modalities, perturbations in low-dimensional space | `single_cell_embedding`, `perturbation_effect_embedding` |
| Single-cell summaries | Marker expression, group-level signatures, abundance, composition | `marker_signature_heatmap`, `composition_stacked_bar`, `abundance_box_violin` |
| Trajectory and dynamics | Pseudotime, branching, RNA velocity, phase portraits, gene dynamics | `pseudotime_trajectory`, `trajectory_gene_heatmap`, `rna_velocity_stream`, `phase_portrait_dynamics` |
| Spatial omics | Tissue coordinates, spatial domains, neighborhoods, ligand-receptor proximity | `spatial_feature_and_celltype_map`, `neighborhood_enrichment_heatmap`, `spatial_ligand_receptor_map` |
| Differential expression | DE table, effect size, significance, mean abundance | `volcano_differential_expression`, `ma_mean_difference` |
| Enrichment | ORA, GSEA, pathway rank, gene sets | `enrichment_bubble`, `gsea_running_score` |
| Intersections and flows | Shared genes, sample overlap, clone/state transitions, lineage flow | `upset_intersection`, `alluvial_state_flow`, `lineage_clone_fishplot` |
| Genomics and epigenomics | Variant burden, CNV, Manhattan, genome tracks, chromatin links | `clinical_genomics_oncoprint_survival`, `copy_number_profile`, `manhattan_locus_plot`, `genome_browser_track`, `circos_genomic_links`, `methylation_epigenomics_track` |
| Immune repertoire | TCR/BCR clone expansion, overlap, lineage sharing | `clonotype_overlap`, `lineage_clone_fishplot` |
| Cell communication and networks | Ligand-receptor scores, pathway networks, co-expression modules | `ligand_receptor_dotplot`, `cellchat_network`, `coexpression_network_wgcna` |
| Multi-omics integration | Factor loadings, assay concordance, modality-specific contributions | `assay_correlation_scatter`, `multiomics_factor_loading` |
| Perturbation and drug response | CRISPR screens, perturbation signatures, dose-response, synergy | `crispr_screen_rank`, `perturbation_effect_embedding`, `drug_dose_response_curve` |
| Method evaluation | Benchmark metrics, calibration, runtime, ablations, null comparisons | `method_benchmark_dot_box`, `calibration_reliability_curve` |

## Selection Rules

- Use `volcano_differential_expression` when the y-axis is significance; use `ma_mean_difference` when the x-axis is mean abundance or expression.
- Use `gsea_running_score` for a ranked gene list and running enrichment curve; use `enrichment_bubble` for summarized pathway terms.
- Use `upset_intersection` for set overlap with more than three sets; avoid Venn diagrams for dense gene-set comparisons.
- Use `alluvial_state_flow` for categorical state transitions; use `lineage_clone_fishplot` when clone prevalence changes over time.
- Use `circos_genomic_links` only when genomic coordinates or inter-chromosomal links matter. Use a network plot when coordinates are irrelevant.
- Use `genome_browser_track` for locus-level signals along genomic coordinates; use `methylation_epigenomics_track` for CpG/region-level methylation or accessibility tracks.
- Use `cellchat_network` for aggregated pathway or cell-cell communication networks; use `ligand_receptor_dotplot` for ligand-receptor pair scoring tables.
- Use `spatial_ligand_receptor_map` when the communication claim depends on tissue proximity or spatial domains.
- For final claims, avoid using cell-level points as biological replicates. Aggregate to sample, patient, clone, or perturbation replicate when the claim requires inference.

## Minimum Recipe Fields

Every recipe should define:

- `recipe_id`
- `plot_type`
- `purpose`
- `input_data.shape`
- `input_data.required_columns`
- `mappings`
- `statistics.rule`
- `statistics.missing_statistics_policy`
- `implementation.r_packages`
- `implementation.python_packages`
- `qc`
