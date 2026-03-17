from pathlib import Path
import sys

from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.db.session import SessionLocal, engine
from app.models.agent import Agent
from app.models.base import Base


def seed_agents(db: Session) -> None:
    mock_agents = [
        {
            "agent_id": "agent_cs_001",
            "agent_name": "客服应答助手",
            "agent_icon": "https://cdn.yunrong.tech/icons/cs.png",
            "agent_desc": "适用于售前咨询、工单回复和常见问题自动应答。",
            "category": "客服助手",
            "tags": ["热门", "推荐"],
            "status": "online",
            "use_count": 328,
            "is_hot": True,
            "jump_url": "https://ai.yunrong.tech/chat/cs",
        },
        {
            "agent_id": "agent_data_002",
            "agent_name": "经营数据分析师",
            "agent_icon": "https://cdn.yunrong.tech/icons/data.png",
            "agent_desc": "支持多维数据归因分析与日报自动解读。",
            "category": "数据分析",
            "tags": ["BI", "推荐"],
            "status": "online",
            "use_count": 214,
            "is_hot": True,
            "jump_url": "https://ai.yunrong.tech/chat/data",
        },
        {
            "agent_id": "agent_doc_003",
            "agent_name": "文档写作教练",
            "agent_icon": "https://cdn.yunrong.tech/icons/doc.png",
            "agent_desc": "帮助生成 PRD、周报、方案说明和总结文档。",
            "category": "办公提效",
            "tags": ["写作", "高频"],
            "status": "online",
            "use_count": 156,
            "is_hot": False,
            "jump_url": "https://ai.yunrong.tech/chat/doc",
        },
        {
            "agent_id": "agent_dev_004",
            "agent_name": "代码审查助手",
            "agent_icon": "https://cdn.yunrong.tech/icons/dev.png",
            "agent_desc": "用于接口设计审查、异常排查和重构建议输出。",
            "category": "研发效能",
            "tags": ["代码", "质量"],
            "status": "online",
            "use_count": 189,
            "is_hot": False,
            "jump_url": "https://ai.yunrong.tech/chat/dev",
        },
        {
            "agent_id": "agent_hr_005",
            "agent_name": "招聘面试助理",
            "agent_icon": "https://cdn.yunrong.tech/icons/hr.png",
            "agent_desc": "快速生成 JD、面试题和候选人评估模板。",
            "category": "人力资源",
            "tags": ["招聘", "模板"],
            "status": "maintenance",
            "use_count": 67,
            "is_hot": False,
            "jump_url": "https://ai.yunrong.tech/chat/hr",
        },
        {
            "agent_id": "agent_ops_006",
            "agent_name": "运营增长顾问",
            "agent_icon": "https://cdn.yunrong.tech/icons/ops.png",
            "agent_desc": "支持活动策略策划、用户分层和转化路径优化。",
            "category": "运营增长",
            "tags": ["增长", "推荐"],
            "status": "online",
            "use_count": 273,
            "is_hot": True,
            "jump_url": "https://ai.yunrong.tech/chat/ops",
        },
    ]
    for item in mock_agents:
        exists = db.query(Agent).filter(Agent.agent_id == item["agent_id"]).first()
        if exists is None:
            db.add(Agent(**item))
    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_agents(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
