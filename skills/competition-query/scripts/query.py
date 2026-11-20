import argparse
import json
import requests
import sys

# 蓝桥杯官方 API 地址
API_URL = "https://www.lanqiao.cn/api/v2/problems/"

def fetch_problems(search=None, page=1, page_size=30):
    """调用蓝桥杯官方 API 抓取赛题"""
    params = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="搜索关键词，如 2024")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=30)
    args = parser.parse_args()

    try:
        data = fetch_problems(search=args.name, page=args.page, page_size=args.size)
        result = {
            "status": "success",
            "search": args.name,
            "page": args.page,
            "data": data
        }
    except Exception as e:
        result = {"status": "error", "message": str(e)}

    # 同时输出到屏幕和文件（UTF-8 编码，避免 Windows GBK 乱码问题）
    output_file = f"output_{args.name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n[已保存到 {output_file}]", file=sys.stderr)

if __name__ == "__main__":
    main()