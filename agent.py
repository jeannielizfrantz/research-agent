import anthropic

client = anthropic.Anthropic()

def run_agent(topic: str) -> str:
    messages = [{"role": "user", "content": topic}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system="You are a research agent. Search the web for current information on the topic, then write a clear 3-5 sentence summary of what you found.",
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages
        )
        
        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if hasattr(b, "text"))
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": b.id, "content": "Search completed."}
            for b in response.content if b.type == "tool_use"
        ]})

if __name__ == "__main__":
    result = run_agent("What are the latest developments in AI agents?")
    print(result)
