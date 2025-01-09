import openai,os

class MergeStackChatAssistant:
    def __init__(self):  
        self.thread = openai.beta.threads.create()
        
        vector_store = openai.beta.vector_stores.create(name="MergeStack Policy Store")

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        file_paths = [
            os.path.join(base_dir, "files", "mergestack_policy.pdf")
        ]

        file_streams = [open(path, "rb") for path in file_paths]
        
        file_batch = openai.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )
        

        self.my_assistant = openai.beta.assistants.create(
            instructions="You are a personal assistant which answers questions about any policies and procedures of a company named Mergestack.",
            name="Mergestack Assistant",
            tools=[{"type":"file_search"}],
            model="gpt-4o",
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
        

    def pollAndRun(self):
        run = openai.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.my_assistant.id,
        )
        
        while run.status != "completed":
            run = openai.beta.threads.runs.retrieve(thread_id=self.thread.id,run_id= run.id)
            
        return openai.beta.threads.messages.list(thread_id=self.thread.id).data[0]

   