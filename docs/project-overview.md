# Project Overview

## Project name

IT Support Triage Assistant

## Summary

The IT Support Triage Assistant is a working service-desk workflow application built with Python and Gradio. It helps turn unstructured IT support requests into organized troubleshooting reports.

The app is designed to demonstrate practical technical support thinking, including categorization, prioritization, escalation awareness, documentation, user communication, and report generation.

## Problem statement

Many support requests arrive with missing details. A user may say:

> Outlook is not working.

That message does not immediately explain whether the issue is a Microsoft 365 sign-in problem, a local Outlook profile issue, a DNS/mail-flow issue, a password problem, or a wider outage.

This project improves the intake process by asking for useful context and generating a structured output that can be reviewed by a technician.

## Main goals

- Improve IT ticket intake quality
- Reduce unclear support handoffs
- Create consistent troubleshooting documentation
- Identify urgent or business-critical issues earlier
- Flag security, DNS, Microsoft 365, and outage issues for escalation
- Produce both technician notes and user-friendly responses
- Create downloadable support reports

## Core workflow

1. User submits a support request.
2. Assistant reviews the issue summary and supporting details.
3. Assistant detects or confirms the ticket category.
4. Assistant assigns a priority level.
5. Assistant checks whether escalation is required.
6. Assistant generates troubleshooting steps.
7. Assistant produces technician notes and a user-friendly response.
8. Assistant creates a downloadable Markdown report.

## Supported ticket categories

- Windows
- Microsoft 365
- Networking
- DNS
- Email
- Hardware
- Security
- General IT

## Priority model

The assistant uses four priority levels:

### Low

Used for how-to requests, documentation requests, minor settings changes, and non-urgent issues.

### Medium

Used for issues that affect productivity but do not fully block work, such as slow devices, intermittent Wi-Fi, Outlook sync problems, or application errors.

### High

Used for issues where a user cannot work, cannot sign in, cannot access business systems, or where admin-level review may be needed.

### Critical

Used for business-wide outages, multiple users affected, suspected breach, ransomware, data loss, business email outage, or payment system impact.

## Escalation model

The assistant recommends escalation when the request mentions high-risk or admin-level areas such as:

- Compromised account
- Phishing
- Malware or ransomware
- Data loss
- DNS records
- MX, SPF, DKIM, or DMARC
- Business-wide outage
- Microsoft 365 tenant/admin changes
- Multiple users affected
- Payment systems
- Domain or website production issues

## Output sections

Each ticket report includes:

- Ticket ID
- Date generated
- Ticket summary
- Category
- Priority
- Escalation required
- Escalation reason
- Affected system
- User impact
- Likely causes
- Troubleshooting steps
- Technician notes
- User-friendly response
- Recommended next action
- Confidence score
- Privacy reminder

## Why this project matters

This project shows more than basic coding. It demonstrates an understanding of real service-desk workflow, support documentation, user communication, and escalation logic.

It can be used as:

- A portfolio project
- A recruiter demo
- A service-desk workflow example
- A foundation for a small-business IT support intake tool

## Current limitations

- Rule-based logic only
- No persistent database
- No ticketing system integration
- No email notification
- No login or user accounts
- No real-time system diagnostics
- No live Microsoft 365, DNS, or endpoint checks

## Future direction

Future versions can add PDF reports, saved ticket history, dashboard views, client branding, LLM integration, email notifications, and ticketing system exports.
