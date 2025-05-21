from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download
import shutil
import os

# 设置模型名称和保存路径
model_id = "Qwen/Qwen3-8B"
save_dir = "./Qwen3-8B-offline"

# Step 1: 下载整个模型快照到本地缓存目录（含权重、配置、tokenizer等）
print("📦 Downloading model from Hugging Face Hub...")
local_dir = snapshot_download(repo_id=model_id, local_dir=save_dir, local_dir_use_symlinks=False)

print(f"✅ 模型已保存到：{local_dir}")
