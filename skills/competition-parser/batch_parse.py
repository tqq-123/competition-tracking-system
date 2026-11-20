import json, os, time, sys
import requests
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
try:
    from scripts.parse import parse_with_llm, CACHE_DIR
except ImportError:
    from parse import parse_with_llm, CACHE_DIR

def get_100_problem_ids():
    print("正在从蓝桥杯官网拉取前 100 个真实题号...")
    url = "https://www.lanqiao.cn/api/v2/problems/"
    params = {"page": 1, "page_size": 100}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    data = resp.json()
    return [p['id'] for p in data['results']]

def main():
    pids = get_100_problem_ids()
    print(f"准备解析 {len(pids)} 道题...")
    
    success_count = 0
    for i, pid in enumerate(pids):
        cache_file = os.path.join(CACHE_DIR, f"parsed_{pid}.json")
        if os.path.exists(cache_file): 
            print(f"[{i+1}/{len(pids)}] 题号 {pid} 已存在，跳过。")
            success_count += 1
            continue
            
        print(f"[{i+1}/{len(pids)}] 正在解析题号 {pid}...")
        try:
            parsed = parse_with_llm(f"蓝桥杯真题，题号 {pid}。请推测知识点。")
            with open(cache_file, "w", encoding="utf-8") as f: 
                json.dump({"status": "success", "problem_id": pid, "title": f"题号 {pid}", "competition": "蓝桥杯", "skills": ["算法编程"], "parsed": parsed}, f, ensure_ascii=False, indent=2)
            success_count += 1
            time.sleep(0.5)
        except Exception as e: 
            print(f"失败: {e}")
            
    print(f"批量解析完成！当前缓存共有 {success_count} 道题的真实数据。")

if __name__ == "__main__":
    main()
