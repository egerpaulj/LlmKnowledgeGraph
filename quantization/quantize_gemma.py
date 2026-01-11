from llmcompressor import oneshot
from llmcompressor.modifiers.awq import AWQModifier, AWQMapping

MODEL_ID = "google/gemma-3-12b-it"
OUTPUT_DIR = "gemma-3-12b-it-w4a16"

# choose quant algorithm:
# either GPTQ:
#quant_mod = GPTQModifier(scheme="W4A16", targets="Linear", ignore=["lm_head"])
# or AWQ:

awq_mappings = []

for i in range(48):
    awq_mappings.append(
        AWQMapping(
            smooth_layer=f"model.language_model.layers.{i}.input_layernorm",
            balance_layers=[
                f"model.language_model.layers.{i}.self_attention.q_proj",
                f"model.language_model.layers.{i}.self_attention.k_proj",
                f"model.language_model.layers.{i}.self_attention.v_proj",
            ],
        )
    )

quant_mod = AWQModifier(
        scheme="W4A16", 
        targets="Linear", 
        ignore=["lm_head"])

recipe = [quant_mod]

oneshot(
    model=MODEL_ID,
    recipe=recipe,
    output_dir=OUTPUT_DIR,
    # calibration is used internally — you can optionally specify a dataset
    max_seq_length=2048,
    num_calibration_samples=256,
)

