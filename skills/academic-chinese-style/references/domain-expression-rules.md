# Domain Expression Rules

## 生物信息学

- `差异表达`: 写清比较方向、阈值、FDR、效应量和样本层级。
- `富集分析`: 区分 ORA 与 GSEA，说明背景基因集或排序依据。
- `单细胞`: 区分 cell type、cell state、cluster 和 annotation confidence。
- `通讯/轨迹`: 使用“提示”“推测”“支持某种假设”，除非有验证实验。

## 肿瘤免疫

- 细胞比例变化不等于功能增强。
- exhaustion、cytotoxicity、antigen presentation、IFN response 需要 marker 或 gene set 证据。
- ICI response 相关结论要写清 cohort、response definition 和 patient-level analysis。

## 药物化学

- docking pose、binding affinity、cell activity、ADMET 和 efficacy 分开表述。
- SAR 需要 matched analogs 和一致 assay 条件。
- 不从体外活性直接外推临床疗效。

## AI/算法

- 写清 task、input、label、split、baseline、metric、calibration 和 validation。
- 把模型解释写成 association 或 prioritization，不写成机制证明。
- 报告 failure modes，尤其是 data leakage、batch effect、class imbalance 和 domain shift。
