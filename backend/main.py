from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from neo4j import GraphDatabase
import json
import os
from typing import List, Optional

app = FastAPI(title="竞赛赛题追踪与学习路径生成系统", version="1.0.0")

# 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Neo4j 连接
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 测试数据路径（你桌面上的测试数据文件夹）
DATA_DIR = r"C:\Users\田青青\Desktop\毕业设计\测试数据"


# ============ 1. 首页 ============
@app.get("/")
def root():
    return {
        "system": "竞赛赛题追踪与学习路径生成系统",
        "version": "1.0.0",
        "status": "running"
    }


# ============ 2. 赛题列表 ============
@app.get("/api/problems")
def get_problems():
    """返回抓取到的赛题列表"""
    file_path = os.path.join(DATA_DIR, "output_2024.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="赛题数据文件不存在")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "count": data["data"]["count"],
        "problems": data["data"]["results"]
    }


# ============ 3. 单道赛题详情 ============
@app.get("/api/problems/{problem_id}")
def get_problem_detail(problem_id: int):
    """返回某道赛题的解析结果"""
    file_path = os.path.join(DATA_DIR, f"parsed_{problem_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"未找到题号 {problem_id} 的解析数据")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# ============ 4. 知识图谱数据 ============
@app.get("/api/graph")
def get_graph():
    """从 Neo4j 返回知识图谱数据（节点 + 关系）"""
    driver = get_driver()
    try:
        with driver.session() as session:
            nodes_result = session.run(
                "MATCH (n) RETURN labels(n)[0] AS type, n.name AS name, properties(n) AS props"
            )
            nodes = []
            for r in nodes_result:
                nodes.append({
                    "type": r["type"],
                    "name": r["name"],
                    "properties": dict(r["props"])
                })

            rels_result = session.run(
                "MATCH (a)-[r]->(b) RETURN a.name AS source, type(r) AS relation, b.name AS target"
            )
            relations = []
            for r in rels_result:
                relations.append({
                    "source": r["source"],
                    "relation": r["relation"],
                    "target": r["target"]
                })

            return {"nodes": nodes, "relations": relations}
    finally:
        driver.close()


# ============ 5. 变更报告 ============
@app.get("/api/changes")
def get_changes():
    """返回变更监测报告"""
    file_path = os.path.join(DATA_DIR, "change_report_2024.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="变更报告不存在")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# ============ 6. 学习路径生成 ============
class PathRequest(BaseModel):
    problem_id: int
    known_knowledge: Optional[List[str]] = []

@app.post("/api/path/generate")
def generate_path(req: PathRequest):
    """根据学生已掌握的知识点，生成学习路径"""
    file_path = os.path.join(DATA_DIR, f"parsed_{req.problem_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="赛题解析数据不存在")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    kps = data["parsed"]["knowledge_points"]

    # 简单逻辑：按前置关系顺序推荐未掌握的知识点
    path = []
    for kp in kps:
        if kp["name"] not in req.known_knowledge:
            path.append({
                "knowledge": kp["name"],
                "prerequisites": kp["prerequisites"],
                "status": "待学习"
            })

    return {
        "problem_id": req.problem_id,
        "problem_title": data["title"],
        "known_knowledge": req.known_knowledge,
        "learning_path": path,
        "total_steps": len(path)
    }


# ============ 7. 智能问答 ============
class ChatRequest(BaseModel):
    question: str

@app.post("/api/chat")
def chat(req: ChatRequest):
    """简单的智能问答（演示用）"""
    return {
        "question": req.question,
        "answer": f"收到你的问题：{req.question}。智能问答模块将基于知识图谱回答，目前为演示版本。",
        "status": "demo"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)