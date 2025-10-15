# Project Organization Guide

This document explains how to organize framework files vs. study-specific files.

---

## 📁 **File Organization Strategy**

This project serves **two purposes**:
1. **Generic Research Framework** - Reusable for any chat-based experiment
2. **Specific Study** - Your poetry blame attribution research

**Solution:** Separate generic framework files from study-specific files

---

## 🗂️ **Directory Structure**

```
flask-chat-experiment/
│
├── app/                              # FRAMEWORK - Generic application code
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   │   ├── chat.html
│   │   └── test_interface.html
│   │   └── test_interface.html.example
│   └── static/
│       └── images/
│           ├── chip.png
│           └── brain.png
│
├── docs/                             # FRAMEWORK - Generic documentation
│   ├── EXPERIMENTAL_CONDITIONS_GUIDE.md
│   ├── QUALTRICS_SETUP.md
│   ├── DEPLOYMENT.md
│   ├── DOCKER_DEPLOYMENT.md
│   └── SECURITY.md
│
├── study_docs/                       # STUDY-SPECIFIC - Your poetry research
│   ├── README.md                     # Study-specific README
│   ├── STUDY_OVERVIEW.md             # Research design
│   ├── WORKFLOW_SPECIFICATION.md     # 5-step poetry workflow
│   └── CONDITION_REFERENCE.md        # Your 9 conditions
│
├── bot.py                            # FRAMEWORK - Core bot logic
├── wsgi.py                           # FRAMEWORK - WSGI entry
├── db_utils.py                       # FRAMEWORK - Data utilities
├── requirements.txt                  # FRAMEWORK - Dependencies
├── docker-compose.yml                # FRAMEWORK - Docker config
├── Dockerfile                        # FRAMEWORK - Docker build
│
├── experimental_conditions.json      # STUDY-SPECIFIC - Your actual conditions
├── experimental_conditions.example.json  # FRAMEWORK - Generic template
│
├── .env.example                      # FRAMEWORK - Template
├── .env                              # STUDY-SPECIFIC - Your secrets (gitignored)
│
├── README.md                         # FRAMEWORK - Generic framework docs
├── .gitignore                        # FRAMEWORK - Protects sensitive files
│
└── data/                             # STUDY-SPECIFIC - Your data (gitignored)
    └── chat_experiment.db
```

---

## 🔑 **Key Principles**

### **1. Framework Files (Shareable):**
**What:** Generic, reusable components

**Includes:**
- Application code (`app/`)
- Generic documentation (`docs/`)
- Example configurations (`.example` files)
- Core scripts (`bot.py`, `db_utils.py`)

**These can be:**
- ✅ Shared publicly on GitHub
- ✅ Reused for other studies
- ✅ Modified for different research questions

---

### **2. Study-Specific Files (Private):**
**What:** Your specific research implementation

**Includes:**
- Study documentation (`study_docs/`)
- Actual experimental conditions (`experimental_conditions.json`)
- Participant data (`data/`)
- Configuration with secrets (`.env`)

**These should be:**
- ❌ NOT shared publicly (until published)
- ❌ NOT in public repository
- ✅ Protected by `.gitignore`
- ✅ Backed up securely

---

## 📊 **What Goes in study_docs/?**

### **Required Study Documentation:**

**1. README.md**
- Quick summary of YOUR study
- Your specific conditions
- How to run YOUR study
- Links to other study docs

**2. STUDY_OVERVIEW.md**
- Research questions and hypotheses
- Experimental design
- Sample plan
- Expected outcomes
- IRB information

**3. WORKFLOW_SPECIFICATION.md**
- Detailed task description
- Step-by-step interaction flow
- Error behavior specification
- Implementation details

**4. CONDITION_REFERENCE.md**
- Quick lookup for your conditions
- Testing shortcuts
- Condition descriptions
- URL patterns

### **Optional Study Documentation:**

**5. IRB_DOCUMENTATION.md**
- IRB protocol number
- Consent form text
- Data handling procedures
- Risk assessment

**6. ANALYSIS_PLAN.md**
- Statistical analysis plan
- Dependent variables
- Planned comparisons
- Sample code for analysis

**7. PILOT_RESULTS.md**
- Pilot study findings
- Issues encountered
- Changes made

---

## 🔄 **Working with Both Versions**

### **Scenario 1: Developing Your Study**

**Use:**
- Main `README.md` → Ignore, use `study_docs/README.md` instead
- `docs/` → Reference when needed
- `study_docs/` → Your primary documentation
- `experimental_conditions.json` → Your actual conditions

### **Scenario 2: Releasing Framework**

**Share:**
- Main `README.md` (generic template version)
- `docs/` (generic documentation)
- `experimental_conditions.example.json`
- `.env.example`

**Don't Share:**
- `study_docs/` (your research)
- `experimental_conditions.json` (your conditions)
- `.env` (your secrets)
- `data/` (participant data)

### **Scenario 3: After Publication**

**Can Share:**
- Everything! Including `study_docs/`
- Update main README to reference your published paper
- Add citation information

---

## 🎯 **Recommended Workflow**

### **During Development (Now):**

1. **Keep two READMEs:**
   - `README.md` - Generic framework (for eventual public release)
   - `study_docs/README.md` - Your study (what you actually use day-to-day)

2. **Maintain study_docs/**
   - Document your specific design
   - Reference generic `docs/` when needed
   - Keep study-specific details here

3. **Use .gitignore**
   - Protect `study_docs/` from accidental commits
   - Protect `experimental_conditions.json`
   - Protect all data

### **When Sharing Framework:**

1. **Create public repository**
   - Include `README.md` (generic)
   - Include `docs/` (generic)
   - Include `experimental_conditions.example.json`
   - **Exclude** `study_docs/`
   - **Exclude** `experimental_conditions.json`

2. **Keep private repository**
   - Contains everything including `study_docs/`
   - Your actual working version
   - All participant data

### **After Publication:**

1. **Update public repository**
   - Can include `study_docs/` now
   - Add citation to published paper
   - Share as reproducibility package

---

## 📝 **Naming Conventions**

### **For Framework Files:**
```
README.md                          # Generic, public-facing
docs/DEPLOYMENT.md                 # Generic guide
experimental_conditions.example.json  # Generic template
.env.example                       # Template without secrets
```

### **For Study Files:**
```
study_docs/README.md               # Study-specific
study_docs/STUDY_OVERVIEW.md       # Study design
experimental_conditions.json       # Actual conditions (no .example)
.env                               # Actual secrets (gitignored)
```

**Clarity through naming!**

---

## 🔄 **Migration Checklist**

If organizing an existing project:

- [ ] Create `study_docs/` folder
- [ ] Move study-specific docs to `study_docs/`
- [ ] Create `study_docs/README.md` (study-specific)
- [ ] Keep main `README.md` generic
- [ ] Update `.gitignore` to protect `study_docs/`
- [ ] Create `.env.example` from your `.env` (remove secrets)
- [ ] Create `experimental_conditions.example.json` (generic version)
- [ ] Test that framework still works
- [ ] Document the organization in this file

---

## ✅ **Benefits of This Organization**

### **For You (Researcher):**
- ✅ Study documentation separate and organized
- ✅ Easy to reference framework docs
- ✅ Clear what's private vs. shareable
- ✅ Framework improvements don't clutter study docs

### **For Framework (Public Release):**
- ✅ Clean, focused documentation
- ✅ No research-specific details leaked
- ✅ Easy for others to understand
- ✅ Reusable for different studies

### **For Collaboration:**
- ✅ Team members know where to find study docs
- ✅ Clear separation of concerns
- ✅ Easy to onboard new researchers
- ✅ Framework can evolve independently

---

## 🎓 **Example: Running Multiple Studies**

If you later run a second study:

```
flask-chat-experiment/
├── app/                           # Shared framework
├── docs/                          # Shared generic docs
│
├── study_poetry/                  # Study 1 - Poetry blame
│   ├── README.md
│   ├── conditions.json
│   ├── study_docs/ (renamed from study_docs/)
│   └── data/
│
└── study_trust/                   # Study 2 - Trust study
    ├── README.md
    ├── conditions.json
    ├── study_docs/
    └── data/
```

Each study is self-contained!

---

## 🚀 **Next Steps**

To implement this organization:

1. **Create `study_docs/` folder**
2. **Move study-specific documentation** (CONDITION_REFERENCE.md)
3. **Create new study documentation** (the 3 files I just created)
4. **Update `.gitignore`** to protect study files
5. **Keep using the generic README.md** as the main README

This keeps your research organized while preserving the framework for future reuse!

---

**Does this organization make sense for your needs?**