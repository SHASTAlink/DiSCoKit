# Flask Experimental Chat Interface

A Flask-based web application for conducting experimental conversations with LLMs. Designed for psychology and HCI research studying how different AI presentations affect user perceptions and behavior.

**Key Features:**
- Secure, iframe-embeddable chat interface
- Multiple experimental condition support
- Session-based authentication
- Complete data export tools
- Production-ready deployment

---

## 🎯 **What Is This?**

This is a **research experiment framework** for studying human-AI interaction. It allows researchers to:

1. **Define experimental conditions** with different AI presentations (names, icons, personalities, behaviors)
2. **Embed in survey platforms** like Qualtrics for seamless integration
3. **Collect structured conversation data** with complete metadata
4. **Analyze interactions** across conditions to answer research questions

**Example Research Questions:**
- Does giving AI a human name affect user trust?
- How do visual representations (icons) influence perceptions of AI capability?
- Does self-referential language ("I" vs "this AI") impact user engagement?
- How do users respond when AI makes mistakes?

---

## 🚀 **Quick Start**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment (see Configuration section)
cp experimental_conditions.example.json experimental_conditions.json
# Edit experimental_conditions.json for your study

# 3. Create .env file with Azure OpenAI credentials

# 4. Run the app
python -m flask run

# 5. Test at http://localhost:5000/
```

---

## 📊 **How It Works**

### **Researcher Workflow:**

1. **Design Study** - Define experimental conditions in JSON
2. **Deploy** - Host on university server or Docker
3. **Integrate** - Embed in Qualtrics survey
4. **Collect** - Participants interact through chat interface
5. **Export** - Download conversation data for analysis
6. **Analyze** - Compare behavior across conditions

### **Participant Experience:**

1. Opens Qualtrics survey
2. Randomly assigned to condition
3. Interacts with chat interface
4. Conversation saved to database
5. Continues with survey

---

## 🔬 **Defining Your Experimental Conditions**

Conditions are defined in `experimental_conditions.json`. Each condition can vary:

- **Bot Identity:** Name (human vs robotic vs none), Icon (emoji vs image vs none)
- **Visual Style:** Colors, layout, header visibility
- **AI Behavior:** System prompts, temperature, response style
- **Model Parameters:** Temperature, max tokens, etc.

### **System Prompt Organization**

The `system_prompt` field is an object where you can organize your prompt into sections:

```json
"system_prompt": {
    "role": "You are a helpful assistant.",
    "behavior": "Be concise and friendly."
}
```

**Key Point:** The section names (`role`, `behavior`, etc.) are **completely arbitrary** - you can use ANY names you want! They're just for organizing your prompt into readable sections. The application concatenates all values together:

```python
# Behind the scenes:
final_prompt = "\n".join(system_prompt.values())
# Result: "You are a helpful assistant.\nBe concise and friendly."
```

You could just as easily use:
```json
"system_prompt": {
    "part_1": "You are a helpful assistant.",
    "part_2": "Be concise and friendly."
}
```

Or even a single section:
```json
"system_prompt": {
    "instructions": "You are a helpful assistant. Be concise and friendly."
}
```

**Choose section names that help YOU organize and maintain your conditions!**

**See detailed guide:** `docs/EXPERIMENTAL_CONDITIONS_GUIDE.md`

**Example template:** `experimental_conditions.example.json`

### **Example Condition:**

```json
{
    "id": "friendly_assistant",
    "name": "Condition A - Friendly Tone",
    "description": "Tests effect of warm, casual language",
    "enabled": true,
    "bot_name": "Alex",
    "bot_icon": "👋",
    "bot_styles": {
        "primary_color": "#4A90E2",
        "background_color": "#F5F5F5",
        "text_color": "#333333",
        "show_header": true
    },
    "model_overrides": {
        "temperature": 0.9
    },
    "system_prompt": {
        "role": "You are a friendly AI assistant named Alex.",
        "behavior": "Use warm, conversational language. Be enthusiastic and supportive."
    }
}
```

---

## 🔒 **Security Features**

This application implements enterprise-grade security:

### **1. Session Token Authentication**
- Prevents unauthorized API access
- Each participant gets unique cryptographic token
- APIs only accessible through chat interface

### **2. Iframe Embedding Control**
- Restricts which websites can embed the chat
- Configured via `ALLOWED_FRAME_ANCESTORS` environment variable
- Prevents cost attacks and data pollution

### **3. Rate Limiting**
- 30 messages per minute per IP
- 500 messages per day per IP
- Prevents spam and abuse

### **4. Input Validation**
- Validates participant IDs (alphanumeric only)
- Validates condition indices (within range)
- Limits message length (2000 characters)

### **5. Secure Data Export**
- No web-accessible data export
- Requires SSH access to server
- Export via command-line tools only

**For complete security documentation:** See `docs/SECURITY.md`

---

## 📦 **Features**

- **Iframe-Embeddable**: Works in Qualtrics and other survey platforms
- **No Cookie Dependencies**: Functions perfectly in cross-origin iframes
- **Experimental Design**: Support unlimited conditions with factorial designs
- **Server-Side Persistence**: All conversations stored with metadata
- **Participant Tracking**: Links conversations to participant IDs and conditions
- **Customizable UI**: Per-condition styling (colors, icons, names)
- **RESTful API**: Clean authenticated API for chat operations
- **Export Tools**: Multiple formats (JSON, CSV) for analysis
- **Production Ready**: Factory pattern, Docker support, systemd service
- **Secure by Default**: Authentication, rate limiting, input validation

---

## 🎓 **Use Cases**

### **Psychology Research:**
- Trust in AI systems
- Anthropomorphism effects
- Error attribution and blame
- Emotional responses to AI

### **HCI Research:**
- Interface design testing
- Conversation flow analysis
- User experience studies
- Accessibility research

### **AI Research:**
- Prompt engineering experiments
- Model behavior analysis
- Human-AI collaboration patterns
- Response quality evaluation

---

## 📁 **Project Structure**

```
.
├── app/
│   ├── __init__.py                    # Application factory
│   ├── models.py                      # Database models (with session tokens)
│   ├── routes.py                      # Authenticated routes
│   ├── templates/
│   │   ├── chat.html                  # Chat interface
│   │   └── test_interface.html        # Test page
│   │   └── test_interface.html.example # Test page template
│   └── static/
│       └── images/                    # Bot icons
├── bot.py                             # Bot logic and config loading
├── experimental_conditions.json       # Your study conditions
├── experimental_conditions.example.json  # Generic template
├── wsgi.py                            # WSGI entry point
├── docker-compose.yml                 # Docker configuration
├── requirements.txt                   # Python dependencies
├── db_utils.py                        # Data management CLI
├── .env.example                       # Environment template
├── docs/
│   ├── EXPERIMENTAL_CONDITIONS_GUIDE.md  # How to design conditions
│   ├── QUALTRICS_SETUP.md             # Survey integration guide
│   ├── DEPLOYMENT.md                  # Production deployment
│   ├── DOCKER_DEPLOYMENT.md           # Container deployment
│   ├── SECURITY.md                    # Security features
│   └── CONDITION_REFERENCE.md         # Quick reference
├── DEPLOYMENT_CHECKLIST.md            # Pre-launch checklist
└── data/
    └── chat_experiment.db             # SQLite database
```

---

## 🛠️ **Customization Guide**

To adapt this for your research:

1. **Design Your Conditions** - Edit `experimental_conditions.json`
   - Define your independent variables
   - Create condition configurations
   - See `docs/EXPERIMENTAL_CONDITIONS_GUIDE.md`

2. **Customize Templates** (Optional) - Edit `app/templates/chat.html`
   - Modify chat interface appearance
   - Add custom elements
   - Adjust styling

3. **Configure Environment** - Create `.env` file
   - Set Azure OpenAI credentials
   - Configure security settings
   - See `.env.example`

4. **Deploy** - Follow deployment guides
   - Local: `python -m flask run`
   - Server: See `docs/DEPLOYMENT.md`
   - Docker: See `docs/DOCKER_DEPLOYMENT.md`

5. **Integrate** - Embed in Qualtrics
   - Follow `docs/QUALTRICS_SETUP.md`
   - Test all conditions
   - Launch study

---

## 📖 **Documentation**

- **Getting Started:** This README
- **Condition Design:** `docs/EXPERIMENTAL_CONDITIONS_GUIDE.md`
- **Qualtrics Integration:** `docs/QUALTRICS_SETUP.md`
- **Deployment:** `docs/DEPLOYMENT.md`, `docs/DOCKER_DEPLOYMENT.md`
- **Security:** `docs/SECURITY.md`
- **Pre-Launch:** `DEPLOYMENT_CHECKLIST.md`

---

## 🤝 **Contributing**

This is a research tool template. Contributions welcome for:
- Additional example conditions
- Improved documentation
- Bug fixes
- Feature enhancements

---

## 📄 **License**

[Your License Here - Consider MIT or GPL for open source]

---

## 🙏 **Citation**

If you use this framework in your research, please cite:

```
[Your citation format here]
```

---

## 📧 **Contact**

For questions or support:
- **Issues:** [GitHub issues link]
- **Email:** [Your email]
- **Documentation:** See docs/ folder

---

## ⚠️ **IRB Considerations**

When using this for human subjects research:

- Review your institution's IRB requirements
- Ensure informed consent includes AI interaction
- Document data handling procedures
- Consider participant privacy protections
- Review security features with IRB
- Establish data retention policies

See `docs/SECURITY.md` for security measures you can reference in IRB applications.

---

**Ready to conduct rigorous HCI research with AI systems!** 🔬