import traceback
from transformers import pipeline

try:
    print("Testing pipeline initialization...")
    p = pipeline("text-generation", model="google/flan-t5-small")
    print("Success!")
except Exception as e:
    print("Error during initialization:")
    traceback.print_exc()
