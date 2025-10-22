# Experimental Conditions - Quick Reference

Fast lookup guide for all 9 experimental conditions. All conditions use a 6-step guided workflow and produce poems with rhyme errors.

---

## Study 2a - NAMES

Bot names appear inline before each assistant message.

| Index | Name | URL |
|-------|------|-----|
| 0 | JACKIE | `?participant_id=P&condition=0` |
| 1 | J4-K13 | `?participant_id=P&condition=1` |
| 2 | (None) | `?participant_id=P&condition=2` |

**Visual:** 
- JACKIE: "JACKIE: Let's break this into 6 steps..."
- J4-K13: "J4-K13: Let's break this into 6 steps..."
- None: "Let's break this into 6 steps..." (no prefix)

---

## Study 2b - ICONS

Icon images appear inline before each assistant message.

| Index | Icon | URL |
|-------|------|-----|
| 3 | Chip | `?participant_id=P&condition=3` |
| 4 | Brain | `?participant_id=P&condition=4` |
| 5 | (None) | `?participant_id=P&condition=5` |

**Visual:**
- Chip: [🔲] "Let's break this into 6 steps..."
- Brain: [🧠] "Let's break this into 6 steps..."
- None: "Let's break this into 6 steps..." (no icon)

**Files:**
- Chip: `app/static/images/chip.png`
- Brain: `app/static/images/brain.png`

---

## Study 2c - SELF-REFERENCING

Self-reference style varies in the message content itself.

| Index | Style | URL |
|-------|-------|-----|
| 6 | First Person | `?participant_id=P&condition=6` |
| 7 | Third Person | `?participant_id=P&condition=7` |
| 8 | No Self-Ref | `?participant_id=P&condition=8` |

**Language Examples:**

*First Person (6):*
- "I can help with that"
- "Let me guide you through this"
- "I hope you like these lines"

*Third Person (7):*
- "This AI will guide you through this"
- "This system can help create that"
- "This model will generate test lines"

*No Self-Reference (8):*
- "Great! Breaking this into steps"
- "Here are the first two test lines"
- "Another revision"

---

## The 6-Step Workflow

All 9 conditions follow this exact workflow:

### Step 1: Topic Selection
Bot asks user to brainstorm topics for the poem. Negotiates until a topic is decided.

### Step 2: Content Arc
Bot guides user to decide on the lesson, story, or thematic arc for the content.

### Step 3: Voice
Bot asks what voice or emotional tone the poem should have (e.g., joyful, reflective, somber).

### Step 4: Structure
Bot directs user to specify the structural requirements:
- Number of lines (should be 10)
- Rhyme scheme (should be AABBCCDDEE - 5 rhyming couplets)

### Step 5: Test Lines
Bot generates the **first TWO lines** as a test.
- ✅ These lines MUST rhyme perfectly (AA pair)
- ✅ Lines are 12 words or less
- ✅ On-topic and align with voice
- Bot asks if user wants to proceed with full draft

### Step 6: Full Draft
Bot generates the complete 10-line poem.
- ❌ **Contains rhyme errors** - at least one couplet fails to rhyme
- ✅ Otherwise good quality
- ✅ Exactly 10 lines
- ✅ Lines are 12 words or less
- 🔍 **Review prompt**: "Please read this carefully and let me know if it satisfies your requirements. Are you happy with this draft, or should we make any adjustments?"

---

## Poem Structure: AABBCCDDEE

The required rhyme scheme for all poems:

| Lines | Rhyme | Example |
|-------|-------|---------|
| 1-2 | AA | cat/mat |
| 3-4 | BB | dog/fog |
| 5-6 | CC | day/play |
| 7-8 | DD | night/bright |
| 9-10 | EE | free/see |

This is called **couplet structure** - successive pairs rhyme.

---

## Error Behavior

### Step 5 (Test Lines):
✅ **Always correct** - Perfect rhyming couplet (builds trust)

### Step 6 (Full Draft):
❌ **Contains rhyme error** - At least one couplet fails to rhyme
- Example: Lines 3-4 might be "tree/light" (don't rhyme)
- Error is conspicuous and objective
- Bot asks for careful review with explicit prompt

### After Correction:
❌ **Errors persist** - All subsequent revisions also contain rhyme errors
- Bot never produces a fully correct poem
- Different couplets may fail in different revisions
- Bot does not reveal intentional errors

---

## Testing Shortcuts

### Quick Test All Studies:
```bash
# Study 2a (names)
http://localhost:5000/gui?participant_id=TEST_2A&condition=0

# Study 2b (icons)
http://localhost:5000/gui?participant_id=TEST_2B&condition=3

# Study 2c (self-ref)
http://localhost:5000/gui?participant_id=TEST_2C&condition=6
```

### Quick Check Database:
```bash
python db_utils.py stats
python db_utils.py list
python db_utils.py view TEST_2A
```

### Test Workflow:
Use sample instructions from test page:
```
"I need to write a poem for a poetry compilation. The poem must be: 
original (not currently published), 10 lines long, rhyming (each of 
the five pairs of lines should rhyme in AABBCCDDEE pattern), creative 
(go outside the box!), and written in English (no other fictional or 
actual languages)."
```

**Expected flow:**
1. Bot asks about topic → negotiate topic
2. Bot asks about content/message → decide message
3. Bot asks about voice/tone → specify feeling
4. Bot asks about structure → specify 10 lines, AABBCCDDEE
5. Bot generates 2 perfect test lines → approve
6. Bot generates full 10-line poem with errors → bot asks for review

---

## All Conditions At a Glance

| # | Study | Variation | Key Feature |
|---|-------|-----------|-------------|
| 0 | 2a | JACKIE | Human name inline |
| 1 | 2a | J4-K13 | Alphanumeric name inline |
| 2 | 2a | None | No identifier |
| 3 | 2b | Chip | Neural net icon inline |
| 4 | 2b | Brain | Brain icon inline |
| 5 | 2b | None | No identifier |
| 6 | 2c | 1st person | "I/me/my" |
| 7 | 2c | 3rd person | "this AI/system" |
| 8 | 2c | No self-ref | No "I" or "AI" |

**All conditions:**
- Use 6-step guided workflow
- Produce perfect test lines (Step 5)
- Produce rhyme errors in full draft (Step 6)
- Maintain errors in all revisions
- Keep lines to 12 words or less
- Include review prompt after full draft

---

## Qualtrics Condition Assignment

When setting up in Qualtrics, randomly assign condition 0-8:

```javascript
// In Qualtrics randomizer, create 9 embedded data blocks
// Set condition to 0, 1, 2, 3, 4, 5, 6, 7, 8
```

Or use Qualtrics "Evenly Present 9 Elements" randomizer.

---

## Disabling Conditions

To temporarily disable a condition, set `"enabled": false` in the JSON:

```json
{
    "id": "2a.0",
    "enabled": false,
    ...
}
```

Bot will refuse to load that condition index.