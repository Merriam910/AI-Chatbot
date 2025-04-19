from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
import torch
import os
import re

# 1. Configuration
os.makedirs("./fine_tuned_model", exist_ok=True)
os.makedirs("./logs", exist_ok=True)

# 2. Load Dataset
try:
    dataset = load_dataset("json", data_files="data/train_data.jsonl", split="train")
    print(f"Loaded dataset with {len(dataset)} examples")
except Exception as e:
    raise ValueError(f"Error loading dataset: {e}")

# 3. Initialize Tokenizer with Enhanced Settings
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
tokenizer.pad_token = tokenizer.eos_token
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# 4. Text Cleaning Function
def clean_text(text):
    text = str(text)  # Ensure it's string
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special chars
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

# 5. Robust Preprocessing
def preprocess(example):
    try:
        # Clean and format dialog
        formatted = []
        for i, text in enumerate(example["dialog"]):
            speaker = "User" if i % 2 == 0 else "AI"
            cleaned = clean_text(text)
            formatted.append(f"{speaker}: {cleaned}")
        
        # Tokenize safely
        result = tokenizer(
            "\n".join(formatted),
            truncation=True,
            max_length=256,
            padding="max_length",
            return_tensors="pt"
        )
        
        # Handle OOV tokens
        input_ids = result["input_ids"]
        if (input_ids >= tokenizer.vocab_size).any():
            input_ids[input_ids >= tokenizer.vocab_size] = tokenizer.unk_token_id
        
        return {
            "input_ids": input_ids[0],
            "attention_mask": result["attention_mask"][0]
        }
    except Exception as e:
        print(f"Skipping example due to error: {e}")
        return None

# 6. Safe Dataset Processing
try:
    # Process and filter in two steps
    processed = dataset.map(preprocess, batched=False)
    tokenized_dataset = processed.filter(lambda x: x is not None)
    print(f"Successfully processed {len(tokenized_dataset)} examples")
except Exception as e:
    raise ValueError(f"Tokenization failed: {e}")

# 7. Model Initialization
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/DialoGPT-large",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
model.resize_token_embeddings(len(tokenizer))

# 8. Training Configuration
training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    learning_rate=3e-5,
    warmup_steps=100,
    logging_dir="./logs",
    logging_steps=50,
    save_steps=500,
    save_total_limit=2,
    fp16=torch.cuda.is_available(),
    gradient_accumulation_steps=4,
    report_to="none"
)

# 9. Data Collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# 10. Trainer Initialization
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

# 11. Start Training
print("Starting training...")
try:
    trainer.train()
except Exception as e:
    print(f"Training failed: {e}")
    exit(1)

# 12. Save Model
trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
print("Training complete! Model saved to ./fine_tuned_model")