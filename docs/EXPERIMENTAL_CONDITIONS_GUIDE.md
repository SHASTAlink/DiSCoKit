# Experimental Conditions Configuration Guide (Generic Template)

This document provides a **project-agnostic template** for configuring experimental conditions in `experimental_conditions.json`. It is intended for public reuse across studies and does **not** reference any specific domain, task, or prior project.

---

## Overview

The `experimental_conditions.json` file defines:

- **Study metadata** – high-level information for documentation and recordkeeping
- **Experimental conditions** – variations in how an AI assistant is presented or behaves

Participants are randomly assigned to one condition. The structure supports simple experiments (e.g., A/B tests) as well as more complex multi-condition designs.

---

## File Structure

The configuration file is a JSON object with two required sections:

```json
{
  "study_metadata": { ... },
  "conditions": [ ... ]
}
```

Both sections are required.

---

## Study Metadata

The `study_metadata` section contains descriptive information about the study. These fields do not affect runtime behavior but are useful for organization, auditing, and collaboration.

```json
"study_metadata": {
  "study_id": "example_study",
  "study_name": "AI Interaction Study",
  "description": "Examines user interaction with an AI assistant.",
  "irb_protocol": "IRB-XXXX-XXX",
  "principal_investigator": "Dr. Name",
  "identity_protection": {
    "enabled": true
  }
}
```

### Identity Protection

If enabled, identity protection automatically prepends a short instruction to each condition’s system prompt, preventing the assistant from revealing implementation or model details.

This helps maintain experimental validity and ensures consistency across conditions.

---

## Conditions

Each entry in the `conditions` array defines one experimental condition.

### Required Condition Fields

- `id` – unique identifier (string)
- `name` – human-readable label
- `description` – brief explanation of what varies in this condition
- `enabled` – whether the condition is active
- `bot_name` – name shown to participants (empty string for unnamed assistant)
- `bot_icon` – optional icon filename
- `bot_styles` – visual configuration
- `system_prompt` – instructions that shape assistant behavior

### Minimal Condition Example

```json
{
  "id": "baseline",
  "name": "Baseline Assistant",
  "description": "Neutral assistant with no personalization.",
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
    "behavior": "Provide clear, neutral guidance and follow task instructions."
  }
}
```

---

## System Prompt Structure

The keys inside `system_prompt` are arbitrary. The application concatenates all values in order.

```json
"system_prompt": {
  "role": "...",
  "behavior": "...",
  "constraints": "..."
}
```

Avoid including identity statements such as "You are a helpful AI assistant". These are automatically generated when identity protection is enabled.

---

## Example: Three-Condition Study

```json
"conditions": [
  {
    "id": "baseline",
    "name": "Baseline",
    "bot_name": "",
    "system_prompt": {"behavior": "Use a neutral, professional tone."}
  },
  {
    "id": "named",
    "name": "Named Assistant",
    "bot_name": "Alex",
    "system_prompt": {"behavior": "Use a neutral, professional tone."}
  },
  {
    "id": "conversational",
    "name": "Conversational Style",
    "bot_name": "",
    "system_prompt": {"behavior": "Use a warm, conversational tone."}
  }
]
```

---

## Common Design Patterns

### A/B Test (2 Conditions)

Vary one factor while holding all others constant.

### Multi-Condition Comparison (3+ Conditions)

Compare multiple presentation or behavior styles against a baseline.

### Factorial Designs

Combine multiple independent variables (e.g., naming × tone) for structured comparisons.

---

## Best Practices

- Change **one variable per condition** whenever possible
- Keep task instructions identical across conditions
- Use clear, neutral descriptions
- Validate JSON before deployment
- Test each condition manually

---

This template is intended as a **neutral starting point** for a wide range of AI interaction studies.

