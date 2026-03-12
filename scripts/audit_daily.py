import os
import json
import re
from datetime import datetime, timedelta

# 配置路径
WORKSPACE = "/home/yuyizhong/.openclaw/workspace"
SESSION_DIR = "/home/yuyizhong/.openclaw/agents/main/sessions/"
ERROR_FILE = os.path.join(WORKSPACE, "skills/memory-loop/ERRORS.md")
SCORE_FILE = os.path.join(WORKSPACE, "skills/memory-loop/SCOREBOARD.md")

def get_today_sessions():
    today = datetime.now().date()
    files = []
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
    # 匹配用户负面信号
    neg_pattern = re.compile(r"(不对|写错了|重做|错误|算了|不是这个意思|不行)", re.I)

    for file in session_files:
        with open(file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                data = json.loads(line)
                text = data.get("content", "")
                role = data.get("role", "")
                
                # 寻找 AI 的自省标记
                if role == "assistant":
                    matches = err_pattern.findall(text)
                    for m in matches:
                        errors.append({"id": m[0], "reason": m[1], "context": text[-100:]})
                
                # 寻找用户的负面信号（检测逃单）
                if role == "user":
                    if neg_pattern.search(text):
                        # 检查上一轮 AI 是否有打标
                        # 这里只是简化演示逻辑
                        escaped_errors.append({"user_msg": text, "context": "Pending AI self-check"})

    return errors, escaped_errors

def generate_daily_report(errors, escaped):
    report = f"# 📅 memory-loop 日报 | {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += "### 1. 结账明细\n"
    if not errors:
        report += "- 今日无记录错误。✅\n"
    for e in errors:
        report += f"- **[Err: #{e['id']}]**\n  - **简述**: {e['reason']}\n  - **修正建议**: [待 AI 补全深思熟虑建议]\n"
    
    if escaped:
        report += "\n### 2. 逃单核查 ⚠️\n"
        for ex in escaped:
            report += f"- 发现疑似漏报: \"{ex['user_msg']}\"\n"
            
    report += "\n---\n*审计脚本运行完成。请 Agent 在次日首轮对以上建议进行‘深思熟虑’补全并执行。*"
    return report

if __name__ == "__main__":
    sessions = get_today_sessions()
    errs, esc = audit_sessions(sessions)
    print(generate_daily_report(errs, esc))
