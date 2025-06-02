import openai,os

class MergeStackChatAssistant:
    def __init__(self, model):  
        # Thread creation
        self.thread = openai.beta.threads.create()
        
        # Vector store creation
        vector_store = openai.beta.vector_stores.create(name="MergeStack Policy Store")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        file_paths = [
            os.path.join(base_dir, "uploads", "mergestack_policy.pdf")
        ]
        file_streams = [open(path, "rb") for path in file_paths]
        file_batch = openai.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )
        
        # Assistant creation
        self.my_assistant = openai.beta.assistants.create(
            instructions="Your name is MergeGPT and you are an expert HR assistant for Mergestack. Use your knowledge base to answer any queries regarding the company, its policies and procedures. All this responses should follow proper markdown formatting.",
            name="MergeGPT",
            tools=[{"type":"file_search"}],
            model=model,
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

   