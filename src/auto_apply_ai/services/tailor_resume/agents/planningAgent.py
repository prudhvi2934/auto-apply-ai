from pydantic import BaseModel
from typing import Any,Dict,List,Optional
from dataclasses import dataclass
import asyncio
import json
import os
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
import opik
from opik import track
from opik.integrations.genai import track_genai
load_dotenv()

class ContextItem(BaseModel):
    key: str
    values: List[str]

# Agent Task Models
class AgentTask(BaseModel):
    """Instructions for a specific agent"""
    agent_name: str
    priority_items: List[str]
    specific_instructions: str
    context: Optional[List[ContextItem]] = None

class GapAnalysis(BaseModel):
    direct_matches: List[str]
    transferable: List[str]
    gaps: List[str]
    how_to_address: str


class TailoringPlan(BaseModel):
    """Plan created by Planning Agent"""
    strategy: str
    key_themes: List[str]
    gap_analysis: GapAnalysis
    summary_task: AgentTask
    skills_task: AgentTask
    experience_task: AgentTask
    ats_keywords: List[str]

# Minimal Gemini LLM client with an async interface
class GeminiClient:
    """Thin wrapper around Google's Gen AI SDK that exposes an async .generate().
    The SDK call is sync, so we run it in a thread to keep our agent async-friendly.
    Reads GEMINI_KEY from env by default (set via .env already loaded above).
    """
    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None, **default_config):
        self._client = track_genai(genai.Client(api_key=api_key))
        self._model = model
        self._default_config = default_config or {}

    async def generate(self, prompt: str, **override_config) -> TailoringPlan:
        cfg = {**self._default_config, **(override_config or {})}

        def _call_genai():
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TailoringPlan,
                temperature=0,
                **cfg  # for determinism
            )
            kwargs = {"model": self._model, "contents": prompt,"config":config}
            resp = self._client.models.generate_content(**kwargs)
            # `resp.text` is the concatenated text output from the SDK
            text = getattr(resp, "text", None)
            if text is None:
                raise RuntimeError("No text in Gemini response")
            return TailoringPlan.model_validate_json(text)

        # Run the blocking SDK call in a worker thread to preserve async API
        return await asyncio.to_thread(_call_genai)


# Your existing models
class Resume(BaseModel):
    id: str
    basics: Any  # Basics 
    summary: str
    skills: List[str] 
    experience: List[Any]  # List[Experience]
    education: str
    certifications: Optional[str] = None
    projects: Optional[str] = None

class JobDesc(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    must_have: List[str] = []
    nice_to_have: List[str] = []
    responsibilities: List[str] = []
    tools: List[str] = []
    keywords: List[str] = []
    years_experience: Optional[Dict[str, int]] = None
    salary: Any = None
    meta: Dict = {}


class PlanningAgent:
    """
    Analyzes JD & Resume, creates comprehensive tailoring strategy
    with awareness of downstream agents
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
    @track(name="planning_agent.create_plan", tags=["agent:PlanningAgent"],project_name="Auto-apply-AI")
    async def create_plan(self, resume: Resume, job_desc: JobDesc) -> TailoringPlan:
        """
        Uses Chain-of-Thought reasoning to create a tailoring plan
        """
        
        prompt = f"""You are a Planning Agent in a resume tailoring system. You coordinate three specialist agents:
1. SUMMARY AGENT - Rewrites professional summaries
2. SKILLS AGENT - Reorders and optimizes skills section
3. EXPERIENCE AGENT - Rewrites experience bullet points

RESUME:
{resume.model_dump_json(indent=2)}

JOB DESCRIPTION:
{job_desc.model_dump_json(indent=2)}

TASK: Create a comprehensive tailoring plan using Chain-of-Thought reasoning.

Think through this step-by-step:

1. ANALYSIS PHASE:
   - What are the top 5 competencies this JD REALLY values?
   - What's the hiring manager's likely pain points?
   - What experience level are they seeking?
   - What's the company culture signal (formal/startup/technical)?

2. GAP ANALYSIS:
   - Direct matches: What resume items perfectly align?
   - Transferable matches: What experience applies indirectly?
   - Missing elements: What does the JD want that's not in resume?
   - Strategic response: How do we address gaps honestly?

3. STRATEGY FORMULATION:
   - Overall approach: What's our tailoring strategy?
   - Key themes: What 3-4 themes should we emphasize throughout?
   - Tone adjustment: Should we adjust formality/technical depth?
   - ATS keywords: What exact keywords must appear?

4. AGENT TASK DELEGATION:
   For each agent, specify:
   - Priority items to focus on
   - Specific instructions
   - Context they need to know
   - Success criteria

Return your plan in this JSON structure:
{{
    "strategy": "overall tailoring approach",
    "key_themes": ["theme1", "theme2", "theme3"],
    "gap_analysis": {{
        "direct_matches": ["item1", "item2"],
        "transferable": ["item1", "item2"],
        "gaps": ["item1", "item2"],
        "how_to_address": "strategy"
    }},
    "summary_task": {{
        "agent_name": "summary",
        "priority_items": ["what to emphasize"],
        "specific_instructions": "detailed instructions",
        "context": {{"key_info": ["value"]}}
    }},
    "skills_task": {{
        "agent_name": "skills",
        "priority_items": ["which skills to highlight"],
        "specific_instructions": "detailed instructions",
        "context": {{"key_info": ["value"]}}
    }},
    "experience_task": {{
        "agent_name": "experience",
        "priority_items": ["which experiences to focus on"],
        "specific_instructions": "detailed instructions",
        "context": {{"key_info": ["value"]}}
    }},
    "ats_keywords": ["keyword1", "keyword2"]
}}
"""
        
        response = await self.llm.generate(prompt)
        # plan_data = self._parse_json_response(response)
        
        return response
        # return self.plan_with_mapped_contexts(response)
        # return TailoringPlan(
        #     strategy=plan_data["strategy"],
        #     key_themes=plan_data["key_themes"],
        #     gap_analysis=plan_data["gap_analysis"],
        #     summary_task=AgentTask(**plan_data["summary_task"]),
        #     skills_task=AgentTask(**plan_data["skills_task"]),
        #     experience_task=AgentTask(**plan_data["experience_task"]),
        #     ats_keywords=plan_data["ats_keywords"]
        # )
    
    # def _parse_json_response(self, response: str) -> Dict:
    #     """Parse JSON from LLM response"""
    #     import json
    #     import re
    #     # Extract JSON from markdown code blocks if present
    #     json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
    #     if json_match:
    #         return json.loads(json_match.group(1))
    #     return json.loads(response)
    def _dedupe_preserve_order(self,items: List[str]) -> List[str]:
        seen = set()
        out = []
        for x in items:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def _context_list_to_map(self,ctx: Optional[List[ContextItem]]) -> Optional[Dict[str, List[str]]]:
        if ctx is None:
            return None
        merged: Dict[str, List[str]] = {}
        for item in ctx:
            if item.key not in merged:
                merged[item.key] = []
            merged[item.key].extend(item.values)
        # de-duplicate each list while preserving order
        for k, vals in merged.items():
            merged[k] = self._dedupe_preserve_order(vals)
        return merged
    

    def plan_with_mapped_contexts(self,plan: TailoringPlan) -> Dict:
        """
        Export TailoringPlan as a dict, converting each AgentTask.context
        from List[ContextItem] -> Dict[str, List[str]].
        """
        data = plan.model_dump()

        def _convert_task(task_key: str):
            if task_key in data and data[task_key] is not None:
                ctx_list = data[task_key].get("context")
                if ctx_list is not None:
                    # Reconstruct ContextItem objects to reuse the parser if needed
                    ctx_objs = [ContextItem(**c) if not isinstance(c, ContextItem) else c for c in ctx_list]
                    data[task_key]["context"] =self._context_list_to_map(ctx_objs)

        for tk in ("summary_task", "skills_task", "experience_task"):
            _convert_task(tk)

        return data




async def main():
    
    opik.configure(use_local=False)
    
    resume = Resume(
        id="user123",
        basics={"name": "John Doe"},
        summary="Software engineer with 5 years experience",
        skills=["Python", "JavaScript", "React", "SQL"],
        experience=[],
        education="BS Computer Science"
    )

    job_desc = JobDesc(
        role="Senior Full Stack Developer",
        must_have=["Python", "React", "AWS"],
        responsibilities=["Build scalable web applications"],
        tools=["Docker", "Kubernetes"]
    )
    
    llm_client = GeminiClient(api_key=os.getenv("GEMINI_KEY"),model="gemini-2.5-flash")
    planning_agent = PlanningAgent(llm_client)
    plan = await planning_agent.create_plan(resume, job_desc)
    print(json.dumps(plan.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
    ##TODO: Check later if ContextItem model (currently using key/values list) causes schema or response issues in next pipeline stages.