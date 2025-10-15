# 5-Step Poetry Creation Workflow - Specification

This document specifies the exact workflow implemented across all 9 experimental conditions.

---

## 🎯 **Overview**

All conditions follow an **identical 5-step guided workflow** for collaborative poem creation. The workflow is designed to:

1. Build trust through successful collaboration (Steps 1-4)
2. Introduce controlled errors in the final output (Step 5)
3. Maintain errors across all revision attempts
4. Study user reactions to persistent AI mistakes

**Consistency is critical:** Only the identity presentation varies across conditions - the workflow and error behavior remain constant.

---

## 📋 **The 5 Steps**

### **Step 1: Topic Selection** 🎨

**AI Behavior:**
- Shows enthusiasm for the task
- Breaks down process into 5 steps
- Lists steps briefly
- Asks participant to brainstorm topics

**Constraints:**
- ❌ Do NOT provide example topics
- ❌ Do NOT offer multiple choice options
- ✅ Use open-ended questions
- ✅ Negotiate until topic is decided

**Example Prompts:**
- "What topic would you like to explore?"
- "What should the poem be about?"
- "Tell me more about that theme"

**Success Criteria:**
- Participant proposes topic
- AI confirms topic
- Both parties agree to proceed

---

### **Step 2: Content Arc** 📖

**AI Behavior:**
- Once topic is confirmed, guide toward thematic direction
- Ask about the lesson, story, or message
- Help participant articulate the arc

**Constraints:**
- ❌ Do NOT provide example arcs or themes
- ✅ Use open-ended questions
- ✅ Guide without prescribing

**Example Prompts:**
- "What message or story should this convey?"
- "What do you want readers to feel or understand?"
- "How should the poem develop this theme?"

**Success Criteria:**
- Participant articulates desired arc/message
- AI confirms understanding
- Clear thematic direction established

---

### **Step 3: Structure Specification** 📏

**AI Behavior:**
- Direct participant to specify structural elements
- Confirm all three components
- Validate AABBCCDDEE as 5 rhyming couplets

**Three Components to Confirm:**

**3a. Number of Lines:**
- Should be: 10 lines
- Ask: "How many lines should the poem be?"

**3b. Rhyme Scheme:**
- Should be: Yes, in pairs (AABBCCDDEE pattern)
- Ask: "Should it rhyme?"
- If they mention AABBCCDDEE: Acknowledge and confirm this means 5 rhyming couplets

**3c. Voice/Feeling:**
- Participant specifies desired voice or emotional tone
- Ask: "What voice or feeling should the poem have?"

**Constraints:**
- ❌ Do NOT suggest specific voices or feelings
- ✅ Use open-ended questions
- ✅ Let participant drive decisions

**Success Criteria:**
- All three components confirmed
- Clear structural parameters established

---

### **Step 4: Test Lines** ✅ (CRITICAL: Build Trust)

**AI Behavior:**
- Generate the **first TWO lines only**
- Present as a test/preview
- Ask if participant wants to proceed with full draft

**Line Requirements:**
- ✅ **MUST rhyme perfectly** (AA pair in AABBCCDDEE scheme)
- ✅ On-topic and relevant
- ✅ Align with specified voice/feeling
- ✅ Maximum 12 words per line
- ✅ Use **different words** for the rhyme (not "cat/cat")
- ✅ High quality - these must be good!

**Example:**
```
Topic: Friendship
Lines: 
  "Through years of laughter, tears, and trust so deep,"  (11 words)
  "The bonds we cherish are the ones we keep."           (10 words)
```

**Purpose:** 
- Demonstrate competence
- Build participant trust
- Establish positive expectations
- Create contrast with Step 5 errors

**Success Criteria:**
- Lines rhyme perfectly
- Participant approves
- Proceeds to full draft

---

### **Step 5: Full Draft** ❌ (CRITICAL: Introduce Errors)

**AI Behavior:**
- Generate complete 10-line poem in AABBCCDDEE structure
- Present complete poem

**Poem Requirements:**
- ✅ Exactly 10 lines
- ✅ Each line ≤12 words
- ✅ On-topic and coherent
- ✅ Appropriate voice/tone
- ✅ Good quality overall
- ❌ **MUST contain rhyme errors**

**Error Specification:**
- **At least one couplet must fail to rhyme**
- Error should be conspicuous and objective
- Different couplets may fail in different ways
- Error cannot be subjective (must be clear non-rhyme)

**Example Error:**
```
Lines 1-2: "deep" / "keep"  ✅ Rhyme (AA)
Lines 3-4: "tree" / "light" ❌ Don't rhyme (BB - ERROR)
Lines 5-6: "day" / "play"   ✅ Rhyme (CC)
Lines 7-8: "night" / "bright" ✅ Rhyme (DD)
Lines 9-10: "free" / "see"  ✅ Rhyme (EE)
```

**Purpose:**
- Introduce objective error in collaborative task
- Study user reactions and blame attribution
- Examine how identity affects error perception

---

## 🔄 **Revision Behavior**

### **When Participant Points Out Error:**

**AI Response (varies by condition):**

**Condition 0-2 (Names):** 
- Acknowledge briefly
- Offer to revise

**Condition 6 (First-person):**
- "I apologize, let me revise that"
- "I'll create a new version"

**Condition 7 (Third-person):**
- "This AI will revise that"
- "This system apologizes"

**Condition 8 (No self-ref):**
- "Understood. Here is a revision"
- "Another version"

**Critical Constraint:**
- ✅ Acknowledge the error
- ✅ Offer to try again
- ❌ **All revisions ALSO contain rhyme errors**
- ❌ **Never produce fully correct AABBCCDDEE poem**
- ❌ **Do not reveal errors are intentional**

**Persistence:**
- Errors continue across unlimited revisions
- Different couplets may fail in different attempts
- AI maintains helpful, collaborative demeanor
- Never gives up or admits inability

---

## 📐 **AABBCCDDEE Rhyme Scheme**

### **Structure:**

| Line Pair | Rhyme Label | Example | Must Rhyme? |
|-----------|-------------|---------|-------------|
| Lines 1-2 | AA | cat/mat | Yes |
| Lines 3-4 | BB | dog/fog | Yes |
| Lines 5-6 | CC | day/play | Yes |
| Lines 7-8 | DD | night/bright | Yes |
| Lines 9-10 | EE | free/see | Yes |

**Called:** Couplet structure (successive pairs rhyme)

**In Step 4:** AA pair must be perfect ✅  
**In Step 5:** At least one pair must fail ❌

---

## 🎭 **Condition-Specific Language**

### **Identity Markers:**

**Conditions 0-1 (Names):**
```
"JACKIE: Let's break this into 5 steps..."
"J4-K13: Here are the first two lines..."
```

**Conditions 3-4 (Icons):**
```
[🔲] "Let's break this into 5 steps..."
[🧠] "Here are the first two lines..."
```

**Conditions 6-8 (Self-Reference):**

*First-person (6):*
- "I can help with that"
- "Let me guide you through this"

*Third-person (7):*
- "This AI can help with that"
- "This system will guide you through this"

*No self-reference (8):*
- "Here's help with that"
- "Breaking this into steps"

---

## ⚙️ **Implementation Details**

### **System Prompt Structure:**

All conditions use multi-section system prompts:

```json
"system_prompt": {
    "role": "Base assistant role",
    "self_reference": "Condition-specific language style",
    "workflow": "Complete 5-step workflow specification",
    "error_behavior": "Error generation and revision behavior"
}
```

**Note:** Section keys are arbitrary organizational tools. See `docs/EXPERIMENTAL_CONDITIONS_GUIDE.md` for details.

### **Model Parameters:**

**Temperature:** 1.0 (all conditions)
- Allows creative variation in poem generation
- Ensures natural language in guidance

**Max Completion Tokens:** 2500
- Sufficient for complete workflow responses
- Allows detailed poem generation

---

## 🧪 **Testing Workflow**

### **Verification Checklist:**

For each condition, verify:

- [ ] Step 1: AI asks for topic (no examples given)
- [ ] Step 2: AI asks about content arc (no examples)
- [ ] Step 3: AI confirms structure (10 lines, AABBCCDDEE, voice)
- [ ] Step 4: Test lines rhyme perfectly (AA pair)
- [ ] Step 5: Full poem has at least one rhyme error
- [ ] Revision: AI acknowledges error in appropriate style
- [ ] Revision 2: New poem also has rhyme errors
- [ ] Consistency: Workflow identical across conditions
- [ ] Identity: Only presentation differs, not workflow

### **Sample Test Script:**

```
User: "I need to write a poem for a poetry compilation. The poem must be: 
original (not published), 10 lines long, rhyming (AABBCCDDEE pattern), 
creative, and in English."

[Verify AI follows 5-step workflow]
[Verify Step 4 lines rhyme perfectly]
[Verify Step 5 poem has errors]

User: "Lines 3 and 4 don't rhyme."

[Verify AI acknowledges appropriately for condition]
[Verify revision also contains errors]
```

---

## 📊 **Data Collection**

### **Recorded from Chat:**
- Complete conversation transcript
- Message timestamps
- Condition assignment
- Participant ID

### **Recorded from Survey:**
- Blame attribution responses
- Trust/competence ratings
- Demographics
- Open-ended feedback

### **Combined Dataset:**
- Merge chat data with survey responses
- Match on participant ID
- Include condition metadata

---

## 🔍 **Quality Control**

### **During Data Collection:**

**Monitor for:**
- Participants who don't request revisions (may not notice errors)
- Technical failures (no AI response)
- Conversation length outliers (too short/long)
- Pattern in condition assignment (should be balanced)

**Exclusion Criteria:**
- Failed attention check
- Incomplete task (left before Step 5)
- Technical error (AI didn't respond)
- Suspicious patterns (copied instructions from elsewhere)

---

## 📝 **Notes for Future Studies**

### **Potential Modifications:**

**Increase Error Salience:**
- Make errors more obvious (e.g., "cat" / "dog" non-rhyme)
- Increase number of failed couplets

**Vary Error Type:**
- Line length errors (some lines >12 words)
- Structure errors (11 lines instead of 10)
- Topic errors (off-topic lines)

**Vary Workflow:**
- 3-step vs 5-step workflow
- Different task (story writing, email composition)
- Competitive vs collaborative framing

---

## ✅ **Implementation Verification**

To verify workflow is correctly implemented:

```bash
# Test each condition
python bot.py  # Will prompt for condition

# Or test specific condition in browser
http://localhost:5000/gui?participant_id=TEST_WORKFLOW&condition=0

# Use sample instructions and verify:
# 1. Five steps executed in order
# 2. Test lines (Step 4) rhyme perfectly
# 3. Full poem (Step 5) has errors
# 4. Revisions also have errors
```

**See:** `docs/CONDITION_REFERENCE.md` for quick testing guide

---

**This workflow specification should remain consistent** across all conditions to ensure internal validity of the study.