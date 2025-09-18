# MIT-MAS665-AssignmentsHW-1
Here I am building the greatest agent of all :)


Homework Report: Build or Analyze Your First Agent
==================================================

Track: Tech — Create a CrewAI Agent That Represents Me

What I Built
------------
- A single CrewAI agent named Coco that acts as my “digital twin lite.”
- Coco can:
  - Deliver who Coco is based on a persona description
  - Explain the Chinese education ecosystem
  - Draft client emails
  - Answer Q&A from potential clients about a bootcamp product

Implementation Summary
----------------------
- Agent defined in `src/edu_sales/config/agents.yaml` as `coco`.
- Tasks defined in `src/edu_sales/config/tasks.yaml` with inputs.
- Custom tools in `src/edu_sales/tools/`:
  - ProfileResponder: reads `knowledge/persona_coco.md`
  - ChinaEducationExplainer: reads `knowledge/china_education.md`
  - EmailDraftTool: creates a structured email
  - BootcampFAQTool: reads `knowledge/bootcamp_faq.md`
- Crew wiring in `src/edu_sales/crew.py` attaches all tools to the Coco agent.
- `src/edu_sales/main.py` seeds example inputs to run end-to-end.

How To Run
----------
1) Add your `OPENAI_API_KEY` to `.env` if required by your runtime.
2) From project root:
   ```bash
   uv run crewai run
   ```
3) Adjust inputs in `src/edu_sales/main.py` to test different prompts.

What Worked
-----------
- YAML agent/task definitions kept setup simple and transparent.
- Pydantic input schemas for tools improved reliability and ergonomics.
- Markdown knowledge base made the agent’s grounding easy to audit and edit.

What Didn’t
-----------
- Using only AI agent from a browser and a seperated VS code did a very bad job, it had to be programmed with the entire code dir (in example with Cursor)
- A lot of manual changes had to be made. The code breaks often, probabily due to the lack of the history timeline examples of CrewAi
- As a person coming from a non-technical background, I had to actively find the answers and use the help of more experienced developers. One one hand, I learned so much from the process, but on the down-side the productivety and learning-curve was slower than expected.
- The persona (edu_sales/src/edu_sales/tools/profile_responder.py-->ProfileResponder) syntax errors were hard to debug at first.
- No live web search/browsing; answers are limited to provided knowledge.
- If the FAQ lacks a detail, the agent must explicitly call out the gap.
- Tokens can run out fast if you don't understand what you're doing
- The LLM's answer can be very weird. It's very hard to trust it. In example, if I use DeepSeek model I get a Python code answer that represents the desired output instead of human readable code. So "RULES.md" have to be applied also to the 3rd party LLMs used.

What I Learned
--------------
- CrewAI’s decorators + YAML enable fast iteration on agent behavior.
- Small, composable tools that surface authoritative text are effective for grounded outputs.
- Clear expected_output fields improve consistency across runs.
- There are so many open tier tokens to be used, I started by paying to OpenAI > 100$ but after some research I now understand this technology is much more accessible than ever before
- Working with commits is so important. As I was working on this project, the commits in my original repo expanded so much. I ended up creating an entirely new git repo because the history graph was such a mess.
- 

