import os
import json
import time
from datetime import datetime, timedelta

# 配置路径
WORKSPACE = "/home/yuyizhong/.openclaw/workspace"
INSIGHT_DIR = os.path.join(WORKSPACE, "memory/insights")
STATE_FILE = os.path.join(INSIGHT_DIR, "state.json")
BUFFER_FILE = os.path.join(INSIGHT_DIR, "pending_push.md")

os.makedirs(INSIGHT_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_push": None}

def save_state(last_push):
    with open(STATE_FILE, 'w') as f:
        json.dump({"last_push": last_push.isoformat()}, f)

def fetch_insights():
    # 改为指令触发模式，由 Agent 本身在读取此文件后，调用自身的真实联网搜索工具
    now_str = datetime.now().strftime('%Y-%m-%d')
    return f"""# 🌐 今日全域情报采集任务 ({now_str})

[System Task] 请立即调用你的联网搜索工具（优先 minimax-web-search，备用 search），完成今日的早报采集与推送：

### 搜索方向：
1. **AI 行业最新动态**（核心大模型发布、AI商业化落地等）
2. **游戏行业最新动态**（版号、重磅游戏发售、大厂动向等）

### 执行要求：
1. 提取 3-5 条今天最有战略价值的新闻。
2. 进行“CEO 视角翻译”：每条新闻附带一句针对一中（游戏公司CEO）的业务启示或潜在影响。
3. 整理排版后，直接在当前会话中推送给一中。
"""

def main():
    state = load_state()
    now = datetime.now()
    
    # 模拟生成内参触发指令
    content = fetch_insights()
    
    # 存入缓冲区待 Agent 醒来后推送
    with open(BUFFER_FILE, 'w') as f:
        f.write(content)
    
    save_state(now)
    print(f"[System] {now.strftime('%Y-%m-%d %H:%M:%S')} 触发指令生成完成，等待 Agent 执行真实搜索。")

if __name__ == "__main__":
    main()
