from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling, GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
from datasets import load_dataset


path = 'data.txt'

inp = "print(hello)"


# load tokenizer model
tokenizer = GPT2Tokenizer.from_pretrained('tokenizer')
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

# test
t = tokenizer.encode(inp)
print(t)
print(tokenizer.decode(t))


# load gpt model
config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    bos_token = tokenizer.bos_token,
    eos_token = tokenizer.bos_token
)

model = GPT2LMHeadModel(config)

dataset = load_dataset("text", data_files=path)

def encode(lines):
    return tokenizer(lines['text'], add_special_tokens=True, truncation=True, max_length=512)

dataset.set_transform(encode)
dataset = dataset['train']

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

training_args = TrainingArguments(
    output_dir="model_out",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    save_steps=100,
    save_total_limit=2,
    prediction_loss_only=True,
    remove_unused_columns=False
)

trainer = Trainer(
    model = model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset
)

trainer.train()
trainer.save_model("my_model")