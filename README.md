# Homework Report: MIT-MAS665-AssignmentsHW-1 
## Build or Analyze Your First Agent
### Builiding my first agent with code



### Track  
**Tech — Create a CrewAI Agent That Represents Me**

---

### What I Built
- A single CrewAI agent named **Coco** that acts as my “digital twin lite.”  
- Coco can:  
  - Deliver who Coco is based on a persona description  
  - Explain the Chinese education ecosystem  
  - Draft client emails  
  - Answer Q&A from potential clients about an education bootcamp for languages product  

---

### Implementation Summary
- Agent defined in `src/edu_sales/config/agents.yaml` as `coco`.  
- Tasks defined in `src/edu_sales/config/tasks.yaml` with inputs.  
- Custom tools in `src/edu_sales/tools/`:  
  - **ProfileResponder**: reads `knowledge/persona_coco.md`  
  - **ChinaEducationExplainer**: reads `knowledge/china_education.md`  
  - **EmailDraftTool**: creates a structured email  
  - **BootcampFAQTool**: reads `knowledge/bootcamp_faq.md`  
- Crew wiring in `src/edu_sales/crew.py` attaches all tools to the Coco agent.  
- `src/edu_sales/main.py` seeds example inputs to run end-to-end.  

---

### How To Run
1. Add your `LLM KEY` to `.env` if required by your runtime.  
2. From the project root, run:  
3. Adjust inputs in `src/edu_sales/main.py` to test different prompts.  

---

### What Worked
- YAML agent/task definitions kept setup simple and transparent.  
- Pydantic input schemas for tools improved reliability and ergonomics.  
- Markdown knowledge base made the agent’s grounding easy to audit and edit.  

---

### What Didn’t
- Relying only on an AI agent from a browser plus a separate VS Code setup was inefficient; it required programming with the entire code directory (e.g., using Cursor).  
- Many manual changes were necessary, and the code frequently broke—likely due to the lack of CrewAI timeline/history examples.  
- As someone from a non-technical background, I had to search actively for answers and rely on help from experienced developers. This was educational but slowed productivity due to the steep learning curve.  
- The **ProfileResponder** tool (`edu_sales/src/edu_sales/tools/profile_responder.py`) had syntax errors that were initially difficult to debug.  
- No live web browsing/search meant answers were restricted to the provided knowledge base.  
- If the FAQ lacks details, the agent must explicitly call out these gaps.  
- Tokens can be consumed quickly if not used carefully.  
- The LLM’s outputs were sometimes unreliable (e.g., DeepSeek model returned Python code representing the desired output instead of human-readable text). This means `RULES.md` also has to be enforced for third-party models.
- AI Agents are often busy! Even the paid versions!

---

### What I Learned
- CrewAI’s decorators and YAML configuration enable fast iteration on agent behavior.  
- Small, composable tools that surface authoritative text lead to grounded and reliable outputs.  
- Using clear `expected_output` fields improves consistency across runs.  
- There are many open-tier tokens available for use. I initially paid over $100 to OpenAI, but later discovered that accounts set up via Google include $300 worth of tokens. OpenRoute is another great example. Using agents effectively is as much about resource management as technical skill.  
- The business considerations of deploying AI systems are just as significant as the technical aspects.  
- Version control discipline is vital: my original repository became cluttered with excessive commits, which eventually led me to create a fresh Git repo to restore clarity to the project’s history.  
