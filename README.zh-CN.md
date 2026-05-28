<div align="center">

# incoherence-aware-control

**能否用"答案不稳定性"作为信号,把测试时计算分配得更聪明一些**

![Status](https://img.shields.io/badge/status-dormant-lightgrey)
![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)
![Closure](https://img.shields.io/badge/closure-2026--03-blue)

[한국어](./README.md) · [English](./README.md#english) · **中文**

</div>

> 🧊 **休眠中的研究试点。**

## 这项研究想看什么

在选择题推理基准(如 GPQA、MMLU)上,当给模型一份固定额度的"思考时间(测试时计算)"时,能不能造一个比"均匀分配"更聪明的控制器,把这份预算分配得更合理?

核心想法很朴素:

- 让模型对同一道题独立尝试多次。
- 用一个叫 **"不稳定性(incoherence)"** 的量来衡量答案在多次尝试间摆动的程度。
- 根据这个不稳定性信号,把更多计算花在看起来更"摇摆"的题目上。

出发假设是:这样做应该能在同等预算下,**同时**改善准确率和答案稳定性。

## 发现了什么

经过若干轮迭代,结论逐步收窄。直到关闭时,最诚实的描述是这样的:

- **控制器本身确有效果。** 在预算足够大的区间里,无论是准确率还是稳定性,都比"均匀分配"的对照更好。
- **但效果取决于预算大小。** 预算较小时,稳定性提升了,但准确率反而可能下降。也就是说:"满足条件时赢",不是"任何情况都赢"。
- **没有干净地战胜"最强的简单 baseline"。** 单纯地"问 N 次、按多数投票"的方法出乎意料地强,我们没能干净地把控制器自身的额外收益从这个强基线中分离出来。

完整数字可在以下两份关闭报告中查阅:

- 🇰🇷 [`closure_reports/project_closure_report_ko_20260327.md`](closure_reports/project_closure_report_ko_20260327.md)
- 🇬🇧 [`closure_reports/project_closure_report_20260327.md`](closure_reports/project_closure_report_20260327.md)

## 为什么暂停

最初的野心是"这种控制器总是更好"。经过几轮迭代后,这个主张被收窄为"在某些预算区间下更好"。这个更窄的结论本身仍有价值,但比起立刻继续追加投入,把它暂时封存,等到出现新的契机(不同的数据集、新的控制器家族、对强基线更彻底的拆解)再唤醒,更加自然。

## 重启时先看哪里

- 📖 [`GLOSSARY.md`](GLOSSARY.md) —— 把代码与关闭报告里出现的内部术语(`incoherence`、`spend sweep`、`hard_cap`、`ours_controller_v3_nofallback`、`T*`、splitA/B 等)翻成日常用语的对照表
- [`docs/HANDOVER_MASTER.md`](docs/HANDOVER_MASTER.md) —— 一次性看完整项目脉络
- [`docs/EXPERIMENT_TIMELINE.md`](docs/EXPERIMENT_TIMELINE.md) —— 各轮做了什么改动
- [`docs/ARTIFACT_INDEX.md`](docs/ARTIFACT_INDEX.md) —— 哪个产物在哪儿
- [`docs/REPRODUCTION_GUIDE.md`](docs/REPRODUCTION_GUIDE.md) —— 怎样重新跑
- [`docs/NEXT_STEPS_CHECKLIST.md`](docs/NEXT_STEPS_CHECKLIST.md) —— 候选的下一步

## 代码地图

| 文件 | 做什么 |
|---|---|
| [`src/run_pilot.py`](src/run_pilot.py) | 真正跑实验的主运行器 |
| [`src/methods.py`](src/methods.py) | 用于对照的 baseline 们与我们这一侧的控制器实现 |
| [`src/parser.py`](src/parser.py) | 把模型答案抽取成规范格式的解析器 |
| [`src/token_meter.py`](src/token_meter.py) | 用统一口径统计每题花了多少 token 的会计 |
| [`src/analyze_hotmess_style.py`](src/analyze_hotmess_style.py) | 不稳定性(incoherence)等诊断指标的计算 |
| [`src/report_spend_sweep.py`](src/report_spend_sweep.py) | 跨预算对比结果,整理成表格与报告 |

## 目录概览

```
.
├── src/                实验代码
├── configs/            各轮实验配置
├── scripts/            流水线运行脚本
├── tests/              回归 / smoke 测试
├── reports/            各轮报告与预注册(prereg)资料
├── docs/               全局交接文档
├── selected_runs/      各轮关键 run 的摘要
├── closure_reports/    关闭报告(韩文 / 英文)
└── GLOSSARY.md         内部术语词典
```

## 环境

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -U -r requirements.txt
export HF_TOKEN=...   # 仅在需要时
```

## 状态

🧊 **休眠中** —— 主动开发已停,但仍可随时唤醒。

## 许可证

以 [CC BY-NC 4.0](./LICENSE) 发布。
