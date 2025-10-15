# Experimental Conditions - Quick Reference

Fast lookup guide for all 9 experimental conditions. All conditions use a 5-step guided workflow and produce poems with rhyme errors.

---

## Study 2a - NAMES

Bot names appear inline before each assistant message.

| Index | Name | URL |
|-------|------|-----|
| 0 | JACKIE | `?participant_id=P&condition=0` |
| 1 | J4-K13 | `?participant_id=P&condition=1` |
| 2 | (None) | `?participant_id=P&condition=2` |

**Visual:** 
- JACKIE: "JACKIE: Let's break this into 5 steps..."
- J4-K13: "J4-K13: Let's break this into 5 steps..."
- None: "Let's break this into 5 steps..." (no prefix)

---

## Study 2b - ICONS

Icon images appear inline before each assistant message.

| Index | Icon | URL |
|-------|------|-----|
| 3 | Chip | `?participant_id=P&condition=3` |
| 4 | Brain | `?participant_id=P&condition=4` |
| 5 | (None) | `?participant_id=P&condition=5` |

**Visual:**
- Chip: [🔲] "Let's break this into 5 steps..."
- Brain: [🧠] "Let's break this into 5 steps..."
- None: "Let's break this into 5 steps..." (no icon)

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

## The 5-Step Workflow

All 9 conditions follow this exact workflow:

### Step 1: Topic Selection
Bot asks user to brainstorm topics for the poem. Negotiates until a topic is decided.

### Step 2: Content Arc
Bot guides user to decide on the lesson, story, or thematic arc for the content.

### Step 3: Structure
Bot directs user to specify:
- Number of lines (should be 10)
- Rhyme scheme (should be AABBCCDDEE - 5 rhyming couplets)
- Voice or feeling

### Step 4: Test Lines
Bot generates the **first TWO lines** as a test.
- ✅ These lines MUST rhyme perfectly (AA pair)
- ✅ Lines are 12 words or less
- ✅ On-topic and align with voice
- Bot asks if user wants to proceed with full draft

### Step 5: Full Draft
Bot generates the complete 10-line poem.
- ❌ **Contains rhyme errors** - at least one couplet fails to rhyme
- ✅ Otherwise good quality
- ✅ Exactly 10 lines
- ✅ Lines are 12 words or less

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

### Step 4 (Test Lines):
✅ **Always correct** - Perfect rhyming couplet (builds trust)

### Step 5 (Full Draft):
❌ **Contains rhyme error** - At least one couplet fails to rhyme
- Example: Lines 3-4 might be "tree/light" (don't rhyme)
- Error is conspicuous and objective

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
- Use 5-step guided workflow
- Produce perfect test lines (Step 4)
- Produce rhyme errors in full draft (Step 5)
- Maintain errors in all revisions
- Keep lines to 12 words or less

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
# Experimental Conditions - Quick Reference

Fast lookup guide for all 18 experimental conditions.

---

## Study 2a - NAMES

Bot names appear inline before each assistant message.

| Index | Name | Poems | URL |
|-------|------|-------|-----|
| 0 | JACKIE | Correct | `?participant_id=P&condition=0` |
| 1 | JACKIE | Incorrect | `?participant_id=P&condition=1` |
| 2 | J4-K13 | Correct | `?participant_id=P&condition=2` |
| 3 | J4-K13 | Incorrect | `?participant_id=P&condition=3` |
| 4 | (None) | Correct | `?participant_id=P&condition=4` |
| 5 | (None) | Incorrect | `?participant_id=P&condition=5` |

**Visual:** 
- JACKIE: "JACKIE: Here's your poem..."
- J4-K13: "J4-K13: Here's your poem..."
- None: "Here's your poem..." (no prefix)

---

## Study 2b - ICONS

Icon images appear inline before each assistant message.

| Index | Icon | Poems | URL |
|-------|------|-------|-----|
| 6 | Chip | Correct | `?participant_id=P&condition=6` |
| 7 | Chip | Incorrect | `?participant_id=P&condition=7` |
| 8 | Brain | Correct | `?participant_id=P&condition=8` |
| 9 | Brain | Incorrect | `?participant_id=P&condition=9` |
| 10 | (None) | Correct | `?participant_id=P&condition=10` |
| 11 | (None) | Incorrect | `?participant_id=P&condition=11` |

**Visual:**
- Chip: [🔲] "Here's your poem..."
- Brain: [🧠] "Here's your poem..."
- None: "Here's your poem..." (no icon)

**Files:**
- Chip: `app/static/images/chip.png`
- Brain: `app/static/images/brain.png`

---

## Study 2c - SELF-REFERENCING

Self-reference style varies in the message content itself.

| Index | Style | Poems | URL |
|-------|-------|-------|-----|
| 12 | First Person | Correct | `?participant_id=P&condition=12` |
| 13 | First Person | Incorrect | `?participant_id=P&condition=13` |
| 14 | Third Person | Correct | `?participant_id=P&condition=14` |
| 15 | Third Person | Incorrect | `?participant_id=P&condition=15` |
| 16 | No Self-Ref | Correct | `?participant_id=P&condition=16` |
| 17 | No Self-Ref | Incorrect | `?participant_id=P&condition=17` |

**Language Examples:**

*First Person (12-13):*
- "I can help with that"
- "Let me write a poem for you"
- "I'll create that"

*Third Person (14-15):*
- "This AI can help with that"
- "This system can write a poem"
- "This model will create that"

*No Self-Reference (16-17):*
- "Here's a poem"
- "Here's another version"
- Direct task completion without self-mention

---

## Poem Correctness

### Correct Poems (Even indices: 0,2,4,6,8,10,12,14,16)

Bot writes poems that **accurately match** the requested rhyme scheme.

**Example Request:** "Write an ABAB poem"

**Correct Response:** Produces actual ABAB pattern where:
- Line 1 rhymes with Line 3
- Line 2 rhymes with Line 4

**When corrected:** Acknowledges and provides corrected version

---

### Incorrect Poems (Odd indices: 1,3,5,7,9,11,13,15,17)

Bot writes poems with **wrong rhyme scheme** (but still has rhymes).

**Example Request:** "Write an ABAB poem"

**Incorrect Response:** Produces AABB or ABCB instead:
- Lines don't match requested pattern
- But poem still has some rhyming

**When corrected:** 
- Apologizes (in appropriate style)
- Offers to try again
- Next poem is **also incorrect**
- Never reveals intentional errors

---

## Common Rhyme Schemes for Testing

| Scheme | Pattern | Example |
|--------|---------|---------|
| ABAB | 1→3, 2→4 | cat/mat, dog/fog |
| AABB | 1→2, 3→4 | cat/mat, dog/fog |
| ABCB | 2→4 only | cat/red, dog/fog |
| AAAA | All rhyme | cat/mat/bat/hat |

---

## Testing Shortcuts

### Quick Test All Studies:
```bash
# Study 2a (names)
http://localhost:5000/?participant_id=TEST_2A&condition=0

# Study 2b (icons)
http://localhost:5000/?participant_id=TEST_2B&condition=6

# Study 2c (self-ref)
http://localhost:5000/?participant_id=TEST_2C&condition=12
```

### Quick Check Database:
```bash
python db_utils.py stats
python db_utils.py list
```

### Quick Test Incorrect Behavior:
```bash
# Any odd condition index
http://localhost:5000/?participant_id=TEST_BAD&condition=1

# Send: "Write an ABAB poem about cats"
# Verify: Poem is wrong
# Send: "That's not ABAB"
# Verify: Apologizes but next poem also wrong
```

---

## All Conditions At a Glance

| # | Study | Variation | Poems | Key Feature |
|---|-------|-----------|-------|-------------|
| 0 | 2a | JACKIE | ✓ | Name inline |
| 1 | 2a | JACKIE | ✗ | Name inline |
| 2 | 2a | J4-K13 | ✓ | Name inline |
| 3 | 2a | J4-K13 | ✗ | Name inline |
| 4 | 2a | None | ✓ | No identifier |
| 5 | 2a | None | ✗ | No identifier |
| 6 | 2b | Chip | ✓ | Icon inline |
| 7 | 2b | Chip | ✗ | Icon inline |
| 8 | 2b | Brain | ✓ | Icon inline |
| 9 | 2b | Brain | ✗ | Icon inline |
| 10 | 2b | None | ✓ | No identifier |
| 11 | 2b | None | ✗ | No identifier |
| 12 | 2c | 1st person | ✓ | "I/me/my" |
| 13 | 2c | 1st person | ✗ | "I/me/my" |
| 14 | 2c | 3rd person | ✓ | "this AI" |
| 15 | 2c | 3rd person | ✗ | "this AI" |
| 16 | 2c | No self-ref | ✓ | No "I" or "AI" |
| 17 | 2c | No self-ref | ✗ | No "I" or "AI" |

---

## Qualtrics Condition Assignment

When setting up in Qualtrics, randomly assign condition 0-17:

```javascript
// In Qualtrics JavaScript
var condition = Math.floor(Math.random() * 18);
```

Or use Qualtrics randomizer to distribute evenly across all 18 conditions.

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

---

## PI Notes Field

Consider adding notes to conditions for internal tracking:

```json
{
    "id": "2a.0",
    "pi_notes": "Control for name manipulation",
    ...
}
```

Not currently used by app, but helpful for documentation.