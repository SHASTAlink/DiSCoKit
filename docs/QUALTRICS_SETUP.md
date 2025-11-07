# Qualtrics Integration Guide

**For Survey Authors:** This guide shows you how to embed the chat interface in your Qualtrics survey. You'll need about 15-20 minutes.

**Before you start:** You need the web address (URL) where the chat app is hosted. It will look like: `https://my-chat-app.com`

**About the conditions:** There are 9 experimental conditions (0-8) that vary how the AI presents itself (names, icons, or language style). All conditions use a 6-step guided workflow where participants collaborate with the AI to create a poem.

---

## 📋 **Table of Contents**

1. [Basic Setup](#step-1-set-up-survey-flow-5-minutes) - Single-stage experiment
2. [Multi-Stage Experiments](#multi-stage-experiment-designs) - Using `task_active` parameter
3. [Common Patterns](#common-multi-stage-patterns) - Example flows

---

## Step 1: Set Up Survey Flow (5 minutes)

### 1.1 Open Survey Flow
1. In your Qualtrics survey, click **"Survey Flow"** in the left sidebar

### 1.2 Add Participant ID and Condition Fields
1. At the very top, click **"Add a New Element Here"**
2. Select **"Embedded Data"**
3. Click **"Create New Field or Choose From Dropdown"**, type `participant_id`, press Enter
4. Click **"Create New Field or Choose From Dropdown"** again, type `condition`, press Enter

You should now see:
```
Embedded Data
    participant_id
    condition
```

### 1.3 Set Participant ID (Choose ONE option)

**Option A: Use Qualtrics ResponseID (Recommended)**
1. Click **"Set a value now"** next to `participant_id`
2. Paste this: `${e://Field/ResponseID}`
3. Click the checkmark

**Why this is best:**
- ✅ Guaranteed unique across all responses
- ✅ Automatically matches Qualtrics data export
- ✅ Already in your survey data (default column)
- ✅ Most reliable for linking chat data to survey responses

**Option B: Use Prolific/MTurk ID**
1. Click **"Set a value now"** next to `participant_id`
2. Select **"Value from URL Parameter"**
3. Type the parameter name (e.g., `PROLIFIC_PID` for Prolific, `workerId` for MTurk)
4. Click the checkmark

**Option C: Generate Random ID (Not Recommended)**
1. Click **"Set a value now"** next to `participant_id`
2. Paste this: `P${rand://int/1000000:9999999}`
3. Click the checkmark

**Note:** Option C creates a random ID that won't appear in standard Qualtrics exports unless you explicitly add the `participant_id` embedded data field to your export. Use Option A (ResponseID) for foolproof data linking.

### 1.4 Set Up Random Condition Assignment
1. Below your Embedded Data, click **"Add a New Element Here"**
2. Select **"Randomizer"**
3. Change dropdown to **"Evenly Present Elements"**
4. Now add 9 blocks inside the Randomizer:

**Repeat these steps 9 times (for conditions 0, 1, 2, 3, 4, 5, 6, 7, 8):**
- Inside the Randomizer, click **"Add a New Element Here"**
- Select **"Embedded Data"**
- Select `condition` from the dropdown
- Click **"Set a value now"**, type the number (`0`, then `1`, then `2`, etc.)
- Click checkmark
- Drag into the Randomizer box if needed

Your Survey Flow should look like:
```
Embedded Data
    participant_id = [set]
    condition = (not set)

Randomizer - Evenly Present 9 Elements
    ├─ Embedded Data (condition = 0)
    ├─ Embedded Data (condition = 1)
    ├─ Embedded Data (condition = 2)
    ├─ Embedded Data (condition = 3)
    ├─ Embedded Data (condition = 4)
    ├─ Embedded Data (condition = 5)
    ├─ Embedded Data (condition = 6)
    ├─ Embedded Data (condition = 7)
    └─ Embedded Data (condition = 8)

[Your survey questions]
```

5. Click **"Apply"** to save

---

## Step 2: Add Chat to Your Survey (8 minutes)

### 2.1 Add Instructions (Optional)
1. In your survey, add a new question
2. Change type to **"Text/Graphic"**
3. Add your instructions (see example below)

**Example instructions:**
```
You will chat with an AI poetry assistant.

Task:
1. Ask the assistant to help you write a poem
2. Follow the 6-step process to create a 10-line poem with rhyme scheme AABBCCDDEE
3. Review the poem carefully when presented
4. Provide feedback if anything seems incorrect
5. Click "Next" when you're finished

The assistant will guide you through:
• Choosing a topic
• Deciding the message
• Selecting voice/tone
• Specifying structure (10 lines, AABBCCDDEE)
• Reviewing test lines
• Getting the final poem
```

### 2.2 Add Chat Question
1. Add a new question
2. Change type to **"Text Entry"**
3. Question text: `Chat Interface` (or leave blank)
4. Click the **gear icon** ⚙️
5. Click **"JavaScript"**
6. Delete all the template code
7. **Copy and paste this COMPLETE code block:**

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    // CHANGE THIS: Replace with your chat app URL (no trailing slash)
    var CHAT_APP_URL = "https://your-chat-app.com";
    
    // OPTIONAL: Set to false to show conversation in review-only mode
    var TASK_ACTIVE = true;
    
    // ============================================================
    // Don't change anything below this line
    // ============================================================
    
    this.hideNextButton();
    var textInput = this.getQuestionContainer().querySelector('.InputText');
    if (textInput) textInput.style.display = 'none';
    
    var participantId = "${e://Field/participant_id}";
    var condition = "${e://Field/condition}";
    
    // Validate data - check if piping failed
    if (!participantId || participantId.length < 2 || participantId.charAt(0) === '$') {
        alert("Error: Participant ID not set. Check Survey Flow.");
        return;
    }
    if (!condition || condition.length < 1 || condition.charAt(0) === '$') {
        alert("Error: Condition not set. Check Survey Flow randomizer.");
        return;
    }
    
    // Build URL with optional task_active parameter
    var url = CHAT_APP_URL + "/gui?participant_id=" + encodeURIComponent(participantId) + 
              "&condition=" + encodeURIComponent(condition);
    
    if (TASK_ACTIVE === false) {
        url += "&task_active=false";
    }
    
    // Create iframe
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
    
    // Backup: show Next button after 5 seconds
    setTimeout(function() {
        Qualtrics.SurveyEngine.getInstance().showNextButton();
    }, 5000);
});

Qualtrics.SurveyEngine.addOnReady(function() {});
Qualtrics.SurveyEngine.addOnUnload(function() {});
```

8. **IMPORTANT:** Find this line near the top:
   ```javascript
   var CHAT_APP_URL = "https://your-chat-app.com";
   ```
   
9. Replace `https://your-chat-app.com` with your actual chat app URL
   - ✅ Good: `https://shade.ischool.syr.edu`
   - ✅ Good: `https://chatbot.university.edu`
   - ❌ Bad: `https://chatbot.com/` (remove trailing slash)
   - ❌ Bad: `http://localhost:5000` (must be a public URL)

10. Click **"Save"**

---

## 🎭 **Multi-Stage Experiment Designs**

The `task_active` parameter enables sophisticated multi-stage experiments where you control when the AI performs its main task.

### **How It Works:**

- `task_active=true` (or omitted) → AI performs main task normally
- `task_active=false` → AI politely declines task work, conversation history preserved

### **Setting task_active in Qualtrics:**

In the JavaScript code block, change this line:

```javascript
var TASK_ACTIVE = true;   // Task active
var TASK_ACTIVE = false;  // Review mode only
```

Or build the URL manually in JavaScript (advanced):
```javascript
var url = CHAT_APP_URL + "/gui?participant_id=" + participantId + 
          "&condition=" + condition + "&task_active=false";
```

---

## 📚 **Common Multi-Stage Patterns**

### **Pattern 1: Task → Reflect → Review**

**Use case:** Participants complete task, answer questions, then review their conversation

```
┌─────────────────────────────────────────────────┐
│ Block 1: Poetry Writing                         │
│ TASK_ACTIVE = true                              │
│ Participant writes poem with AI                 │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 2: Experience Questions                   │
│ Standard Qualtrics questions:                   │
│ - How satisfied were you?                       │
│ - Did the AI make any mistakes?                 │
│ - How much do you blame the AI for errors?      │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 3: Conversation Review                    │
│ TASK_ACTIVE = false                             │
│ Shows same conversation, AI declines new poetry │
│ Instructions: "Review your conversation above"  │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 4: Reflection Questions                   │
│ - Looking back, what do you think caused...?    │
│ - After reviewing, how would you rate...?       │
└─────────────────────────────────────────────────┘
```

### **Pattern 2: Multiple Task Attempts**

**Use case:** Test learning or adaptation across multiple attempts

```
┌─────────────────────────────────────────────────┐
│ Block 1: First Attempt                          │
│ TASK_ACTIVE = true                              │
│ "Write a poem about nature"                     │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 2: Questions about first attempt          │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 3: Second Attempt                         │
│ TASK_ACTIVE = true (same participant_id!)       │
│ "Write a different poem about friendship"       │
│ Conversation history preserved                  │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 4: Review Both Poems                      │
│ TASK_ACTIVE = false                             │
│ Shows complete conversation with both poems     │
└─────────────────────────────────────────────────┘
```

### **Pattern 3: Pre-Task Exposure → Task**

**Use case:** Prime participants before main task

```
┌─────────────────────────────────────────────────┐
│ Block 1: Get Acquainted                         │
│ TASK_ACTIVE = false                             │
│ "Chat with the AI about anything for 2 minutes" │
│ AI won't do main task yet                       │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 2: Main Task                              │
│ TASK_ACTIVE = true                              │
│ "Now work with the AI to write a poem"         │
│ Previous casual chat visible in history         │
└─────────────────────────────────────────────────┘
```

### **Pattern 4: Intervention Study**

**Use case:** Test effect of interruption or feedback

```
┌─────────────────────────────────────────────────┐
│ Block 1: Initial Task                           │
│ TASK_ACTIVE = true                              │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 2: Intervention/Training                  │
│ Show training material or manipulation          │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 3: Post-Intervention Task                 │
│ TASK_ACTIVE = true                              │
│ Same participant_id, can reference prior work   │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Block 4: Review & Compare                       │
│ TASK_ACTIVE = false                             │
│ "Review both poems - before and after training" │
└─────────────────────────────────────────────────┘
```

---

## 🔧 **Implementation Examples**

### **Example 1: Single Chat Block (Basic)**

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    var CHAT_APP_URL = "https://shade.ischool.syr.edu";
    var TASK_ACTIVE = true;  // Task is active
    
    // ... rest of code from Step 2.2 ...
});
```

### **Example 2: Review Block (Task Disabled)**

Create a second question with this JavaScript:

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    var CHAT_APP_URL = "https://shade.ischool.syr.edu";
    var TASK_ACTIVE = false;  // Review mode - AI won't write new poems
    
    // ... rest of code from Step 2.2 ...
});
```

Instructions for this block:
```
Review Your Conversation

Above is your complete conversation with the AI. Take a moment to review 
what was discussed. You can ask the AI questions about the conversation, 
but it will not write additional poems.

After reviewing, click Next to continue.
```

### **Example 3: Reactivation Block**

Create a third question:

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    var CHAT_APP_URL = "https://shade.ischool.syr.edu";
    var TASK_ACTIVE = true;  // Task active again
    
    // ... rest of code from Step 2.2 ...
});
```

Instructions:
```
Write Another Poem

Work with the AI again to write a second poem on a different topic. 
Your previous conversation is still visible.
```

---

## 🎯 **What Participants See**

### **When task_active=true:**
```
Participant: "Help me write a poem"
AI: "Great! Let's do this. We'll follow a 6-step process..."
```

### **When task_active=false (same conversation):**
```
Participant: "Help me write another poem"
AI: "The task portion of this activity is complete. 
     Feel free to continue with the survey!"

Participant: "What rhyme scheme did we use?"
AI: "We used AABBCCDDEE for your poem about homework. 
     Anything else I can help clarify?"
```

### **When reactivated (task_active=true again):**
```
Participant: "Write a poem about friendship"
AI: "Perfect. What message or story should this convey?"
```

**Note:** The conversation history is always visible. Only the AI's willingness to perform the main task changes.

---

## 📊 **Database Logging**

When participants load the interface with `task_active=false` for the first time, a system message is automatically logged:

```
TASK_STATE: inactive - Task completion mode enabled
```

**Benefits for PIs:**
- ✅ Clear audit trail of when review mode was active
- ✅ Timestamp shows exact transition point
- ✅ Visible in data exports
- ✅ Not visible to participants (system messages are filtered from UI)

**Example database export:**
```
timestamp           | role      | content
--------------------|-----------|----------------------------------
2025-11-07 14:00:00 | user      | help me write a poem
2025-11-07 14:00:15 | assistant | Great! Let's do this...
2025-11-07 14:05:00 | system    | TASK_STATE: inactive - Task completion mode enabled
2025-11-07 14:05:10 | user      | write another poem
2025-11-07 14:05:12 | assistant | The task portion is complete...
```

---

## ✅ **Testing Your Setup**

**Before launching to participants, test these scenarios:**

### Test 1: Basic Flow
1. Open survey preview
2. Complete poetry task
3. Click Next
4. Verify data appears in Qualtrics

### Test 2: Multi-Stage (if applicable)
1. Complete first chat block
2. Answer intermediate questions
3. Load second chat block (review mode)
4. Try to request new poem → AI should decline
5. Ask general question → AI should respond

### Test 3: Cross-Block History
1. Complete first chat (create poem about Topic A)
2. Load second chat block
3. Verify conversation history includes Topic A poem
4. Ask "what topic did we use?" → AI should reference Topic A

### Test 4: Condition Variation
1. Open survey in incognito/private window
2. Complete task
3. Repeat 9 times to test all conditions
4. Verify each condition looks/behaves correctly

### Test 5: Data Export
1. Complete test survey
2. Export data from Flask app: `python db_utils.py export participants`
3. Verify participant_id matches Qualtrics ResponseID
4. Verify condition assignment is logged
5. Check for `TASK_STATE` markers if using multi-stage

---

## 🐛 **Troubleshooting**

**"Error: Participant ID not set"**
- Check Survey Flow: participant_id must be set BEFORE the chat question
- Verify piping syntax: `${e://Field/ResponseID}` or `${e://Field/participant_id}`

**"Error: Condition not set"**
- Check randomizer is BEFORE the chat question in Survey Flow
- Verify condition values are 0-8 (not 1-9)

**"Chat doesn't load"**
- Verify CHAT_APP_URL has no trailing slash
- Check your university firewall isn't blocking the chat server
- Test the URL directly in a browser

**"Conversation doesn't persist across blocks"**
- Verify both blocks use same `participant_id` piping
- Check that participant_id is actually the same value (not regenerating)

**"task_active not working"**
- Verify TASK_ACTIVE = false (not "false" in quotes)
- Check Flask console logs for "TASK_STATE: inactive" message
- Test URL directly: `https://yourapp.com/gui?participant_id=TEST&condition=2&task_active=false`

**"AI still writes poems when task_active=false"**
- Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
- Check browser console for `taskActive: false` in initialization logs
- Verify the override is being injected (check Flask logs)

---

## 🎓 **Tips for Survey Design**

### **Best Practices:**

1. **Clear Instructions:** Tell participants what to expect in each block
2. **Block Labeling:** Use descriptive question text like "Part 1: Write Your Poem"
3. **Time Estimates:** Let participants know how long each chat will take
4. **Progress Indicators:** Show where they are in the survey
5. **Test Extensively:** Complete the entire survey yourself multiple times

### **Recommended Question Flow:**

```
1. Consent
2. Instructions
3. Demographics
4. [CHAT BLOCK 1 - Task Active]
5. Experience questions (satisfaction, ease, etc.)
6. [CHAT BLOCK 2 - Review Mode]
7. Attribution questions (who's responsible for errors?)
8. Open-ended reflection
9. Debrief
```

### **Timing Guidance:**

- Poetry task typically takes: 5-8 minutes
- Review block: 2-3 minutes
- Include buffer time in Prolific/MTurk estimates

### **Attention Checks:**

Consider adding:
- "What was the topic of your poem?" (measures engagement)
- "Did the AI make any mistakes?" (measures attention to task)

---

## 📈 **Data Analysis Tips**

After data collection:

1. **Export from Flask:** `python db_utils.py export participants`
2. **Export from Qualtrics:** Include participant_id in export
3. **Merge datasets:** Join on participant_id/ResponseID
4. **Look for patterns:**
   - Conversation length by condition
   - Error detection by condition
   - Blame attribution by condition
   - Time spent in each stage

**Database markers to filter on:**
- `TASK_STATE: inactive` - Reviews/reflections
- `role = 'system'` with `CRITICAL OVERRIDE` - Task-inactive states
- Message timestamps - Interaction timing

---

## ⚙️ **Advanced Configurations**

### **Dynamic Task Control:**

Use Qualtrics embedded data to control task_active:

```javascript
// Set in Survey Flow before chat block
Embedded Data: task_mode = "active" or "review"

// In JavaScript:
var taskMode = "${e://Field/task_mode}";
var TASK_ACTIVE = (taskMode !== "review");
```

### **Conditional Blocks:**

Use Branch Logic in Survey Flow:

```
If condition = 0-2 (Study 2a)
    → Show poetry review block
If condition = 3-5 (Study 2b)
    → Skip review, go to attribution questions
```

### **Custom Instructions Per Stage:**

```
Block 1 (task_active=true):
"Create a poem with the AI assistant."

Block 2 (task_active=false):
"Review the conversation above. Note any mistakes or issues."

Block 3 (task_active=true):
"Work with the AI to revise the poem based on your notes."
```

---

## 🔍 **Verifying Your Setup**

### **Quick Verification Checklist:**

- [ ] Survey Flow has participant_id set at the top
- [ ] Survey Flow has condition randomizer (9 conditions)
- [ ] Chat question has correct CHAT_APP_URL
- [ ] Test preview shows chat interface
- [ ] Can complete full poetry task in preview
- [ ] Participant_id appears in Qualtrics data
- [ ] Can export matching data from Flask app
- [ ] (If multi-stage) Review mode works correctly
- [ ] (If multi-stage) Task can be reactivated
- [ ] All 9 conditions tested

### **Final Pre-Launch Test:**

1. Complete survey as a real participant would
2. Export Qualtrics data
3. Export Flask data: `python db_utils.py export participants`
4. Verify you can match records by participant_id
5. Check conversation content matches expectations
6. Confirm condition assignment logged correctly

---

## 📞 **Need Help?**

- **Technical issues:** Check Flask app logs
- **Qualtrics issues:** Use Qualtrics Support
- **Research design:** Consult with your methodology team
- **Integration questions:** See this guide or contact your developer

---

**You're ready to launch your experiment!** 🚀