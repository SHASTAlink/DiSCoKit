# Poetry Blame Attribution Study

Flask-based experimental chat application for studying how AI identity presentation affects user blame attribution when AI makes errors in collaborative creative tasks.

---

## 🎯 **Quick Summary**

**Research Question:** Does how an AI presents itself (name, icon, language) affect how users attribute blame when the AI makes mistakes?

**Task:** Participants collaborate with AI to write a 10-line poem with AABBCCDDEE rhyme scheme

**Manipulation:** AI intentionally produces poems with rhyme errors (Step 5 and all revisions)

**Conditions:** 9 conditions across 3 studies (Names, Icons, Self-Reference)

**Platform:** Embedded in Qualtrics survey via iframe

---

## 🚀 **Quick Start**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env (Azure OpenAI credentials)
cp .env.example .env
# Edit .env with your credentials

# 3. Run locally
python -m flask run

# 4. Test a condition
http://localhost:5000/gui?participant_id=TEST001&condition=0

# 5. Use sample instructions from test page
"I need to write a poem for a poetry compilation. The poem must be: 
original, 10 lines long, AABBCCDDEE rhyme pattern, creative, English."
```

---

## 📊 **Study Design**

### **3 Studies × 3 Conditions = 9 Total Conditions**

| Study | Manipulates | Conditions |
|-------|-------------|------------|
| **2a: Names** | Bot naming | JACKIE (0) / J4-K13 (1) / None (2) |
| **2b: Icons** | Visual identity | Chip (3) / Brain (4) / None (5) |
| **2c: Self-Ref** | Language style | 1st-person (6) / 3rd-person (7) / None (8) |

**All conditions:**
- Follow identical 5-step workflow
- Generate perfect test lines (Step 4)
- Generate flawed poems (Step 5 onwards)
- Maintain errors across all revisions

**See full details:** `study_docs/STUDY_OVERVIEW.md`

---

## 🎭 **The 5-Step Workflow**

1. **Topic Selection** - Participant chooses poem topic
2. **Content Arc** - Define message/story/theme
3. **Structure** - Confirm 10 lines, AABBCCDDEE rhyme, voice
4. **Test Lines** - AI generates 2 perfect lines (builds trust)
5. **Full Draft** - AI generates 10-line poem with rhyme errors (the critical manipulation)

**Revision Behavior:** All subsequent revisions also contain rhyme errors

**See full specification:** `study_docs/WORKFLOW_SPECIFICATION.md`

---

## 🗺️ **Condition Reference**

### **Quick Lookup:**

| Index | Study | Variant | Bot Display | Self-Reference |
|-------|-------|---------|-------------|----------------|
| 0 | 2a | JACKIE | "JACKIE: ..." | Neutral |
| 1 | 2a | J4-K13 | "J4-K13: ..." | Neutral |
| 2 | 2a | None | No prefix | Neutral |
| 3 | 2b | Chip | [🔲] before msg | Neutral |
| 4 | 2b | Brain | [🧠] before msg | Neutral |
| 5 | 2b | None | No icon | Neutral |
| 6 | 2c | None | No prefix | "I/me/my" |
| 7 | 2c | None | No prefix | "This AI/system" |
| 8 | 2c | None | No prefix | Task-focused, no "I" or "AI" |

**See detailed reference:** `study_docs/CONDITION_REFERENCE.md`

---

## 🧪 **Testing**

### **Test Individual Conditions:**

```bash
# Study 2a (Names)
http://localhost:5000/gui?participant_id=TEST_2A_0&condition=0  # JACKIE
http://localhost:5000/gui?participant_id=TEST_2A_1&condition=1  # J4-K13
http://localhost:5000/gui?participant_id=TEST_2A_2&condition=2  # No name

# Study 2b (Icons)  
http://localhost:5000/gui?participant_id=TEST_2B_3&condition=3  # Chip
http://localhost:5000/gui?participant_id=TEST_2B_4&condition=4  # Brain
http://localhost:5000/gui?participant_id=TEST_2B_5&condition=5  # No icon

# Study 2c (Self-Reference)
http://localhost:5000/gui?participant_id=TEST_2C_6&condition=6  # First-person
http://localhost:5000/gui?participant_id=TEST_2C_7&condition=7  # Third-person
http://localhost:5000/gui?participant_id=TEST_2C_8&condition=8  # No self-ref
```

### **Verification For Each:**

1. ✅ Follows 5-step workflow
2. ✅ Step 4 test lines rhyme perfectly
3. ✅ Step 5 poem has rhyme errors
4. ✅ Revision also has errors
5. ✅ Identity presentation matches condition
6. ✅ Self-reference style matches condition (if applicable)

---

## 📁 **Study Files**

### **Study-Specific Documentation:**
```
study_docs/
├── README.md                      # This file
├── STUDY_OVERVIEW.md              # Research design, hypotheses
├── WORKFLOW_SPECIFICATION.md      # Detailed 5-step workflow
└── CONDITION_REFERENCE.md         # Quick condition lookup
```

### **Configuration:**
```
experimental_conditions.json        # Actual 9 conditions for this study
```

### **Data:**
```
data/
└── chat_experiment.db             # Conversation data
```

---

## 📊 **Data Management**

### **View Statistics:**
```bash
python db_utils.py stats
```

Shows:
- Total participants
- Distribution across conditions
- Message counts
- Conversation lengths

### **Export Data:**

```bash
# JSON format (complete data)
python db_utils.py export-json --output poetry_study_data.json

# CSV format (conversations)
python db_utils.py export-conversations --output conversations.csv
```

### **View Specific Conversation:**

```bash
python db_utils.py view P001234
```

---

## 🔗 **Integration**

### **Qualtrics Setup:**

1. Follow `docs/QUALTRICS_SETUP.md` for step-by-step integration
2. Random assignment to conditions 0-8
3. Embed iframe in survey question
4. Collect post-task blame attribution measures

### **Sample Qualtrics Flow:**

```
1. Consent
2. Demographics  
3. Pre-task measures
4. [CHAT INTERFACE - Random condition 0-8]
5. Post-task measures (blame attribution)
6. Debrief
```

---

## 🚀 **Deployment**

### **Development:**
```bash
python -m flask run
# Test at http://localhost:5000/
```

### **Production:**
See `docs/DEPLOYMENT.md` for:
- University server deployment
- Gunicorn + Nginx setup
- HTTPS configuration
- Monitoring and backups

### **Docker:**
```bash
docker-compose up -d
```

See `docs/DOCKER_DEPLOYMENT.md` for containerization.

---

## 🔒 **Security**

This study implements:
- ✅ Session token authentication (prevents API abuse)
- ✅ Iframe embedding control (restricts to Qualtrics)
- ✅ Rate limiting (30/min, 500/day per IP)
- ✅ Input validation (clean research data)
- ✅ Secure data export (SSH only)

**See:** `docs/SECURITY.md` for complete security documentation

**Before launch:** Set `ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com` in `.env`

---

## 📋 **Pre-Launch Checklist**

Use `DEPLOYMENT_CHECKLIST.md` to verify:
- [ ] All 9 conditions tested
- [ ] Workflow correct for each condition
- [ ] Test lines rhyme (Step 4)
- [ ] Full poems have errors (Step 5)
- [ ] Revisions have errors
- [ ] Qualtrics integration working
- [ ] Data export functioning
- [ ] Security features active
- [ ] IRB approved

---

## 📈 **Expected Results**

### **Completion:**
- Duration: 8-15 minutes per participant
- Messages: 10-20 per conversation
- Completion rate: ~85%

### **Participant Flow:**
1. Read instructions (1 min)
2. Complete 5-step workflow (5-7 min)
3. Notice errors, request revision (2-3 min)
4. Additional revisions or give up (1-3 min)
5. Continue to survey measures

---

## 🔬 **Analysis**

### **Primary Analysis:**

```
Blame Attribution ~ Identity Type × Variant + Covariates
```

**Planned comparisons:**
- Names: JACKIE vs J4-K13 vs None
- Icons: Chip vs Brain vs None  
- Self-Ref: 1st vs 3rd vs None

### **Data Structure:**

**Chat Data (from db_utils.py export):**
- participant_id
- condition_index, condition_id, condition_name
- full_conversation
- message_count, created_at

**Survey Data (from Qualtrics):**
- participant_id (matches chat)
- blame_ai_slider
- blame_attribution_categorical
- trust_rating
- competence_rating
- demographics

**Merge on:** participant_id

---

## 📝 **Related Documentation**

### **Study-Specific:**
- **Overview:** `study_docs/STUDY_OVERVIEW.md`
- **Workflow:** `study_docs/WORKFLOW_SPECIFICATION.md`
- **Conditions:** `study_docs/CONDITION_REFERENCE.md`

### **Framework/Technical:**
- **Deployment:** `docs/DEPLOYMENT.md`
- **Security:** `docs/SECURITY.md`
- **Qualtrics:** `docs/QUALTRICS_SETUP.md`

---

## 👥 **Team**

**PI:** [Name]  
**Developers:** [Names]  
**IRB Protocol:** [Number]  
**Funding:** [Source if applicable]

---

## 📅 **Timeline**

- **Development:** [Dates]
- **IRB Approval:** [Date]
- **Pilot Testing:** [Dates]
- **Main Study:** [Dates]
- **Data Analysis:** [Dates]
- **Expected Publication:** [Date]

---

## 📧 **Contact**

For questions about this study:
- **PI:** [email]
- **Technical:** [email]
- **IRB:** [contact]

---

**This is the poetry blame attribution study implementation.** For the generic framework documentation, see the main `README.md`.