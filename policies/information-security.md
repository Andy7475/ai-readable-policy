---
id: info-sec
title: Information Security Policy
version: "2.1"
date: "2025-01-15"
owner: "IT Security Team"
---

## Purpose and Scope

This policy establishes the minimum information security requirements for all employees, contractors, and third parties who access company information systems and data. It applies to all information assets owned, leased, or managed by the organisation, regardless of location or format.

The objectives of this policy are to protect the confidentiality, integrity, and availability of information assets; to comply with applicable legal, regulatory, and contractual requirements; and to maintain trust with customers, partners, and staff.

## Roles and Responsibilities

The Chief Information Security Officer (CISO) is accountable for the overall information security programme and reports to the Board.

Information Asset Owners are responsible for classifying the data assets under their stewardship in accordance with the Data Classification Policy, and for ensuring appropriate controls are applied.

All employees and contractors are responsible for complying with this policy and for reporting suspected security incidents or vulnerabilities to the IT Security Team without delay.

The IT Security Team is responsible for implementing technical controls, monitoring for threats, and maintaining this policy.

## Access Control

All access to information systems must be granted on a least-privilege basis. Users must be provisioned with the minimum permissions required to perform their job function. Requests for access must be approved by the relevant Information Asset Owner before provisioning.

Privileged accounts (administrator, root, service accounts) must be used only for tasks requiring elevated permissions. Privileged access must not be used for day-to-day activities such as email or web browsing.

Access rights must be reviewed quarterly by Information Asset Owners. Dormant accounts (inactive for more than 90 days) must be disabled. Access must be revoked within one business day of an employee or contractor leaving the organisation.

Multi-factor authentication (MFA) is mandatory for all remote access, all cloud-based services, and all privileged accounts.

## Password Requirements

Passwords must be a minimum of 14 characters and must not contain the user's name, username, or commonly known words. Passwords must be unique across systems; reuse of previous passwords is prohibited.

Passwords must not be shared between users under any circumstances. Where a system requires a shared credential (e.g. a service account), the credential must be stored in an approved password vault and access to the vault audited.

Passwords must be changed immediately upon any suspicion of compromise. The IT Security Team may force a password reset at any time if a compromise is suspected.

## Data Encryption

All data classified as Confidential or Restricted (as defined in the Data Classification Policy) must be encrypted at rest using AES-256 or equivalent. All such data must be encrypted in transit using TLS 1.2 or higher.

Laptop and mobile device storage must be fully encrypted using an approved solution. Unencrypted storage of Confidential or Restricted data on removable media is prohibited.

Encryption keys must be managed through an approved key management system. Keys must be rotated annually and whenever a key custodian leaves the organisation.

## Incident Response

All suspected or confirmed security incidents must be reported to the IT Security Team immediately and no later than one hour after discovery. Incidents include but are not limited to: unauthorised access, malware infection, data loss or exfiltration, and phishing attacks.

The IT Security Team will assess, contain, and remediate incidents in accordance with the Incident Response Procedure. A post-incident review must be conducted for all Severity 1 and Severity 2 incidents within ten business days.

Personal data breaches that meet the threshold for regulatory notification must be reported to the relevant supervisory authority within 72 hours of discovery, in accordance with applicable data protection legislation.

## Policy Compliance and Enforcement

Compliance with this policy is mandatory. The IT Security Team will conduct periodic audits and penetration tests to assess compliance. Findings will be reported to the CISO and relevant business owners.

Violations of this policy may result in disciplinary action up to and including termination of employment or contract. Serious violations may be referred to law enforcement authorities.

Exceptions to this policy must be formally requested, documented, and approved by the CISO. Exceptions are granted for a defined period only and must be reviewed before expiry.
