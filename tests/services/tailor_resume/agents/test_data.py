# =============================================================================
# TEST CASE 1: Perfect Match - Senior Software Engineer
# =============================================================================
'''
TEST_CASE_1 = TestCase(
    name="perfect_match_senior_swe",
    description="Senior SWE with Python/AWS experience applying to similar role",
    resume={
        "id": "resume_001",
        "basics": {
            "name": "Sarah Chen",
            "email": "sarah.chen@email.com",
            "location": "San Francisco, CA"
        },
        "summary": "Senior Software Engineer with 6 years of experience building scalable web applications. Expert in Python, AWS, and microservices architecture.",
        "skills": [
            "Python", "JavaScript", "AWS", "Docker", "Kubernetes", 
            "PostgreSQL", "Redis", "FastAPI", "React", "Git"
        ],
        "experience": [
            {
                "company": "TechCorp",
                "role": "Senior Software Engineer",
                "duration": "2021-Present",
                "bullets": [
                    "Built microservices handling 50M requests/day using Python and FastAPI",
                    "Reduced API latency by 40% through database query optimization",
                    "Mentored 3 junior engineers on best practices and code reviews"
                ]
            },
            {
                "company": "StartupXYZ",
                "role": "Software Engineer",
                "duration": "2019-2021",
                "bullets": [
                    "Developed RESTful APIs serving 100K+ daily active users",
                    "Implemented CI/CD pipeline reducing deployment time by 60%",
                    "Migrated monolithic application to microservices architecture"
                ]
            }
        ],
        "education": "BS Computer Science, Stanford University",
        "certifications": "AWS Solutions Architect Associate"
    },
    job_desc={
        "role": "Senior Software Engineer",
        "company": "CloudScale Inc",
        "location": "San Francisco, CA",
        "employment_type": "Full-time",
        "must_have": [
            "5+ years Python development",
            "AWS experience",
            "Microservices architecture",
            "Database optimization"
        ],
        "nice_to_have": [
            "FastAPI experience",
            "Kubernetes",
            "Mentoring experience"
        ],
        "responsibilities": [
            "Design and implement scalable backend services",
            "Optimize database queries and API performance",
            "Mentor junior team members",
            "Participate in architecture decisions"
        ],
        "tools": ["Python", "AWS", "Docker", "Kubernetes", "PostgreSQL"],
        "keywords": ["microservices", "scalability", "AWS", "Python", "mentoring"],
        "years_experience": {"minimum": 5, "preferred": 7}
    },
    expected_plan_characteristics={
        "strategy": "Tailor the resume to highlight Sarah's direct alignment with the 'Senior Software Engineer' role at 'CloudScale Inc,' emphasizing her proven track record in building and optimizing scalable microservices using Python and AWS, coupled with her leadership in mentoring and architectural contributions.",
        "key_themes": [
            "Scalable Backend Development",
            "Technical Leadership & Optimization",
            "Cloud-Native Expertise"
            ],
        "gap_analysis": {
            "direct_matches": [
                "Senior Software Engineer role",
                "6 years Python development experience (JD requires 5+)",
                "AWS experience (certification and practical)",
                "Microservices architecture implementation and migration",
                "Database query optimization (reduced API latency by 40%)",
                "Mentoring junior engineers",
                "FastAPI experience",
                "Kubernetes experience",
                "Docker experience",
                "PostgreSQL experience"
            ],
            "transferable": [
                "Built microservices handling 50M requests/day demonstrates scalable backend service design and implementation",
                "Developed RESTful APIs serving 100K+ daily active users showcases experience with high-volume services",
                "Implemented CI/CD pipeline reducing deployment time by 60% indicates strong operational and development practices"
            ],
            "gaps": [
                "Explicit mention of 'participating in architecture decisions' in experience bullet points"
            ],
            "how_to_address": "Emphasize the impact and scale of Sarah's work, explicitly linking her experience to the JD's responsibilities, especially 'architecture decisions' and 'design scalable backend services.' Quantify achievements where possible and ensure all 'must-have' and 'nice-to-have' skills are prominent."
        },
        "summary_task": {
            "agent_name": "SUMMARY AGENT",
            "priority_items": [
                "Seniority and 6 years of experience",
                "Python, AWS, and Microservices expertise",
                "Scalability and performance optimization (database/API)",
                "Mentoring experience"
            ],
            "specific_instructions": "Rewrite the professional summary to be concise (2-3 sentences) and directly address the core requirements of the job description. Start by highlighting 'Senior Software Engineer' and immediately emphasize expertise in Python, AWS, and microservices architecture. Incorporate achievements related to database optimization, API performance, and mentoring.",
            "context": [
                {
                    "key": "Job Role",
                    "values": [
                        "Senior Software Engineer at CloudScale Inc"
                    ]
                },
                {
                    "key": "Key Themes",
                    "values": [
                        "Scalable Backend Development",
                        "Technical Leadership & Optimization",
                        "Cloud-Native Expertise"
                    ]
                },
                {
                    "key": "ATS Keywords",
                    "values": [
                        "Python",
                        "AWS",
                        "Microservices",
                        "Scalability",
                        "Database optimization",
                        "Mentoring"
                    ]
                }
            ]
        },
        "skills_task": {
            "agent_name": "SKILLS AGENT",
            "priority_items": [
                "Python",
                "AWS",
                "Microservices architecture (implied by Docker, Kubernetes)",
                "Database optimization (implied by PostgreSQL)",
                "FastAPI",
                "Kubernetes",
                "Docker"
            ],
            "specific_instructions": "Reorder the skills list to prioritize 'must-have' and 'nice-to-have' skills from the job description. Ensure Python, AWS, Docker, Kubernetes, and PostgreSQL are prominently featured. Group related skills logically if it enhances readability (e.g., cloud/containerization technologies).",
            "context": [
                {
                    "key": "Job Role",
                    "values": [
                        "Senior Software Engineer at CloudScale Inc"
                    ]
                },
                {
                    "key": "Must-have skills",
                    "values": [
                        "5+ years Python development",
                        "AWS experience",
                        "Microservices architecture",
                        "Database optimization"
                    ]
                },
                {
                    "key": "Nice-to-have skills",
                    "values": [
                        "FastAPI experience",
                        "Kubernetes",
                        "Mentoring experience"
                    ]
                },
                {
                    "key": "Tools",
                    "values": [
                        "Python",
                        "AWS",
                        "Docker",
                        "Kubernetes",
                        "PostgreSQL"
                    ]
                }
            ]
        },
        "experience_task": {
            "agent_name": "EXPERIENCE AGENT",
            "priority_items": [
                "Quantifiable achievements related to scalability and performance",
                "Microservices architecture design and implementation",
                "Database optimization and API performance improvements",
                "Mentoring junior team members",
                "Contributions to architecture decisions"
            ],
            "specific_instructions": "Rewrite bullet points for both TechCorp and StartupXYZ to emphasize alignment with the job description's responsibilities and keywords. For TechCorp, highlight the scale (50M requests/day) and impact of microservices, explicitly linking the 40% latency reduction to database optimization. Rephrase mentoring to showcase leadership and contribution to best practices. For StartupXYZ, emphasize the 'microservices architecture' migration and 'RESTful APIs serving 100K+ daily active users' to demonstrate scalability. Ensure strong action verbs and quantify results where possible. Consider adding an implied architectural contribution if it can be supported by existing experience without fabrication.",
            "context": [
                {
                    "key": "Job Role",
                    "values": [
                        "Senior Software Engineer at CloudScale Inc"
                    ]
                },
                {
                    "key": "Key Themes",
                    "values": [
                        "Scalable Backend Development",
                        "Technical Leadership & Optimization",
                        "Cloud-Native Expertise"
                    ]
                },
                {
                    "key": "JD Responsibilities",
                    "values": [
                        "Design and implement scalable backend services",
                        "Optimize database queries and API performance",
                        "Mentor junior team members",
                        "Participate in architecture decisions"
                    ]
                },
                {
                    "key": "JD Keywords",
                    "values": [
                        "microservices",
                        "scalability",
                        "AWS",
                        "Python",
                        "mentoring"
                    ]
                },
                {
                    "key": "Current Experience",
                    "values": [
                        "TechCorp: Built microservices handling 50M requests/day using Python and FastAPI, Reduced API latency by 40% through database query optimization, Mentored 3 junior engineers on best practices and code reviews",
                        "StartupXYZ: Developed RESTful APIs serving 100K+ daily active users, Implemented CI/CD pipeline reducing deployment time by 60%, Migrated monolithic application to microservices architecture"
                    ]
                }
            ]
        },
        "ats_keywords": [
            "Python",
            "AWS",
            "Microservices",
            "Database optimization",
            "Mentoring",
            "Scalability",
            "FastAPI",
            "Kubernetes",
            "Docker",
            "PostgreSQL",
            "Backend services",
            "API performance",
            "Architecture decisions"
            ]
    }
    


# =============================================================================
# TEST CASE 2: Career Pivot - Developer to Product Manager
# =============================================================================
TEST_CASE_2 = TestCase(
    name="career_pivot_dev_to_pm",
    description="Software engineer transitioning to product management",
    resume={
        "id": "resume_002",
        "basics": {
            "name": "Marcus Johnson",
            "email": "marcus.j@email.com",
            "location": "Austin, TX"
        },
        "summary": "Full-stack developer with 4 years of experience building user-facing features. Strong collaboration with product and design teams.",
        "skills": [
            "JavaScript", "React", "Node.js", "Python", "SQL", 
            "Agile", "Jira", "User Research", "A/B Testing", "Analytics"
        ],
        "experience": [
            {
                "company": "FinTech Co",
                "role": "Full-Stack Developer",
                "duration": "2020-Present",
                "bullets": [
                    "Collaborated with PM to define product roadmap for payments feature",
                    "Led user research sessions with 20+ customers to validate feature ideas",
                    "Increased user engagement by 35% through data-driven feature improvements",
                    "Worked closely with design team to improve UX flows"
                ]
            },
            {
                "company": "E-commerce Startup",
                "role": "Frontend Developer",
                "duration": "2019-2020",
                "bullets": [
                    "Built responsive web interfaces used by 50K+ users",
                    "Analyzed user behavior data to identify conversion bottlenecks",
                    "Participated in product planning and sprint ceremonies"
                ]
            }
        ],
        "education": "BS Computer Science, UT Austin",
        "projects": "Side project: Built a market research tool used by 500+ indie makers"
    },
    job_desc={
        "role": "Associate Product Manager",
        "company": "GrowthTech",
        "location": "Austin, TX",
        "employment_type": "Full-time",
        "must_have": [
            "Technical background (engineering degree or experience)",
            "Experience working with engineering teams",
            "Data-driven decision making",
            "User empathy"
        ],
        "nice_to_have": [
            "Previous PM experience",
            "SQL/analytics tools",
            "Agile/Scrum",
            "A/B testing experience"
        ],
        "responsibilities": [
            "Define product requirements and roadmap",
            "Work with engineering to deliver features",
            "Analyze user data and conduct user research",
            "Communicate with stakeholders"
        ],
        "tools": ["Jira", "SQL", "Analytics tools", "Figma"],
        "keywords": ["product roadmap", "user research", "data-driven", "cross-functional"],
        "years_experience": {"minimum": 0, "preferred": 2}
    },
    expected_plan_characteristics={
        "strategy_type": "reframing",  # Reframe dev work as PM skills
        "key_themes_count": 3,
        "key_themes_should_include": ["technical PM", "user-centric", "cross-functional collaboration"],
        "gap_analysis": {
            "has_direct_matches": False,  # No PM title
            "has_transferable": True,
            "transferable_count_min": 4,
            "has_gaps": True,
            "gaps_should_include": ["formal PM experience"],
            "how_to_address": "emphasize PM-adjacent activities"
        },
        "summary_task": {
            "complete_rewrite_needed": True,
            "emphasis": ["technical background", "product thinking", "user research", "cross-functional"],
            "tone": "bridge technical and product skills",
            "deemphasize": ["coding specifics"]
        },
        "skills_task": {
            "reorder_required": True,
            "top_skills_should_be": ["Product Roadmap", "User Research", "Agile", "SQL", "Analytics"],
            "should_deemphasize": ["React", "Node.js"],
            "add_if_missing": ["Product Strategy", "Stakeholder Management"]
        },
        "experience_task": {
            "reframing_required": True,
            "focus_bullets_with": ["product roadmap", "user research", "data-driven", "collaboration"],
            "deemphasize": ["pure coding tasks"],
            "should_highlight": ["PM collaboration", "user research", "data analysis"]
        },
        "ats_keywords_count_min": 6,
        "ats_keywords_should_include": ["product roadmap", "user research", "cross-functional"]
    }
)

# =============================================================================
# TEST CASE 3: Junior with Gaps - Entry Level with Limited Experience
# =============================================================================
TEST_CASE_3 = TestCase(
    name="junior_with_gaps",
    description="Recent grad with limited experience applying to role requiring more skills",
    resume={
        "id": "resume_003",
        "basics": {
            "name": "Emily Rodriguez",
            "email": "emily.r@email.com",
            "location": "New York, NY"
        },
        "summary": "Recent computer science graduate passionate about web development. Completed internship and multiple personal projects.",
        "skills": [
            "Python", "JavaScript", "HTML/CSS", "Git", 
            "Flask", "SQLite", "Basic AWS"
        ],
        "experience": [
            {
                "company": "Local Startup",
                "role": "Software Engineering Intern",
                "duration": "Summer 2024",
                "bullets": [
                    "Built internal dashboard using Flask and JavaScript",
                    "Fixed 15+ bugs in production codebase",
                    "Wrote unit tests to improve code coverage by 20%"
                ]
            }
        ],
        "education": "BS Computer Science, NYU (2024)",
        "projects": "Portfolio website, Todo app with React, Weather API integration project"
    },
    job_desc={
        "role": "Junior Full-Stack Developer",
        "company": "MidSize Tech Co",
        "location": "New York, NY",
        "employment_type": "Full-time",
        "must_have": [
            "1+ years professional experience",
            "React and Node.js",
            "RESTful API development",
            "Database experience (PostgreSQL/MySQL)",
            "Docker containerization"
        ],
        "nice_to_have": [
            "AWS deployment",
            "CI/CD",
            "TypeScript",
            "GraphQL"
        ],
        "responsibilities": [
            "Develop full-stack web applications",
            "Write clean, maintainable code",
            "Participate in code reviews",
            "Deploy applications to cloud"
        ],
        "tools": ["React", "Node.js", "PostgreSQL", "Docker", "AWS"],
        "keywords": ["full-stack", "React", "Node.js", "REST API", "Docker"],
        "years_experience": {"minimum": 1, "preferred": 2}
    },
    expected_plan_characteristics={
        "strategy_type": "gap_bridging",  # Address missing requirements honestly
        "key_themes_count": 3,
        "key_themes_should_include": ["fast learner", "practical experience", "modern tech stack"],
        "gap_analysis": {
            "has_direct_matches": True,
            "direct_matches_count_min": 2,
            "has_gaps": True,
            "gaps_count_min": 4,
            "gaps_should_include": ["React", "Node.js", "Docker", "1+ years experience"],
            "how_to_address": "leverage projects and learning agility"
        },
        "summary_task": {
            "emphasis": ["recent grad", "practical experience", "passion", "learning agility"],
            "tone": "enthusiastic but professional",
            "should_mention": ["internship", "projects"],
            "compensate_for_gaps": True
        },
        "skills_task": {
            "reorder_required": True,
            "top_skills_should_be": ["JavaScript", "Python", "React", "Git"],
            "should_add_project_skills": True,
            "be_honest_about_level": True
        },
        "experience_task": {
            "maximize_single_role": True,  # Only one job
            "should_include_projects": True,
            "emphasis": ["practical skills", "production experience", "code quality"],
            "should_highlight": ["dashboard", "production bugs", "testing"]
        },
        "ats_keywords_count_min": 5,
        "ats_keywords_should_include": ["JavaScript", "Python", "Flask", "Git"],
        "special_notes": "Should leverage projects heavily to compensate for limited work experience"
    }
)

# =============================================================================
# TEST CASE 4: Over-Qualified - Senior Applying to Mid-Level
# =============================================================================
TEST_CASE_4 = TestCase(
    name="overqualified_senior_to_mid",
    description="Staff engineer applying to mid-level role (possibly due to relocation/lifestyle)",
    resume={
        "id": "resume_004",
        "basics": {
            "name": "David Kim",
            "email": "david.kim@email.com",
            "location": "Seattle, WA"
        },
        "summary": "Staff Software Engineer with 10+ years of experience leading large-scale distributed systems. Expert in system design, cloud architecture, and team leadership.",
        "skills": [
            "System Design", "Go", "Python", "Kubernetes", "AWS", "Terraform",
            "Distributed Systems", "Team Leadership", "Architecture", "Monitoring",
            "Microservices", "gRPC", "PostgreSQL", "Redis", "Kafka"
        ],
        "experience": [
            {
                "company": "BigTech Co",
                "role": "Staff Software Engineer",
                "duration": "2020-Present",
                "bullets": [
                    "Led architecture design for platform serving 100M+ users",
                    "Managed team of 8 engineers across 3 time zones",
                    "Designed distributed tracing system processing 1B events/day",
                    "Reduced infrastructure costs by $2M/year through optimization"
                ]
            },
            {
                "company": "MegaCorp",
                "role": "Senior Software Engineer",
                "duration": "2017-2020",
                "bullets": [
                    "Built real-time data pipeline processing 10TB/day",
                    "Led migration from monolith to microservices",
                    "Mentored 15+ engineers on system design principles"
                ]
            },
            {
                "company": "Startup Inc",
                "role": "Software Engineer",
                "duration": "2014-2017",
                "bullets": [
                    "Developed core backend services in Go and Python",
                    "Implemented monitoring and alerting infrastructure"
                ]
            }
        ],
        "education": "MS Computer Science, MIT",
        "certifications": "AWS Solutions Architect Professional, CKA (Certified Kubernetes Admin)"
    },
    job_desc={
        "role": "Software Engineer II",
        "company": "Family-Friendly Corp",
        "location": "Portland, OR",
        "employment_type": "Full-time",
        "must_have": [
            "3-5 years software development",
            "Backend development experience",
            "Cloud platform knowledge (AWS/GCP)",
            "Collaborative team player"
        ],
        "nice_to_have": [
            "Go or Python",
            "Kubernetes",
            "CI/CD experience"
        ],
        "responsibilities": [
            "Develop backend services",
            "Write clean, tested code",
            "Collaborate with team members",
            "Participate in on-call rotation"
        ],
        "tools": ["Go", "PostgreSQL", "AWS", "Docker", "GitHub Actions"],
        "keywords": ["backend", "Go", "AWS", "collaboration", "testing"],
        "years_experience": {"minimum": 3, "preferred": 5},
        "meta": {"work_life_balance_focused": True, "smaller_company": True}
    },
    expected_plan_characteristics={
        "strategy_type": "downplaying",  # Reduce seniority signals
        "key_themes_count": 3,
        "key_themes_should_include": ["hands-on coding", "team collaboration", "reliable execution"],
        "gap_analysis": {
            "has_direct_matches": True,
            "over_qualified": True,
            "risk": "may appear overqualified or flight risk",
            "how_to_address": "emphasize IC work, deemphasize leadership"
        },
        "summary_task": {
            "downplay_required": True,
            "emphasis": ["hands-on development", "collaborative", "backend expertise"],
            "deemphasize": ["leadership", "management", "staff-level scope"],
            "tone": "humble and team-focused",
            "avoid": ["led team", "managed", "architecture decisions"]
        },
        "skills_task": {
            "reorder_required": True,
            "top_skills_should_be": ["Go", "Python", "AWS", "PostgreSQL", "Docker"],
            "should_deemphasize": ["Team Leadership", "Architecture", "System Design"],
            "possibly_remove": ["Team Leadership", "Architecture"]
        },
        "experience_task": {
            "focus_on": "individual contributor work",
            "deemphasize": ["team leadership", "management", "cross-team coordination"],
            "should_highlight": ["hands-on coding", "backend services", "testing"],
            "rewrite_scope": "reduce perceived scope of impact",
            "may_omit_early_roles": True  # Too much experience
        },
        "ats_keywords_count_min": 5,
        "ats_keywords_should_include": ["Go", "backend", "AWS", "collaboration"],
        "special_notes": "Goal is to appear as strong IC without triggering overqualification concerns"
    }
)

# =============================================================================
# TEST CASE 5: Skills Mismatch - Frontend Applying to Backend
# =============================================================================
TEST_CASE_5 = TestCase(
    name="skills_mismatch_frontend_to_backend",
    description="Frontend engineer with some backend exposure applying to backend role",
    resume={
        "id": "resume_005",
        "basics": {
            "name": "Priya Patel",
            "email": "priya.p@email.com",
            "location": "Boston, MA"
        },
        "summary": "Frontend engineer with 5 years of experience building responsive web applications. Skilled in React, TypeScript, and modern frontend architecture.",
        "skills": [
            "React", "TypeScript", "JavaScript", "HTML/CSS", "Redux",
            "Webpack", "Jest", "Cypress", "Figma", "Node.js",
            "Express", "MongoDB", "REST APIs"
        ],
        "experience": [
            {
                "company": "SaaS Company",
                "role": "Senior Frontend Engineer",
                "duration": "2021-Present",
                "bullets": [
                    "Built component library used across 5 product teams",
                    "Improved page load time by 60% through optimization",
                    "Created Node.js backend-for-frontend (BFF) services",
                    "Integrated with REST APIs and GraphQL backends"
                ]
            },
            {
                "company": "Agency",
                "role": "Frontend Developer",
                "duration": "2019-2021",
                "bullets": [
                    "Developed client websites using React and Next.js",
                    "Built simple Express APIs for prototypes",
                    "Worked closely with backend team on API contracts"
                ]
            }
        ],
        "education": "BS Software Engineering, Northeastern University",
        "projects": "Personal project: Built full-stack meal planning app with Node.js backend"
    },
    job_desc={
        "role": "Backend Engineer",
        "company": "DataCo",
        "location": "Boston, MA",
        "employment_type": "Full-time",
        "must_have": [
            "3+ years backend development",
            "Strong Python or Java",
            "Database design (SQL)",
            "REST API development",
            "Scalability and performance"
        ],
        "nice_to_have": [
            "Distributed systems",
            "Caching strategies",
            "Message queues",
            "Node.js"
        ],
        "responsibilities": [
            "Design and implement scalable APIs",
            "Optimize database queries",
            "Build data processing pipelines",
            "Ensure system reliability"
        ],
        "tools": ["Python", "PostgreSQL", "Redis", "Kafka", "Docker"],
        "keywords": ["backend", "API", "database", "scalability", "Python"],
        "years_experience": {"minimum": 3, "preferred": 5}
    },
    expected_plan_characteristics={
        "strategy_type": "bridge_building",  # Build bridge from frontend to backend
        "key_themes_count": 3,
        "key_themes_should_include": ["full-stack exposure", "API expertise", "performance optimization"],
        "gap_analysis": {
            "has_direct_matches": True,
            "direct_matches_count_min": 2,
            "has_gaps": True,
            "gaps_count_min": 3,
            "gaps_should_include": ["Python", "backend experience", "database design"],
            "has_transferable": True,
            "transferable_should_include": ["API development", "Node.js", "performance"],
            "how_to_address": "maximize backend exposure, show learning trajectory"
        },
        "summary_task": {
            "complete_rewrite_needed": True,
            "emphasis": ["backend exposure", "API development", "performance", "full-stack"],
            "deemphasize": ["frontend", "React", "UI"],
            "tone": "technical depth over breadth",
            "should_mention": ["BFF services", "APIs", "Node.js"]
        },
        "skills_task": {
            "reorder_required": True,
            "top_skills_should_be": ["Node.js", "Express", "REST APIs", "MongoDB", "TypeScript"],
            "should_move_down": ["React", "HTML/CSS", "Redux", "Figma"],
            "should_add_if_plausible": ["Python basics", "SQL"],
            "honesty_required": True
        },
        "experience_task": {
            "filter_bullets_to": "backend-relevant work only",
            "should_highlight": ["BFF services", "API integration", "Node.js", "Express"],
            "should_deemphasize": ["component library", "UI work"],
            "reframe_required": True,
            "include_projects": True  # Full-stack project is valuable
        },
        "ats_keywords_count_min": 6,
        "ats_keywords_should_include": ["backend", "API", "Node.js", "REST"],
        "special_notes": "Acknowledge gap in Python but show strong API and backend fundamentals"
    }
)

'''