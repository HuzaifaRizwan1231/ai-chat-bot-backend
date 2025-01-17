from openai import OpenAI

client = OpenAI()


# uploaded_file = client.files.create(
#   file=open("./openai_dataset.jsonl", "rb"),
#   purpose="fine-tune"
# )


# job = client.fine_tuning.jobs.create(
#     training_file=uploaded_file.id,
#     model="gpt-4o-mini-2024-07-18",
# )

# getting the id of the fine tuned model
print(client.fine_tuning.jobs.retrieve('ftjob-RwkDAhw9ObgckD3Q6cA7LbRq').fine_tuned_model)

# ft:gpt-4o-mini-2024-07-18:mergestack::AqhhvrOU


