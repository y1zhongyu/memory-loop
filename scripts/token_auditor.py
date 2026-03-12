import os
import json
import re
from datetime import datetime

# 配置路径
SESSION_DIR = "/home/yuyizhong/.openclaw/agents/main/sessions/"

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

def audit_tokens(session_files):
    stats = {
        "GameAnalysis": 0,
        "SystemMaintenance": 0,
        "RoutineChat": 0,
        "Unknown": 0
    }
    total_prompt = 0
    total_completion = 0
    
    # 匹配 [TAG: BusinessName]
    tag_pattern = re.compile(r"\[TAG:\s*(\w+)\s*\]")

    for file in session_files:
        with open(file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    usage = data.get("usage", {})
                    p_tokens = usage.get("prompt_tokens", 0)
                    c_tokens = usage.get("completion_tokens", 0)
                    total_tokens = p_tokens + c_tokens
                    
                    if total_tokens == 0:
                        continue

                    total_prompt += p_tokens
                    total_completion += c_tokens
                    
                    # 尝试从内容中提取标签
                    content = data.get("content", "")
                    tags = tag_pattern.findall(content)
                    
                    if tags:
                        tag = tags[0]
                        if tag not in stats:
                            stats[tag] = 0
                        stats[tag] += total_tokens
                    else:
                        stats["Unknown"] += total_tokens
                except:
                    continue

    return stats, total_prompt, total_completion

def generate_token_report(stats, p_total, c_total):
    total = p_total + c_total
    if total == 0:
        return "### 2. 算力消耗分布\n- 今日暂无 Token 消耗数据。💰\n"

    report = "### 2. 算力消耗分布\n"
    report += f"- **今日总计**: {total:,} Tokens (Prompt: {p_total:,} / Completion: {c_total:,})\n\n"
    report += "| 业务标签 | 消耗量 | 占比 |\n"
    report += "| :--- | :--- | :--- |\n"
    
    # 按消耗量排序
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    for tag, amount in sorted_stats:
        if amount > 0:
            percentage = (amount / total) * 100
            report += f"| {tag} | {amount:,} | {percentage:.1f}% |\n"
            
    return report

if __name__ == "__main__":
    sessions = get_today_sessions()
    stats, p, c = audit_tokens(sessions)
    print(generate_token_report(stats, p, c))
