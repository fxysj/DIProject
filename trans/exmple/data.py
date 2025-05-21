import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from typing import Optional, Dict, Any, Callable


class Web3TradingAnalyzer:
    def __init__(
            self,
            model_name: str = "qwen/Qwen3-8B",
            dataset_name: str = "0xscope/web3-trading-analysis",
            output_dir: str = "./qwen3-8b-web3-trading",
            lora_r: int = 8,
            lora_alpha: int = 32,
            lora_dropout: float = 0.1,
            load_in_4bit: bool = False,
            bnb_4bit_compute_dtype: torch.dtype = torch.bfloat16
    ):
        """初始化Web3交易分析模型训练器"""
        self.model_name = model_name
        self.dataset_name = dataset_name
        self.output_dir = output_dir
        self.lora_r = lora_r
        self.lora_alpha = lora_alpha
        self.lora_dropout = lora_dropout
        self.load_in_4bit = load_in_4bit
        self.bnb_4bit_compute_dtype = bnb_4bit_compute_dtype

        self.tokenizer = None
        self.model = None
        self.dataset = None
        self.data_columns = None

    def load_data(self, split: str = "train") -> None:
        """加载Web3交易分析数据集并探查结构"""
        print(f"加载数据集: {self.dataset_name}")
        self.dataset = load_dataset(self.dataset_name, split=split)
        print(f"数据集加载完成，样本数: {len(self.dataset)}")

        if len(self.dataset) > 0:
            self.data_columns = list(self.dataset[0].keys())
            print(f"数据集列名: {self.data_columns}")
        else:
            print("警告: 数据集为空，无法探查结构")

    def setup_model(self):
        """加载Tokenizer和模型，并配置LoRA参数"""
        print("正在加载Tokenizer和模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)

        quantization_config = None
        if self.load_in_4bit:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=self.bnb_4bit_compute_dtype
            )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            load_in_4bit=False,  # 关闭 4-bit 量化
            device_map="auto",
            trust_remote_code=True,
            quantization_config=quantization_config
        )

        self.model = prepare_model_for_kbit_training(self.model)
        lora_config = LoraConfig(
            r=self.lora_r,
            lora_alpha=self.lora_alpha,
            lora_dropout=self.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM"
        )
        self.model = get_peft_model(self.model, lora_config)
        print("模型和Tokenizer加载完成")

    def preprocess_data(
            self,
            text_processor: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
    ) -> None:
        """预处理数据"""
        if self.dataset is None:
            raise ValueError("请先调用load_data()加载数据集")

        if text_processor is None:
            if "text" in self.data_columns:
                def default_processor(examples):
                    return {"text": examples["text"]}
                text_processor = default_processor
            else:
                raise ValueError("请提供自定义text_processor函数，因为数据集中没有'text'列")

        def tokenize_function(examples):
            processed = text_processor(examples)
            return self.tokenizer(
                processed["text"],
                truncation=True,
                max_length=512,
                padding="max_length"
            )

        print("正在预处理数据...")
        self.dataset = self.dataset.map(tokenize_function, batched=True)
        self.dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])
        print("数据预处理完成")

    def train(self):
        """训练模型"""
        print("开始训练...")
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=2,
            num_train_epochs=1,
            logging_dir=os.path.join(self.output_dir, "logs"),
            logging_steps=10,
            save_steps=500,
            save_total_limit=2,
            fp16=True if torch.cuda.is_available() else False
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator
        )

        trainer.train()
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)
        print("训练完成，模型已保存。")

    def predict(self, prompt: str) -> str:
        """简单推理函数"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


def main():
    analyzer = Web3TradingAnalyzer(
        model_name="qwen/Qwen3-8B",
        dataset_name="0xscope/web3-trading-analysis",
        output_dir="./qwen3-8b-web3-trading"
    )

    # 1. 加载数据
    analyzer.load_data()

    # 2. 加载模型和Tokenizer（⚠️必须在预处理前执行）
    analyzer.setup_model()

    # 3. 自定义文本处理函数
    def custom_text_processor(examples):
        texts = []
        for event_type, event in zip(examples["event_type"], examples["event"]):
            prompt = f"分析这个Web3事件: 类型={event_type}, 详情={event}"
            answer = "这是一个示例分析..."  # TODO: 替换为真实答案
            texts.append(f"问题: {prompt}\n回答: {answer}")
        return {"text": texts}

    # 4. 数据预处理
    analyzer.preprocess_data(text_processor=custom_text_processor)

    # 5. 模型训练
    analyzer.train()

    # 6. 推理示例
    prompt = "分析这个Web3事件: 类型=swap, 详情={from: USDT, to: ETH, amount: 1000}"
    result = analyzer.predict(prompt)
    print(f"预测结果: {result}")


if __name__ == "__main__":
    main()
