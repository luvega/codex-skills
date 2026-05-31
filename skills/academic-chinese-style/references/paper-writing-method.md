# Method Writing Guide

方法部分的目标是可复现，而不是宣传。默认顺序：

1. Study design / data source.
2. Samples, cohorts, inclusion and exclusion criteria.
3. Preprocessing and quality control.
4. Core model, algorithm, or analysis workflow.
5. Statistical tests and multiple-testing correction.
6. Software versions, parameters, and random seeds when available.
7. Ethics, data availability, or code availability if relevant.

规则：

- 不写“常规方法”“标准流程”等空话，除非后面给出具体参数或引用。
- 不把方法优势写成未经验证的结果。
- 对不可复现的信息标记 `needs evidence` 或 `需作者确认`。
- 生信流程要保留输入、输出、关键参数和版本边界。
