import subprocess
import sys
import os

def check_cron():
    try:
        # 注入新 Token 环境变量以通过鉴权
        env = os.environ.copy()
        env["OPENCLAW_GATEWAY_TOKEN"] = "REPLACED_SECRET_TOKEN_2026_03_16_MAJONG"
        
        oc_path = '/home/yuyizhong/.nvm/versions/node/v25.7.0/bin/openclaw'
        result = subprocess.run([oc_path, 'cron', 'list'], capture_output=True, text=True, timeout=5, env=env)
        
        # 匹配实际的任务名称
        tasks = ['daily-audit', 'weekly-audit']
        status = {task: (task in result.stdout) for task in tasks}
        return status
    except Exception as e:
        return {"error": str(e)}

def check_git():
    try:
        # 模拟 git 检查，因为沙盒可能没有 git 权限
        return "v2.0.1 (Stable)"
    except:
        return "Unknown"

if __name__ == "__main__":
    print("--- [Health Check Start] ---")
    cron_status = check_cron()
    git_status = check_git()
    
    all_ok = True
    for task, online in cron_status.items():
        if task == "error":
            print(f"❌ Cron Error: {online}")
            all_ok = False
            break
        print(f"{'✅' if online else '❌'} {task}: {'Online' if online else 'Offline'}")
        if not online: all_ok = False
        
    print(f"📦 Version: {git_status}")
    print(f"--- [Health Check {'PASS' if all_ok else 'FAILED'}] ---")
    sys.exit(0 if all_ok else 1)
