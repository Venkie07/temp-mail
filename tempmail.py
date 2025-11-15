import requests
import time
import random
import string
import json
import os

BASE = "https://api.mail.gw"
DATA_FILE = "tempmail_data.json"

# ---------------------------
# Load / Save JSON Database
# ---------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"accounts": {}, "mails": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------------------------
# Utility Functions
# ---------------------------

def random_string(n=10):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

# ---------------------------
# Email Creation
# ---------------------------

def create_email():
    domains = requests.get(f"{BASE}/domains").json()["hydra:member"]
    domain = domains[0]["domain"]

    email = f"{random_string()}@{domain}"
    password = random_string(12)

    payload = {"address": email, "password": password}

    # Create account
    requests.post(f"{BASE}/accounts", json=payload)

    # Create token
    token = requests.post(f"{BASE}/token", json=payload).json()["token"]

    # Save to database
    data["accounts"][email] = {
        "password": password,
        "token": token
    }
    data["mails"][email] = []  # empty inbox storage
    save_data(data)

    return email, password, token

# ---------------------------
# API Mail Functions
# ---------------------------

def check_inbox(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/messages", headers=headers).json()
    return r["hydra:member"]

def read_mail(token, mail_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/messages/{mail_id}", headers=headers).json()
    return r

# ---------------------------
# MAIN PROGRAM
# ---------------------------

def choose_existing_email():
    emails = list(data["accounts"].keys())
    print("\nSaved Temp Emails:\n")

    for i, mail in enumerate(emails):
        print(f"{i} : {mail}")

    choice = int(input("\nEnter index to use that email: "))
    email = emails[choice]
    password = data["accounts"][email]["password"]
    token = data["accounts"][email]["token"]
    return email, password, token

def main():
    while True:   # 🔁 Always come back to menu
        print("1 -> Create New Temp Mail")
        print("2 -> Use Existing Temp Mail")
        print("3 -> Exit")

        try:
            option = int(input("\nChoose option: "))
        except ValueError:
            print("Invalid input!\n")
            continue

        if option == 3:
            print("Goodbye!")
            exit(0)
            break

        if option == 1:
            print("\nCreating new temp email...")
            email, password, token = create_email()
        elif option == 2:
            try:
                email, password, token = choose_existing_email()
            except Exception:
                print("Invalid index!\n")
                continue
        else:
            print("Invalid option!\n")
            continue

        print("\n------------------------------------")
        print("Your temp email:", email)
        print("------------------------------------\n")

        print("Checking mails forever... Press CTRL+C to stop.\n")

        # preload
        seen = set()
        try:
            old = check_inbox(token)
            for m in old:
                seen.add(m["id"])
        except:
            pass

        # --------------- MAIN LISTEN LOOP ---------------
        try:
            while True:
                inbox = check_inbox(token)

                for msg in inbox:
                    if msg["id"] not in seen:
                        seen.add(msg["id"])
                        full = read_mail(token, msg["id"])

                        print("\n📩 New Mail Received!")
                        print("From:", full["from"]["address"])
                        print("Subject:", full["subject"])
                        print("Body:\n", full["text"])

                        data["mails"][email].append(full)
                        save_data(data)

                time.sleep(5)

        except KeyboardInterrupt:
            print("\n\n🛑 Program stopped by user (Ctrl + C). Returning to menu...\n")
            continue

    print("1 -> Create New Temp Mail")
    print("2 -> Use Existing Temp Mail")
    option = int(input("\nChoose option: "))

    if option == 1:
        print("\nCreating new temp email...")
        email, password, token = create_email()
    else:
        email, password, token = choose_existing_email()

    print("\n------------------------------------")
    print("Your temp email:", email)
    print("------------------------------------\n")

    print("Checking mails forever... Press CTRL+C to stop.\n")

    # -------------------------------
    # PRELOAD OLD MAIL IDs (so they don't print again)
    # -------------------------------
    seen = set()
    try:
        old_inbox = check_inbox(token)
        for msg in old_inbox:
            seen.add(msg["id"])     # mark old messages as seen
    except:
        pass

    # -------------------------------
    # MAIN LOOP
    # -------------------------------
    try:
        while True:
            inbox = check_inbox(token)

            for msg in inbox:
                msg_id = msg["id"]
                if msg_id not in seen:
                    seen.add(msg_id)
                    full = read_mail(token, msg_id)

                    print("\n📩 New Mail Received!")
                    print("From:", full["from"]["address"])
                    print("Subject:", full["subject"])
                    print("Body:\n", full["text"])

                    # Save mail to JSON
                    data["mails"][email].append(full)
                    save_data(data)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n🛑 Program stopped by user (Ctrl + C). Exiting safely...\n")

    print("1 -> Create New Temp Mail")
    print("2 -> Use Existing Temp Mail")
    option = int(input("\nChoose option: "))

    if option == 1:
        print("\nCreating new temp email...")
        email, password, token = create_email()
    else:
        email, password, token = choose_existing_email()

    print("\n------------------------------------")
    print("Your temp email:", email)
    print("------------------------------------\n")

    print("Checking mails forever... Press CTRL+C to stop.\n")

    seen = set()  # track already printed IDs

    try:
        while True:
            inbox = check_inbox(token)

            for msg in inbox:
                msg_id = msg["id"]
                if msg_id not in seen:
                    seen.add(msg_id)
                    full = read_mail(token, msg_id)

                    print("\n📩 New Mail Received!")
                    print("From:", full["from"]["address"])
                    print("Subject:", full["subject"])
                    print("Body:\n", full["text"])

                    data["mails"][email].append(full)
                    save_data(data)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n🛑 Program stopped by user (Ctrl + C). Exiting safely...\n")


if __name__ == "__main__":
    main()

