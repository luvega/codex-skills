# Results And Discussion Interpretation

结果讨论采用四步：

1. `观察`: 图表、统计、模型或实验看到什么。
2. `解释`: 在当前设计下最保守的含义是什么。
3. `边界`: 混杂、替代解释、样本或方法限制是什么。
4. `验证`: 需要什么补充分析、实验或外部队列。

规则：

- 结果段先写观察，讨论段再写机制或意义。
- 关联结果不能写成因果机制。
- 单一队列不能写成普遍规律。
- 模型性能不能直接写成临床可用。
- 富集、通讯、轨迹、docking、SHAP 等结果默认是解释线索，除非有独立验证。

若已有 JSON 卡片，先运行：

```powershell
python scripts\check_research_interpretation_card.py path\to\card.json
```
