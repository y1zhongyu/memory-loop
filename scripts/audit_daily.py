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
                            errors.append({"id": m[0], "reason": m[1]})
                    if role == "user":
                        if neg_pattern.search(text):
                            escaped_errors.append({"user_msg": text[:50]})
                except:
                    continue
    return errors, escaped_errors

def generate_report():
    sessions = get_today_sessions()
    errors, escaped = audit_sessions(sessions)
    
    report = f"# 📅 memory-loop 日报 | {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    # 第一部分：错误结账
    report += "### 1. 记忆审计明细\n"
    if not errors:
        report += "- 今日无记录错误。✅\n"
    for e in errors:
        report += f"- **[Err: #{e['id']}]** - {e['reason']}\n"
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
    print(generate_report())
