import os
import re
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from secret_keys import openaiapi_key
#from langchain.chat_models import init_chat_model
from langchain_classic.chat_models import init_chat_model
import warnings
warnings.filterwarnings('ignore')
os.environ['OPENAI_API_KEY'] = openaiapi_key
llm = init_chat_model("openai:gpt-4.1")
db = SQLDatabase.from_uri("sqlite:///retail_database.db")
SCHEMA = db.get_table_info()
# print(SCHEMA)
# Avoid any DML/DDL
DENY_RE = re.compile(r"\b(INSERT|UPDATE|DELETE|ALTER|DROP|CREATE|REPLACE|TRUNCATE)\b", re.I)
#Limit output rows
HAS_LIMIT_TAIL_RE = re.compile(r"(?is)\blimit\b\s+\d+(\s*,\s*\d+)?\s*;?\s*$")

# This function ensure only one SELECT is issued at a time. Multiple statements are not allowed
def safe_sql(q:str) -> str:
    q = q.strip()
    if q.count(";") > 1 or (q.endswith(';') and ";" in q[:-1]):
        return "Error:Multiple statements are not allowed"
    q = q.strip(";").strip()
    if not q.lower().startswith("select"):
        return "Error: Only SELECT statements are allowed"
    if DENY_RE.search(q):
        return "Error:DML/DDL detected. Only read-only queries are allowed"
    if not HAS_LIMIT_TAIL_RE.search(q):
        q += " LIMIT 5"
    return q

@tool
def execute_query(query: str) -> str:
    """Execute a READ-ONLY SQLite SELECT query and return results."""
    query = safe_sql(query)
    q = query
    if q.startswith("Error"):
        return q
    try:
        return db.run(q)
    except Exception as e:
        return f'Error:{e}'

SYSTEM = f"""You are a careful SQLite analyst.

Authoritative schema (do not invent columns/tables):{SCHEMA}

Rules:
- Think step-by-step.
- When you need data, call the tool `execute_sql` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Limit to 5 rows unless user explicitly asks otherwise.
- If the tool returns 'Error:', revise the SQL and try again.
- Limit the number of attempts to 5.
- If you are not successful after 5 attempts, return a note to the user.
- Prefer explicit column lists; avoid SELECT *.
"""

#from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_core.messages import SystemMessage
#from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.agents import AgentExecutor

def agent_function(input: str):
    agent = create_sql_agent(
        llm = llm,
        tools=[execute_query],
        system_prompt=SystemMessage(content=SYSTEM),
        #verbose=True,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    return agent.run(input)


