# Qualtrics Integration Guide

**For Survey Authors:** This guide shows you how to embed a web-based AI chat interface into a Qualtrics survey. You'll need about 15–20 minutes.

**Before you start:** You need the web address (URL) where your chat application is hosted (e.g., `https://my-chat-app.example.edu`). Your application developer can provide this.

---

## Table of Contents

1. [Survey Flow Setup](#step-1-survey-flow-setup) — Embedded variables and randomization
2. [Embedding the Chat Interface](#step-2-embedding-the-chat-interface) — JavaScript and iframe configuration
3. [Multi-Stage Experiment Designs](#multi-stage-experiment-designs) — Using the `task_active` parameter
4. [Testing and Troubleshooting](#testing-and-troubleshooting) — Verification checklist and common issues

---

## Step 1: Survey Flow Setup

All embedded variables must be defined and populated in the Survey Flow **before** the survey block containing the chat interface. If they appear after the chat block, the JavaScript will not be able to read them.

### 1.1 Create Embedded Data Fields

Open your survey's flow editor and add an **Embedded Data** element at the very top. Define two fields:

| Field Name       | Purpose                                    |
|------------------|--------------------------------------------|
| `participant_id` | Unique identifier for each respondent      |
| `condition`      | Experimental condition assignment (numeric) |

After this step your flow should show both fields listed under a single Embedded Data element near the top.

### 1.2 Set the Participant ID

Set the value of `participant_id` using one of the following approaches. Choose the one that fits your recruitment method.

**Option A — Qualtrics ResponseID (recommended for most studies)**

Set the value of `participant_id` to the piped field `${e://Field/ResponseID}`.

This is the simplest and most reliable option: it is guaranteed unique, appears automatically in every Qualtrics data export, and requires no external coordination.

**Option B — External panel ID (Prolific, MTurk, etc.)**

If your participants arrive via a recruitment platform that passes an ID through the survey URL, set `participant_id` to pull from the appropriate URL parameter. Common parameter names include `PROLIFIC_PID` (Prolific) and `workerId` (MTurk). Use whichever mechanism Qualtrics provides to read a value from a URL query parameter.

**Option C — Random ID (not recommended)**

If you have no other option, you can generate a random numeric ID using Qualtrics' random integer piping (e.g., `P${rand://int/1000000:9999999}`). Be aware that this ID will not appear in standard Qualtrics exports unless you explicitly include the `participant_id` embedded data field.

### 1.3 Set Up Random Condition Assignment

Below the Embedded Data element, add a **Randomizer** element configured to evenly present its child elements. Inside the Randomizer, add one Embedded Data element per condition, each setting the `condition` field to a different value.

For example, a three-condition study would have:

```
Embedded Data
    participant_id = ${e://Field/ResponseID}
    condition      = (not yet set — assigned below)

Randomizer — Evenly Present 3 Elements
    ├─ Embedded Data: condition = 0
    ├─ Embedded Data: condition = 1
    └─ Embedded Data: condition = 2

[Your survey blocks follow here]
```

Adjust the number of conditions to match your study design. Condition values must be numeric and must correspond to the indices your chat application expects (typically starting from 0).

> **Important:** Click **Apply** (or the equivalent save action) to commit your Survey Flow changes before proceeding.

---

## Step 2: Embedding the Chat Interface

### 2.1 Participant Instructions (Optional)

Before the chat question, consider adding a text-only question with brief, neutral instructions. Tailor these to your specific task but avoid revealing experimental conditions or hypotheses.

**Example (adapt to your study):**

```
You will interact with an AI assistant through a chat interface.

Follow the assistant's guidance to complete the activity.
When you are finished, click "Next" to continue the survey.
```

### 2.2 Add the Chat Question

Create a new **Text Entry** question. This question's visible text can be minimal (e.g., "Chat Interface") — participants will see the embedded chat, not a text box.

Open the question's JavaScript editor and replace any template code with the script below. The method for accessing the JavaScript editor varies across Qualtrics versions, but it is typically available through the question's settings or context menu.

**Copy and paste this complete script:**

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    // ============================================================
    // CONFIGURATION — Edit these two values
    // ============================================================

    // Your chat application URL (no trailing slash)
    var CHAT_APP_URL = "https://your-chat-app.example.edu";

    // Set to false for review-only mode (see Multi-Stage Designs)
    var TASK_ACTIVE = true;

    // ============================================================
    // Do not change anything below this line
    // ============================================================

    this.hideNextButton();

    var textInput = this.getQuestionContainer().querySelector('.InputText');
    if (textInput) textInput.style.display = 'none';

    var participantId = "${e://Field/participant_id}";
    var condition = "${e://Field/condition}";

    // Validate — a leading '$' means Qualtrics piping failed
    if (!participantId || participantId.length < 2 || participantId.charAt(0) === '$') {
        console.error("participant_id not set. Check Survey Flow.");
        return;
    }
    if (!condition || condition.length < 1 || condition.charAt(0) === '$') {
        console.error("condition not set. Check Survey Flow randomizer.");
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

    // Show the Next button once the iframe loads (or after 5s as a fallback)
    iframe.onload = function() {
        Qualtrics.SurveyEngine.getInstance().showNextButton();
    };
    setTimeout(function() {
        Qualtrics.SurveyEngine.getInstance().showNextButton();
    }, 5000);
});

Qualtrics.SurveyEngine.addOnReady(function() {});
Qualtrics.SurveyEngine.addOnUnload(function() {});
```

**After pasting**, update `CHAT_APP_URL` to point to your deployed chat application:

- Use the full URL with `https://` and **no trailing slash**.
- The URL must be publicly accessible (not `localhost`).

Save the question.

---

## Multi-Stage Experiment Designs

The `task_active` parameter lets you reuse the same chat conversation across multiple survey blocks while controlling whether the AI performs its primary task.

| `TASK_ACTIVE` value | Behavior |
|---------------------|----------|
| `true` (default)    | AI performs its main task normally |
| `false`             | AI enters review/conversation-only mode; declines new task work |

Conversation history is always preserved across blocks as long as the same `participant_id` is used. Only the AI's willingness to perform the primary task changes.

### How to Use

Create a separate Text Entry question with its own copy of the JavaScript for each chat block. Set `TASK_ACTIVE = true` or `TASK_ACTIVE = false` as needed. The rest of the script remains identical.

### Common Patterns

**Pattern 1 — Task → Questionnaire → Review:**
The participant completes the task (active), answers survey questions, then returns to the conversation in review mode (inactive) to reflect before answering attribution or evaluation questions.

**Pattern 2 — Pre-task Exposure → Task:**
The participant chats casually with the AI first (inactive), building familiarity, then completes the main task (active) with that conversation history intact.

**Pattern 3 — Multiple Task Attempts:**
The participant completes a task (active), answers questions, then completes a second task (active again) with the full conversation history visible.

**Pattern 4 — Intervention Study:**
Task (active) → intervention or training material (standard Qualtrics questions) → second task (active) → review (inactive).

### Advanced: Dynamic Task Control via Embedded Data

Instead of hardcoding `TASK_ACTIVE` per block, you can drive it from the Survey Flow:

1. Add an embedded data field (e.g., `task_mode`) and set its value to `"active"` or `"review"` at the appropriate point in the flow.
2. Replace the `TASK_ACTIVE` line in the JavaScript with:

```javascript
var taskMode = "${e://Field/task_mode}";
var TASK_ACTIVE = (taskMode !== "review");
```

This is useful when condition assignment should also determine which blocks show active vs. review mode.

---

## Testing and Troubleshooting

### Pre-Launch Checklist

Before deploying to participants, verify each of the following in a survey preview:

- `participant_id` is populated (not blank or showing raw piping syntax).
- `condition` is set to an expected numeric value.
- The chat interface loads and is interactive.
- The Next button appears after the iframe loads.
- Completing the chat and clicking Next advances the survey normally.
- If using multi-stage blocks: review mode shows conversation history but the AI declines new task requests.
- A test data export from Qualtrics includes `participant_id` and `condition`.
- A test data export from your chat application can be joined to Qualtrics data on `participant_id`.
- All conditions have been tested at least once (use incognito/private windows for fresh sessions).

### Common Issues

**Chat interface does not load:**
Verify that `CHAT_APP_URL` has no trailing slash, the URL is reachable from a browser, and your institution's firewall is not blocking the domain.

**"participant_id not set" or "condition not set" in browser console:**
The Embedded Data and Randomizer elements must appear **above** the chat block in the Survey Flow. Confirm they are in the correct order and that you clicked Apply/Save.

**Conversation does not persist across blocks:**
Both chat blocks must reference the same `participant_id` value. If using Option C (random ID), ensure the ID is not being regenerated between blocks.

**`task_active` has no effect:**
Confirm that `TASK_ACTIVE` is set to the boolean `false`, not the string `"false"`. Check your application's server logs for the `task_active` query parameter value.

**Condition values do not match expected behavior:**
Condition numbering in the Survey Flow must match the indices your chat application expects. Most applications use 0-based indexing.

---

## Data Linking

After data collection, you will have two datasets: one from Qualtrics and one from your chat application. Both contain `participant_id`, which serves as the join key.

If you used Option A (ResponseID) for `participant_id`, the Qualtrics ResponseID column and the chat application's `participant_id` column will contain identical values.

When using multi-stage designs, your chat application may log state transition markers (e.g., when the task mode changed). Consult your application's documentation for details on these markers and how they appear in data exports.

---

## Notes for Reuse and Adaptation

This guide is written to be study-agnostic. When adapting it for a specific experiment:

- Adjust the number of conditions in the Randomizer to match your design.
- Customize the participant-facing instructions for your task.
- Set `TASK_ACTIVE` per block as your multi-stage design requires.
- Update `CHAT_APP_URL` to point to your deployed application.

The JavaScript integration script, embedded variable names (`participant_id`, `condition`), and URL parameter contract (`/gui?participant_id=...&condition=...&task_active=...`) are stable across studies and do not need modification unless your application uses a different API contract.