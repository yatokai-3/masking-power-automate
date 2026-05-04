# 🔐 Power Automate Masking API (Presidio + spaCy)

This repository contains a **Python-based PII masking API** built using **Microsoft Presidio** and **spaCy**, deployed on **Render**, and consumed by **Power Automate** via an **HTTP POST** action.

The API is used to **mask sensitive information from email content** (or any text) before it is stored, logged, or forwarded inside Power Automate flows.

---

## ✅ Why this exists

- Power Automate does **not** provide a native masking/anonymization action
- Emails often contain **PII / confidential data**
- This API acts as a **secure masking layer** before downstream processing

---

## 🧠 What gets detected & masked

### Built-in Presidio detections
- Email addresses
- Phone numbers
- Person names
- Credit card numbers
- IP addresses
- URLs
- Bank numbers (region-specific)

### Custom detections added in this project
- **Account numbers** (10–18 digits)
- **PIN / OTP codes** (4–6 digits)
- **Passwords** (`password is / = / : value`)

All detected values are replaced with `*` characters **matching the original length**.
