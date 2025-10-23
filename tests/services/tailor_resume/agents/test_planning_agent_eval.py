import json
import pytest
import os
from pathlib import Path
from auto_apply_ai.services.tailor_resume.agents.planningAgent import PlanningAgent, Resume, JobDesc, GeminiClient


from difflib import SequenceMatcher
def string_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def jaccard_similarity(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)

@pytest.fixture
def planning_agent():
    # Use real Gemini client for evaluation tests
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        pytest.skip("GEMINI_KEY environment variable not set")
    
    llm_client = GeminiClient(api_key=api_key, model="gemini-2.5-flash")
    return PlanningAgent(llm_client=llm_client)

def pytest_generate_tests(metafunc):
    if "case" in metafunc.fixturenames:
        # Load golden cases for parametrization
        path = Path(__file__).parent.parent.parent.parent / "fixtures" / "golden_planning_cases.json"
        with open(path, "r", encoding="utf-8") as f:
            golden_cases = json.load(f)
        metafunc.parametrize("case", golden_cases, ids=[case["name"] for case in golden_cases])

@pytest.mark.asyncio
async def test_plan_evaluation(planning_agent, case):
    resume_input = case["resume"]
    jobdesc_input = case["job_desc"]
    expected = case["expected_plan"]

    # Create Resume and JobDesc model objects (adapt as needed)
    resume = Resume(**resume_input)
    jobdesc = JobDesc(**jobdesc_input)

    plan = await planning_agent.create_plan(resume, jobdesc)

    # Convert TailoringPlan object to dictionary for easier testing
    plan_dict = plan.model_dump()

    # 1. Check basic keys exist
    required_keys = ["strategy", "key_themes", "gap_analysis", "summary_task", "skills_task", "experience_task", "ats_keywords"]
    for key in required_keys:
        assert key in plan_dict, f"Missing key {key} in plan output for case {case['name']}"

    # Strategy similarity
    sim_strategy = string_similarity(plan_dict['strategy'], expected["strategy"])
    assert sim_strategy >= 0.8, f"Strategy similarity too low ({sim_strategy:.2f}) for case {case['name']}"

    # Key themes similarity (as sets)
    expected_themes = set(expected["key_themes"])
    produced_themes = set(plan_dict["key_themes"])
    sim_themes = jaccard_similarity(produced_themes, expected_themes)
    assert sim_themes >= 0.7, f"Key themes overlap too low ({sim_themes:.2f}) for case {case['name']}"

    # ATS keywords similarity
    expected_kw = set(expected["ats_keywords"])
    produced_kw = set(plan_dict["ats_keywords"])
    sim_kw = jaccard_similarity(produced_kw, expected_kw)
    assert sim_kw >= 0.6, f"ATS keywords overlap too low ({sim_kw:.2f}) for case {case['name']}"

    # Gap analysis: direct_matches (set overlap)
    expected_dm = set(expected["gap_analysis"]["direct_matches"])
    produced_dm = set(plan_dict["gap_analysis"]["direct_matches"])
    sim_dm = jaccard_similarity(produced_dm, expected_dm)
    assert sim_dm >= 0.7, f"Direct matches overlap too low ({sim_dm:.2f}) for case {case['name']}"

    # Gap analysis: gaps
    expected_gaps = set(expected["gap_analysis"]["gaps"])
    produced_gaps = set(plan_dict["gap_analysis"]["gaps"])
    sim_gaps = jaccard_similarity(produced_gaps, expected_gaps)
    assert sim_gaps >= 0.5, f"Gaps overlap too low ({sim_gaps:.2f}) for case {case['name']}"
