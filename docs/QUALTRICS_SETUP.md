# Qualtrics Integration Guide

**For Survey Authors:** This guide shows you how to embed the chat interface in your Qualtrics survey. You'll need about 15 minutes.

**Before you start:** You need the web address (URL) where the chat app is hosted. It will look like: `https://my-chat-app.com`

**About the conditions:** There are 9 experimental conditions (0-8) that vary how the AI presents itself (names, icons, or language style). All conditions use a 6-step guided workflow where participants collaborate with the AI to create a poem.

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

**Option A: Generate Random ID (Easiest)**
1. Click **"Set a value now"** next to `participant_id`
2. Paste this: `P${rand://int/1000000:9999999}`
3. Click the checkmark

**Option B: Use Prolific/MTurk**
1. Click **"Set a value now"** next to `participant_id`
2. Select **"Value from URL Parameter"**
3. Type the parameter name (e.g., `PROLIFIC_PID` for Prolific, `workerId` for MTurk)
4. Click the checkmark

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
    
    // Create iframe
    var iframe = document.createElement('iframe');
    iframe.src = CHAT_APP_URL + "/gui?participant_id=" + encodeURIComponent(participantId) + 
                 "&condition=" + encodeURIComponent(condition);
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