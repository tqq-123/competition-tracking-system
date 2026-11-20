import argparse
import json
import os
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678"

def load_parsed(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_graph(driver, data):
    problem_id = data["problem_id"]
    title = data["title"]
    competition = data.get("competition", "未知竞赛")
    skills = data.get("skills", [])
    kps = data["parsed"]["knowledge_points"]
    difficulty = data["parsed"].get("difficulty", "未知")
    ptype = data["parsed"].get("problem_type", "未知")

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        session.run(
            "MERGE (c:Competition {name: $name})",
            name=competition
        )

        session.run(
            """MERGE (p:Problem {id: $id})
               SET p.name = $title, p.title = $title, p.difficulty = $difficulty, p.type = $ptype
               WITH p
               MATCH (c:Competition {name: $comp})
               MERGE (p)-[:BELONGS_TO]->(c)""",
            id=problem_id, title=title, difficulty=difficulty,
            ptype=ptype, comp=competition
        )

        for sk in skills:
            session.run(
                """MERGE (s:Skill {name: $name})
                   WITH s
                   MATCH (c:Competition {name: $comp})
                   MERGE (s)-[:RELATES_TO]->(c)""",
                name=sk, comp=competition
            )

        for kp in kps:
            session.run(
                """MERGE (k:Knowledge {name: $name})
                   WITH k
                   MATCH (p:Problem {id: $pid})
                   MERGE (p)-[:CONTAINS]->(k)""",
                name=kp["name"], pid=problem_id
            )

        for kp in kps:
            for pre in kp.get("prerequisites", []):
                session.run(
                    """MERGE (a:Knowledge {name: $pre})
                       MERGE (b:Knowledge {name: $name})
                       MERGE (a)-[:PREREQUISITE_OF]->(b)""",
                    pre=pre, name=kp["name"]
                )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    data = load_parsed(args.file)
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    try:
        build_graph(driver, data)
        print(f"[成功] 图谱构建完成：赛题 {data['title']}")

        with driver.session() as session:
            stats = session.run(
                """MATCH (c:Competition) WITH count(c) AS comp
                   MATCH (p:Problem) WITH comp, count(p) AS prob
                   MATCH (k:Knowledge) WITH comp, prob, count(k) AS kp
                   MATCH (s:Skill) WITH comp, prob, kp, count(s) AS sk
                   RETURN comp, prob, kp, sk"""
            ).single()
            print(f"竞赛节点: {stats['comp']}")
            print(f"赛题节点: {stats['prob']}")
            print(f"知识点节点: {stats['kp']}")
            print(f"技能节点: {stats['sk']}")

            print("\n知识点依赖关系：")
            rels = session.run(
                """MATCH (a:Knowledge)-[:PREREQUISITE_OF]->(b:Knowledge)
                   RETURN a.name AS from_kp, b.name AS to_kp"""
            )
            for r in rels:
                print(f"  {r['from_kp']} → {r['to_kp']}")

    finally:
        driver.close()

if __name__ == "__main__":
    main()