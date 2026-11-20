import json, os, glob
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
files = glob.glob("/home/admin/competition-demo/skills/competition-parser/cache/parsed_*.json")
print(f"找到 {len(files)} 个解析文件，准备灌入图谱...")

for f in files:
    with open(f, encoding="utf-8") as file:
        data = json.load(file)
        with driver.session() as s:
            s.run("MERGE (c:Competition {name: $name})", name=data.get("competition", "未知"))
            s.run("MERGE (p:Problem {id: $id}) SET p.title = $title", id=data["problem_id"], title=data["title"])
            s.run("MATCH (p:Problem {id: $id}), (c:Competition {name: $comp}) MERGE (p)-[:BELONGS_TO]->(c)", id=data["problem_id"], comp=data.get("competition", "未知"))
            for kp in data["parsed"]["knowledge_points"]:
                s.run("MERGE (k:Knowledge {name: $name})", name=kp["name"])
                s.run("MATCH (p:Problem {id: $id}), (k:Knowledge {name: $name}) MERGE (p)-[:CONTAINS]->(k)", id=data["problem_id"], name=kp["name"])
                for pre in kp.get("prerequisites", []):
                    s.run("MERGE (a:Knowledge {name: $pre})", pre=pre)
                    s.run("MATCH (a:Knowledge {name: $pre}), (b:Knowledge {name: $name}) MERGE (a)-[:PREREQUISITE_OF]->(b)", pre=pre, name=kp["name"])

with driver.session() as s:
    node_count = s.run("MATCH (n) RETURN count(n)").single()[0]
    rel_count = s.run("MATCH ()-[r]->() RETURN count(r)").single()[0]
    print(f"图谱构建完成！当前共 {node_count} 个节点，{rel_count} 条关系。")

driver.close()
