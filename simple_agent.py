import os
import re
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from colorama import init, Fore, Style, Back
from tools import run_tool, get_tool_descriptions

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
init(autoreset=True)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = f"""你是一個 ReAct Agent，請遵循以下規則進行思考與行動：

你的輸出格式必須嚴格遵循：

Thought: 你對當前問題的思考與推理
Action: 選擇一個工具名稱（若需要工具）
Action Input: 傳給工具的參數（JSON 格式）
Observation: 工具的觀察結果（由系統填寫）

當你認為已經有足夠資訊回答使用者時，請輸出：

Thought: 我已經有足夠資訊回答
Final Answer: 你的最終回答

可用工具：
{get_tool_descriptions()}

請注意：
- 每次只能使用一個工具
- Action Input 必須是合法的 JSON 物件
- 如果工具回傳錯誤，請嘗試修正後重試
- 最多進行 10 輪思考"""

def parse_react(text: str) -> dict:
    result = {}
    if match := re.search(r"Thought:\s*(.+?)(?=\n(?:Action|Final)|$)", text, re.DOTALL):
        result["thought"] = match.group(1).strip()
    if match := re.search(r"Action:\s*(\w+)", text):
        result["action"] = match.group(1).strip()
    if match := re.search(r"Action Input:\s*(\{.*?\})", text, re.DOTALL):
        try:
            result["action_input"] = eval(match.group(1).strip())
        except:
            result["action_input"] = {}
    if match := re.search(r"Final Answer:\s*(.+?)$", text, re.DOTALL):
        result["final_answer"] = match.group(1).strip()
    return result

def run_agent(user_input: str, max_steps: int = 10):
    messages = [
        {"role": "user", "parts": [SYSTEM_PROMPT + f"\n\n使用者問題：{user_input}"]}
    ]

    print(f"\n{Back.BLUE}{Fore.WHITE} [Agent] 啟動 {Style.RESET_ALL}\n")

    for step in range(max_steps):
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[Step] {step + 1}/{max_steps}{Style.RESET_ALL}")

        response = model.generate_content(messages)
        raw = response.text.strip()

        print(f"\n{Fore.GREEN}[模型輸出]{Style.RESET_ALL}")
        print(raw)

        parsed = parse_react(raw)
        thought = parsed.get("thought", "")
        action = parsed.get("action", "")
        action_input = parsed.get("action_input", {})
        final_answer = parsed.get("final_answer", "")

        if final_answer:
            print(f"\n{Back.GREEN}{Fore.BLACK} [最終回答] {Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Back.GREEN}{final_answer}{Style.RESET_ALL}")
            return final_answer

        if action:
            print(f"\n{Fore.MAGENTA}[工具] 執行：{action}{Style.RESET_ALL}")
            observation = run_tool(action, **action_input)
            print(f"{Fore.BLUE}[觀察] {observation}{Style.RESET_ALL}")

            messages.append({"role": "model", "parts": [raw]})
            messages.append({
                "role": "user",
                "parts": [f"Observation: {observation}\n\n請根據觀察結果繼續思考。"]
            })
        else:
            print(f"{Fore.RED}[錯誤] 無法解析 Action，結束循環{Style.RESET_ALL}")
            break

    print(f"\n{Back.RED}{Fore.WHITE} [結束] 達到最大步數 {max_steps}，強制結束 {Style.RESET_ALL}")
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        run_agent(query)
    else:
        print(f"{Fore.CYAN}{Back.BLACK}ReAct Agent{Style.RESET_ALL}")
        print(f"{Fore.WHITE}輸入你的問題（輸入 exit 結束）{Style.RESET_ALL}")
        while True:
            user_input = input(f"\n{Fore.GREEN}You: {Style.RESET_ALL}")
            if user_input.lower() in ("exit", "quit"):
                break
            run_agent(user_input)
