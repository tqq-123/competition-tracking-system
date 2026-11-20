import subprocess
import sys

def run_step(name, cmd):
    print(f"\n[{name}] 启动...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[{name}] ✅ 完成")
    else:
        print(f"[{name}] ❌ 失败")
        print(result.stderr)
        sys.exit(1)

def main():
    print("="*50)
    print("🤖 OpenClaw 多智能体流水线调度")
    print("="*50)
    
    # 1. 抓取
    run_step("数据采集 Agent", "cd skills/competition-query && python3 scripts/query.py --name '2024'")
    # 2. 解析
    run_step("赛题解析 Agent", "cd skills/competition-parser && python3 batch_parse.py")
    # 3. 灌图
    run_step("知识图谱 Agent", "cd skills/knowledge-graph && python3 batch_build.py")
    
    print("\n✅ 三大智能体协同工作完成，系统数据链路已闭环。")

if __name__ == "__main__":
    main()
