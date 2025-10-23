import pytest
from auto_apply_ai.services.tailor_resume.agents.planningAgent import PlanningAgent, GeminiClient, Resume, JobDesc

class DummyLLM:
    async def generate(self, prompt: str, **cfg):
        # Simulate returning a JSON string
        return {
          "strategy": "Focus on Python full-stack",
          "key_themes": ["Python","React","AWS"],
          "gap_analysis": {
            "direct_matches": ["Python","React"],
            "transferable": ["JavaScript"],
            "gaps": ["AWS experience"],
            "how_to_address": "Highlight transferable and plan training"
          },
          "summary_task": {
            "agent_name": "summary",
            "priority_items": ["Strategy"],
            "specific_instructions": "Rewrite summary emphasising full-stack Python",
            "context": {"key_info": ["Python", "React"]}
          },
          "skills_task": { "…"},
          "experience_task": { "…" },
          "ats_keywords": ["Python", "React", "AWS"]
        }

@pytest.fixture
def planning_agent():
    dummy_llm = DummyLLM()
    return PlanningAgent(llm_client=dummy_llm)

@pytest.fixture
def simple_resume():
    return Resume(id="r1", basics={"name":"Alice"}, summary="Developer", skills=["Python","Javascript"], experience=[], education="BS CS")

@pytest.fixture
def simple_jobdesc():
    return JobDesc(role="Full-stack Dev", must_have=["Python","React","AWS"], responsibilities=["Build web apps"], tools=["Docker","Kubernetes"], keywords=["full-stack"])



@pytest.mark.asyncio
async def test_create_plan_happy_path(planning_agent, simple_resume, simple_jobdesc):
    plan = await planning_agent.create_plan(simple_resume, simple_jobdesc)
    # Because dummy returns known structure, we can assert:
    assert plan['strategy'] == "Focus on Python full-stack"
    assert "Python" in plan['key_themes']
    assert "AWS experience" in plan['gap_analysis']['gaps']

@pytest.mark.asyncio
async def test_create_plan_missing_fields( simple_resume, simple_jobdesc):
    # Have LLM return JSON missing a key
    class BadLLM:
        async def generate(self, prompt: str, **cfg):
            return {"strategy":"foo"}  # missing many fields
    agent = PlanningAgent(llm_client=BadLLM())
    plan = await agent.create_plan(simple_resume, simple_jobdesc)
    # Current implementation returns whatever LLM gives it, so we just check it returns something
    assert plan is not None
    assert plan['strategy'] == "foo"

