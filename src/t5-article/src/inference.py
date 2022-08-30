def summarize(tokenizer, model, text):
    input_ids = tokenizer(f"summarize: {text}", return_tensors="pt", max_length=512, truncation=True).input_ids
    input_ids = input_ids.to('cpu')
    outputs = model.generate(input_ids,
                             max_length=256,
                             num_beams=5,
                             no_repeat_ngram_size=5
                             )

    decoded_preds = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded_preds