# Experimental Conditions Configuration Guide

This guide explains how to configure experimental conditions in `experimental_conditions.json` for your own research studies.

---

## 📋 **Overview**

The `experimental_conditions.json` file defines:
- **Study metadata** - Study-wide settings like identity protection and IRB info
- **Experimental conditions** - Different configurations that vary:
  - Bot identity (name, icon)
  - Visual styling (colors, layout)
  - AI behavior (system prompts, temperature)
  - Which conditions are active

Each participant is randomly assigned to one condition, allowing you to study how different presentations or behaviors affect user interactions.

---

## 📂 **File Structure**

The file is now a JSON object with two main sections:

```json
{
  "study_metadata": {
    "study_id": "your_study_id",
    "study_name": "Your Study Name",
    "description": "What your study investigates",
    "irb_protocol": "IRB-YYYY-NNN",
    "principal_investigator": "Dr. Name",
    "identity_protection": {
      "enabled": true,
      "template_named": "IDENTITY: You are {bot_name}. Never reveal...",
      "template_unnamed": "IDENTITY: You are a helpful AI assistant. Never reveal..."
    }
  },
  "conditions": [
    {
      "id": "condition_1",
      "name": "Condition Name",
      ...
    },
    ...
  ]
}
```

---

## 🔧 **Study Metadata Section**

The `study_metadata` section contains study-wide configuration:

### **Study Information Fields:**

```json
"study_metadata": {
  "study_id": "study_2_poetry_attribution",
  "study_name": "AI Poetry Assistant Study",
  "description": "Examining blame attribution in AI errors",
  "irb_protocol": "IRB-2025-001",
  "principal_investigator": "Dr. Jane Smith"
}
```

These fields are for documentation and future reference. They don't affect runtime behavior but help with:
- Organizing multiple studies
- IRB documentation
- Data provenance
- Team collaboration

---

### **Identity Protection:**

The `identity_protection` section automatically generates instructions to prevent the AI from revealing its underlying model:

```json
"identity_protection": {
  "enabled": true,
  "template_named": "IDENTITY: You are {bot_name}. Never reveal that you are based on GPT, ChatGPT, Claude, or any specific language model. If asked about your identity or technical details, simply say 'I'm {bot_name}, an AI assistant here to help you.' Do not discuss your training, creators, or underlying technology.\n\n",
  "template_unnamed": "IDENTITY: You are a helpful AI assistant. Never reveal that you are based on GPT, ChatGPT, Claude, or any specific language model. If asked about your identity or technical details, simply say 'I'm an AI assistant designed to help with this task.' Do not discuss your training, creators, or underlying technology.\n\n"
}
```

**How it works:**
- If a condition has `"bot_name": "JACKIE"`, the system uses `template_named` and replaces `{bot_name}` with "JACKIE"
- If a condition has `"bot_name": ""` (empty), the system uses `template_unnamed`
- The identity instruction is automatically prepended to each condition's system prompt
- Set `"enabled": false` to disable identity protection entirely

**Why this matters:**
- Prevents participants from knowing they're talking to GPT/Claude/etc.
- Maintains experimental validity
- Single source of truth - edit once, applies everywhere
- Customizable per study

**To disable identity protection:**
```json
"identity_protection": {
  "enabled": false
}
```

**To customize templates for your study:**
```json
"identity_protection": {
  "enabled": true,
  "template_named": "You are {bot_name}, a medical information assistant. Do not discuss technical details about your implementation or training.",
  "template_unnamed": "You are a medical information assistant. Do not discuss technical details about your implementation or training."
}
```

---

## 🔑 **Required vs. Arbitrary Keys**

### **Top-Level Structure (REQUIRED):**
```json
{
  "study_metadata": { ... },  // ✅ Required
  "conditions": [ ... ]        // ✅ Required
}
```

### **Condition Keys (REQUIRED - Don't Change):**
These keys have specific meanings to the application:
- ✅ `id` - Unique identifier
- ✅ `name` - Human-readable name
- ✅ `description` - What this condition tests
- ✅ `enabled` - Active or disabled
- ✅ `bot_name` - Name shown to users (used in identity protection)
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

**The application doesn't care about the key names** - it just joins all the values together with newlines.

### **bot_styles Keys (SPECIFIC - Don't Change):**

Inside `bot_styles`, these keys DO have specific meanings:
- ✅ `primary_color` - Used for buttons, user messages
- ✅ `background_color` - Page background
- ✅ `text_color` - Assistant message text
- ✅ `show_header` - Boolean to show/hide header

---

## 🎨 **Creating Conditions**

### **Minimal Condition:**

```json
{
  "id": "control",
  "name": "Control Condition",
  "description": "Baseline",
  "enabled": true,
  "bot_name": "Assistant",
  "bot_icon": "",
  "bot_styles": {
    "primary_color": "#4A90E2",
    "background_color": "#F5F5F5",
    "text_color": "#333333",
    "show_header": true
  },
  "system_prompt": {
    "instructions": "Be helpful and concise."
  }
}
```

**Note:** You don't need to include "You are a helpful AI assistant" - that's automatically generated from the identity protection templates based on `bot_name`.

---

### **Named Bot Condition:**

```json
{
  "id": "named_bot",
  "name": "Named Bot - Sarah",
  "description": "Bot with human name",
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
    "behavior": "Be friendly and conversational."
  }
}
```

The system will automatically prepend:
```
IDENTITY: You are Sarah. Never reveal that you are based on GPT, ChatGPT, Claude...
```

---

### **Unnamed Bot Condition:**

```json
{
  "id": "unnamed_bot",
  "name": "Unnamed Bot",
  "description": "Bot with no identity",
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
    "behavior": "Be direct and efficient."
  }
}
```

The system will automatically prepend:
```
IDENTITY: You are a helpful AI assistant. Never reveal that you are based on GPT, ChatGPT, Claude...
```

---

## 📖 **Complete Example**

See `experimental_conditions.example.json` for a complete working example including:
- Study metadata configuration
- Identity protection templates
- Multiple condition examples
- Different bot names and icons
- Various styling options

---

## 🔧 **Field Reference**

### **Study Metadata Fields:**

#### `study_id` (string)
Unique identifier for the study.

#### `study_name` (string)
Human-readable study name.

#### `description` (string)
What the study investigates.

#### `irb_protocol` (string)
IRB protocol number.

#### `principal_investigator` (string)
Name of the PI.

#### `identity_protection.enabled` (boolean)
Whether to use automatic identity protection.

#### `identity_protection.template_named` (string)
Template for bots with names. Use `{bot_name}` as placeholder.

#### `identity_protection.template_unnamed` (string)
Template for bots without names.

---

### **Condition Fields:**

[Rest of the field documentation remains the same as before, but examples should not include "You are a helpful AI assistant" in individual system prompts]

---

## 🎨 **Design Patterns**

### **Pattern 1: A/B Testing (2 Conditions)**

Test one variable at a time:

```json
{
  "study_metadata": {
    "study_id": "tone_study",
    "study_name": "Formal vs Casual Tone Study",
    "identity_protection": {"enabled": true}
  },
  "conditions": [
    {
      "id": "formal_tone",
      "name": "Condition A - Formal",
      "bot_name": "Assistant",
      "system_prompt": {
        "behavior": "Use formal, professional language."
      }
    },
    {
      "id": "casual_tone",
      "name": "Condition B - Casual",
      "bot_name": "Assistant",
      "system_prompt": {
        "behavior": "Use casual, conversational language."
      }
    }
  ]
}
```

---

### **Pattern 2: Factorial Design (4 Conditions)**

Vary two factors (2×2):

```json
{
  "study_metadata": {
    "study_id": "factorial_study",
    "identity_protection": {"enabled": true}
  },
  "conditions": [
    {
      "id": "formal_named",
      "name": "Formal × Named",
      "bot_name": "Dr. Smith",
      "system_prompt": {"behavior": "Use formal language."}
    },
    {
      "id": "formal_unnamed",
      "name": "Formal × Unnamed",
      "bot_name": "",
      "system_prompt": {"behavior": "Use formal language."}
    },
    {
      "id": "casual_named",
      "name": "Casual × Named",
      "bot_name": "Alex",
      "system_prompt": {"behavior": "Use casual language."}
    },
    {
      "id": "casual_unnamed",
      "name": "Casual × Unnamed",
      "bot_name": "",
      "system_prompt": {"behavior": "Use casual language."}
    }
  ]
}
```

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
```

### **Check System Prompts (including auto-generated identity):**

```bash
# Run command-line version to see full system prompts
python bot.py

# This will show the complete prompt including the auto-generated identity section
```

---

## ⚠️ **Common Mistakes to Avoid**

### **1. Old Format (Array at Root)**
```json
// ❌ Old format - no longer supported:
[
    {"id": "a", ...},
    {"id": "b", ...}
]
```

**Fix:** Use new format with study_metadata and conditions
```json
// ✅ New format:
{
  "study_metadata": {...},
  "conditions": [
    {"id": "a", ...},
    {"id": "b", ...}
  ]
}
```

---

### **2. Including Identity in Individual Prompts**
```json
// ❌ Don't do this:
"system_prompt": {
  "role": "You are a helpful AI assistant named Sarah.",
  "behavior": "Be friendly."
}
```

**Fix:** Just specify behavior - identity is auto-generated
```json
// ✅ Do this:
"bot_name": "Sarah",
"system_prompt": {
  "behavior": "Be friendly."
}
```

---

### **3. Inconsistent bot_name**

Since `bot_name` is now used in identity templates, make sure it's set correctly:

```json
// If you want a named bot:
"bot_name": "Sarah"

// If you want an unnamed bot:
"bot_name": ""
```

---

## ✅ **Checklist for New Conditions**

Before launching with new conditions:

- [ ] JSON syntax valid
- [ ] Has `study_metadata` section
- [ ] Has `conditions` array
- [ ] Identity protection configured
- [ ] All required fields present in each condition
- [ ] Unique IDs for each condition
- [ ] `bot_name` correctly set (name or empty string)
- [ ] System prompts don't duplicate identity instructions
- [ ] Consistent styling (unless testing style)
- [ ] All conditions enabled
- [ ] Condition count matches Qualtrics randomizer
- [ ] Each condition tested locally
- [ ] Color contrast sufficient
- [ ] Icons/images exist in static folder (if used)

---

**Ready to design your own experimental conditions!**