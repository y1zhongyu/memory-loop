import os
import json
import re
import subprocess
from datetime import datetime

# 配置路径
WORKSPACE = "/home/yuyizhong/.openclaw/workspace"
SESSION_DIR = "/home/yuyizhong/.openclaw/agents/main/sessions/"
ERROR_FILE = os.path.join(WORKSPACE, "skills/memory-loop/ERRORS.md")
SCORE_FILE = os.path.join(WORKSPACE, "skills/memory-loop/SCOREBOARD.md")
TOKEN_AUDITOR = os.path.join(WORKSPACE, "skills/memory-loop/scripts/token_auditor.py")

def get_today_sessions():
    today = datetime.now().date()
    files = []
    if not os.path.exists(SESSION_DIR):
        return []
    for f in os.listdir(SESSION_DIR):
        if f.endswith(".jsonl"):
            path = os.path.join(SESSION_DIR, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(path)).date()
            if mtime == today:
                files.append(path)
    return files

def audit_sessions(session_files):
    errors = []
    escaped_errors = []
    error_counts = {}
    
    # 匹配 [Err: #XXX (简述)]
    err_pattern = re.compile(r"\[Err:\s*#(\d+)\s*\((.*?)\)\]")
    neg_pattern = re.compile(r"(不对|写错了|重做|错误|算了|不是这个意思|不行)", re.I)

    for file in session_files:
        with open(file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    text = data.get("content", "")
                    role = data.get("role", "")
                    if role == "assistant":
                        matches = err_pattern.findall(text)
                        for m in matches:
                            err_id, reason = m
                            errors.append({"id": err_id, "reason": reason})
                            error_counts[err_id] = error_counts.get(err_id, 0) + 1
                    if role == "user":
                        if neg_pattern.search(text):
                            escaped_errors.append({"user_msg": text[:50]})
                except:
                    continue
    return errors, escaped_errors, error_counts

def generate_report():
    sessions = get_today_sessions()
    errors, escaped, error_counts = audit_sessions(sessions)
    
    report = f"# 📅 memory-loop 日报 | {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    # 第一部分：错误结账
    report += "### 1. 记忆审计明细\n"
    if not errors:
        report += "- 今日无记录错误。✅\n"
    
    # 热度检测：如果单日出现多次，提示固化建议
    consolidation_suggestions = []
    for e in errors:
        count_str = f" (今日出现 {error_counts[e['id']]} 次)" if error_counts[e['id']] > 1 else ""
        report += f"- **[Err: #{e['id']}]** - {e['reason']}{count_str}\n"
        if error_counts[e['id']] >= 2: # 设定单日阈值为 2 次
            suggestion = f"**[Err: #{e['id']}]** ({e['reason']}) 触发频次过高，建议考虑固化至 MEMORY.md。"
            if suggestion not in consolidation_suggestions:
                consolidation_suggestions.append(suggestion)
    
    if consolidation_suggestions:
        report += "\n#### 🧠 记忆新陈代谢建议 (Consolidation)\n"
        for s in consolidation_suggestions:
            report += f"- {s}\n"

    if escaped:
        report += "\n- **逃单核查 ⚠️**: 发现疑似漏报项，请 Agent 及时自检。\n"

    # 第二部分：Token 审计（调用独立脚本）
    try:
        token_report = subprocess.check_output(["python3", TOKEN_AUDITOR]).decode()
        report += "\n" + token_report
    except:
        report += "\n### 2. 算力消耗分布\n- 脚本执行异常。❌\n"

    report += "\n### 3. 沙盘状态 (DECISIONS)\n- 详见 DECISIONS.md。有 [等待转正] 项建议明日确认。\n"
    report += "\n---\n*审计脚本运行完成。请 Agent 在次日首轮对以上项进行‘深思熟虑’补全并执行。*"
    
    return report

if __name__ == "__main__":
    report = generate_report()
print(report)
log_path = "/home/yuyizhong/.openclaw/workspace/memory/audit_log.txt"
with open(log_path, "w") as f:
    f.write(report)

