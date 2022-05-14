import os
from tokenizers import ByteLevelBPETokenizer


path = ['data.txt']

# make tokenizer model
if not os.path.exists('tokenizer'):
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(files=path, vocab_size=52000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>"
    ])

    tokenizer.save_model('tokenizer')