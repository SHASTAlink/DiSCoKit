# Qualtrics Integration Guide (Generic Template)

This guide explains how to embed a web-based AI chat interface into a Qualtrics survey using a **platform-agnostic, task-neutral approach**. It intentionally avoids step-by-step UI instructions that may change over time and instead focuses on **conceptual requirements and stable configuration patterns**.

---

## Purpose and Scope

This document is designed to:

- Describe **what must be configured** in Qualtrics (conceptually)
- Explain **why each configuration element is required**
- Provide **copy-paste–ready technical artifacts** (e.g., JavaScript, variable names)

It does **not** attempt to mirror the exact wording, buttons, or layout of the Qualtrics user interface.

---

## High-Level Integration Model

At a minimum, the integration requires:

1. A **unique participant identifier** provided by Qualtrics
2. A **randomly assigned experimental condition**
3. An **embedded web application** loaded via iframe
4. A mechanism to **pass identifiers and condition values** to that application

All instructions below are framed in these terms.

---

## Required Embedded Variables

Your survey must define and populate the following embedded variables **before** the chat interface loads:

| Variable Name   | Purpose |
|-----------------|---------|
| `participant_id` | Unique identifier for each participant |
| `condition`      | Experimental condition assignment |

### Participant Identifier

The `participant_id` must be:

- Unique per respondent
- Stable across survey blocks
- Accessible to JavaScript via Qualtrics piping

**Recommended source:** the Qualtrics ResponseID.

Other sources (e.g., panel IDs or URL parameters) may be used if they meet the same criteria.

---

## Condition Assignment

Participants must be assigned to **exactly one condition**.

This is typically achieved by:

- Using Qualtrics randomization logic
- Setting the `condition` embedded variable to a numeric or string value
- Ensuring assignments are approximately evenly distributed

### Example Condition Scheme

For a three-condition study:

```
condition = 0
condition = 1
condition = 2
```

The meaning of each value must correspond to the condition ordering used by the chat application.

---

## Participant-Facing Instructions

Before the chat interface appears, include brief neutral instructions explaining the interaction.

### Example (Generic)

```
You will interact with an AI assistant through a chat interface.

Use the chat to complete the activity described by the assistant.
Follow the assistant’s guidance and ask questions if anything is unclear.

When you are finished, return to the survey and continue.
```

Avoid references to experimental conditions, hypotheses, or system behavior.

---

## Embedding the Chat Interface

The chat interface is embedded using a Qualtrics question that supports custom JavaScript.

### Technical Requirements

- JavaScript execution enabled
- Ability to hide the default text-entry input
- Ability to inject an iframe

---

## Integration Script

The following JavaScript illustrates the required logic. UI-specific steps for inserting this code are intentionally omitted.

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    // Replace with your deployed chat app URL (no trailing slash)
    var CHAT_APP_URL = "https://your-chat-app.com";

    // Set to false to disable task execution (review-only mode)
    var TASK_ACTIVE = true;

    this.hideNextButton();

    var textInput = this.getQuestionContainer().querySelector('.InputText');
    if (textInput) textInput.style.display = 'none';

    var participantId = "${e://Field/participant_id}";
    var condition = "${e://Field/condition}";

    if (!participantId || participantId.charAt(0) === '$') {
        console.error("Participant ID not set");
        return;
    }
    if (!condition || condition.charAt(0) === '$') {
        console.error("Condition not set");
        return;
    }

    var url = CHAT_APP_URL + "/gui?participant_id=" + encodeURIComponent(participantId) +
              "&condition=" + encodeURIComponent(condition);

    if (TASK_ACTIVE === false) {
        url += "&task_active=false";
    }

    var iframe = document.createElement('iframe');
    iframe.src = url;
    iframe.style.width = '100%';
    iframe.style.height = '700px';
    iframe.style.border = '1px solid #ccc';
    iframe.style.borderRadius = '8px';
    iframe.frameBorder = '0';

    this.getQuestionContainer().appendChild(iframe);

    iframe.onload = function() {
        Qualtrics.SurveyEngine.getInstance().showNextButton();
    };

    setTimeout(function() {
        Qualtrics.SurveyEngine.getInstance().showNextButton();
    }, 5000);
});
```

---

## Optional: Multi-Stage Designs

The optional `task_active` parameter allows reuse of the same conversation across multiple survey stages.

| Value | Behavior |
|------|----------|
| `true`  | Assistant performs the task |
| `false` | Assistant enters review-only mode |

This enables designs such as:

- Task → questionnaire → review
- Pre-task exposure → task
- Multiple task attempts with shared context

---

## Validation and Testing

Before launch, confirm that:

- `participant_id` is populated correctly
- `condition` values match the application’s condition index
- The chat interface loads consistently
- Navigation controls behave as expected
- Test data can be exported and linked via `participant_id`

---

## Notes for Public Reuse

- Avoid UI-specific language that may change over time
- Focus documentation on **data flow and invariants**
- Treat Qualtrics as an interchangeable survey platform
- Keep task logic in the application, not the survey

---

This guide is intended as a **stable, public-facing reference** for embedding AI chat interfaces into survey platforms such as Qualtrics.

