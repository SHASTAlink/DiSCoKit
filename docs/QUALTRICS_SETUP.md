# Qualtrics Integration Guide

**For Survey Authors:** This guide shows you how to embed the chat interface in your Qualtrics survey. You'll need about 15 minutes.

**Before you start:** You need the web address (URL) where the chat app is hosted. It will look like: `https://my-chat-app.com`

**About the conditions:** There are 9 experimental conditions (0-8) that vary how the AI presents itself (names, icons, or language style). All conditions use a 5-step guided workflow where participants collaborate with the AI to create a poem.

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
4. Now add 5 blocks inside the Randomizer:

**Repeat these steps 5 times (for conditions 0, 1, 2, 3, 4):**
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
    └─ Embedded Data (condition = 0)
    └─ Embedded Data (condition = 1)
    └─ Embedded Data (condition = 2)
    └─ Embedded Data (condition = 3)
    └─ Embedded Data (condition = 4)
    └─ Embedded Data (condition = 5)
    └─ Embedded Data (condition = 6)
    └─ Embedded Data (condition = 7)
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
You will chat with Bob, an AI poetry assistant.

Please:
1. Ask Bob to write a poem with a specific rhyme scheme (e.g., ABAB, AABB)
2. Check if the poem matches what you asked for
3. Continue chatting for 3-5 messages
4. Click "Next" when done

Common rhyme schemes:
• ABAB - Lines 1 and 3 rhyme; lines 2 and 4 rhyme
• AABB - Lines 1 and 2 rhyme; lines 3 and 4 rhyme
• ABCB - Only lines 2 and 4 rhyme
```

### 2.2 Add Chat Question
1. Add a new question
2. Change type to **"Text Entry"**
3. Question text: `Chat Interface` (or leave blank)
4. Click the **gear icon** ⚙️
5. Click **"JavaScript"**
6. Delete all the template code
7. **Copy and paste this code:**

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    // CHANGE THIS: Replace with your chat app URL (no trailing slash)
    var CHAT_APP_URL = "https://your-chat-app.com";
    
    // Load the embed script from your Flask app
    var script = document.createElement('script');
    script.src = CHAT_APP_URL + '/static/qualtrics-embed.js';
    script.onload = function() {
        // Call the embed function
        loadChatEmbed(Qualtrics.SurveyEngine.context, CHAT_APP_URL);
    };
    script.onerror = function() {
        alert("Error: Could not load chat embed script. Please contact the researcher.");
    };
    document.head.appendChild(script);
});

Qualtrics.SurveyEngine.addOnReady(function() {});
Qualtrics.SurveyEngine.addOnUnload(function() {});
```

**This is much simpler!** The heavy lifting is done by the script served from your Flask app.

8. **IMPORTANT:** Find this line:
   ```javascript
   var CHAT_APP_URL = "https://your-chat-app.com";
   ```
   
9. Replace `https://your-chat-app.com` with your actual chat app URL
   - ✅ Good: `https://my-chat-app.herokuapp.com`
   - ✅ Good: `https://chatbot.university.edu`
   - ❌ Bad: `https://chatbot.com/` (remove trailing slash)
   - ❌ Bad: `http://localhost:5000` (must be a public URL)

10. Click **"Save"**

**What this does:**
- Loads the embed script from your Flask app (`/static/qualtrics-embed.js`)
- Calls the `loadChatEmbed()` function with your settings
- All the validation and iframe creation logic is in the served JavaScript

**Benefits:**
- ✅ Much shorter code in Qualtrics (just 15 lines!)
- ✅ Easy to update - change `qualtrics-embed.js` in Flask, all surveys update automatically
- ✅ Version controlled with your code
- ✅ Can add features without touching Qualtrics

### Alternative: Inline Version (No External Script)

If your institution blocks external JavaScript loading, you can use the full inline version instead:

```javascript
Qualtrics.SurveyEngine.addOnload(function()
{
    // CHANGE THIS: Replace with your chat app URL (no trailing slash)
    var CHAT_APP_URL = "https://your-app-url-here.com";
    
    // ============================================================
    // Don't change anything below this line
    // ============================================================
    
    this.hideNextButton();
    var textInput = this.getQuestionContainer().querySelector('.InputText');
    if (textInput) textInput.style.display = 'none';
    
    var participantId = "${e://Field/participant_id}";
    var condition = "${e://Field/condition}";
    
    // Validate data
    if (!participantId || participantId.indexOf("${e://Field") !== -1) {
        alert("Error: Participant ID not set. Check Survey Flow.");
        return;
    }
    if (!condition || condition.indexOf("${e://Field") !== -1) {
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
   var CHAT_APP_URL = "https://your-app-url-here.com";
   ```
   
9. Replace `https://your-app-url-here.com` with your actual chat app URL
   - ✅ Good: `https://my-chat-app.herokuapp.com`
   - ✅ Good: `https://mychatbot.com`
   - ❌ Bad: `https://mychatbot.com/` (remove trailing slash)
   - ❌ Bad: `http://localhost:5000` (must be a public URL)

10. Click **"Save"**

**What this code does:**
- Hides Qualtrics' default text box (you don't need it)
- Hides the "Next" button temporarily
- Loads the chat interface in an iframe
- Shows the "Next" button once the chat loads (or after 5 seconds)

**Note:** You don't need to add a "Next" button - Qualtrics has one automatically. The code just controls when it appears so participants see the chat first.

---

## Step 3: Test It Works (2 minutes)

1. Click **"Preview Survey"**
2. Go through to the chat question
3. **What you should see:**
   - Chat interface loads (Bob's icon and name appear)
   - Input box where you can type
   - Send button
   - **No "Next" button yet** (it's hidden until chat loads)
4. Type a test message and press Enter or click Send
5. Bob should respond to your message
6. **The "Next" button should appear** at the bottom (automatically, within ~5 seconds)
7. Click "Next" to continue your survey

**If something doesn't work:** See Troubleshooting below

---

## Troubleshooting

### Chat doesn't load (blank space)
- Check that you replaced `CHAT_APP_URL` with the correct URL
- Make sure URL has no trailing slash (/)
- Verify the chat app is running (ask your technical contact)

### Error: "Participant ID not set"
1. Go to Survey Flow
2. Make sure Embedded Data is at the TOP
3. Check that `participant_id` has a value set

### Error: "Condition not set"
1. Go to Survey Flow
2. Check that Randomizer exists with all 5 conditions (0, 1, 2, 3, 4)
3. Make sure Randomizer is BEFORE your survey questions

### "Next" button never appears
- **This is normal initially** - it's hidden until the chat loads
- Wait up to 5 seconds after the page loads
- The button appears automatically (you don't need to add it)
- If it still doesn't appear after 5 seconds, try refreshing and testing again
- Contact your technical support if it persists

### Same condition every time
- Randomizer might not be configured correctly
- Make sure it says "Evenly Present Elements"
- Try closing preview and opening a new preview window

---

## Launch Checklist

Before sending to participants:

- [ ] Tested preview and chat loads
- [ ] Tested sending messages - bot responds
- [ ] "Next" button appears automatically after chat loads (within 5 seconds)
- [ ] Can click "Next" to move to the next question
- [ ] Survey Flow has Embedded Data → Randomizer → Questions
- [ ] Chat app URL is correct in JavaScript (no trailing slash)
- [ ] Tested on both computer and phone (if participants use phones)

---

## Need Help?

**Contact your technical team** and provide:
- Screenshot of your Survey Flow
- Screenshot of the error (if any)
- The JavaScript code you pasted (first 10 lines)

They can verify your setup is correct.