import os
import re
import shutil
from datetime import datetime

# 路径定义
WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SKILL_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
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
        print(f"[Warn] 目标文件不存在: {target_path}。跳过。")
        return

    with open(template_path, 'r') as tf:
        patch_content = tf.read().strip()

    with open(target_path, 'r') as f:
        content = f.read()

    # 检查是否已存在
    marker_start = config["marker_start"]
    marker_end = config["marker_end"]
    
    pattern = re.compile(f"{re.escape(marker_start)}.*?{re.escape(marker_end)}", re.S)
    
    if pattern.search(content):
        print(f"[Info] {filename} 已存在 memory-loop 补丁，正在更新内容...")
        new_content = pattern.sub(patch_content, content)
    else:
        print(f"[Info] 正在向 {filename} 注入 memory-loop 补丁...")
        backup_file(target_path)
        
        if config["anchor"]:
            anchor_match = re.search(config["anchor"], content, re.S)
            if anchor_match:
                insert_pos = anchor_match.end()
                new_content = content[:insert_pos] + "\n" + patch_content + "\n" + content[insert_pos:]
            else:
                print(f"[Warn] 未能在 {filename} 中找到锚点。采用末尾追加模式。")
                new_content = content + "\n\n" + patch_content
        else:
            new_content = content + "\n\n" + patch_content

    with open(target_path, 'w') as f:
        f.write(new_content)
    print(f"[Success] {filename} 缝合完成。")

def main():
    print(f"=== memory-loop 自举安装程序 (v1.8.2) ===")
    print(f"工作区根目录: {WORKSPACE}")
    
    for filename, config in FILES_TO_PATCH.items():
        try:
            patch_file(filename, config)
        except Exception as e:
            print(f"[Error] 缝合 {filename} 失败: {str(e)}")

    print(f"\n[Final] 环境对齐完成。请重启 Agent 会话以激活最新的记忆审计逻辑。")

if __name__ == "__main__":
    main()
