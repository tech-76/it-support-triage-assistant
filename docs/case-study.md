# Case Study: IT Support Triage Assistant

## Project title

IT Support Triage Assistant

## Project type

Service desk workflow automation project

## Overview

The IT Support Triage Assistant is a working support intake tool built with Python, Gradio, and Hugging Face Spaces. It helps organize IT support requests by categorizing issues, assigning priority, identifying escalation needs, generating troubleshooting steps, and creating technician-ready reports.

## Problem

Support requests are often submitted with incomplete or unclear details. This creates extra back-and-forth between the user and technician, slows down troubleshooting, and makes documentation inconsistent.

Examples of unclear requests include:

- “My email is not working.”
- “The internet keeps disconnecting.”
- “My laptop is slow.”
- “I clicked a suspicious link.”

Each of these could involve different systems, risks, and escalation paths.

## Goal

The goal was to build a working assistant that turns unclear IT support messages into structured reports that a technician can review and act on.

The project needed to show:

- Practical IT support thinking
- Ticket categorization
- Priority assessment
- Escalation awareness
- Troubleshooting documentation
- User-friendly communication
- Working deployment on Hugging Face Spaces

## Solution

The assistant was built as a Gradio web application. The user enters issue details such as summary, category, affected users, device type, operating system, error message, and recent changes.

The app then generates a structured support report with:

- Ticket summary
- Category
- Priority
- Escalation recommendation
- User impact
- Likely causes
- Troubleshooting steps
- Technician notes
- User-friendly response
- Recommended next action
- Confidence score
- Downloadable report

## Categories supported

- Windows
- Microsoft 365
- Networking
- DNS
- Email
- Hardware
- Security
- General IT

## Example scenario

Input:

```text
Multiple users are not receiving business email after a domain change. Senders are getting bounce messages.
```

Expected triage result:

- Category: Email/DNS
- Priority: Critical
- Escalation required: Yes
- User impact: Multiple users affected; possible business email outage
- Recommended next action: Review MX, SPF, DKIM, DMARC, DNS changes, bounce messages, and mail routing configuration

## Tools and technologies

- Python
- Gradio
- Hugging Face Spaces
- CSV processing
- Markdown report generation
- Rule-based support logic

## Outcome

The result is a working v2.1 prototype that can be used as:

- A portfolio project
- A recruiter demo
- A service-desk workflow example
- A starting point for a small-business support intake service

## Skills demonstrated

- Technical support workflow design
- Help desk ticket analysis
- Microsoft 365 support awareness
- DNS and email troubleshooting awareness
- Networking support awareness
- Security escalation awareness
- Python application development
- Gradio app deployment
- Technical documentation
- User communication

## Privacy approach

The app includes warnings not to enter passwords, MFA codes, recovery codes, private keys, payment information, customer personal information, or confidential business data.

## Limitations

The app is a triage and documentation tool. It does not replace an authorized technician, administrator, cybersecurity professional, or business approval process.

The current version does not connect to live Microsoft 365, DNS, endpoint, or ticketing systems.

## Future improvements

Planned improvements include:

- PDF reports
- Ticket history
- Admin dashboard
- Email notifications
- Private client version
- Ticketing integrations
- Optional LLM-assisted reasoning
- Client-specific branding
