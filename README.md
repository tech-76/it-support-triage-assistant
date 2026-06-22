# IT Support Triage Assistant

A service-desk intake tool that turns IT support requests into structured troubleshooting reports.

This project demonstrates practical IT support workflow automation using Python, Gradio, and Hugging Face Spaces. The assistant helps categorize support requests, assign priority, detect escalation needs, generate troubleshooting steps, and produce technician-ready notes and downloadable reports.

## Live demo

```text
https://huggingface.co/spaces/1kvsh/it-support-triage-assistant
```

## Project status

Working prototype: **v2.1**

The current version is designed for portfolio, recruiter review, service-desk workflow demonstration, and early small-business support intake testing.

## Key features

- Single-ticket IT issue analysis
- Auto-detection for support categories
- Manual category override
- Priority assignment: Low, Medium, High, or Critical
- Escalation detection with reasoning
- User impact summary
- Likely cause summary
- Structured troubleshooting steps
- Technician notes
- User-friendly response
- Recommended next action
- Confidence score
- Downloadable Markdown support report
- Bulk CSV ticket analysis
- Sample ticket file for testing
- Privacy warning for sensitive information

## Supported categories

The assistant supports the following ticket categories:

- Windows
- Microsoft 365
- Networking
- DNS
- Email
- Hardware
- Security
- General IT

## Example use cases

- Microsoft 365 login issue
- Outlook password popup
- Business email outage
- Suspicious email or phishing report
- Website DNS issue
- Wi-Fi disconnecting
- Slow Windows laptop
- Hardware or peripheral issue
- General IT support intake

## Tech stack

- Python
- Gradio
- Hugging Face Spaces
- CSV processing
- Markdown report generation
- Rule-based triage logic

## Repository structure

```text
it-support-triage-assistant/
├── README.md
├── app.py
├── requirements.txt
├── sample_tickets.csv
├── service-overview.md
├── docs/
│   ├── project-overview.md
│   ├── testing-guide.md
│   ├── roadmap.md
│   └── case-study.md
└── screenshots/
    └── add-screenshots-here.md
```

## How to run locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/it-support-triage-assistant.git
cd it-support-triage-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Open the local Gradio URL shown in the terminal.

## How to deploy on Hugging Face Spaces

1. Create a new Hugging Face Space.
2. Choose **Gradio** as the SDK.
3. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `sample_tickets.csv`
   - `service-overview.md`
4. Wait for the Space to rebuild.
5. Test the Single Ticket tab first.
6. Test the Bulk CSV tab using `sample_tickets.csv`.

## Hugging Face Space metadata

If using this README directly inside Hugging Face Spaces, add this metadata block to the very top of the README:

```yaml
---
title: IT Support Triage Assistant
emoji: 🛠️
colorFrom: blue
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
short_description: IT ticket triage reports.
---
```

The `short_description` must stay under the Hugging Face character limit.

## Privacy and safety reminder

Do not enter passwords, MFA codes, recovery codes, private keys, payment information, customer personal information, or confidential business data.

This assistant is a triage and documentation tool. It does not replace an authorized technician, administrator, cybersecurity professional, legal advisor, or business approval process.

## Limitations

- This version uses structured rule-based logic, not a live AI model API.
- It does not connect to a ticketing system yet.
- It does not send email notifications yet.
- It does not store ticket history.
- It does not validate real DNS, Microsoft 365, or endpoint data.
- Security-related output should always be reviewed by a qualified technician.

## Future improvements

Planned improvements include:

- PDF report downloads
- Ticket ID history
- Cleaner UI branding
- Screenshot upload support
- Email notification option
- GitHub Actions deployment sync
- Admin dashboard
- Client-specific branding
- Optional LLM-based reasoning layer
- Integration with ticketing tools

## Portfolio summary

**IT Support Triage Assistant** is a service-desk workflow project that shows practical IT support documentation, triage logic, escalation awareness, and deployment of a working Python/Gradio application on Hugging Face Spaces.

## Suggested GitHub topics

```text
python
gradio
huggingface-spaces
it-support
help-desk
service-desk
troubleshooting
microsoft-365
networking
dns
ticketing
technical-support
```
