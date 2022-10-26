import os

import nltk
import numpy as np
from datasets import load_dataset, load_metric
from transformers import DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer
from transformers import T5ForConditionalGeneration
from transformers import T5Tokenizer


def preprocess_function_headline(examples):
    inputs = [prefix + doc for doc in examples["text"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["headline"], max_length=128, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Rouge expects a newline after each sentence
    decoded_preds = ['\n'.join(nltk.sent_tokenize(pred.strip())) for pred in decoded_preds]
    decoded_labels = ['\n'.join(nltk.sent_tokenize(label.strip())) for label in decoded_labels]

    result = metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True)
    # Extract a few results
    result = {key: value.mid.fmeasure * 100 for key, value in result.items()}

    # Add mean generated length
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions]
    result['gen_len'] = np.mean(prediction_lens)

    return {k: round(v, 4) for k, v in result.items()}


# import tokenizer and model
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
model_name = '/home/azagar/myfiles/t5/models/t5_sl_small_v2-pytorch'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
print(model_name)

# prepare data
data_files = {'train': 'data/sta_headline/train.jsonl',
              'test': 'data/sta_headline/test.jsonl',
              'val': 'data/sta_headline/val.jsonl'}
data = load_dataset('json', data_files=data_files)
tokenized_data = data.map(preprocess_function_headline, batched=True)
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

# load metric
metric = load_metric('rouge')

# set folders for output, logs, ...
train, evaluate = True, True
exp = 'SloT5-headline'
output_dir = os.path.join('./results', exp)
save_path = os.path.join('./models', exp)
log_dir = os.path.join('./logs', exp)
training_args = Seq2SeqTrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=False,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    save_total_limit=5,
    num_train_epochs=2,
    fp16=True,
    save_steps=1000,
    eval_steps=1000,
    logging_steps=1000,
    logging_dir=log_dir,
    gradient_accumulation_steps=4,
    eval_accumulation_steps=1,
    predict_with_generate=True,
    generation_max_length=256,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data['train'],
    eval_dataset=tokenized_data['val'],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

if train:
    print('Training model ...')
    trainer.train()
    trainer.save_model(save_path)

# evaluate
if evaluate:
    print('Evaluating model ...')
    test_results = trainer.predict(test_dataset=tokenized_data['test'])
    print('Test results:', test_results.metrics)
