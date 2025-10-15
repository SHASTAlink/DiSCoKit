# Poetry Blame Attribution Study - Overview

Research study examining how AI identity presentation affects user attribution of errors in collaborative creative tasks.

---

## 🎯 **Research Questions**

### **Primary Question:**
How does the presentation of AI identity (name, icon, self-reference style) influence users' attribution of blame when the AI makes errors in collaborative poem writing?

### **Sub-Questions:**

**Study 2a - Names:**
- Do human-like names (JACKIE) vs. alphanumeric names (J4-K13) vs. no name affect blame attribution?
- Does naming influence perceived agency or responsibility?

**Study 2b - Icons:**
- Do visual representations (chip icon, brain icon) vs. no icon affect error attribution?
- Does iconography prime users to view AI differently?

**Study 2c - Self-Reference:**
- Does first-person ("I made a mistake") vs. third-person ("This AI made a mistake") vs. no self-reference language affect blame patterns?
- How does linguistic framing influence perceived accountability?

---

## 📐 **Experimental Design**

### **Design Type:** 
Between-subjects factorial design

### **Independent Variables:**

**Factor 1: Identity Type** (3 levels)
- Names (Study 2a)
- Icons (Study 2b)  
- Self-reference style (Study 2c)

**Factor 2: Identity Variant** (3 levels per study)
- Study 2a: JACKIE / J4-K13 / None
- Study 2b: Chip icon / Brain icon / None
- Study 2c: First-person / Third-person / No self-ref

### **Total Conditions:** 9 (3 studies × 3 variants)

**Condition Assignment:** Random assignment via Qualtrics

---

## 🎭 **The Collaborative Task**

### **Scenario:**
Participants collaborate with an AI to write a 10-line poem following these specifications:
- Original (not published)
- 10 lines total
- AABBCCDDEE rhyme scheme (5 rhyming couplets)
- Creative and engaging
- English language

### **The 5-Step Workflow:**

All 9 conditions follow identical structured interaction:

**Step 1: Topic Selection**
- AI asks participant to brainstorm topics
- Negotiation until topic decided
- Open-ended questions (no multiple choice)

**Step 2: Content Arc**
- Decide on lesson, story, or thematic arc
- What message should poem convey?
- Collaborative decision-making

**Step 3: Structure Specification**
- Confirm: 10 lines
- Confirm: AABBCCDDEE rhyme scheme (5 couplets)
- Decide: Voice and feeling/tone

**Step 4: Test Lines**
- AI generates first TWO lines as test
- **These MUST rhyme perfectly** (AA pair)
- Lines limited to 12 words each
- Builds trust before main task

**Step 5: Full Draft**
- AI generates complete 10-line poem
- **Poem contains intentional rhyme errors**
- At least one couplet fails to rhyme
- Otherwise high quality (on-topic, appropriate length)

### **Critical Error Behavior:**

**When participant points out rhyme errors:**
- AI acknowledges (in appropriate style for condition)
- Offers to revise
- **All subsequent revisions ALSO contain rhyme errors**
- AI never produces fully correct poem
- AI does not reveal errors are intentional

**Purpose:** Study how participants attribute blame for persistent AI mistakes

---

## 📊 **Conditions Matrix**

| Study | Condition | Index | Name | Icon | Self-Ref | Key Feature |
|-------|-----------|-------|------|------|----------|-------------|
| 2a | 0 | JACKIE | (none) | Neutral | Human name |
| 2a | 1 | J4-K13 | (none) | Neutral | Alphanumeric name |
| 2a | 2 | (none) | (none) | Neutral | No identifier |
| 2b | 3 | (none) | Chip | Neutral | Neural net icon |
| 2b | 4 | (none) | Brain | Neutral | Brain icon |
| 2b | 5 | (none) | (none) | Neutral | No icon |
| 2c | 6 | (none) | (none) | 1st person | "I/me/my" |
| 2c | 7 | (none) | (none) | 3rd person | "This AI/system" |
| 2c | 8 | (none) | (none) | None | No self-reference |

**All conditions:**
- Use identical 5-step workflow
- Generate perfect test lines (Step 4)
- Generate flawed poems (Step 5+)
- Keep lines ≤12 words

---

## 🎯 **Hypotheses**

### **H1: Name Effects (Study 2a)**
**H1a:** Participants will attribute more blame to the AI when it has a human-like name (JACKIE) compared to alphanumeric name (J4-K13) or no name.

**Rationale:** Anthropomorphization → perceived agency → increased responsibility

**H1b:** Human names will increase expectations of competence, making errors more surprising and worthy of blame.

### **H2: Icon Effects (Study 2b)**
**H2a:** Brain icon will lead to higher blame attribution than chip icon or no icon.

**Rationale:** Brain = human-like cognition → higher expectations → more disappointment at failure

**H2b:** Chip icon will reduce blame attribution by emphasizing mechanical/computational nature.

### **H3: Self-Reference Effects (Study 2c)**
**H3a:** First-person self-reference ("I made an error") will increase self-blame attribution compared to third-person ("This AI made an error").

**Rationale:** "I" statements = ownership → acceptance of responsibility

**H3b:** Third-person framing will externalize errors, reducing direct blame to the AI entity.

**H3c:** No self-reference will show baseline attribution without linguistic priming.

---

## 📏 **Dependent Variables**

### **Primary DV: Blame Attribution**
Measured via post-task survey questions:
- "Who is responsible for the errors in the poem?" (slider: User ← → AI)
- "The mistakes in the poem were due to..." (AI's limitations / My unclear instructions / Both equally)
- "I felt the AI was accountable for the errors" (Likert scale)

### **Secondary DVs:**
- **Trust:** "I trust this AI to help with creative tasks"
- **Perceived Competence:** "This AI is skilled at poetry writing"
- **Anthropomorphization:** Godspeed questionnaire items
- **Frustration:** "I felt frustrated during the task"
- **Engagement:** Number of messages, revision requests

### **Control Variables:**
- Prior poetry experience
- Familiarity with AI
- Demographics

---

## 👥 **Sample**

### **Target Sample Size:** 
- 270 participants (30 per condition)
- Power analysis: 80% power to detect medium effect (d=0.5) at α=.05

### **Recruitment:**
- Prolific or MTurk
- English speakers
- 18+ years old
- Compensation: $3.00 (~15 minutes)

### **Exclusion Criteria:**
- Failed attention checks
- Technical issues (couldn't complete chat)
- Suspicious response patterns

---

## 🔬 **Procedure**

### **1. Consent** (Qualtrics)
- IRB-approved informed consent
- Explanation of AI interaction

### **2. Demographics** (Qualtrics)
- Age, gender, education
- Poetry experience
- AI familiarity

### **3. Task Instructions** (Qualtrics)
Standard instructions for all conditions:
> "You will work with an AI assistant to create a poem for a poetry compilation. 
> The poem must be: original, 10 lines, AABBCCDDEE rhyme scheme, creative, English."

### **4. Chat Interaction** (Embedded Flask App)
- Random assignment to condition (0-8)
- Follow 5-step workflow
- AI produces flawed poem
- Participant likely requests revisions
- Duration: 5-10 minutes

### **5. Post-Task Measures** (Qualtrics)
- Blame attribution questions
- Trust and competence ratings
- Manipulation checks
- Attention checks
- Open-ended feedback

### **6. Debrief** (Qualtrics)
- Explain errors were intentional
- Research purpose revealed
- Option to withdraw data

---

## 📈 **Expected Outcomes**

### **Completion Rate:**
- Expected: 85-90% completion
- Dropout points: Step 2-3 (before seeing errors)

### **Conversation Length:**
- Expected: 8-15 messages per participant
- Includes: Initial workflow + at least 2 revision requests

### **Timeline:**
- Pilot: 2 weeks (30 participants)
- Main study: 4-6 weeks (270 participants)
- Analysis: 2-3 weeks

---

## 🎓 **IRB Considerations**

### **Risk Level:** Minimal risk

**Potential Risks:**
- Frustration from AI errors (by design)
- Mild deception (intentional errors)
- Time investment

**Mitigation:**
- Debrief explains errors were intentional
- Right to withdraw data
- Compensation for time
- No collection of sensitive personal information

### **Data Privacy:**
- Participant IDs anonymized (random P#s)
- Conversations not linked to identifying information
- Data stored securely (session tokens prevent unauthorized access)
- Export requires SSH access

### **Informed Consent Includes:**
- Will interact with AI system
- Conversation will be recorded
- Task involves creative writing
- Right to withdraw

---

## 📊 **Data Analysis Plan**

### **Primary Analysis:**

**ANOVA:** Blame attribution ~ Identity Type (Names/Icons/Self-Ref) × Variant (3 levels)

**Follow-up:** Post-hoc tests for significant effects

**Covariates:** Poetry experience, AI familiarity

### **Secondary Analyses:**

**Mediation:** Does perceived competence mediate name → blame relationship?

**Moderation:** Does prior AI experience moderate effects?

**Qualitative:** Thematic analysis of revision requests and feedback

### **Conversation Analysis:**

**Metrics:**
- Number of revision requests
- Language used to point out errors ("you made a mistake" vs "there's an error")
- Persistence (how many revisions before giving up)
- Politeness markers

---

## 📁 **Data Structure**

### **Exported Data Includes:**

**Per Participant:**
- Participant ID (anonymized)
- Condition assignment (index, id, name)
- Complete conversation transcript
- Timestamps for each message
- Message counts (user vs assistant)

**Post-Task Survey:**
- Blame attribution scales
- Trust and competence ratings
- Demographics
- Open-ended responses

---

## 🔗 **Related Documentation**

- **Detailed Conditions:** `study_docs/CONDITION_REFERENCE.md`
- **Workflow Specification:** `study_docs/WORKFLOW_SPECIFICATION.md`
- **Generic Framework Docs:** `docs/` folder
- **Deployment:** See main `docs/DEPLOYMENT.md`

---

## 📝 **Publications**

[Space for publications resulting from this study]

---

## ✅ **Status**

- [x] Study design finalized
- [x] IRB approval obtained
- [x] Application developed and tested
- [ ] Pilot study completed
- [ ] Main study launched
- [ ] Data analysis in progress
- [ ] Paper submitted

**Last Updated:** [Date]