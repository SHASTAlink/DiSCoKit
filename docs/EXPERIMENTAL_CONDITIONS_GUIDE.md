# Experimental Conditions Configuration Guide

This guide explains how to configure experimental conditions in `experimental_conditions.json` for your own research studies.

---

## 📋 **Overview**

The `experimental_conditions.json` file defines different experimental conditions that vary:
- Bot identity (name, icon)
- Visual styling (colors, layout)
- AI behavior (system prompts, temperature)
- Which conditions are active

Each participant is randomly assigned to one condition, allowing you to study how different presentations or behaviors affect user interactions.

---

## 🔑 **Required vs. Arbitrary Keys**

### **Top-Level Keys (REQUIRED - Don't Change):**
These keys have specific meanings to the application:
- ✅ `id` - Unique identifier
- ✅ `name` - Human-readable name
- ✅ `description` - What this condition tests
- ✅ `enabled` - Active or disabled
- ✅ `bot_name` - Name shown to users
- ✅ `bot_icon` - Icon shown to users
- ✅ `bot_styles` - Visual customization object
- ✅ `system_prompt` - Prompt sections object
- ⚠️ `model_overrides` - Optional parameter overrides

### **System Prompt Keys (ARBITRARY - Your Choice!):**

**Inside** the `system_prompt` object, ALL keys are arbitrary:

```json
"system_prompt": {
    "role": "...",      // ← You chose this name
    "behavior": "..."   // ← You chose this name
}
```

**Could be:**
```json
"system_prompt": {
    "section_a": "...",  // ← Any name works
    "section_b": "..."   // ← Any name works
}
```

**Or:**
```json
"system_prompt": {
    "personality": "...",        // ← Organize however you want
    "task_instructions": "...",
    "special_rules": "..."
}
```

**The application doesn't care about the key names** - it just joins all the values together with newlines.

### **bot_styles Keys (SPECIFIC - Don't Change):**

Inside `bot_styles`, these keys DO have specific meanings:
- ✅ `primary_color` - Used for buttons, user messages
- ✅ `background_color` - Page background
- ✅ `text_color` - Assistant message text
- ✅ `show_header` - Boolean to show/hide header

---

## 📁 **File Structure**

The file contains a JSON array of condition objects:

```json
[
    {
        "id": "unique_condition_id",
        "name": "Human-Readable Condition Name",
        "description": "What this condition tests",
        "enabled": true,
        "bot_name": "Bot Name",
        "bot_icon": "emoji or /static/images/icon.png",
        "bot_styles": { /* visual customization */ },
        "model_overrides": { /* optional API parameter overrides */ },
        "system_prompt": { /* sections that define bot behavior */ }
    },
    // ... more conditions
]
```

---

## 🔧 **Field Reference**

### **🔑 IMPORTANT NOTE ABOUT system_prompt Keys**

> **The keys you use inside `system_prompt` are completely arbitrary!**
> 
> Common misconception: "I must use `role`, `behavior`, etc."  
> Reality: "I can use ANY key names I want - they're just labels for organization."
>
> The application simply concatenates all the values together. The key names are for YOUR organizational convenience only.
>
> Think of it like sections in a document - you choose the section headers based on what makes sense to you.

---

### **Required Fields:**

#### `id` (string)
Unique identifier for the condition.

**Examples:**
```json
"id": "control"
"id": "condition_1a"
"id": "formal_tone"
```

**Guidelines:**
- Use lowercase, underscores, or hyphens
- Keep short but descriptive
- Must be unique across all conditions

---

#### `name` (string)
Human-readable name shown in logs and exports.

**Examples:**
```json
"name": "Control - Standard Assistant"
"name": "Condition 1A - Formal Tone"
"name": "Treatment Group - High Empathy"
```

**Guidelines:**
- Clear and descriptive
- Include condition ID or number for easy reference
- Will appear in database exports

---

#### `description` (string)
Detailed description of what this condition tests.

**Examples:**
```json
"description": "Baseline condition with standard AI behavior"
"description": "Tests effect of formal language on user trust"
"description": "High empathy responses with emotional validation"
```

**Guidelines:**
- Explain the experimental manipulation
- Useful for documentation and analysis
- Not shown to participants

---

#### `enabled` (boolean)
Whether this condition is active.

**Values:**
```json
"enabled": true   // Condition can be assigned to participants
"enabled": false  // Condition disabled, won't be loaded
```

**Use Cases:**
- Disable conditions during pilot testing
- Temporarily remove problematic conditions
- Phase experiments (enable/disable sets of conditions)

---

#### `bot_name` (string)
Name displayed in the chat interface.

**Examples:**
```json
"bot_name": "Assistant"        // Generic
"bot_name": "Alex"             // Human name
"bot_name": "Support Bot"      // Functional name
"bot_name": ""                 // No name shown
```

**Display Locations:**
- Header (if `show_header: true`)
- Inline before each assistant message (if not empty)

---

#### `bot_icon` (string)
Icon/emoji displayed with the bot.

**Options:**

**Emoji:**
```json
"bot_icon": "🤖"   // Robot
"bot_icon": "👋"   // Waving hand
"bot_icon": "💬"   // Speech bubble
```

**Image File:**
```json
"bot_icon": "/static/images/robot.png"
"bot_icon": "/static/images/brain.png"
```

**None:**
```json
"bot_icon": ""     // No icon
```

**Display Locations:**
- Header (if `show_header: true`)
- Inline before each assistant message (if not empty)

**Note:** If using image files, place them in `app/static/images/`

---

#### `bot_styles` (object)
Visual customization for the chat interface.

**Structure:**
```json
"bot_styles": {
    "primary_color": "#4A90E2",      // Buttons, user messages, header
    "background_color": "#F5F5F5",   // Page background
    "text_color": "#333333",         // Assistant message text
    "show_header": true              // Show/hide header bar
}
```

**Color Guidelines:**
- Use hex codes (#RRGGBB)
- Ensure sufficient contrast for accessibility
- Consider color psychology for your study

**Example Themes:**

**Professional Blue:**
```json
{
    "primary_color": "#2C3E50",
    "background_color": "#ECF0F1",
    "text_color": "#2C3E50",
    "show_header": true
}
```

**Warm Orange:**
```json
{
    "primary_color": "#E67E22",
    "background_color": "#FFF8F0",
    "text_color": "#333333",
    "show_header": false
}
```

---

#### `system_prompt` (object)
Instructions that define the AI's behavior.

**IMPORTANT:** The keys under `system_prompt` are **completely arbitrary** - you can name them whatever you want! They exist purely for organizational purposes. All sections are concatenated together with newlines to form the final system prompt sent to the API.

**Structure (keys are YOUR choice):**
```json
"system_prompt": {
    "role": "High-level role definition",
    "behavior": "Specific behavioral instructions",
    "constraints": "Any limitations or requirements"
}
```

**These keys could just as easily be:**
```json
"system_prompt": {
    "part1": "...",
    "part2": "...",
    "part3": "..."
}
```

**Or:**
```json
"system_prompt": {
    "personality": "...",
    "task_instructions": "...",
    "special_rules": "..."
}
```

**The application simply joins all values together:**
```python
# In bot.py:
system_prompt = "\n".join(experimental_condition["system_prompt"].values())
```

**Choose key names that make sense for YOUR organization!**

**Examples:**

**Helpful Assistant:**
```json
"system_prompt": {
    "identity": "You are a helpful AI assistant.",
    "communication_style": "Be friendly, clear, and concise in your responses."
}
```

**Tutoring Bot:**
```json
"system_prompt": {
    "role": "You are an educational tutor helping students learn.",
    "teaching_approach": "Ask probing questions to guide learning. Don't give direct answers immediately.",
    "difficulty_level": "Keep explanations appropriate for high school level."
}
```

**Customer Support:**
```json
"system_prompt": {
    "job_description": "You are a customer support assistant.",
    "response_framework": "Be empathetic and solution-focused. Always acknowledge the customer's concern first.",
    "escalation_rules": "Escalate to human agent if the issue involves billing or account security."
}
```

**Single Section (Also Valid):**
```json
"system_prompt": {
    "instructions": "You are a helpful AI assistant. Be friendly and concise."
}
```

**Many Sections (Also Valid):**
```json
"system_prompt": {
    "core_identity": "You are a research assistant.",
    "primary_task": "Help users understand scientific concepts.",
    "communication_guidelines": "Use clear language, avoid jargon.",
    "response_structure": "Start with a direct answer, then elaborate if needed.",
    "constraints": "Don't provide medical or legal advice.",
    "tone": "Professional but approachable."
}
```

**Final Prompt:** All values concatenated with newlines:
```
You are a research assistant.
Help users understand scientific concepts.
Use clear language, avoid jargon.
Start with a direct answer, then elaborate if needed.
Don't provide medical or legal advice.
Professional but approachable.
```

**Bottom line:** The key names are for YOUR organizational convenience only - name them whatever helps you maintain and understand your conditions!

---

### **Optional Fields:**

#### `model_overrides` (object)
Override default API parameters for this specific condition.

**Available Overrides:**
```json
"model_overrides": {
    "temperature": 0.9,              // Sampling temperature (0.0-2.0)
    "max_completion_tokens": 3000    // Maximum response length
}
```

**When to Use:**
- Test effect of temperature on responses
- Vary response length across conditions
- A/B test different model parameters

**If not specified:** Uses defaults from `.env` file

---

#### `pi_notes` (string) - Custom Field
You can add custom fields for your own documentation:

```json
"pi_notes": "This is the control condition for Study 1",
"internal_id": "EXP_2024_A1",
"recruitment_target": 100
```

**These fields are ignored by the application** but useful for:
- Internal documentation
- Data analysis later
- Collaboration with team members

---

## 🎨 **Design Patterns**

### **Pattern 1: A/B Testing (2 Conditions)**

Test one variable at a time:

```json
[
    {
        "id": "formal_tone",
        "name": "Condition A - Formal",
        "system_prompt": {
            "role": "You are a professional assistant. Use formal language."
        }
    },
    {
        "id": "casual_tone",
        "name": "Condition B - Casual",
        "system_prompt": {
            "role": "You are a friendly assistant. Use casual, conversational language."
        }
    }
]
```

---

### **Pattern 2: Factorial Design (4 Conditions)**

Vary two factors (2×2):

```json
[
    {
        "id": "formal_named",
        "name": "Formal × Named",
        "bot_name": "Dr. Smith",
        "system_prompt": {"role": "Use formal language."}
    },
    {
        "id": "formal_unnamed",
        "name": "Formal × Unnamed",
        "bot_name": "",
        "system_prompt": {"role": "Use formal language."}
    },
    {
        "id": "casual_named",
        "name": "Casual × Named",
        "bot_name": "Alex",
        "system_prompt": {"role": "Use casual language."}
    },
    {
        "id": "casual_unnamed",
        "name": "Casual × Unnamed",
        "bot_name": "",
        "system_prompt": {"role": "Use casual language."}
    }
]
```

---

### **Pattern 3: Progressive Conditions**

Test increasing levels of a variable:

```json
[
    {
        "id": "empathy_low",
        "name": "Low Empathy",
        "system_prompt": {
            "role": "Provide factual responses. Focus on accuracy over emotional support."
        }
    },
    {
        "id": "empathy_medium",
        "name": "Medium Empathy",
        "system_prompt": {
            "role": "Balance factual accuracy with acknowledgment of user feelings."
        }
    },
    {
        "id": "empathy_high",
        "name": "High Empathy",
        "system_prompt": {
            "role": "Prioritize emotional validation. Acknowledge feelings before providing information."
        }
    }
]
```

---

## 🔬 **Example Use Cases**

### **Research Study 1: Anthropomorphism**

**Research Question:** Does giving the AI a human name affect user trust?

```json
[
    {
        "id": "human_name",
        "bot_name": "Sarah",
        "bot_icon": ""
    },
    {
        "id": "robot_name",
        "bot_name": "Bot-X7",
        "bot_icon": ""
    },
    {
        "id": "no_name",
        "bot_name": "",
        "bot_icon": ""
    }
]
```

---

### **Research Study 2: Visual Identity**

**Research Question:** How does visual representation affect perceptions?

```json
[
    {
        "id": "brain_icon",
        "bot_name": "",
        "bot_icon": "/static/images/brain.png"
    },
    {
        "id": "robot_icon",
        "bot_name": "",
        "bot_icon": "/static/images/robot.png"
    },
    {
        "id": "no_icon",
        "bot_name": "",
        "bot_icon": ""
    }
]
```

---

### **Research Study 3: Communication Style**

**Research Question:** Does self-referential language affect user engagement?

```json
[
    {
        "id": "first_person",
        "system_prompt": {
            "role": "Use first-person pronouns: I, me, my. Example: 'I can help you with that.'"
        }
    },
    {
        "id": "third_person",
        "system_prompt": {
            "role": "Refer to yourself in third person: 'This AI', 'This system'. Example: 'This AI can help you with that.'"
        }
    },
    {
        "id": "no_self_reference",
        "system_prompt": {
            "role": "Avoid self-reference. Be direct. Example: 'Here's help with that.'"
        }
    }
]
```

---

## ⚙️ **System Prompt Best Practices**

### **Keep It Concise**

❌ **Too Long (Costly):**
```json
"system_prompt": {
    "role": "You are a helpful AI assistant designed to provide information and support to users. You should always be polite, respectful, and considerate of the user's needs. When responding to questions, make sure to provide accurate information based on your training data. If you don't know something, be honest about it. Always maintain a professional demeanor and avoid any offensive or inappropriate content..."
}
```
**Problem:** 100+ tokens per message just for system prompt = higher costs

✅ **Better (Efficient):**
```json
"system_prompt": {
    "role": "You are a helpful AI assistant. Be polite and accurate.",
    "behavior": "If unsure, acknowledge uncertainty. Maintain professional tone."
}
```
**Benefit:** 20 tokens, same effect

---

### **Be Specific for Your Study**

If testing specific behaviors, be explicit:

```json
"system_prompt": {
    "role": "You are a medical information assistant.",
    "behavior": "Always include a disclaimer that you're not a doctor. Suggest consulting healthcare professionals for medical decisions.",
    "tone": "Be empathetic but maintain professional boundaries."
}
```

---

### **Use Sections for Organization**

Sections help you organize complex prompts:

```json
"system_prompt": {
    "role": "Core identity and purpose",
    "conversation_style": "How to interact with users",
    "constraints": "What not to do",
    "special_instructions": "Condition-specific behavior"
}
```

All sections are concatenated with `\n` to form the complete prompt.

---

## 🎨 **Styling Guidelines**

### **Color Accessibility**

Ensure sufficient contrast:

**Good Contrast:**
```json
{
    "primary_color": "#2C3E50",      // Dark blue
    "background_color": "#FFFFFF",   // White
    "text_color": "#2C3E50"          // Dark blue
}
```

**Poor Contrast (Avoid):**
```json
{
    "primary_color": "#FFFF00",      // Yellow
    "background_color": "#FFFFFF",   // White (too similar)
    "text_color": "#CCCCCC"          // Light gray (too light)
}
```

Use tools like [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to verify.

---

### **Color Psychology for Research**

Consider how colors might influence participant perceptions:

| Color | Psychology | Use For |
|-------|-----------|---------|
| Blue (#4A90E2) | Trust, professionalism | Control conditions |
| Green (#27AE60) | Growth, positivity | Supportive bots |
| Orange (#E67E22) | Friendly, energetic | Casual conditions |
| Purple (#9B59B6) | Creative, unique | Novel/experimental |
| Gray (#95A5A6) | Neutral, minimal | No-identity conditions |
| Red (#E74C3C) | Alert, urgent | Warning/error studies |

**For unbiased research:** Keep colors consistent across conditions unless color itself is the independent variable.

---

### **Header Visibility**

```json
"show_header": true   // Show top bar with bot name/icon
"show_header": false  // Hide header, minimal interface
```

**When to hide header:**
- Testing if header affects perceptions
- Minimal interface studies
- Focus on conversation content

**When to show header:**
- Bot identity is important
- Professional appearance desired
- Clear branding needed

---

## 🧪 **Creating Your Own Conditions**

### **Step 1: Define Your Research Question**

**Example:** "Does a human-sounding name increase user trust in AI?"

### **Step 2: Identify Your Variables**

**Independent Variable:** Bot name type
- Human name (e.g., "Sarah")
- Robot name (e.g., "Bot-X7")
- No name (control)

**Dependent Variable:** User trust (measured through survey questions)

### **Step 3: Create Conditions**

```json
[
    {
        "id": "human_name",
        "name": "Human Name Condition",
        "description": "Bot presented with human name to test anthropomorphism effect",
        "enabled": true,
        "bot_name": "Sarah",
        "bot_icon": "",
        "bot_styles": {
            "primary_color": "#4A90E2",
            "background_color": "#F5F5F5",
            "text_color": "#333333",
            "show_header": true
        },
        "system_prompt": {
            "role": "You are a helpful AI assistant. Be friendly and conversational."
        }
    },
    {
        "id": "robot_name",
        "name": "Robot Name Condition",
        "description": "Bot presented with robotic name as alternative to human name",
        "enabled": true,
        "bot_name": "Bot-X7",
        "bot_icon": "",
        "bot_styles": {
            "primary_color": "#4A90E2",
            "background_color": "#F5F5F5",
            "text_color": "#333333",
            "show_header": true
        },
        "system_prompt": {
            "role": "You are a helpful AI assistant. Be friendly and conversational."
        }
    },
    {
        "id": "no_name",
        "name": "No Name Control",
        "description": "Control condition with no bot name displayed",
        "enabled": true,
        "bot_name": "",
        "bot_icon": "",
        "bot_styles": {
            "primary_color": "#4A90E2",
            "background_color": "#F5F5F5",
            "text_color": "#333333",
            "show_header": true
        },
        "system_prompt": {
            "role": "You are a helpful AI assistant. Be friendly and conversational."
        }
    }
]
```

**Key Principle:** Change ONLY the variable you're testing. Keep everything else identical.

---

## 🔄 **Model Overrides**

Override default API parameters per condition:

### **Temperature:**

**Low Temperature (0.1-0.5):** Focused, deterministic
```json
"model_overrides": {
    "temperature": 0.3
}
```
**Use for:** Factual Q&A, consistent responses

**Medium Temperature (0.6-0.8):** Balanced
```json
"model_overrides": {
    "temperature": 0.7
}
```
**Use for:** General conversation, default

**High Temperature (0.9-1.5):** Creative, varied
```json
"model_overrides": {
    "temperature": 1.2
}
```
**Use for:** Creative tasks, diverse responses

---

### **Max Completion Tokens:**

```json
"model_overrides": {
    "max_completion_tokens": 1000  // Shorter responses
}
```

```json
"model_overrides": {
    "max_completion_tokens": 4000  // Longer responses
}
```

**Use for:**
- Testing effect of response length
- Different task complexity
- Cost management

---

## 📊 **Condition Assignment in Qualtrics**

### **For 3 Conditions:**

In Qualtrics Survey Flow, create randomizer with 3 embedded data blocks:
```
Randomizer - Evenly Present 3 Elements
    ├─ Embedded Data (condition = 0)
    ├─ Embedded Data (condition = 1)
    └─ Embedded Data (condition = 2)
```

### **For More Conditions:**

Add more blocks matching your condition count:
- 6 conditions = 0, 1, 2, 3, 4, 5
- 9 conditions = 0, 1, 2, 3, 4, 5, 6, 7, 8

**Condition indices start at 0!**

---

## 🧪 **Testing Your Conditions**

### **Validate JSON Syntax:**

```bash
# Check JSON is valid
python -c "import json; json.load(open('experimental_conditions.json')); print('✓ Valid JSON')"
```

### **Test Each Condition:**

```bash
# Test condition 0
http://localhost:5000/gui?participant_id=TEST_C0&condition=0

# Test condition 1
http://localhost:5000/gui?participant_id=TEST_C1&condition=1

# Verify each loads without errors
```

### **Check System Prompts:**

```bash
# Run command-line version to see full system prompts
python bot.py

# Select different conditions to review prompts
```

---

## 📝 **Example Template**

See `experimental_conditions.example.json` for a complete working example with 6 conditions demonstrating:
- Different bot names
- Different icons (emoji and images)
- Different colors/styling
- Different system prompts
- Disabled condition example
- Model parameter overrides

**To use as starting point:**
```bash
# Copy example to create your own:
cp experimental_conditions.example.json my_study_conditions.json

# Edit my_study_conditions.json for your study
# Update bot.py to use: config_file="my_study_conditions.json"
```

---

## ⚠️ **Common Mistakes to Avoid**

### **1. Missing Comma**
```json
[
    {"id": "a"}   // ❌ Missing comma
    {"id": "b"}
]
```

**Fix:** Add comma between objects
```json
[
    {"id": "a"},  // ✅ Comma added
    {"id": "b"}
]
```

---

### **2. Duplicate IDs**
```json
[
    {"id": "control", "name": "Control A"},
    {"id": "control", "name": "Control B"}  // ❌ Duplicate ID
]
```

**Fix:** Use unique IDs
```json
[
    {"id": "control_a", "name": "Control A"},
    {"id": "control_b", "name": "Control B"}  // ✅ Unique
]
```

---

### **3. Wrong Condition Index**

In Qualtrics, you use indices (0, 1, 2...), not IDs:

```javascript
// ❌ Wrong:
iframe.src = "...?condition=control"

// ✅ Correct:
iframe.src = "...?condition=0"  // Index in array
```

---

### **4. Inconsistent Styling**

If color isn't your variable, keep it consistent:

```json
// ❌ Don't vary colors unintentionally:
{"id": "a", "bot_styles": {"primary_color": "#4A90E2"}},
{"id": "b", "bot_styles": {"primary_color": "#E74C3C"}}  // Different color!

// ✅ Keep consistent if not testing color:
{"id": "a", "bot_styles": {"primary_color": "#4A90E2"}},
{"id": "b", "bot_styles": {"primary_color": "#4A90E2"}}  // Same
```

---

## 🔍 **Debugging Conditions**

### **Condition Won't Load:**

Check:
```bash
# 1. JSON syntax
python -c "import json; json.load(open('experimental_conditions.json'))"

# 2. Condition index in valid range
# If you have 6 conditions, valid indices are 0-5

# 3. Condition is enabled
# Check: "enabled": true
```

---

### **System Prompt Not Working as Expected:**

```bash
# View the actual prompt being sent:
python bot.py

# Select your condition and check what the combined prompt looks like
```

---

## 📚 **Additional Resources**

- **Full Example:** See `experimental_conditions.example.json`
- **Your Conditions:** `experimental_conditions.json` (your actual study)
- **Quick Reference:** `docs/CONDITION_REFERENCE.md`
- **Qualtrics Setup:** `docs/QUALTRICS_SETUP.md`

---

## ✅ **Checklist for New Conditions**

Before launching with new conditions:

- [ ] JSON syntax valid
- [ ] All required fields present
- [ ] Unique IDs for each condition
- [ ] Consistent styling (unless testing style)
- [ ] System prompts tested
- [ ] All conditions enabled
- [ ] Condition count matches Qualtrics randomizer
- [ ] Each condition tested locally
- [ ] Color contrast sufficient
- [ ] Icons/images exist in static folder (if used)

---

**Ready to design your own experimental conditions!**