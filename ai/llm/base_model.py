from ai.llm.model_loader import load_model, load_tokenizer


class BaseLanguageModel:
    """
    Wrapper around the base language model.

    This class gives the rest of the application a stable interface
    regardless of which underlying LLM is used.
    """

    def __init__(self):
        self.tokenizer = load_tokenizer()
        self.model = load_model()

    def generate(self, messages, max_new_tokens=256):
        """
        Generate a response from a list of chat messages.

        Expected format:
        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
        ]
        """

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

        generated_tokens = outputs[
            0,
            inputs["input_ids"].shape[1]:
        ]

        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response.strip()