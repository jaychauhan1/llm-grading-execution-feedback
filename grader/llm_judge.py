import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "Qwen/Qwen2.5-Coder-7B-Instruct"

print("Loading model:", MODEL_ID)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
)

SCHEMA_REMINDER = """Return ONLY valid JSON with EXACTLY these keys:
{
  "verdict": "correct" | "partial" | "incorrect",
  "score": <integer 0-100>,
  "reasons": ["...", "..."],
  "evidence_used": ["code_only" | "stderr" | "tests_summary" | "failure_traces"],
  "confidence": <number 0.0-1.0>
}
No markdown. No code fences. No extra keys. No extra text.
"""

def grade_prompt(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are a strict grader. " + SCHEMA_REMINDER},
        {"role": "user", "content": prompt + "\n\n" + SCHEMA_REMINDER},
    ]

    chat_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(chat_text, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            temperature=0.0,
            eos_token_id=tokenizer.eos_token_id,
        )

    gen_ids = out[0][inputs["input_ids"].shape[1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True).strip()
    return text
