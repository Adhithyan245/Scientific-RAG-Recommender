from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
from app.config import GENERATION_MODEL_NAME, PROMPTS_DIR
import json
import re

class Reasoner:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL_NAME)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(GENERATION_MODEL_NAME)
        except Exception:
            self.tokenizer = None
            self.model = None
            
        self.prompt_path = PROMPTS_DIR / "recommendation_prompt.txt"
        
    def generate_reasoning(self, query: str, context: str) -> dict:
        fallback_result = {
            "instrument": "Unknown",
            "reasoning": "Model inference unavailable or failed. Based on retrieval.",
            "alternatives": [],
            "limitations": "See general constraints."
        }
        
        if not self.model or not self.tokenizer:
            return fallback_result

        try:
            if self.prompt_path.exists():
                with open(self.prompt_path, "r", encoding="utf-8") as f:
                    prompt_template = f.read()
            else:
                prompt_template = "Context:\n{context}\n\nQuery:\n{query}\n\nProvide JSON reasoning:"
                
            # SAFE REPLACEMENT: Avoids Python str.format() which crashes on literal JSON braces '{}'
            prompt = prompt_template.replace("{context}", str(context)).replace("{query}", str(query))
            
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_new_tokens=250)
            raw_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            result = fallback_result.copy()
            match = re.search(r'\{(?:[^{}]|(?(?=\{).*\}))*\}', raw_output, re.DOTALL)
            
            if match:
                parsed = json.loads(match.group(0))
                # Safely update with type checking
                if isinstance(parsed.get("instrument"), str):
                    result["instrument"] = parsed["instrument"]
                if isinstance(parsed.get("reasoning"), str):
                    result["reasoning"] = parsed["reasoning"]
                if isinstance(parsed.get("limitations"), str):
                    result["limitations"] = parsed["limitations"]
                if isinstance(parsed.get("alternatives"), list):
                    result["alternatives"] = [str(a) for a in parsed["alternatives"]]
            else:
                if raw_output and str(raw_output).strip() and not str(raw_output).startswith("Failed"):
                    result["reasoning"] = str(raw_output).strip()[:200]
                    
            return result
        except Exception as e:
            # Catch inference crashes or weird formatting errors generically
            print(f"Reasoner Error: {e}")
            return fallback_result
