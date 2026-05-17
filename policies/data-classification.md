---
id: data-class
title: Data Classification Policy
version: "1.4"
date: "2024-09-01"
owner: "Data Governance Team"
---

## Purpose and Scope

This policy defines the classification framework for all data assets held or processed by the organisation. It establishes four classification levels and specifies the handling, storage, transmission, and disposal requirements for each level.

This policy applies to all structured and unstructured data, regardless of format (digital or physical) or location (on-premises, cloud, or third-party systems). All employees, contractors, and third parties who create, access, or process organisational data are subject to this policy.

## Classification Levels

Data must be assigned one of the following four classification levels at the point of creation or acquisition. When in doubt, data should be assigned the higher classification level.

**Public** — Information that has been formally approved for unrestricted public disclosure. Examples include published marketing materials, press releases, and publicly available product documentation. No special handling is required beyond accuracy and brand consistency.

**Internal** — Information intended solely for internal use by employees and authorised contractors. Examples include internal procedures, meeting minutes, project plans, and non-sensitive operational data. Internal data must not be shared externally without explicit authorisation from the Information Asset Owner.

**Confidential** — Sensitive business information whose unauthorised disclosure could cause significant harm to the organisation, its employees, customers, or partners. Examples include financial forecasts, contracts, HR records, customer data, and security configurations. Confidential data requires encryption at rest and in transit, and access must be limited to those with a documented business need.

**Restricted** — The highest classification level, reserved for information whose unauthorised disclosure could cause severe legal, financial, reputational, or safety consequences. Examples include cryptographic keys, authentication credentials, personal data subject to regulatory protection, and merger or acquisition details before public announcement. Restricted data requires the strongest available technical and procedural controls.

## Classification Responsibilities

Information Asset Owners are responsible for assigning and maintaining the correct classification for data assets under their stewardship. Classifications must be reviewed at least annually and whenever there is a material change in the nature or sensitivity of the data.

All employees are responsible for handling data in accordance with its classification. Employees who are uncertain about the correct classification of a particular dataset must consult the Information Asset Owner or the Data Governance Team before processing or sharing the data.

## Handling Requirements by Classification Level

**Public** — No special handling required. May be freely shared internally and externally.

**Internal** — Must not be sent to external recipients without approval. Must not be stored on personal devices or unapproved cloud storage services. Physical copies must be disposed of by cross-cut shredding.

**Confidential** — Must be encrypted at rest (AES-256 or equivalent) and in transit (TLS 1.2 or higher). Must only be shared on a need-to-know basis. Email containing Confidential data must use encrypted email or a secure file transfer service. Physical copies must be kept in locked storage and disposed of by cross-cut shredding. Access must be logged and auditable.

**Restricted** — All Confidential requirements apply, plus: access must be approved by both the Information Asset Owner and the CISO; data must never leave approved systems without explicit CISO authorisation; all access events must be logged and reviewed; physical copies require secure courier for transit and witnessed destruction for disposal.

## Retention and Disposal

Data must be retained for the minimum period required by legal, regulatory, or contractual obligations as specified in the Retention Schedule maintained by the Data Governance Team. Data must not be retained beyond its defined retention period unless subject to a legal hold.

At the end of its retention period, data must be securely disposed of. Digital data must be overwritten using an approved multi-pass method or cryptographically erased. Physical media containing Confidential or Restricted data must be physically destroyed.

Records of disposal must be retained for three years.

## Third-Party Data Sharing

Before sharing Confidential or Restricted data with a third party, a Data Sharing Agreement (DSA) or equivalent contractual protection must be in place. The DSA must specify the permitted purposes, handling requirements, retention limits, and obligations on the third party in the event of a breach.

Third parties must demonstrate compliance with handling requirements equivalent to those in this policy before data is transferred. The Data Governance Team must approve all new third-party data sharing arrangements involving Confidential or Restricted data.
