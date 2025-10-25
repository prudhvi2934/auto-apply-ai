from pydantic import BaseModel
from typing import Any, List, Optional, Dict, Generic, TypeVar
from auto_apply_ai.services.tailor_resume.tailor_resume_scm import Experience, Basics
from google import genai
from google.genai.types import GenerateContentConfig
import asyncio
import json
import os
import opik
from opik.integrations.genai import track_genai
from opik import track
from dotenv import load_dotenv
load_dotenv()

T = TypeVar('T')

class Resume(BaseModel):
    id: str
    basics: Any  # Basics 
    summary: str
    skills: List[str] 
    experience: List[Any]  # List[Experience]
    education: str
    certifications: str = None
    projects: str = None


class AgentResult(BaseModel):
    """Result from an agent execution"""
    agent_name: str
    output: T
    reasoning: str
    confidence: float

class AgentTask(BaseModel):
    """Instructions for a specific agent"""
    agent_name: str
    priority_items: List[str]
    specific_instructions: str
    context: Dict[str, Any]

class TailoringPlan(BaseModel):
    """Plan created by Planning Agent"""
    strategy: str
    key_themes: List[str]
    gap_analysis: Dict[str, Any]
    summary_task: AgentTask
    skills_task: AgentTask
    experience_task: AgentTask
    ats_keywords: List[str]

class Experience(BaseModel):
    """A single work experience entry"""
    company: str
    title: str
    original_bullets: list[str]
    changes_made: str
    new_bullets: list[str]


class ExperienceGeminiSchema(BaseModel):
    """Flattened schema for Gemini - all fields at top level"""
    agent_name: str = "experience_agent"
    experiences: list[Experience]  # List of structured experiences
    reasoning: str
    confidence: float

class ExperienceAgentOutput(BaseModel):
    """Output for Experience Agent"""
    experiences: list[Experience]


class GeminiClient:
    """Thin wrapper around Google's Gen AI SDK that exposes an async .generate().
    The SDK call is sync, so we run it in a thread to keep our agent async-friendly.
    Reads GEMINI_KEY from env by default (set via .env already loaded above).
    """
    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None, **default_config):
        self._client = track_genai(genai.Client(api_key=api_key))
        self._model = model
        self._default_config = default_config or {}

    
    async def generate(self, prompt: str, **override_config):
        cfg = {**self._default_config, **(override_config or {})}

        def _call_genai():
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExperienceGeminiSchema,
                temperature=0,
                **cfg  # for determinism
            )
            kwargs = {"model": self._model, "contents": prompt,"config":config}
            if cfg:
                kwargs["config"] = cfg
            resp = self._client.models.generate_content(**kwargs)
            # `resp.text` is the concatenated text output from the SDK
            text = getattr(resp, "text", None)
            if text is None:
                raise RuntimeError("No text in Gemini response")
            return ExperienceGeminiSchema.model_validate_json(text)

        # Run the blocking SDK call in a worker thread to preserve async API
        return await asyncio.to_thread(_call_genai)




class ExperienceAgent:
    """Rewrites experience bullets to highlight relevant aspects"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    @track(name="experienceAgent.create_experience", tags=["agent:ExperienceAgent"],project_name="Auto-apply-AI")
    async def execute(self, task: AgentTask, resume: Resume, plan: TailoringPlan) -> AgentResult:
        """Execute experience rewriting task"""
        
        prompt = f"""You are an EXPERIENCE AGENT specializing in rewriting work experience bullets.

CURRENT EXPERIENCES:
{resume.model_dump_json(indent=2)}

YOUR TASK:
{task.specific_instructions}

PRIORITY EXPERIENCES TO FOCUS ON:
{', '.join(task.priority_items)}

KEY THEMES TO EMPHASIZE:
{', '.join(plan.key_themes)}

JD RESPONSIBILITIES (for framing context):
{task.context.get('responsibilities', [])}

GUIDELINES:
- Rewrite bullets to emphasize JD-relevant aspects
- Use strong action verbs
- Quantify impact where possible (keep existing numbers)
- Frame experiences to highlight transferable skills
- Keep each bullet concise (1-2 lines)
- NEVER fabricate accomplishments
- If an experience isn't relevant, you can suggest deprioritizing it

For each experience entry, analyze and rewrite the bullets.

Return JSON:
{{
    "rewritten_experiences": [
        {{
            "company": "Company Name",
            "title": "Job Title",
            "original_bullets": ["..."],
            "new_bullets": ["rewritten bullet 1", "rewritten bullet 2"],
            "changes_made": "summary of changes"
        }}
    ],
    "reasoning": "overall strategy for rewrites",
    "confidence": 0.88
}}
"""
        
        response = await self.llm.generate(prompt)
        # result_data = self._parse_json_response(response)
        
        return AgentResult(
            agent_name=response.agent_name,
            output=ExperienceAgentOutput(experiences=response.experiences),
            reasoning=response.reasoning,
            confidence=response.confidence
        )
    
    # def _parse_json_response(self, response: str) -> Dict:
    #     import json
    #     import re
    #     json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
    #     if json_match:
    #         return json.loads(json_match.group(1))
    #     return json.loads(response)




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

    experience_task = AgentTask.model_validate({
        "agent_name": "EXPERIENCE AGENT",
        "priority_items": [
            "Addressing the empty 'experience' section",
            "Providing a detailed template for future experience tailoring",
            "Demonstrating integration of JD keywords, quantifiable results, and senior-level responsibilities."
            ],
        "specific_instructions": "State clearly that the 'experience' array in the provided resume is empty, making specific rewriting impossible. Instead, provide a detailed example of *what kind of bullet points* would be created or rewritten if experience data were available. These example bullet points should: 1. Be highly action-oriented and start with strong verbs. 2. Quantify achievements where possible. 3. Explicitly integrate keywords like 'Python', 'React', 'AWS', 'scalable web applications', 'Docker', 'Kubernetes', and 'full stack'. 4. Reflect senior-level responsibilities such as leading projects, designing architectures, optimizing performance, or mentoring. Provide 2-3 illustrative examples.",
        "context": {
            "current_experience": [],
            "job_role": "Senior Full Stack Developer",
            "must_have_skills": ["Python","React","AWS" ],
            "responsibilities": ["Build scalable web applications"],
            "desired_tools": ["Docker","Kubernetes"],
            "years_experience": "5 years"
            }
        })

    tailoring_plan = TailoringPlan.model_validate({
        "strategy": "Given the resume's empty experience section, the primary strategy is to heavily leverage the Summary and Skills sections to create a strong initial impression. We will position John Doe as a Senior Full Stack Developer by emphasizing direct skill matches (Python, React), strategically incorporating 'must-have' keywords like AWS, and highlighting the ability to build 'scalable web applications'. For the experience section, we will provide a detailed template of how bullet points *would* be tailored if data were available, focusing on quantifiable achievements and senior-level responsibilities aligned with the job description.",
        "key_themes": [ "Full Stack Development (Python & React)","Building Scalable Web Applications","Modern Cloud & DevOps Proficiency (AWS, Docker, Kubernetes)","Senior-Level Impact & Leadership"],
        "gap_analysis": {
        "direct_matches": ["Python (skill)", "React (skill)", "5 years experience (summary, aligns with 'Senior' role)"],
        "transferable": ["JavaScript (front-end development, complements React)", "SQL (database interaction, common in web applications)", "BS Computer Science (foundational knowledge)"],
        "gaps": [
            "AWS (CRITICAL 'must-have' skill, missing from resume)",
            "Actual Experience bullet points (MAJOR GAP, resume array is empty)",
            "Demonstrated ability to 'Build scalable web applications' (specific responsibility)",
            "Docker, Kubernetes (desired tools, missing from resume)",
            "Specific achievements demonstrating 'Senior' level capabilities."
        ],
        "how_to_address": "For AWS, Docker, and Kubernetes: Integrate them into the Summary and Skills sections, assuming a foundational understanding or active learning. For the empty experience section: The Experience Agent will provide a robust template demonstrating how bullet points *would* be rewritten, focusing on JD keywords, quantifiable results, and senior-level responsibilities, to guide the user in future resume updates. The Summary will be crafted to strongly imply full-stack and scalable application development capabilities, making the most of the existing '5 years experience'."
        },
        "summary_task": {
        "agent_name": "SUMMARY AGENT",
        "priority_items": [
            "Positioning as 'Senior Full Stack Developer'",
            "Highlighting Python and React expertise",
            "Integrating 'scalable web applications' capability",
            "Strategically including AWS proficiency (even if aspirational or learned)",
            "Emphasizing 5 years of relevant experience."
        ],
        "specific_instructions": "Rewrite the summary to be 2-4 concise sentences. Start by identifying John Doe as an accomplished Senior Full Stack Developer. Explicitly mention strong expertise in Python for backend and React for frontend development. Integrate the ability to design and build 'scalable web applications'. Crucially, include a statement about proficiency in AWS or active development of AWS skills, given its 'must-have' status. Ensure the summary conveys a senior-level perspective on problem-solving and end-to-end development, aligning with the '5 years experience'.",
        "context": {
            "current_summary": "Software engineer with 5 years experience",
            "job_role": "Senior Full Stack Developer",
            "must_have_skills": ["Python","React","AWS"],
            "responsibilities": ["Build scalable web applications"]
        }
        },
        "skills_task": {
        "agent_name": "SKILLS AGENT",
        "priority_items": [
            "Reordering existing skills to prioritize JD matches",
            "Adding 'must-have' skills (AWS)",
            "Adding desired tools (Docker, Kubernetes)",
            "Optimizing for ATS keywords."
        ],
        "specific_instructions": "Reorder the skills list to place 'Python' and 'React' at the top. Directly after, add 'AWS' as a core skill, assuming John Doe possesses at least foundational or actively developing expertise. Integrate 'Docker' and 'Kubernetes' into the list, potentially under a 'DevOps Tools' or 'Cloud Technologies' sub-section if applicable, or directly into the main list. Maintain 'JavaScript' and 'SQL' as supporting skills. Ensure the updated list is optimized for ATS scanning by including all critical keywords.",
        "context": {
            "current_skills": ["Python","JavaScript","React","SQL"],
            "must_have_skills": ["Python", "React","AWS"],
            "desired_tools": ["Docker","Kubernetes"]
        }
        },
        "experience_task": {
        "agent_name": "EXPERIENCE AGENT",
        "priority_items": [
            "Addressing the empty 'experience' section",
            "Providing a detailed template for future experience tailoring",
            "Demonstrating integration of JD keywords, quantifiable results, and senior-level responsibilities."
        ],
        "specific_instructions": "State clearly that the 'experience' array in the provided resume is empty, making specific rewriting impossible. Instead, provide a detailed example of *what kind of bullet points* would be created or rewritten if experience data were available. These example bullet points should: 1. Be highly action-oriented and start with strong verbs. 2. Quantify achievements where possible. 3. Explicitly integrate keywords like 'Python', 'React', 'AWS', 'scalable web applications', 'Docker', 'Kubernetes', and 'full stack'. 4. Reflect senior-level responsibilities such as leading projects, designing architectures, optimizing performance, or mentoring. Provide 2-3 illustrative examples.",
        "context": {
            "current_experience": [],
            "job_role": "Senior Full Stack Developer",
            "must_have_skills": ["Python","React","AWS" ],
            "responsibilities": ["Build scalable web applications"],
            "desired_tools": ["Docker","Kubernetes"],
            "years_experience": "5 years"
        }
        },
        "ats_keywords": ["Senior Full Stack Developer","Python", "React", "AWS","Web Applications","Scalable","Docker","Kubernetes","JavaScript","SQL","Full Stack","Backend","Frontend","Cloud"]
    })

    llm_client = GeminiClient(api_key=os.getenv("GEMINI_KEY"),model="gemini-2.5-flash")
    experience_agent = ExperienceAgent(llm_client)
    plan = await experience_agent.execute(experience_task,resume,tailoring_plan)
    print(json.dumps(plan.model_dump(), indent=2))


if __name__ == '__main__':
    asyncio.run(main())