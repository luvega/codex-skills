# Algorithm Explanation Writing

算法说明面向生物医学读者时，先讲任务，再讲模型。

段落顺序：

1. `Task`: 输入、输出、标签、预测单位和使用场景。
2. `Design`: 核心模型或统计方法，说明为何适合该任务。
3. `Evaluation`: 数据拆分、baseline、指标、消融、校准和外部验证。
4. `Interpretation`: 模型输出的生物/临床含义。
5. `Limitations`: 泄漏、偏倚、分布漂移、样本量、可解释性和部署边界。

写作规则：

- 不把 AUROC 写成临床获益。
- 不把 SHAP、attention 或特征重要性写成因果机制。
- 不用“智能”“精准”“突破性”等空泛评价替代指标。
- 所有数据集、模型名、参数、指标和 baseline 必须保持原文或用户材料一致。
