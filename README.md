# memory-loop: AI Memory Health & Dynamic Self-Healing System
[中文介绍](#中文介绍) | English Introduction

> **The strictest memory and execution manager in the OpenClaw ecosystem.**
> It doesn't just log your requirements; it diagnoses *why* the AI "knows but fails to execute," and enforces a physical self-healing mechanism.

## Why memory-loop?
Even with a 200K context window, AI models inevitably suffer from **early-context amnesia, implicit rule negligence, and repeating the same mistakes**.
`memory-loop` tackles three fatal pain points in long-term, complex AI tasks:
1. **Context Drift**: Mid-conversation, the AI forgets the template or rules you set initially.
2. **Incorrigibility**: You point out a mistake, the AI apologizes sincerely, but makes the exact same error later.
3. **Alert Fatigue**: When errors pile up, legacy systems repeatedly bombard you with the same old error logs.

## Core Features (v1.5.0 New Architecture)

### 1. 🚦 Dynamic Health Alerts & Soft Interruption
- **SCOREBOARD**: Quantifies each Agent's execution capability on a 100-point scale. Any skipped step, rule violation, or omission results in immediate point deduction.
- **Anti-Fatigue Alerts**: Triggers a warning when the score drops below 70. **Core Optimization: Alerts fire ONLY on score changes, pushing ONLY "newly added errors" since the last alert.** It never digs up old accounts and remains absolutely silent when the score is stable.
- **Soft Interruption (Anti-OOC)**: At <60 points, the AI requests a work pause to self-heal. It strictly uses its defined persona (via `SOUL.md`) to avoid breaking character (Out Of Character), and **leaves the ultimate decision ("fix now" or "keep working") entirely to the user.**

### 2. 🗂️ Cross-Session Task Cache (DECISIONS)
- **Refusing Context Wipes**: `DECISIONS.md` is no longer a burn-after-reading temp file. It acts as a state anchor throughout the project's lifecycle.
- **Active/Dormant Dual Zones**: Active rules and templates are kept in the `[Active Zone]`; once a phase is complete, they retire to the `[Dormant Zone]`.
- **Forced Physical Reads**: Before generating multi-line structured content or executing high-risk operations, the AI **must** read the Active Zone. This trades a tiny token footprint for 100% format and process fidelity.

### 3. 🛠️ Deep Diagnosis & Recovery System (DIAGNOSIS & REPAIR)
- **Finding the Root Cause**: Uses `DIAGNOSIS` to analyze why an error repeats (Ambiguous rules? Ineffective prompts? Or just rushing the execution?).
- **Hard Surgery**: Executes the `REPAIR` workflow to modify core files like `SOUL.md`, turning "promises to improve" into physical constraints.
- **Wounded Recovery (Cap at 80 pts)**: Eliminates meaningless "daily self-assessed bonus points." After a true root-cause repair, the AI's score recovers to a **maximum of 80 points**—offering a chance at redemption while keeping the system highly sensitive to subsequent errors.
- **Weekly True Reckoning**: Weekly reports display not just the final score, but the **total raw points deducted that week**, exposing the true severity of the AI's "illness."

---

## 中文介绍

# memory-loop：AI 记忆健康评估与动态自愈系统

> **OpenClaw 生态最严苛的 AI 记忆与执行力管家。**
> 不仅仅是记下你的需求，更能诊断 AI 为什么总是"记住了但做不到"，并建立强制自愈机制。

## 为什么你需要 memory-loop？
哪怕你拥有 200K 的上下文，AI 依然会**遗忘早期细节、忽视隐性规则、重蹈覆辙**。
`memory-loop` 专注解决大模型在长线复杂任务中的三个致命痛点：
1. **上下文漂移**：聊着聊着，AI 就忘了你最初定的模板和规则。
2. **屡教不改**：你指出了错误，AI 认错态度极好，但下次还敢。
3. **报警疲劳**：错误一多，系统就会无脑翻旧账，把你烦死。

## 核心特性 (v1.5.0 全新架构)

### 1. 🚦 动态健康预警与阻断机制
- **计分板（SCOREBOARD）**：以 100 分制量化每个 Agent 的执行力。只要跳步、违规、遗漏，立刻扣分。
- **不打扰预警（防疲劳）**：分数跌破 70 分时触发预警。**核心优化：分数变动才推送，每次只推"新增错误"，绝不翻旧账**，分数稳定时保持绝对静默。
- **柔性阻断（防 OOC）**：跌破 60 分时，AI 会用符合自身人设的语气（严格遵循 SOUL.md，拒绝 OOC）请求暂停工作进行自愈，但**把最终决定权交给用户**（"现在修" 或 "先干活"）。

### 2. 🗂️ 跨 Session 任务缓存 (DECISIONS)
- **拒绝上下文清空**：`DECISIONS.md` 不再是阅后即焚的临时文件，而是伴随整个项目生命周期的状态锚点。
- **活跃/休眠双区管理**：当前讨论的模板与规则存放在**活跃区**；阶段性完成后退居**休眠区**。
- **物理强制读取**：AI 在生成任何多行结构化内容或执行高危操作前，**必须强制读取活跃区**。这用极低的 Token 消耗，换取了 100% 的格式与流程保真。

### 3. 🛠️ 深度诊断与回血系统 (DIAGNOSIS & REPAIR)
- **找病灶，不看表象**：通过 `DIAGNOSIS` 分析重复犯错的根因（是规范歧义？是提示词失效？还是管不住手？）。
- **硬性手术**：执行 `REPAIR` 流程修改底层的 `SOUL.md` 或核心模板，将"改正承诺"变成物理约束。
- **带伤回血（上限 80 分）**：取消无意义的"日常自评加分"。完成真正的底层修复后，AI 分数最高恢复至 80 分——既给予重生的机会，又保留对再次犯错的高敏感度。
- **周报算总账**：每周末自动生成复盘报告，不仅看最终得分，更展示**本周原始总扣分**，让病情无处遁形。

## 适用场景 / Use Cases
- **长线开发任务 / Long-term Development**：多个代码文件的来回修改，防止架构设定被遗忘。
- **标准化内容生成 / Standardized Content Gen**：如研报撰写、排版输出，保证每一份结果都死死咬住你的定制模板。
- **Agent 调教期 / Agent Tuning Phase**：帮你快速锁定 AI 的认知盲区，并用物理手段打补丁。