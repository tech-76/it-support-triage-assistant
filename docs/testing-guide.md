# Testing Guide

## Purpose

This guide explains how to test the IT Support Triage Assistant after uploading it to Hugging Face Spaces or running it locally.

## Files required

Make sure these files are present:

- `app.py`
- `requirements.txt`
- `README.md`
- `sample_tickets.csv`
- `service-overview.md`

## Local test

Run:

```bash
pip install -r requirements.txt
python app.py
```

Open the local Gradio URL shown in the terminal.

## Hugging Face Spaces test

After uploading or replacing files in the Space:

1. Wait for the Space to rebuild.
2. Open the app.
3. Confirm the app title appears as **IT Support Triage Assistant**.
4. Test the Single Ticket tab.
5. Test a downloadable report.
6. Test the Bulk CSV tab using `sample_tickets.csv`.

## Single ticket test cases

### Test 1: Microsoft 365 login issue

Input:

```text
User cannot sign in to Microsoft 365 after a password reset. Error says MFA required.
```

Expected result:

- Category: Microsoft 365
- Priority: High
- Escalation: likely Yes
- Output should mention sign-in, MFA, account status, license, and admin review.

### Test 2: Business email outage

Input:

```text
Multiple users are not receiving business email after a domain change. Senders are getting bounce messages.
```

Expected result:

- Category: Email, DNS, or Auto-detected related category
- Priority: Critical
- Escalation: Yes
- Output should mention MX, SPF, DKIM, DMARC, mail routing, bounce messages, and business impact.

### Test 3: Suspicious email / phishing

Input:

```text
User clicked a suspicious email link and entered their password.
```

Expected result:

- Category: Security
- Priority: Critical
- Escalation: Yes
- Output should mention account compromise, MFA/password reset, sign-in review, evidence preservation, and safe communication.

### Test 4: DNS issue

Input:

```text
Company website is not loading after changing nameservers. Browser shows DNS_PROBE_FINISHED_NXDOMAIN.
```

Expected result:

- Category: DNS
- Priority: High
- Escalation: Yes if business-critical
- Output should mention DNS records, nameservers, TTL, propagation, and approval before changes.

### Test 5: Wi-Fi issue

Input:

```text
Wi-Fi keeps disconnecting from one laptop every few minutes.
```

Expected result:

- Category: Networking
- Priority: Medium
- Escalation: usually No unless multiple users are affected
- Output should mention signal strength, DHCP, network adapter, router/access point, and testing other devices.

### Test 6: Slow Windows laptop

Input:

```text
Computer is very slow after startup and apps take a long time to open.
```

Expected result:

- Category: Windows
- Priority: Medium
- Escalation: usually No
- Output should mention startup apps, Task Manager, disk usage, updates, Event Viewer, and documentation.

## Bulk CSV test

Use the included `sample_tickets.csv` file.

Expected result:

- The app should process multiple tickets.
- Each row should receive a category, priority, escalation status, confidence score, and recommended next action.
- The app should generate a downloadable output file or table, depending on the current interface behavior.

## Report download test

After analyzing a ticket:

1. Click the download report output.
2. Open the report file.
3. Confirm it includes:
   - Ticket ID
   - Summary
   - Category
   - Priority
   - Escalation required
   - Troubleshooting steps
   - Technician notes
   - User-friendly response
   - Recommended next action

## Privacy test

Confirm the app clearly warns users not to enter:

- Passwords
- MFA codes
- Recovery codes
- Private keys
- Payment information
- Customer personal information
- Confidential business data

## Pass criteria

The app passes testing when:

- It launches successfully.
- The Single Ticket workflow works.
- Reports download successfully.
- Sample tickets produce reasonable results.
- Bulk CSV upload works.
- The app does not ask users for sensitive information.
- The output looks like a professional support ticket/report.
