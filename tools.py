import datetime
import random

def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"結果：{result}"
    except Exception as e:
        return f"計算錯誤：{e}"

def get_weather(city: str) -> str:
    temperatures = {"台北": 28, "台中": 30, "高雄": 32, "花蓮": 27}
    temp = temperatures.get(city, random.randint(20, 35))
    return f"{city} 目前氣溫 {temp}°C，天氣晴朗"

def search(query: str) -> str:
    results = {
        "react": "ReAct (Reasoning + Acting) 是一種讓 LLM 交替思考與行動的提示框架。",
        "agent": "AI Agent 是能自主感知環境、制定計畫並執行工具的智能系統。",
        "python": "Python 是一種廣泛用於 AI/ML 開發的高階程式語言。",
    }
    for kw, answer in results.items():
        if kw in query.lower():
            return answer
    return f"關於「{query}」的搜尋結果：(模擬) 暫無相關資料"

def get_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_time(timezone: str = "local") -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

TOOL_REGISTRY = {
    "calculator": {
        "fn": calculator,
        "description": "計算數學表達式，例如 '2 + 3 * 4'",
        "parameters": {"expression": "要計算的數學表達式字串"},
    },
    "get_weather": {
        "fn": get_weather,
        "description": "查詢指定城市的天氣",
        "parameters": {"city": "城市名稱（如 台北、台中）"},
    },
    "search": {
        "fn": search,
        "description": "搜尋知識庫中的資訊",
        "parameters": {"query": "搜尋關鍵字"},
    },
    "get_date": {
        "fn": get_date,
        "description": "取得目前日期與時間",
        "parameters": {},
    },
}

def get_tool_descriptions() -> str:
    lines = []
    for name, info in TOOL_REGISTRY.items():
        params = ", ".join(f"{k}: {v}" for k, v in info["parameters"].items())
        lines.append(f"- {name}: {info['description']} | 參數: {params}")
    return "\n".join(lines)

def run_tool(name: str, **kwargs) -> str:
    tool = TOOL_REGISTRY.get(name)
    if not tool:
        return f"錯誤：找不到工具 '{name}'"
    try:
        return tool["fn"](**kwargs)
    except TypeError as e:
        return f"參數錯誤：{e}"
    except Exception as e:
        return f"執行錯誤：{e}"
