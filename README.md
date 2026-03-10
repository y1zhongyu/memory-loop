# memory-loop

> AI memory health checker and error-prevention system for OpenClaw agents.

## What is it?

Every new session, your AI agent wakes up fresh — with no memory of past mistakes. And even within a session, long conversations drift — the agent forgets what was agreed earlier and contradicts itself.

**memory-loop** fixes both: a closed-loop error system that carries lessons across sessions, and a decision anchor that keeps long conversations coherent.

## What it solves

- **Bridges the session gap** — enforces error recall before each task, so past mistakes actually carry over across sessions
- **Prevents in-session drift** — logs confirmed decisions as anchors, so long conversations don't contradict earlier agreements
- **Records errors** with actionable check steps, not vague descriptions
- **Scores agents weekly** (100pt baseline, deductions per error type)
- **Detects repeat offenses** and doubles the penalty
- **Runs weekly retrospectives** automatically via heartbeat
- **Alerts you** when an agent's score drops below 70
- **Diagnoses root causes** — whether it's a bad rule file, a vague error log, or a missing pre-task check

## File structure

```
memory-loop/
├── SKILL.md        # Setup guide & initialization flow
├── RULES.md        # Scoring rules and error boundaries
├── ERRORS.md       # Active + archived error log
├── SCOREBOARD.md   # Weekly score tracker
├── DIAGNOSIS.md    # Diagnosis report template
├── REPAIR.md       # 3-layer repair protocol
└── DECISIONS.md    # In-session decision anchor (temporary)
```

## Installation

```bash
cd ~/.openclaw/workspace/skills
git clone git@github.com:yuyizhong1128/memory-loop.git
```

Then tell your agent: *"Set up memory-loop for me."*

## Updating

When a new version is available, your agent will notify you during heartbeat. Run:

```bash
cd ~/.openclaw/workspace/skills/memory-loop
git pull
```

## Scoring system

| Score | Grade | Meaning |
|-------|-------|---------|
| 90–100 | A · Reliable | Rare mistakes, memory working |
| 70–89 | B · Acceptable | Errors present, watch for repeats |
| 50–69 | C · Needs work | Repeated errors, memory suspect |
| < 50 | F · Reset triggered | Full diagnosis required |

---

# memory-loop（中文说明）

> 专为 OpenClaw agent 设计的记忆健康检查与错误防复发系统。

## 它是什么

每次新 session，AI agent 都会失忆——不记得上次犯了什么错。而即使在同一个 session 里，长对话也会漂移——agent 忘记前面已经确认的决策，开始前后矛盾。

**memory-loop** 同时解决这两个问题：跨 session 的错误闭环，让教训真正延续；同 session 的决策锚点，让长对话保持连贯。

## 解决什么问题

- **跨 session 记忆衔接**——任务前强制读取错误记录，让过去的教训真正延续到下一次
- **同 session 上下文连贯**——关键决策实时记录为锚点，防止长对话漂移导致前后矛盾
- 用可操作的检查方式记录错误，不是模糊描述
- 每周从100分开始计分，按错误类型扣分
- 检测重复犯错，罚分翻倍
- 通过 heartbeat 自动执行周复盘
- 分数低于70时主动汇报预警
- 诊断根因：规范文件有歧义？错误描述太模糊？任务前没读记忆？

## 安装

```bash
cd ~/.openclaw/workspace/skills
git clone git@github.com:yuyizhong1128/memory-loop.git
```

然后对 agent 说：「帮我初始化 memory-loop。」

## 更新

有新版本时，agent 会在 heartbeat 时主动提醒你。更新方法：

```bash
cd ~/.openclaw/workspace/skills/memory-loop
git pull
```
