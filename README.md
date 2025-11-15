Here you go Venkie 🔥💙
A **perfect, attractive, GitHub-ready README.md** for your temp-mail Python project.

You can paste this directly into your repository.
It is clean, structured, professional, and fully detailed.

---

# 📧 TempMail-Python — Full Automatic Temporary Email Generator & Mail Receiver

A powerful Python script to **create temporary email addresses**, **receive mails in real-time**, and **store mails locally** using the **Mail.GW API**.
Supports:

✔ Create new temp email
✔ Use previously created temp emails
✔ Auto-listening for incoming mails
✔ JSON-based local storage
✔ Infinite mail fetching
✔ Smooth Ctrl+C interrupt → return to menu
✔ Fast & reliable inbox checking

---

# 🚀 Features

### 🔹 1. Auto-Generate Temp Email

The script uses **Mail.GW API (`https://api.mail.gw`)** to create a random temporary email with a secure password.

### 🔹 2. Automatic Access Token Generation

Every created email gets a **JWT token** from Mail.GW, which is stored and reused.

### 🔹 3. Real-Time Mail Receiving

Your script automatically polls the inbox every 5 seconds and prints new mails immediately.

### 🔹 4. JSON Database

All created emails + received messages are saved in:

```
tempmail_data.json
```

Stores:

* Email address
* Password
* API token
* All received mails (body, subject, sender, etc.)

### 🔹 5. Use Old Emails

You can reuse previously created temp emails anytime.

### 🔹 6. Clean Loop With Smooth Exit

Pressing **CTRL+C** stops inbox listening and returns back to the main menu.

---

# 🧠 How the System Works

## 1️⃣ **API Used — Mail.GW**

Your script uses the official temporary mail service API:

```
https://api.mail.gw
```

This API allows:

| API Function          | Endpoint         |
| --------------------- | ---------------- |
| Get domains           | `/domains`       |
| Create email account  | `/accounts`      |
| Generate access token | `/token`         |
| Fetch inbox messages  | `/messages`      |
| Read specific message | `/messages/{id}` |

---

# 2️⃣ How **Email Generation** Works

### Step 1 — Fetch Available Domains

```python
domains = requests.get(BASE + "/domains").json()
domain = domains["hydra:member"][0]["domain"]
```

Example domains:

* `@oakon.com`
* `@sharklasers.com` (depends on API)

---

### Step 2 — Create Random Email

```python
email = f"{random_string()}@{domain}"
```

### Step 3 — Register the temporary email

```python
requests.post(BASE + "/accounts", json={"address": email, "password": password})
```

---

### Step 4 — Generate Token

```python
token = requests.post(BASE + "/token", json=payload).json()["token"]
```

This token is used to **access the inbox**.

---

# 3️⃣ How **Mail Fetching** Works

### Step 1 — Check inbox

```python
headers = {"Authorization": f"Bearer {token}"}
inbox = requests.get(BASE + "/messages", headers=headers).json()
```

### Step 2 — Detect NEW messages

The script tracks each message by ID using a `seen` set:

```python
if msg_id not in seen:
    seen.add(msg_id)
    # Print it
```

### Step 3 — Fetch full message

```python
full = requests.get(BASE + f"/messages/{msg_id}", headers=headers).json()
```

### Step 4 — Display message

```
📩 New Mail Received!
From: sender@example.com
Subject: ...
Body: ...
```

### Step 5 — Save mail to JSON

```python
data["mails"][email].append(full)
save_data(data)
```

---

# 4️⃣ JSON Database Structure

Your `tempmail_data.json` looks like this:

```json
{
  "accounts": {
    "abcd123@oakon.com": {
      "password": "randompass123",
      "token": "JWT_TOKEN_HERE"
    }
  },
  "mails": {
    "abcd123@oakon.com": [
      {
        "id": "message-id",
        "from": {"address": "someone@mail.com"},
        "subject": "Hello",
        "text": "Mail body..."
      }
    ]
  }
}
```

This makes old accounts reusable anytime.

---

# 🖥 How To Use

### ▶ Run the program:

```
python tempmail.py
```

### Menu appears:

```
1 -> Create New Temp Mail
2 -> Use Existing Temp Mail
3 -> Exit
```

---

# 📬 Example Output

```
------------------------------------
Your temp email: xksu28v@oakon.com
------------------------------------

Checking mails forever... Press CTRL+C to stop.


📩 New Mail Received!
From: no-reply@example.com
Subject: Verify Email
Body:
Click here to verify your email...
```

Press **CTRL + C** to return to the menu.

---

# 🛠 Requirements

* Python 3.8+
* Libraries:

  ```
  requests
  json
  time
  random
  string
  ```

Install required packages:

```
pip install requests
```

---

# 📎 Why This Script Is Amazing

✔ 100% automatic
✔ No browser needed
✔ Great for testing OTP systems
✔ Permanent JSON record of every received mail
✔ Works forever without expiration

---

# 🏁 Conclusion

This Python tool is a **complete temp-mail automation system** using the Mail.GW API.
It supports:

* Creating unlimited temp emails
* Reading mails live
* Storing all data locally
* Reusing past emails

Perfect for developers, testers, automation engineers, and students.

---

If you want, I can also make:

✅ A **GUI version (Tkinter / PyQt)**
✅ A **Command Line Tool (pip installable)**
✅ A **FastAPI Web Dashboard**
✅ A **GitHub logo + banner for the repo**

Just tell me, Venkie 💙🔥
