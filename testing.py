from textwrap import indent
from agents import HostedMCPTool, RunContextWrapper, Agent, ModelSettings, TResponseInputItem, Runner, RunConfig
from dotenv import load_dotenv
from openai.types.shared.reasoning import Reasoning
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv


load_dotenv()
# Tool definitions
mcp = HostedMCPTool(tool_config={
  "type": "mcp",
  "server_label": "googledrive",
  "connector_id": "connector_googledrive",
  "authorization": "{\"expression\":\"${GOOGLE_OAUTH_TOKEN}\",\"format\":\"cel\"}",
  "allowed_tools": [
    "fetch",
    "get_profile",
    "list_drives",
    "recent_documents",
    "search"
  ],
  "require_approval": "never"
})


class AgentContext:
  def __init__(self, workflow_input_as_text: str):
    self.workflow_input_as_text = workflow_input_as_text
    
def agent_instructions(run_context: RunContextWrapper[AgentContext], _agent: Agent[AgentContext]):
  workflow_input_as_text = run_context.context.workflow_input_as_text
  return f"""You are a Resume Matching Agent.
Your task is to analyze resumes stored in the folder MyDrive/Resume and identify the most relevant candidate for the provided job description.
Instructions:

Read all resume files in the folder MyDrive/Resume.
Compare each resume’s content (skills, experience, education, and keywords) with the given Job Description.
Evaluate relevance based on semantic similarity, not just keyword matching.
Select the single most relevant resume that best fits the job description.
Output only the file name of the best-matching resume.

Job Description:
{workflow_input_as_text}"""


agent = Agent(
  name="Agent",
  instructions=agent_instructions,
  model="o4-mini",
  tools=[mcp],
  model_settings=ModelSettings(
    store=True,
    reasoning=Reasoning(
      effort="high",
      summary="auto"
    )
  )
)


class WorkflowInput(BaseModel):
  input_as_text: str


# Main code entrypoint
async def run_workflow(workflow_input: WorkflowInput):
  workflow = workflow_input.model_dump()
  conversation_history: list[TResponseInputItem] = [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": workflow["input_as_text"]
        }
      ]
    }
  ]
  agent_result_temp = await Runner.run(
    agent,
    input=[*conversation_history],
    run_config=RunConfig(trace_metadata={
      "__trace_source__": "agent-builder",
      "workflow_id": "wf_68ecdbe36e2081909f2af6ef87569fa202ba9b25128ec5fd"
    }),
    context=AgentContext(workflow_input_as_text=workflow["input_as_text"])
  )

  for item in agent_result_temp.new_items:
    try:
      print("Step:", item.type)
      print(item.model_dump_json(indent=2))
    except Exception:
      print(repr(item))

  conversation_history.extend([item.to_input_item() for item in agent_result_temp.new_items])

  agent_result = {
    "output_text": agent_result_temp.final_output_as(str)
  }
  end_result = {
    "resume_drive_name": None
  }
  return {
  "output_text": agent_result_temp.final_output_as(str),
  "trace_steps": [getattr(i, "to_input_item", lambda: i)() for i in agent_result_temp.new_items]
  }


async def main():
  job_description = """
    We are looking for a Data Scientist with experience in Python, SQL,
    and machine learning using scikit-learn or TensorFlow.
    """
  # workflow_input = WorkflowInput(input_as_text=job_description)
  # result = asyncio.run(run_workflow(workflow_input))
  profile = await Runner.run(
    agent,
    input=[{"role": "user", "content": [{"type": "input_text", "text": "get_profile"}]}],
    context=AgentContext(workflow_input_as_text="diagnostic: whoami")
  )
  print("PROFILE STEP:", profile.final_output_as(str))
  # print(result)

if __name__=="__main__":
  asyncio.run(main())