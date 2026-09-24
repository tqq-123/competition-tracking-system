from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== 模拟数据 ======
competitions = [
    {"id": "1", "name": "全国职业技能大赛-人工智能赛项", "status": "报名中", "deadline": "2026-10-15"},
    {"id": "2", "name": "蓝桥杯-人工智能组", "status": "已结束", "deadline": "2026-04-30"},
    {"id": "3", "name": "中国机器人大赛-智能机器人", "status": "报名中", "deadline": "2026-09-30"},
]

learning_path = {
    "stages": [
        {"name": "第一阶段：Python基础", "duration": "2周", "tasks": ["Python语法", "NumPy入门"]},
        {"name": "第二阶段：机器学习", "duration": "3周", "tasks": ["线性回归", "决策树", "SVM"]},
        {"name": "第三阶段：深度学习", "duration": "3周", "tasks": ["CNN", "PyTorch", "模型部署"]},
    ],
    "total_weeks": 8,
    "daily_hours": 2
}

knowledge_graph = {
    "nodes": [
        {"id": "Python", "type": "知识点", "level": 1},
        {"id": "NumPy", "type": "知识点", "level": 2},
        {"id": "机器学习", "type": "知识点", "level": 3},
        {"id": "深度学习", "type": "知识点", "level": 4},
        {"id": "CNN", "type": "知识点", "level": 5},
    ],
    "edges": [
        {"from": "Python", "to": "NumPy"},
        {"from": "NumPy", "to": "机器学习"},
        {"from": "机器学习", "to": "深度学习"},
        {"from": "深度学习", "to": "CNN"},
    ]
}

# ====== API接口 ======
@app.get("/")
def root():
    return {"message": "竞赛学习系统Demo", "status": "运行中"}

@app.get("/api/competitions")
def get_competitions():
    return {"code": 200, "data": competitions, "update_time": datetime.now().isoformat()}

@app.get("/api/path")
def get_path():
    return {"code": 200, "data": learning_path}

@app.get("/api/knowledge")
def get_knowledge():
    return {"code": 200, "data": knowledge_graph}

@app.get("/api/updates")
def get_updates():
    return {
        "code": 200,
        "data": [
            {"type": "赛题变更", "content": "技能大赛新增『大模型微调』赛题", "time": datetime.now().isoformat()},
            {"type": "规则更新", "content": "评分标准调整，模型准确率权重提升至40%", "time": datetime.now().isoformat()},
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)