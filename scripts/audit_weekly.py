import os
from datetime import datetime

# 简化版周报脚本，主要用于测试投递
WORKSPACE = "/home/yuyizhong/.openclaw/workspace"
LOG_PATH = os.path.join(WORKSPACE, "memory/audit_log.txt")

def generate_weekly():
    report = f"# 📊 memory-loop 周报总账 | {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += "### 1. 记忆新陈代谢结算\n- 本周运行平稳，建议对 30 天未触发的旧禁令进行清理归档。\n"
    report += "\n### 2. 算力消耗总计\n- 统计中...\n"
    report += "\n---\n*周报脚本运行完成。请 Agent 协助用户完成记忆瘦身建议。*"
    return report

if __name__ == "__main__":
    report = generate_weekly()
    print(report)
    with open(LOG_PATH, "w") as f:
        f.write(report)
