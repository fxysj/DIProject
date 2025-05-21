from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model


# 手动设置模型为训练模式，并冻结部分参数
def prepare_model_for_kbit_training(model):
    # 冻结所有参数，只训练 LoRA 层
    for param in model.parameters():
        param.requires_grad = False
    # LoRA 需要训练的参数会自动打开
    return model
# 1. 加载数据集
dataset = load_dataset("0xscope/web3-trading-analysis")

# 2. 载入Tokenizer和模型
model_name = "meta-llama/Meta-Llama-3-70B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

# LLaMA tokenizer 没有pad token，需要指定
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 3. 加载模型 (这里用int8量化加载减少显存)
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_8bit=True, device_map="auto")

# 4. 准备模型进行LoRA微调
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)


# 5. 数据预处理（示例处理文本输入和标签）
def preprocess_function(examples):
    # 这里示例简单用某个字段，比如"trade_text"当作输入，实际根据数据集字段调整
    inputs = examples["trade_text"]  # 替换成真实字段名
    # 构造prompt，如果是instruct微调可以做指令包装
    prompts = [f"Analyze the following trade data:\n{inp}\nAnswer:" for inp in inputs]

    tokenized = tokenizer(prompts, truncation=True, padding="max_length", max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()  # 因为是causal LM，labels和input_ids相同
    return tokenized


tokenized_dataset = dataset.map(preprocess_function, batched=True)

# 6. 训练参数配置
training_args = TrainingArguments(
    output_dir="./llama3-web3-lora",
    per_device_train_batch_size=1,  # 根据显存调整
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=8,
    evaluation_strategy="steps",
    save_strategy="steps",
    save_steps=500,
    eval_steps=500,
    logging_steps=100,
    num_train_epochs=3,
    learning_rate=3e-4,
    fp16=True,
    save_total_limit=2,
    load_best_model_at_end=True,
    report_to="none",  # 关闭wandb等
)

# 7. Trainer实例
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
)

# 8. 开始训练
trainer.train()

# 9. 保存LoRA权重
model.save_pretrained("./llama3-web3-lora")
