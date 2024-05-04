from openai import OpenAI
import time
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
 
# Initialize the OpenAI client with an API key
client = OpenAI(api_key="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")
# Step 1: Create an assistant (This step assumes the assistant has already been created, just an example)
assistant = client.beta.assistants.create(
    name="Code Explorer",
    instructions="""
You are a software developer creating a README.md for a new project. Your task is to provide a high-level overview of the codebase,
including a summary of API calls for both frontend and backend, major components and their interactions, and the file structure.
The README should help new developers quickly understand and start working with the project.
""",
    model="gpt-4-turbo",
    tools=[{"type": "file_search"}]
)

# Step 2: Create a Vector Store and upload files (Assuming this has been done, shown here for completeness)
vector_store = client.beta.vector_stores.create(name="Code Embeddings")
file_paths = ["aggregated_code.txt"]
file_streams = [open(path, "rb") for path in file_paths]
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)
for stream in file_streams:
    stream.close()

# Update the assistant to use the new Vector Store
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)

# Step 4: Upload a user-provided file and create a thread (This should match your actual use case)
message_file = client.files.create(
    file=open("aggregated_code.txt", "rb"), purpose="assistants"
)

# Create a thread and attach the file to a message
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": '''
            Please provide a detailed README.md including API calls, file structure, and key components. You are to only return the content for the Readme.md file, there is no need for additional information.
             well-crafted README file is crucial for making your project accessible and understandable to new users and contributors. Here are the key components that are typically included in a README file:
             Project Title

Your Project Name
Description

    Brief overview of the project
    Purpose of the project
    Key features and functionalities

Installation Instructions

    Prerequisites (software/dependencies needed)
    Step-by-step guide to set up a development environment
    Any necessary set up in your code base

Usage

    Step-by-step instructions on how to use the project
        Include code examples here
    Screenshots or video demos

Contributing

    How to file an issue
    How to suggest enhancements
    How to make a pull request

License

    Specify the license (MIT, Apache, etc.)

Authors and Acknowledgments

    List of contributors
    Acknowledgments

Features [#Features]

    Feature 1
    Feature 2
    Feature 3

Technology Stack [#TechStack]

    Language 1
    Framework 1
    Library 1

Code Examples [#CodeExamples]

// Code snippet 1

# Code snippet 2

API Endpoints [#API]

    GET /endpoint1
        Description
        Parameters
        Returns
    POST /endpoint2
        Description
        Parameters
        Returns

Status

    Development status
    Build status badge
    Code coverage badge

Contact Information [#Contact]

    How to reach the team or maintainer
''',
            "attachments": [
                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ]
        }
    ]
)

# Create a run and start polling for completion
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Polling the run's status
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run.status not in ['in_progress', 'queued']:
        break
    print(f"Run is {run.status}. Waiting for completion...")
    time.sleep(10)

# Checking the response after run completion
if hasattr(run, 'messages'):
    for message in run.messages:
        if message.role == 'assistant':
            print("Assistant Response:", message.content)
else:
    print("Run completed with status:", run.status)
    if run.status == 'failed':
        print("Run failed with error:", run.last_error)
    else:
        print("No messages attribute in the run object. Run object:", run)


 
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        #save the message content to a file
        with open("README.md", "w") as f:
            f.write(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()