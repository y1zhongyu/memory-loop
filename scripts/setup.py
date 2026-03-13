import os
import re
import shutil
import subprocess
from datetime import datetime

# 路径定义
SKILL_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
WORKSPACE = os.path.abspath(os.path.join(SKILL_ROOT, "../../"))
TEMPLATE_DIR = os.path.join(SKILL_ROOT, "templates")

FILES_TO_PATCH = {
    "AGENTS.md": {
        "template": "AGENTS_patch.md",
        "anchor": r"## Every Session\s+Before doing anything else:\s*",
        "marker_start": "<!-- [memory-loop extension start] -->",
        "marker_end": "<!-- [memory-loop extension end] -->"
    },
    "SOUL.md": {
        "template": "SOUL_patch.md",
        "anchor": None, # Append to end if anchor is None
        "marker_start": "<!-- [memory-loop rules start] -->",
        "marker_end": "<!-- [memory-loop rules end] -->"
    }
}

REQUIRED_FILES = {
    "ERRORS.md": "# 错误记录清单 (ERRORS.md)\n\n## 📌 核心准则\n同样的错误犯两次是不可接受的。发现问题模式时，必须在此处记录并在工作规范中增加物理强制约束。\n\n---\n",
    "DECISIONS.md": "# 认知沙盘 (DECISIONS.md)\n\n## 🔄 待确认推演方案\n（此处存放 Agent 提出的方案草案，等待用户授权执行）\n\n---\n",
    "SCOREBOARD.md": "# 分数看板 (SCOREBOARD.md)\n\n| 日期 | 初始分 | 扣分项 | 结余分 |\n| :--- | :--- | :--- | :--- |\n| 初始化 | 100 | 无 | 100 |\n"
}

CRON_JOBS = [
    {
        "name": "daily-audit",
        "expr": "0 20 * * *",
        "payload": "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK."
    },
    {
        "name": "weekly-audit",
        "expr": "30 10 * * 1",
        "payload": "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK."
    }
]

def backup_file(file_path):
    if os.path.exists(file_path):
        backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path
    return None

def patch_file(filename, config):
    target_path = os.path.join(WORKSPACE, filename)
    template_path = os.path.join(TEMPLATE_DIR, config["template"])
    
    if not os.path.exists(target_path):
        print(f"[-] 目标文件不存在: {target_path}。跳过缝合。")
        return

    if not os.path.exists(template_path):
        print(f"[-] 补丁模板不存在: {template_path}。跳过缝合。")
        return

    with open(template_path, 'r') as tf:
        patch_content = tf.read().strip()

    with open(target_path, 'r') as f:
        content = f.read()

    marker_start = config["marker_start"]
    marker_end = config["marker_end"]
    pattern = re.compile(f"{re.escape(marker_start)}.*?{re.escape(marker_end)}", re.S)
    
    if pattern.search(content):
        print(f"[+] {filename} 已存在 memory-loop 补丁，正在更新...")
        new_content = pattern.sub(patch_content, content)
    else:
        print(f"[+] 正在向 {filename} 注入 memory-loop 补丁...")
        backup_file(target_path)
        if config["anchor"]:
            anchor_match = re.search(config["anchor"], content, re.S)
            if anchor_match:
                insert_pos = anchor_match.end()
                new_content = content[:insert_pos] + "\n" + patch_content + "\n" + content[insert_pos:]
            else:
                new_content = content + "\n\n" + patch_content
        else:
            new_content = content + "\n\n" + patch_content

    with open(target_path, 'w') as f:
        f.write(new_content)

def check_and_create_files():
    print("\n--- 1. 基础依赖文件检查 ---")
    for filename, init_content in REQUIRED_FILES.items():
        file_path = os.path.join(SKILL_ROOT, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(init_content)
            print(f"[+] 自动创建缺失文件: {filename}")
        else:
            print(f"[√] 文件已存在: {filename}")

def check_and_register_cron():
    print("\n--- 2. 定时调度引擎 (Cron) 检查 ---")
    try:
        # 获取现有的 cron 列表
        output = subprocess.check_output(["openclaw", "cron", "list"], stderr=subprocess.STDOUT).decode('utf-8')
    except Exception as e:
        print(f"[-] 无法读取 OpenClaw Cron 列表，请手动执行注册命令。错误: {e}")
        return

    for job in CRON_JOBS:
        if job["name"] in output:
            print(f"[√] Cron 任务已存在: {job['name']}")
        else:
            print(f"[+] 正在注册缺失的 Cron 任务: {job['name']} ...")
            cmd = [
                "openclaw", "cron", "add",
                "--name", job["name"],
                "--cron", job["expr"],
                "--system-event", job["payload"]
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
                print(f"    -> 注册成功 ({job['expr']})")
            except Exception as e:
                print(f"    -> 注册失败: {e}")

def main():
    print(f"=== memory-loop 一键自检与激活程序 (v1.9.3) ===\n")
    print(f"技能目录: {SKILL_ROOT}")
    
    check_and_create_files()
    check_and_register_cron()
    
    print("\n--- 3. 灵魂契约缝合检查 ---")
    for filename, config in FILES_TO_PATCH.items():
        try:
            patch_file(filename, config)
        except Exception as e:
            print(f"[-] 处理 {filename} 时发生错误: {str(e)}")

    print(f"\n[🚀] memory-loop 记忆循环引擎已完成物理激活！")
    print(f"请发送一条消息唤醒 Agent 以加载最新环境。")

if __name__ == "__main__":
    main()
