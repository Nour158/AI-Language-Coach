from ai.llm.qwen_client import QwenClient


client = QwenClient()

response = client.generate(
    "Say hello to an English learner and ask one simple question.",
    max_new_tokens=100,
)

print("\n===== QWEN RESPONSE =====")
print(response)