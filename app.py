import csv
import os
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

import gradio as gr


APP_TITLE = "IT Support Triage Assistant"
APP_VERSION = "v2.1"
APP_TAGLINE = "Turn support requests into structured troubleshooting reports."

CATEGORIES = [
    "Auto-detect",
    "Windows",
    "Microsoft 365",
    "Networking",
    "DNS",
    "Email",
    "Hardware",
    "Security",
    "General IT",
]

PRIORITY_ORDER = ["Low", "Medium", "High", "Critical"]

CATEGORY_KEYWORDS = {
    "Windows": [
        "windows", "blue screen", "bsod", "login", "profile", "update", "driver",
        "event viewer", "slow laptop", "slow computer", "freezing", "restart",
        "boot", "device manager", "bitlocker", "mapped drive", "task manager",
        "windows update", "file explorer", "startup", "crash", "crashing"
    ],
    "Microsoft 365": [
        "microsoft 365", "office 365", "m365", "outlook", "teams", "onedrive",
        "sharepoint", "exchange", "entra", "azure ad", "license", "mailbox",
        "calendar", "admin center", "mfa", "password popup", "conditional access",
        "onedrive sync", "teams meeting", "shared mailbox"
    ],
    "Networking": [
        "wifi", "wi-fi", "internet", "router", "switch", "dhcp", "vpn", "ip address",
        "gateway", "network", "lan", "wan", "packet loss", "ping", "dns server",
        "cable", "ethernet", "no connection", "disconnect", "latency", "slow internet",
        "hotspot", "access point", "firewall"
    ],
    "DNS": [
        "dns", "domain", "mx", "spf", "dkim", "dmarc", "txt record", "a record",
        "cname", "nameserver", "propagation", "mail routing", "website not resolving",
        "nxdomain", "dns_probe_finished", "ttl", "zone file", "verification record"
    ],
    "Email": [
        "email", "mail", "smtp", "imap", "pop3", "bounce", "delivery", "inbox",
        "spam", "junk", "send", "receive", "mailbox", "outlook", "thunderbird",
        "undeliverable", "quarantine", "mail flow", "blocked sender"
    ],
    "Hardware": [
        "hardware", "screen", "keyboard", "mouse", "battery", "charger", "ssd",
        "hard drive", "ram", "fan", "overheating", "printer", "monitor", "dock",
        "usb", "touchscreen", "display", "noise", "physical damage", "power", "won't turn on"
    ],
    "Security": [
        "security", "phishing", "malware", "virus", "ransomware", "hacked",
        "compromised", "breach", "suspicious", "mfa", "2fa", "unauthorized",
        "account takeover", "data loss", "leak", "spam sent", "clicked link",
        "entered password", "sign in from", "impossible travel", "alert"
    ],
}

CATEGORY_STEPS = {
    "Windows": [
        "Confirm the Windows version, device name, username, and whether the issue affects one user or multiple users.",
        "Restart the device and test whether the issue continues after a clean reboot.",
        "Check Windows Update history, recently installed applications, and recent driver changes.",
        "Review Task Manager for high CPU, memory, disk, or startup process usage.",
        "Check Event Viewer for application, system, and security errors around the time the issue started.",
        "Test with another Windows user profile if the issue appears profile-specific.",
        "Document the error message, screenshots, affected application, and exact troubleshooting actions taken."
    ],
    "Microsoft 365": [
        "Confirm the affected user, Microsoft 365 service, license status, and whether the issue affects one user or multiple users.",
        "Check Microsoft 365 service health before making local changes.",
        "Verify sign-in status, MFA prompts, password status, license assignment, and conditional access impact if applicable.",
        "For Outlook issues, test webmail access first to separate mailbox/service issues from local Outlook profile issues.",
        "Check mailbox storage, rules, forwarding, shared mailbox permissions, and recent account changes.",
        "If admin access is required, escalate with the user impact, affected account, error messages, and timestamps.",
        "Document the result in technician notes and provide a user-friendly summary."
    ],
    "Networking": [
        "Confirm whether the issue affects Wi-Fi, wired Ethernet, VPN, one device, multiple devices, or the whole site.",
        "Check physical connectivity, router/switch status, Wi-Fi signal strength, and whether other devices can connect.",
        "Confirm IP address, gateway, DNS server, and DHCP lease status.",
        "Run basic tests such as pinging the gateway, testing DNS resolution, and testing an external site.",
        "Restart the affected device/network adapter before restarting shared network equipment.",
        "For VPN issues, confirm internet access works before testing the VPN client, credentials, MFA, and profile configuration.",
        "Escalate outages affecting multiple users or business-critical systems."
    ],
    "DNS": [
        "Confirm the domain name, DNS host, requested record change, and business impact.",
        "Check current A, CNAME, MX, TXT, SPF, DKIM, and DMARC records depending on the issue.",
        "Confirm whether the issue is email delivery, website resolution, verification, or migration-related.",
        "Review recent DNS changes and compare records against provider documentation.",
        "Avoid making DNS changes without approval because incorrect records can affect email or website availability.",
        "After changes, validate records and document TTL/propagation expectations.",
        "Escalate if records control production email, payment systems, client portals, or business-critical websites."
    ],
    "Email": [
        "Confirm whether the issue affects sending, receiving, authentication, spam/junk placement, or delivery failures.",
        "Collect bounce messages, error codes, timestamps, sender, recipient, and affected mailbox details.",
        "Test webmail access to separate mailbox/service issues from local client issues.",
        "Check mailbox storage, password/MFA prompts, rules, forwarding, and blocked sign-in risk.",
        "For delivery issues, review MX, SPF, DKIM, DMARC, and mail routing configuration.",
        "For Outlook/Thunderbird, confirm account settings, server names, ports, and authentication method.",
        "Escalate suspected compromised accounts, business-wide email outages, or DNS-related changes."
    ],
    "Hardware": [
        "Confirm the device model, serial/asset tag if available, warranty status, and symptoms.",
        "Check power, cables, accessories, docks, ports, and external monitors before replacing parts.",
        "Test with known-good cables, chargers, USB ports, or peripherals when possible.",
        "Check Device Manager/system logs if the hardware is detected but not working properly.",
        "Document photos, error lights, noises, overheating, battery state, and any physical damage.",
        "Escalate hardware failures that block work, involve data loss, or require parts replacement.",
        "Recommend backup before any storage-related troubleshooting."
    ],
    "Security": [
        "Treat the issue as sensitive and avoid collecting passwords, MFA codes, or private keys.",
        "Confirm the affected account/device, suspicious activity, timestamps, and whether multiple users are impacted.",
        "Disconnect an obviously infected device from the network if malware or ransomware is suspected.",
        "Preserve evidence such as email headers, screenshots, alerts, and logs where appropriate.",
        "Check recent sign-ins, mailbox rules/forwarding, MFA status, and unauthorized changes.",
        "Escalate immediately for compromised accounts, malware, ransomware, data loss, or business-wide impact.",
        "Document actions taken and communicate only safe, user-friendly next steps."
    ],
    "General IT": [
        "Clarify the affected user, device, application, error message, and when the issue started.",
        "Confirm whether the issue affects one user, multiple users, or the whole business.",
        "Reproduce the issue or collect screenshots/error details if reproduction is not possible.",
        "Check recent changes such as updates, password changes, new software, DNS changes, or network changes.",
        "Try the lowest-risk troubleshooting steps first and document each result.",
        "Escalate if admin access, security risk, outage, or data loss is involved.",
        "Provide a clear user-friendly summary and next steps."
    ],
}

LIKELY_CAUSES = {
    "Windows": [
        "Recent Windows update, driver change, corrupted user profile, low disk space, high startup load, or application conflict."
    ],
    "Microsoft 365": [
        "Password/MFA change, license issue, service health problem, Outlook profile issue, mailbox rule/forwarding issue, or conditional access policy."
    ],
    "Networking": [
        "Weak Wi-Fi signal, DHCP issue, DNS server issue, VPN profile problem, router/switch issue, firewall rule, or ISP interruption."
    ],
    "DNS": [
        "Incorrect DNS records, nameserver change, TTL/propagation delay, missing verification record, or mail-routing misconfiguration."
    ],
    "Email": [
        "Authentication issue, mailbox storage issue, incorrect SMTP/IMAP settings, mail-flow rule, spam filtering, or DNS record problem."
    ],
    "Hardware": [
        "Cable/power issue, failing accessory, driver issue, damaged component, overheating, battery failure, or storage/RAM problem."
    ],
    "Security": [
        "Phishing attempt, compromised credentials, unauthorized sign-in, malicious attachment/link, mailbox rule abuse, or infected device."
    ],
    "General IT": [
        "Insufficient details yet. The issue may involve recent changes, account access, software configuration, device state, or network connectivity."
    ],
}

CRITICAL_TERMS = [
    "ransomware", "breach", "data loss", "all users", "everyone", "entire company",
    "entire business", "network outage", "email down", "business email down",
    "server down", "payment system", "compromised", "hacked", "leak", "cannot process payments"
]

HIGH_TERMS = [
    "cannot work", "can't work", "unable to work", "cannot login", "can't login",
    "cannot log in", "locked out", "vpn down", "no internet", "outlook not sending",
    "not receiving email", "multiple users", "mfa not working", "password popup", "cannot access"
]

MEDIUM_TERMS = [
    "slow", "freezing", "intermittent", "printer", "disconnecting", "error",
    "crashing", "sync", "calendar", "teams", "onedrive", "sometimes", "delay"
]

ESCALATION_TERMS = [
    "compromised", "hacked", "ransomware", "malware", "breach", "data loss",
    "unauthorized", "phishing", "mfa", "dns", "mx", "spf", "dkim", "dmarc",
    "domain", "admin", "tenant", "payment", "all users", "multiple users",
    "entire company", "entire business", "server down", "network outage", "entered password",
    "clicked link", "email down", "business down"
]

SAMPLES = {
    "Microsoft 365 login issue": [
        "User cannot sign in to Microsoft 365 after a password reset.",
        "Error says sign-in blocked or MFA required.",
        "Microsoft 365",
        "1 user",
        "High",
        "Laptop",
        "Windows 11",
        "Password was changed yesterday and MFA was recently enabled.",
    ],
    "Outlook password popup": [
        "User keeps getting password popups in Outlook and cannot send email.",
        "Outlook says password required. Webmail works sometimes.",
        "Microsoft 365",
        "1 user",
        "High",
        "Laptop",
        "Windows 11",
        "Password was changed yesterday and MFA was recently enabled.",
    ],
    "Business email outage": [
        "Multiple users are not receiving business email after a domain change.",
        "Senders are getting bounce messages.",
        "Auto-detect",
        "Multiple users",
        "Critical",
        "Multiple devices",
        "Microsoft 365",
        "DNS records were updated this morning.",
    ],
    "Suspicious email / phishing": [
        "User clicked a suspicious email link and entered their password.",
        "No error message. User reported the email looked like a Microsoft login page.",
        "Security",
        "1 user",
        "Critical",
        "Laptop",
        "Windows 11",
        "Happened about 20 minutes ago.",
    ],
    "Website DNS issue": [
        "Company website is not loading after changing nameservers.",
        "Browser says DNS_PROBE_FINISHED_NXDOMAIN.",
        "DNS",
        "Entire business",
        "High",
        "Website/domain",
        "Web/DNS",
        "Nameservers were changed last night.",
    ],
    "Wi-Fi disconnecting": [
        "Wi-Fi keeps disconnecting from one laptop every few minutes.",
        "No specific error. Browser says no internet.",
        "Networking",
        "1 user",
        "Medium",
        "Laptop",
        "Windows 11",
        "Started after moving to another office area.",
    ],
    "Slow Windows laptop": [
        "Computer is very slow after startup and apps take a long time to open.",
        "No error code.",
        "Windows",
        "1 user",
        "Medium",
        "Laptop",
        "Windows 10",
        "Several startup apps were installed recently.",
    ],
    "Printer not working": [
        "Office printer is not printing from one Windows laptop.",
        "Print job stays stuck in queue.",
        "Hardware",
        "1 user",
        "Medium",
        "Printer",
        "Windows 11",
        "Printer driver was updated recently.",
    ],
}


def clean_text(value):
    return (value or "").strip()


def combine_text(*values):
    return " ".join(clean_text(v) for v in values if clean_text(v)).lower()


def count_keyword_matches(text, keywords):
    return sum(1 for keyword in keywords if keyword in text)


def detect_category(issue_summary, error_message, recent_changes, selected_category):
    selected_category = selected_category or "Auto-detect"
    if selected_category != "Auto-detect":
        return selected_category, "User-selected category"

    text = combine_text(issue_summary, error_message, recent_changes)
    scores = {
        category: count_keyword_matches(text, keywords)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }

    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "General IT", "No strong category keywords found"

    return best_category, f"Detected from keywords: {scores[best_category]} match(es)"


def determine_priority(text, affected_users, urgency):
    affected = (affected_users or "").lower()
    urgency_value = urgency if urgency in PRIORITY_ORDER else "Medium"

    if any(term in text for term in CRITICAL_TERMS):
        priority = "Critical"
        reason = "Business-critical, security, data-loss, payment, or broad outage language was detected."
    elif "entire" in affected or "business" in affected or "all" in affected:
        priority = "Critical"
        reason = "The issue appears to affect the entire business or all users."
    elif any(term in text for term in HIGH_TERMS):
        priority = "High"
        reason = "The issue appears to block work, access, email, VPN, or multiple users."
    elif "multiple" in affected or "more than one" in affected:
        priority = "High"
        reason = "The issue affects multiple users."
    elif any(term in text for term in MEDIUM_TERMS):
        priority = "Medium"
        reason = "The issue affects productivity but does not clearly indicate a full outage."
    else:
        priority = "Low"
        reason = "No outage, security risk, or work-blocking impact was detected."

    if PRIORITY_ORDER.index(urgency_value) > PRIORITY_ORDER.index(priority):
        reason += f" User-selected urgency raised priority to {urgency_value}."
        priority = urgency_value

    return priority, reason


def escalation_check(text, category, priority):
    if category == "Security":
        return "Yes", "Security-related issues should be reviewed or escalated to an authorized technician/admin."
    if priority == "Critical":
        return "Yes", "Critical priority issues require escalation or immediate technician review."
    if any(term in text for term in ESCALATION_TERMS):
        return "Yes", "The issue includes admin-level, DNS, security, outage, or multi-user risk indicators."
    return "No", "No strong escalation trigger was detected from the provided details."


def calculate_confidence(issue_summary, error_message, recent_changes, category_reason, selected_category):
    text = combine_text(issue_summary, error_message, recent_changes)
    match_count = sum(
        count_keyword_matches(text, keywords)
        for keywords in CATEGORY_KEYWORDS.values()
    )
    confidence = 58 + min(match_count * 4, 24)

    if selected_category and selected_category != "Auto-detect":
        confidence += 8
    if clean_text(error_message):
        confidence += 5
    if len(clean_text(issue_summary)) > 80:
        confidence += 5
    if "No strong category" in category_reason:
        confidence -= 10

    return max(45, min(confidence, 95))


def summarize_user_impact(affected_users, priority, category):
    affected = clean_text(affected_users) or "Not sure"
    if priority == "Critical":
        return f"High business impact. The issue may affect {affected.lower()} and should be reviewed quickly."
    if priority == "High":
        return f"Work-blocking or time-sensitive impact for {affected.lower()}."
    if priority == "Medium":
        return f"Productivity impact for {affected.lower()} with no confirmed full outage."
    return f"Lower immediate impact for {affected.lower()}, but details should still be documented."


def recommended_next_action(category, priority, escalation):
    if escalation == "Yes" and category == "Security":
        return "Escalate to an authorized admin/security contact, preserve evidence, review sign-in activity, and reset credentials through an approved process."
    if escalation == "Yes" and category in ["DNS", "Email", "Microsoft 365"]:
        return "Escalate to the service/admin owner with the affected account/domain, timestamps, error messages, and recent changes."
    if escalation == "Yes":
        return "Escalate with a clear summary, impact level, affected users, error details, and steps already attempted."
    if priority in ["High", "Critical"]:
        return "Collect missing details immediately, confirm business impact, and proceed with the highest-confidence troubleshooting path."
    return "Collect missing details, attempt the listed troubleshooting steps, and document each result."


def missing_info_prompts(category, device_type, operating_system, error_message, affected_users):
    missing = []
    if not clean_text(device_type) or device_type == "Not sure":
        missing.append("device type")
    if not clean_text(operating_system) or operating_system == "Not sure":
        missing.append("operating system or platform")
    if not clean_text(error_message):
        missing.append("exact error message or screenshot details")
    if not clean_text(affected_users) or affected_users == "Not sure":
        missing.append("number of affected users")

    category_specific = {
        "DNS": "domain name, DNS provider, record type, current record values, and recent DNS changes",
        "Email": "sender, recipient, bounce message, email provider, timestamp, and mailbox affected",
        "Microsoft 365": "affected mailbox, license status, MFA state, service health, and recent account changes",
        "Networking": "IP address, gateway, DNS server, Wi-Fi/Ethernet/VPN status, and affected devices",
        "Security": "timestamps, suspicious email headers, sign-in logs, affected account, and actions already taken",
        "Windows": "Windows version, device name, event logs, update history, and affected application",
        "Hardware": "device model, serial/asset tag, warranty status, physical symptoms, and photos if safe",
        "General IT": "affected application, device, account, screenshots, and timeline"
    }
    missing.append(category_specific.get(category, category_specific["General IT"]))
    return missing


def make_ticket_id():
    today = datetime.now().strftime("%Y%m%d")
    short_id = uuid.uuid4().hex[:6].upper()
    return f"ITS-{today}-{short_id}"


def build_report(
    name_company,
    issue_summary,
    selected_category,
    device_type,
    operating_system,
    affected_users,
    urgency,
    error_message,
    recent_changes,
):
    issue_summary = clean_text(issue_summary)
    error_message = clean_text(error_message)
    recent_changes = clean_text(recent_changes)

    if not issue_summary:
        raise gr.Error("Please enter an issue summary before analyzing the ticket.")

    category, category_reason = detect_category(
        issue_summary, error_message, recent_changes, selected_category
    )
    full_text = combine_text(issue_summary, error_message, recent_changes, affected_users, urgency)
    priority, priority_reason = determine_priority(full_text, affected_users, urgency)
    escalation, escalation_reason = escalation_check(full_text, category, priority)
    confidence = calculate_confidence(issue_summary, error_message, recent_changes, category_reason, selected_category)
    impact = summarize_user_impact(affected_users, priority, category)
    likely_causes = LIKELY_CAUSES.get(category, LIKELY_CAUSES["General IT"])
    next_action = recommended_next_action(category, priority, escalation)

    ticket_id = make_ticket_id()
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    steps = CATEGORY_STEPS.get(category, CATEGORY_STEPS["General IT"])
    missing = missing_info_prompts(category, device_type, operating_system, error_message, affected_users)

    technician_notes = [
        f"Ticket should be handled as {priority} priority.",
        f"Primary category: {category}.",
        f"Escalation required: {escalation}.",
        f"Category reason: {category_reason}.",
        f"Priority reason: {priority_reason}",
        f"Escalation reason: {escalation_reason}",
        f"Recommended next action: {next_action}",
        "Confirm user impact and reproduce the issue where possible.",
        "Avoid collecting passwords, MFA codes, private keys, recovery codes, or confidential data."
    ]

    user_response = (
        "Thanks for reporting this. Based on the details provided, this appears to be a "
        f"{priority.lower()} priority {category} issue. "
    )
    if escalation == "Yes":
        user_response += (
            "This should be reviewed by an authorized technician or administrator because it may involve "
            "security risk, admin-level access, DNS changes, multiple users, or business-critical impact. "
        )
    else:
        user_response += (
            "The next step is to collect the missing details and work through the recommended troubleshooting steps. "
        )
    user_response += (
        "Please do not share passwords, MFA codes, recovery codes, private keys, or confidential business information."
    )

    md = f"""# {APP_TITLE} Report

**Ticket ID:** {ticket_id}  
**Generated:** {generated_at}  
**Name / Company:** {clean_text(name_company) or "Not provided"}  
**App Version:** {APP_VERSION}  

## Ticket Summary

{issue_summary}

## Classification

| Field | Result |
|---|---|
| Category | {category} |
| Category Reason | {category_reason} |
| Priority | {priority} |
| Priority Reason | {priority_reason} |
| Escalation Required | {escalation} |
| Escalation Reason | {escalation_reason} |
| Confidence Score | {confidence}% |

## Environment

| Field | Details |
|---|---|
| Device Type | {clean_text(device_type) or "Not provided"} |
| Operating System / Platform | {clean_text(operating_system) or "Not provided"} |
| Affected Users | {clean_text(affected_users) or "Not provided"} |
| User-Selected Urgency | {clean_text(urgency) or "Not provided"} |

## User Impact

{impact}

## Likely Causes

""" + "\n".join([f"- {cause}" for cause in likely_causes]) + f"""

## Error Message / Screenshot Details

{error_message or "Not provided"}

## Recent Changes

{recent_changes or "Not provided"}

## Recommended Next Action

{next_action}

## Recommended Troubleshooting Steps

""" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)]) + f"""

## Information Still Needed

""" + "\n".join([f"- {item}" for item in missing]) + f"""

## Technician Notes

""" + "\n".join([f"- {note}" for note in technician_notes]) + f"""

## User-Friendly Response

{user_response}

## Privacy Reminder

Do not enter or store passwords, MFA codes, recovery codes, private keys, full customer personal information, payment information, or confidential business data in this tool.
"""

    output_md = f"""## Ticket Result

**Ticket ID:** `{ticket_id}`  
**Category:** {category}  
**Priority:** {priority}  
**Escalation Required:** {escalation}  
**Confidence:** {confidence}%

### Ticket Summary
{issue_summary}

### User Impact
{impact}

### Likely Cause
{likely_causes[0]}

### Why
- {priority_reason}
- {escalation_reason}

### Recommended Next Action
{next_action}

### Recommended Troubleshooting Steps
""" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps[:6])]) + f"""

### Technician Notes
""" + "\n".join([f"- {note}" for note in technician_notes[:7]]) + f"""

### User-Friendly Response
{user_response}
"""

    report_path = Path(tempfile.gettempdir()) / f"{ticket_id}_support_report.md"
    report_path.write_text(md, encoding="utf-8")

    return output_md, "\n".join([f"- {note}" for note in technician_notes]), user_response, confidence, str(report_path)


def bulk_analyze(csv_file):
    if csv_file is None:
        raise gr.Error("Upload a CSV file first.")

    path = csv_file if isinstance(csv_file, str) else csv_file.name
    rows = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise gr.Error("The CSV needs a header row. Use columns like issue_summary, category, urgency, affected_users.")
        for row in reader:
            rows.append(row)

    if not rows:
        raise gr.Error("The CSV file does not contain any ticket rows.")

    result_rows = []
    report_sections = [f"# Bulk IT Support Triage Report\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

    for index, row in enumerate(rows, start=1):
        issue = row.get("issue_summary") or row.get("issue") or row.get("summary") or ""
        category_choice = row.get("category") or "Auto-detect"
        urgency = row.get("urgency") or "Medium"
        affected = row.get("affected_users") or row.get("affected") or "Not sure"
        device = row.get("device_type") or row.get("device") or "Not sure"
        os_name = row.get("operating_system") or row.get("os") or "Not sure"
        error = row.get("error_message") or row.get("error") or ""
        changes = row.get("recent_changes") or row.get("changes") or ""

        if not clean_text(issue):
            continue

        category, category_reason = detect_category(issue, error, changes, category_choice)
        full_text = combine_text(issue, error, changes, affected, urgency)
        priority, priority_reason = determine_priority(full_text, affected, urgency)
        escalation, escalation_reason = escalation_check(full_text, category, priority)
        confidence = calculate_confidence(issue, error, changes, category_reason, category_choice)
        impact = summarize_user_impact(affected, priority, category)
        next_action = recommended_next_action(category, priority, escalation)

        result_rows.append([index, issue[:90], category, priority, escalation, confidence, next_action[:90]])
        report_sections.append(
            f"""## Ticket {index}

**Issue:** {issue}  
**Category:** {category}  
**Priority:** {priority}  
**Escalation Required:** {escalation}  
**Confidence:** {confidence}%  
**User Impact:** {impact}  

**Priority Reason:** {priority_reason}  
**Escalation Reason:** {escalation_reason}  
**Recommended Next Action:** {next_action}  

### Recommended Steps
""" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(CATEGORY_STEPS.get(category, CATEGORY_STEPS["General IT"])[:5])]) + "\n"
        )

    if not result_rows:
        raise gr.Error("No usable ticket rows were found. Make sure your CSV has an issue_summary column.")

    report_path = Path(tempfile.gettempdir()) / f"bulk_triage_report_{uuid.uuid4().hex[:6]}.md"
    report_path.write_text("\n".join(report_sections), encoding="utf-8")

    summary = f"Analyzed {len(result_rows)} ticket(s). Download the Markdown report for the full notes."
    return result_rows, summary, str(report_path)


def load_sample(sample_name):
    return SAMPLES.get(sample_name, ["", "", "Auto-detect", "Not sure", "Medium", "Not sure", "Not sure", ""])


custom_css = """
.gradio-container {
    max-width: 1180px !important;
}
#app-header {
    border: 1px solid #243044;
    border-radius: 18px;
    padding: 22px;
    background: linear-gradient(135deg, #0f172a 0%, #111827 60%, #1e293b 100%);
    color: white;
}
#app-header h1 {
    margin-bottom: 6px;
}
.privacy-box {
    border-left: 4px solid #f59e0b;
    padding: 12px 14px;
    border-radius: 10px;
    background: #fff7ed;
}
.small-note {
    color: #64748b;
    font-size: 0.95rem;
}
"""


with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown(
        f"""
<div id="app-header">

# 🛠️ {APP_TITLE} {APP_VERSION}

### {APP_TAGLINE}

This tool categorizes IT issues, assigns priority, checks whether escalation is required, generates troubleshooting steps, and creates technician-ready notes.

</div>
""",
        elem_id="header-markdown",
    )

    gr.Markdown(
        """
<div class="privacy-box">

**Privacy reminder:** Do not enter passwords, MFA codes, recovery codes, private keys, customer personal information, payment information, or confidential business data.

</div>
"""
    )

    with gr.Tab("Single Ticket"):
        with gr.Row():
            with gr.Column(scale=1):
                name_company = gr.Textbox(label="Name / Company", placeholder="Optional")
                issue_summary = gr.Textbox(
                    label="Issue Summary",
                    lines=5,
                    placeholder="Example: Outlook keeps asking for a password and the user cannot send email.",
                )
                error_message = gr.Textbox(
                    label="Error Message / Screenshot Details",
                    lines=3,
                    placeholder="Paste the exact error message if available. Do not paste passwords or private data.",
                )
                recent_changes = gr.Textbox(
                    label="Recent Changes",
                    lines=3,
                    placeholder="Example: Password changed yesterday, new router installed, DNS records updated, Windows update installed.",
                )

            with gr.Column(scale=1):
                selected_category = gr.Dropdown(
                    choices=CATEGORIES,
                    value="Auto-detect",
                    label="Category",
                )
                device_type = gr.Dropdown(
                    choices=[
                        "Not sure",
                        "Desktop",
                        "Laptop",
                        "Mobile device",
                        "Printer",
                        "Router/Switch",
                        "Server",
                        "Website/domain",
                        "Multiple devices",
                    ],
                    value="Not sure",
                    label="Device Type",
                )
                operating_system = gr.Dropdown(
                    choices=[
                        "Not sure",
                        "Windows 11",
                        "Windows 10",
                        "macOS",
                        "Linux",
                        "iOS",
                        "Android",
                        "Network device",
                        "Web/DNS",
                        "Microsoft 365",
                    ],
                    value="Not sure",
                    label="Operating System / Platform",
                )
                affected_users = gr.Dropdown(
                    choices=[
                        "Not sure",
                        "1 user",
                        "Multiple users",
                        "Entire business",
                    ],
                    value="Not sure",
                    label="Affected Users",
                )
                urgency = gr.Dropdown(
                    choices=PRIORITY_ORDER,
                    value="Medium",
                    label="User-Selected Urgency",
                )

        sample_choice = gr.Dropdown(
            choices=list(SAMPLES.keys()),
            label="Load a Sample Ticket",
            value=None,
        )
        sample_choice.change(
            fn=load_sample,
            inputs=sample_choice,
            outputs=[
                issue_summary,
                error_message,
                selected_category,
                affected_users,
                urgency,
                device_type,
                operating_system,
                recent_changes,
            ],
        )

        with gr.Row():
            analyze_btn = gr.Button("Analyze Ticket", variant="primary")
            clear_btn = gr.ClearButton(
                [
                    name_company,
                    issue_summary,
                    error_message,
                    recent_changes,
                    selected_category,
                    device_type,
                    operating_system,
                    affected_users,
                    urgency,
                ],
                value="Clear Form",
            )

        with gr.Row():
            with gr.Column(scale=2):
                ticket_result = gr.Markdown(label="Ticket Result")
            with gr.Column(scale=1):
                confidence_score = gr.Number(label="Confidence Score", precision=0)
                report_file = gr.File(label="Download Support Report")

        with gr.Accordion("Technician Notes", open=False):
            technician_notes_output = gr.Textbox(label="Technician Notes", lines=10)

        with gr.Accordion("User-Friendly Response", open=False):
            user_response_output = gr.Textbox(label="User-Friendly Response", lines=6)

        analyze_btn.click(
            fn=build_report,
            inputs=[
                name_company,
                issue_summary,
                selected_category,
                device_type,
                operating_system,
                affected_users,
                urgency,
                error_message,
                recent_changes,
            ],
            outputs=[
                ticket_result,
                technician_notes_output,
                user_response_output,
                confidence_score,
                report_file,
            ],
        )

    with gr.Tab("Bulk CSV Tickets"):
        gr.Markdown(
            """
Upload a CSV file with columns like:

`issue_summary, category, urgency, affected_users, device_type, operating_system, error_message, recent_changes`

The assistant will analyze each row and generate a combined Markdown report.
"""
        )
        csv_upload = gr.File(label="Upload CSV", file_types=[".csv"], type="filepath")
        bulk_btn = gr.Button("Analyze CSV Tickets", variant="primary")
        bulk_table = gr.Dataframe(
            headers=["#", "Issue", "Category", "Priority", "Escalation", "Confidence", "Recommended Next Action"],
            label="Bulk Results",
            interactive=False,
        )
        bulk_summary = gr.Markdown()
        bulk_report = gr.File(label="Download Bulk Report")

        bulk_btn.click(
            fn=bulk_analyze,
            inputs=csv_upload,
            outputs=[bulk_table, bulk_summary, bulk_report],
        )

    with gr.Tab("About"):
        gr.Markdown(
            f"""
## What this assistant does

The **{APP_TITLE}** helps turn unstructured support requests into organized service-desk style notes.

### Main features

- Categorizes tickets as Windows, Microsoft 365, Networking, DNS, Email, Hardware, Security, or General IT
- Assigns Low, Medium, High, or Critical priority
- Detects whether escalation is required
- Generates likely causes, troubleshooting steps, technician notes, and a user-friendly response
- Creates a downloadable Markdown support report
- Supports bulk CSV ticket analysis

### Best use cases

- Help desk ticket intake
- Small business IT support requests
- Microsoft 365 troubleshooting
- DNS and email issue documentation
- Security issue triage
- Technician handoff notes
- Portfolio/recruiter demonstration

### Important limitation

This tool is a triage and documentation assistant. It does not replace an authorized technician, administrator, cybersecurity professional, or business approval process.
"""
        )


if __name__ == "__main__":
    demo.launch()
