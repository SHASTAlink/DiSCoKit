# Security Documentation

This document explains the security features implemented in the chat application.

---

## 🎯 **Security Model Overview**

This application implements multiple layers of security to protect:
1. **Participant data privacy** - Conversations are protected from unauthorized access
2. **Research data integrity** - Prevents data corruption and pollution
3. **Cost control** - Prevents abuse of Azure OpenAI resources
4. **Authorized use only** - Restricts both API access and iframe embedding

---

## 🔐 **Security Features**

### **1. Session Token Authentication** (Issue #1: API Access Control)

**Problem Solved:** Prevents unauthorized access to API endpoints

#### How It Works:

1. **Token Generation:**
   - When participant loads `/gui`, a cryptographically secure random token is generated
   - Token stored in database with participant record
   - Token passed to chat interface via Flask template

2. **Token Validation:**
   - Every API request must include valid session token
   - Server verifies token matches participant's stored token
   - Invalid or missing tokens rejected with 403 Forbidden

3. **What's Protected:**
   - `/api/send_message` - Can't send messages without valid token
   - `/api/get_history` - Can't read conversations without valid token

#### Security Benefits:

✅ **Prevents impersonation** - Can't send messages as other participants  
✅ **Prevents data theft** - Can't read others' conversations  
✅ **Prevents data pollution** - Can't create fake participants at scale  
✅ **Stateless design** - Token in database, not server memory  
✅ **Works in iframes** - No cookies or sessions required  

#### Example:

**Legitimate Use (chat.html):**
```javascript
// chat.html has the token
fetch('/api/send_message', {
    body: JSON.stringify({
        participant_id: 'P001',
        session_token: 'abc123...xyz',  // Valid token
        message: 'Hello'
    })
})
// Result: ✅ Success
```

**Unauthorized Use (curl/script):**
```bash
curl -X POST https://chat.university.edu/api/send_message \
  -d '{"participant_id":"P001","message":"fake"}'

# Result: ❌ 400 Bad Request: "session_token is required"
```

---

### **2. Frame Embedding Control** (Issue #2: Iframe Access Control)

**Problem Solved:** Prevents unauthorized websites from embedding the chat interface

#### How It Works:

1. **Configuration:**
   - Set `ALLOWED_FRAME_ANCESTORS` environment variable
   - Comma-separated list of allowed domains
   - Leave blank during development (allows all)

2. **Enforcement:**
   - Server sets `Content-Security-Policy: frame-ancestors` header
   - Browser enforces CSP and blocks unauthorized embedding
   - Only specified domains can embed the iframe

3. **What's Protected:**
   - `/gui` endpoint - Controls who can embed the chat interface

#### Configuration Examples:

**Development Mode (Allow All):**
```env
# .env - Leave blank or unset
# ALLOWED_FRAME_ANCESTORS=
```

**Production Mode (Qualtrics Only):**
```env
# .env - Restrict to Qualtrics
ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com
```

**Multiple Domains:**
```env
# .env - Allow multiple domains
ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com,yourschool.az1.qualtrics.com
```

#### Security Benefits:

✅ **Prevents unauthorized embedding** - Can't iframe chat on random websites  
✅ **Prevents cost attacks** - Limits who can create participants  
✅ **Protects reputation** - Chat doesn't appear on inappropriate sites  
✅ **Configurable** - Easy to update without code changes  

#### Example:

**Authorized Embedding (Qualtrics):**
```html
<!-- On https://yourschool.qualtrics.com -->
<iframe src="https://chat.university.edu/gui?participant_id=P001&condition=0"></iframe>
<!-- Result: ✅ Loads successfully -->
```

**Unauthorized Embedding (Evil Site):**
```html
<!-- On https://evil-site.com -->
<iframe src="https://chat.university.edu/gui?participant_id=SPAM&condition=0"></iframe>
<!-- Result: ❌ Browser blocks with CSP error -->
```

---

### **3. Rate Limiting**

**Prevents:** Spam and abuse of API endpoints

#### Limits Applied:

**Default (all endpoints):**
- 200 requests per day per IP
- 50 requests per hour per IP

**Message sending (`/api/send_message`):**
- 30 messages per minute per IP
- 500 messages per day per IP

#### What Happens When Limit Exceeded:

```json
{
  "error": "30 per 1 minute"
}
```

HTTP Status: `429 Too Many Requests`

Counter resets after the time period.

---

### **4. Input Validation**

**Prevents:** Malicious input and data quality issues

#### Participant ID Validation:

**Allowed:** Letters, numbers, hyphens, underscores (1-255 characters)
```
✅ P001
✅ PROLIFIC_abc123
✅ MTurk-Worker-XYZ
```

**Rejected:**
```
❌ '; DROP TABLE--    (SQL injection attempt)
❌ ../../etc/passwd   (path traversal)
❌ user@email.com     (special characters)
❌ 😀💀🔥              (unicode/emoji)
```

#### Condition Index Validation:

**Allowed:** Integers 0-8
```
✅ 0, 1, 2, 3, 4, 5, 6, 7, 8
```

**Rejected:**
```
❌ -1, 99, 999        (out of range)
❌ "abc"              (not an integer)
```

#### Message Length Validation:

**Allowed:** Up to 2000 characters
```
✅ Normal conversation messages
```

**Rejected:**
```
❌ 10,000 character spam messages
❌ Empty messages
```

---

### **5. Environment Variable Validation**

**Prevents:** Configuration errors in production

#### Validation on Startup:

Required variables:
- `MODEL_ENDPOINT`
- `MODEL_DEPLOYMENT`
- `MODEL_API_VERSION`
- `MODEL_SUBSCRIPTION_KEY`
- `MODEL_TEMPERATURE`
- `MODEL_MAX_COMPLETION_TOKENS`
- `MODEL_MAX_RETRIES`
- `MODEL_RETRY_DELAY`

**If any are missing:**
```
RuntimeError: Missing required environment variables: MODEL_ENDPOINT, MODEL_API_KEY
Please check your .env file and ensure all required variables are set.
```

Application **refuses to start** until all required variables are set.

---

## 🛡️ **Defense in Depth Strategy**

All security features work together:

### **Layer 1: Iframe Embedding Control**
Prevents unauthorized sites from embedding your chat

### **Layer 2: Session Token Authentication**
Prevents unauthorized API access even if embedded

### **Layer 3: Rate Limiting**
Limits damage from any successful attack

### **Layer 4: Input Validation**
Ensures data quality and prevents malicious input

### **Layer 5: Environment Validation**
Prevents misconfigurations in production

---

## 📊 **Attack Scenario Analysis**

### **Scenario 1: Direct API Abuse**

**Attack:** Attacker tries to spam `/api/send_message` with curl

**Blocked by:**
1. ❌ No session token → 400 Bad Request
2. ❌ Even if they guess a token, rate limit kicks in → 429 after 30 requests
3. ❌ Message length capped at 2000 chars → Limited cost per message

**Result:** Attack fails, minimal damage

---

### **Scenario 2: Unauthorized Iframe Embedding**

**Attack:** evil-site.com tries to embed your chat

**Blocked by:**
1. ❌ CSP frame-ancestors blocks iframe → Browser refuses to load
2. ❌ Even if they bypass CSP, can't call API without session tokens
3. ❌ Even if they get tokens, rate limited per IP

**Result:** Attack fails at multiple levels

---

### **Scenario 3: Participant Impersonation**

**Attack:** Attacker tries to send messages as participant P001

**Blocked by:**
1. ❌ No session token → 400 Bad Request
2. ❌ Wrong session token → 403 Forbidden
3. ❌ Can't guess token (256-bit random value)

**Result:** Attack fails, P001's data protected

---

### **Scenario 4: Conversation Snooping**

**Attack:** Attacker tries to read participant P001's conversation

**Blocked by:**
1. ❌ No session token → 400 Bad Request
2. ❌ Can't guess P001's specific token
3. ❌ Each participant has unique token

**Result:** Attack fails, privacy maintained

---

## 🔧 **Configuration Guide**

### **Development Environment:**

```env
# .env for development
FLASK_SECRET_KEY=dev-secret-key
# ALLOWED_FRAME_ANCESTORS=     ← Leave blank
```

**Allows:**
- Testing from localhost
- Embedding from any domain
- Flexible development

### **Production Environment:**

```env
# .env for production
FLASK_SECRET_KEY=<generate-with: python -c 'import secrets; print(secrets.token_hex(32))'>
ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com
```

**Enforces:**
- Strong secret key
- Restricted iframe embedding
- All security features active

---

## 🔍 **Monitoring Security**

### **Check for Suspicious Activity:**

```bash
# View recent participants
python db_utils.py list

# Look for:
# - Unusual participant IDs (random characters, SQL attempts)
# - Participants with many failed messages (no assistant responses)
# - Burst of participants created at same time
```

### **Check Logs for Attacks:**

```bash
# View error logs
tail -f logs/error.log

# Look for:
# - "Invalid session token" (impersonation attempts)
# - "session_token is required" (direct API calls)
# - "429 Too Many Requests" (rate limit violations)
# - "Invalid participant_id format" (malicious input)
```

### **Database Integrity Checks:**

```bash
# Get statistics
python db_utils.py stats

# Check for:
# - Abnormally high participant counts
# - Participants with zero messages (abandoned sessions)
# - Unusual condition distributions
```

---

## 🚨 **Incident Response**

### **If You Detect Unauthorized Access:**

1. **Immediately set frame embedding restrictions:**
   ```bash
   # In .env:
   ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com
   
   # Restart:
   sudo systemctl restart chat-experiment
   ```

2. **Review logs for source:**
   ```bash
   tail -100 logs/access.log | grep "api/send_message"
   ```

3. **Identify compromised participants:**
   ```bash
   python db_utils.py list
   # Look for suspicious IDs or activity patterns
   ```

4. **Clean compromised data:**
   ```bash
   python db_utils.py delete SUSPICIOUS_ID --confirm
   ```

5. **Document the incident** for IRB if required

---

## ✅ **Security Best Practices**

### **Before Launch:**
- [ ] Set `ALLOWED_FRAME_ANCESTORS` to Qualtrics domain
- [ ] Change `FLASK_SECRET_KEY` to random value
- [ ] Test all security features work
- [ ] Review logs for any test attack attempts
- [ ] Document security measures for IRB

### **During Study:**
- [ ] Monitor `db_utils.py stats` weekly
- [ ] Check logs for 403/429 errors
- [ ] Verify participant IDs look legitimate
- [ ] Watch for unusual activity patterns

### **After Study:**
- [ ] Export data via `db_utils.py`
- [ ] Archive database securely
- [ ] Review any security incidents
- [ ] Document lessons learned

---

## 🔗 **Related Documentation**

- **Session Token Implementation:** See "Session Token Migration Guide" artifact
- **Frame Embedding Control:** See "Frame Embedding Control Guide" artifact
- **Deployment:** See `DEPLOYMENT.md` for production setup
- **Environment Variables:** See `.env Template` for configuration

---

## 📞 **Security Questions?**

For security concerns or questions:
1. Review this document
2. Check application logs
3. Test security features in development
4. Consult with university IT security team if needed