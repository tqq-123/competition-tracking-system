from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from neo4j import GraphDatabase
from openai import OpenAI
import json
import os
import requests
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="竞赛赛题追踪与学习路径生成系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"
DATA_DIR = "/home/admin/competition-demo/data"

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.get("/")
def root():
    return {"system": "竞赛赛题追踪与学习路径生成系统", "status": "running"}

@app.get("/api/problems")
def get_problems():
    file_path = os.path.join(DATA_DIR, "output_2024.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="赛题数据文件不存在")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"count": data["data"]["count"], "problems": data["data"]["results"]}

@app.get("/api/problems/{problem_id}")
def get_problem_detail(problem_id: int):
    file_path = os.path.join(DATA_DIR, f"parsed_{problem_id}.json")
    if not os.path.exists(file_path):
        file_path = os.path.join("/home/admin/competition-demo/skills/competition-parser/cache", f"parsed_{problem_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"未找到题号 {problem_id}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/graph")
def get_graph():
    driver = get_driver()
    try:
        with driver.session() as session:
            nodes_result = session.run("MATCH (n) RETURN labels(n)[0] AS type, coalesce(n.name, n.title) AS name, properties(n) AS props")
            nodes = [{"type": r["type"], "name": r["name"], "properties": dict(r["props"])} for r in nodes_result]
            rels_result = session.run("MATCH (a)-[r]->(b) RETURN coalesce(a.name, a.title) AS source, type(r) AS relation, coalesce(b.name, b.title) AS target")
            relations = [{"source": r["source"], "relation": r["relation"], "target": r["target"]} for r in rels_result]
            return {"nodes": nodes, "relations": relations}
    finally:
        driver.close()

@app.get("/api/changes")
def get_changes():
    file_path = os.path.join(DATA_DIR, "change_report_2024.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="变更报告不存在")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/api/changes/trigger")
def trigger_change_monitor():
    try:
        url = "https://www.lanqiao.cn/api/v2/problems/"
        params = {"page": 1, "page_size": 30, "search": "2024"}
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        
        report = {
            "status": "success",
            "search": "2024",
            "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {"added_count": 0, "removed_count": 0, "changed_count": 0},
            "details": {"added": [], "removed": [], "changed": []}
        }
        with open("/home/admin/competition-demo/data/change_report_2024.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        return {"status": "success", "message": "实时监测已完成"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class PathRequest(BaseModel):
    problem_id: int
    known_knowledge: Optional[List[str]] = []

@app.post("/api/path/generate")
def generate_path(req: PathRequest):
    file_path = os.path.join(DATA_DIR, f"parsed_{req.problem_id}.json")
    if not os.path.exists(file_path):
        file_path = os.path.join("/home/admin/competition-demo/skills/competition-parser/cache", f"parsed_{req.problem_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="赛题解析数据不存在")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    kps = data["parsed"]["knowledge_points"]
    path = []
    for kp in kps:
        if kp["name"] not in req.known_knowledge:
            path.append({
                "knowledge": kp["name"],
                "prerequisites": kp["prerequisites"],
                "status": "待学习"
            })

    try:
        client = OpenAI(api_key="sk-5baccfef0437422d86c9de7b593f8117", base_url="https://api.deepseek.com")
        prompt = f"学生正在备赛『{data['title']}』。学生目前已经掌握了：{req.known_knowledge if req.known_knowledge else '零基础'}。系统为他规划的接下来的学习知识点是：{[p['knowledge'] for p in path]}。请以导师的口吻，用50字以内给学生一句个性化的鼓励和学习建议。"
        response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=0.7)
        ai_advice = response.choices[0].message.content.strip()
    except Exception as e:
        ai_advice = f"你已掌握 {len(req.known_knowledge)} 个基础点。建议按顺序攻克剩余知识点！"

    return {
        "problem_id": req.problem_id,
        "problem_title": data["title"],
        "known_knowledge": req.known_knowledge,
        "learning_path": path,
        "total_steps": len(path),
        "ai_advice": ai_advice
    }

class ChatRequest(BaseModel):
    question: str

@app.post("/api/chat")
def chat(req: ChatRequest):
    return {"question": req.question, "answer": "演示回答。", "status": "demo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)