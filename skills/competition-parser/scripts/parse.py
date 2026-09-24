import argparse
import json
import os
from openai import OpenAI

API_KEY = "sk-5baccfef0437422d86c9de7b593f8117"   # ← 换成你自己的
BASE_URL = "https://api.deepseek.com"

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(problem_id):
    return os.path.join(CACHE_DIR, f"parsed_{problem_id}.json")

def parse_with_llm(problem_text):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = f"""你是一个竞赛赛题分析专家。请分析下面的赛题，提取知识点、知识点前置关系、难度和题型。

赛题内容：
{problem_text}

请严格按以下 JSON 格式返回，不要有任何其他内容：
{{
  "knowledge_points": [
    {{"name": "知识点名称", "prerequisites": ["前置知识点1", "前置知识点2"]}},
    {{"name": "另一个知识点", "prerequisites": []}}
  ],
  "difficulty": "入门/简单/中等/困难",
  "problem_type": "算法题/模拟题/数学题/图论题"
}}

说明：
- prerequisites 表示学习该知识点前必须先掌握的知识点
- 如果没有前置知识点，prerequisites 为空数组
- 知识点名称用简洁的中文，如"字符串遍历"、"动态规划"、"哈希表" """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        problem = json.load(f)

    problem_id = problem.get("id", "unknown")
    cache_path = get_cache_path(problem_id)

    if not args.no_cache and os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            result = json.load(f)
        result["source"] = "cache"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    problem_text = f"""
标题：{problem.get('title', '')}
所属竞赛：{problem.get('competition', '')}
组别：{problem.get('category', '')}
年份：{problem.get('year', '')}
级别：{problem.get('level', '')}
对应技能：{', '.join(problem.get('skills', []))}
描述：{problem.get('description', '')}
输入格式：{problem.get('input_format', '')}
输出格式：{problem.get('output_format', '')}
数据范围：{problem.get('data_range', '')}
"""

    try:
        parsed = parse_with_llm(problem_text)
        result = {
            "status": "success",
            "problem_id": problem_id,
            "title": problem.get("title", ""),
            "competition": problem.get("competition", ""),
            "skills": problem.get("skills", []),
            "parsed": parsed,
            "source": "llm"
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        result = {"status": "error", "message": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()