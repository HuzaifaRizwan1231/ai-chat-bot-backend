import google.generativeai as genai
import time, json

# Loading data from the file
training_data_file = "src/app/utils/fine_tuning/gemini_dataset.jsonl"

training_data = []
with open(training_data_file, "r") as file:
    for line in file:
        training_data.append(json.loads(line))

base_model = "models/gemini-1.5-flash-001-tuning"
operation = genai.create_tuned_model(
    display_name="increment",
    source_model=base_model,
    epoch_count=20,
    batch_size=4,
    learning_rate=0.001,
    training_data=training_data,
)

for status in operation.wait_bar():
    time.sleep(10)

result = operation.result()
print(result)