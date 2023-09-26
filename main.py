import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import tf2onnx
import onnx
import json

## LOAD DATA
ecommerce_sales_df = pd.read_csv("generated_data/ecommerce_data.csv")
outside_sales_df = pd.read_csv("")
jobapplications_df = pd.read_csv("generated_data/jobapplication_data.csv")
bankrapport_df = pd.read_csv("generated_data/bankrapport_data.csv")

creditcard_df = pd.read_csv("generated_data/sensitive/singlecreditcards_data.csv")
singlecpr_df = pd.read_csv("generated_data/sensitive/singlecprnumbers_data.csv")

## GET AND SET RECORDS
ecommerce_records = ecommerce_sales_df.to_dict(orient="records")
jobapplications_records = jobapplications_df.to_dict(orient="records")
bankrapport_records = bankrapport_df.to_dict(orient="records")
creditcard_records = creditcard_df.to_dict(orient="records") # Load and set records for creditcard
singlecpr_records = singlecpr_df.to_dict(orient="records")

def concatenate_record_fields(records):
    return [' '.join([str(value) for value in record.values()]) for record in records]

ecommerce_texts = concatenate_record_fields(ecommerce_records)
jobapplications_texts = concatenate_record_fields(jobapplications_records)
bankrapport_texts = concatenate_record_fields(bankrapport_records)
creditcard_texts = concatenate_record_fields(creditcard_records) # Concatenate record fields for creditcard
singlecpr_texts = concatenate_record_fields(singlecpr_records)

texts = ecommerce_texts + jobapplications_texts + bankrapport_texts + creditcard_texts + singlecpr_texts

# Concatenate data and define binary output of labels
ecommerce_labels = [[1, 0, 0, 0, 0, 0] for _ in ecommerce_texts]
jobapplications_labels = [[0, 1, 0, 0, 0, 0] for _ in jobapplications_texts]
bankrapport_labels = [[0, 0, 1, 0, 0, 0] for _ in bankrapport_texts]
creditcard_labels = [[0, 0, 0, 1, 0, 0] for _ in creditcard_texts] # Define labels for creditcard
singlecpr_labels = [[0, 0, 0, 0, 1, 0] for _ in singlecpr_texts]

labels = ecommerce_labels + jobapplications_labels + bankrapport_labels + creditcard_labels + singlecpr_labels
labels = np.array(labels)


assert len(texts) == len(labels)  ##Mismatch between number of texts and labels. IMPORTANT 

## ENGINE
# Tokenization
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded = pad_sequences(sequences, padding="post")


# Define the model
model = Sequential([
    Embedding(10000, 16, input_length=padded.shape[1]),
    GlobalAveragePooling1D(),
    Dense(24, activation='relu'),
    Dense(5, activation='sigmoid') 
])

word_to_index = tokenizer.word_index
with open('generated_models/word_to_index.json', 'w') as file:
    json.dump(word_to_index, file)

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
model.fit(padded, labels, epochs=5)

model.save("generated_models/my_keras_model.h5")
# Load the saved model
model = tf.keras.models.load_model("generated_models/my_keras_model.h5")

# Convert the model to ONNX
onnx_model, _ = tf2onnx.convert.from_keras(model)

# Save the ONNX model
onnx.save(onnx_model, "generated_models/my_onnx_model.onnx")



