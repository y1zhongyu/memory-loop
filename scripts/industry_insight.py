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
    # 这里的逻辑在实际运行时会调用 web_search 
    # 此处为脚本框架：定义搜索任务和过滤逻辑
    dimensions = ["AI", "GameIndustry", "InternetBusiness", "CultureConsumption"]
    # 模拟获取结果
    return "### 模拟内参数据\n- 暂无实时联网数据，等待 Agent 运行时填充内容。"

def main():
    state = load_state()
    now = datetime.now()
    
    # 逻辑：检查是否有断点
    if state["last_push"]:
        last_push = datetime.fromisoformat(state["last_push"])
        gap = now - last_push
        if gap > timedelta(hours=24):
            print(f"[System] 检测到断线时长: {gap.total_seconds()/3600:.1f} 小时。触发合并追溯模式。")
    
    # 模拟生成内参
    content = fetch_insights()
    
    # 存入缓冲区待 Agent 推送
    with open(BUFFER_FILE, 'w') as f:
        f.write(content)
    
    save_state(now)
    print(f"[System] {now.strftime('%Y-%m-%d %H:%M:%S')} 情报搜集完成，存入缓冲区。")

if __name__ == "__main__":
    main()
