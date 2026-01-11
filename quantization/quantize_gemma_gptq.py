from llmcompressor.modifiers.quantization.gptq import GPTQModifier
from llmcompressor import oneshot
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

from compressed_tensors.quantization import (
    QuantizationArgs,
    QuantizationScheme,
    QuantizationStrategy,
)

# Select calibration dataset.
DATASET_ID = "HuggingFaceH4/ultrachat_200k"
DATASET_SPLIT = "train_sft"


MODEL_ID="google/gemma-3-12b-it"

# Select number of samples. 256 samples is a good place to start.
# Increasing the number of samples can improve accuracy.
NUM_CALIBRATION_SAMPLES = 256
MAX_SEQUENCE_LENGTH = 512

# Load dataset and preprocess.
ds = load_dataset(DATASET_ID, split=f"{DATASET_SPLIT}[:{NUM_CALIBRATION_SAMPLES}]")
ds = ds.shuffle(seed=42)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

def preprocess(example):
    return {
        "text": tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
        )
    }


ds = ds.map(preprocess)

quant_mod = GPTQModifier(
    scheme="W4A16",  # 4-bit weights
    targets="Linear",
    ignore=["lm_head"],
#    group_size=16
)

quant_mod = GPTQModifier(
    block_size=128,
    dampening_frac=0.001,
    config_groups={
        "gptq_group_16": QuantizationScheme(
            targets=["Linear"],
            weights=QuantizationArgs(
                num_bits=4,
                type="int",
                symmetric=True,
                strategy=QuantizationStrategy.GROUP,
                group_size=32,   # ✅ correct location
            ),
        )
    },
)

oneshot(
    model=MODEL_ID,
    recipe=[quant_mod],
    dataset=ds,
    output_dir="gemma-3-12b-it-gptq",
    max_seq_length=2048,
    num_calibration_samples=256,
)

