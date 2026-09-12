---
layout: post
title: "Cold and Hot Wallet Policy: What Regulators Expect from VASPs"
date: 2026-09-12 17:49:32 +0500
categories: [Licensing]
author: "Noor Aslam"
description: "This article explains how Pakistan's virtual asset regulators expect operators to manage cold and hot wallets to protect client assets."
---

Operating a virtual asset business in Pakistan means navigating a developing regulatory landscape. A critical area of focus for the Pakistan Virtual Assets Regulatory Authority (PVARA) and other relevant bodies is the secure management of client virtual assets. This directly involves your firm's policies and procedures for cold and hot wallets.

The way your business stores, manages, and transfers virtual assets is central to your operational resilience and your ability to protect client funds. Regulators view robust wallet management as a cornerstone of a secure and compliant virtual asset service provider (VASP) operation. Demonstrating clear, auditable, and secure practices is essential for licence application approval and ongoing compliance.

Understanding and implementing best practices for cold and hot wallet management is not just about meeting regulatory checkboxes. It is about building trust with your clients and ensuring the long-term viability of your business in a sector prone to security risks. This analysis outlines what firms should consider as the regulatory framework for virtual assets in Pakistan continues to develop.

## What are cold and hot wallets in the context of virtual assets?

Cold and hot wallets refer to different methods of storing the private keys that control virtual assets. Hot wallets are connected to the internet and are used for frequent transactions, offering high accessibility but increased online risk. Cold wallets are offline, providing greater security for large asset holdings but with less immediate accessibility.

Hot wallets, also known as "online" or "custodial" wallets, are typically used for operational liquidity, facilitating quick deposits, withdrawals, and trading activities. Because they are internet-connected, they are more vulnerable to cyberattacks, hacking, and malware. Examples include exchange wallets, mobile wallets, and desktop wallets. Managing these requires stringent cybersecurity protocols. For insights into general cybersecurity expectations, see our article on [cybersecurity requirements for licensed virtual asset firms in Pakistan](/blog/cyber-security-requirements-for-licensed-virtual-asset-firms/).

Cold wallets, often called "offline" or "non-custodial" wallets, are designed for long-term storage of significant virtual asset reserves. They are disconnected from the internet, making them highly resistant to online threats. Hardware wallets, paper wallets, and deep cold storage solutions are common examples. The trade-off is reduced convenience for transactions, which typically require a manual process to bring assets online. The PVARA, in line with international best practices, expects firms to segregate client virtual assets effectively, a principle often best achieved through a combination of cold and hot storage. More details on this can be found in our guide to [virtual asset custody and segregating client crypto in Pakistan](/blog/custody-rules-how-client-virtual-assets-must-be-segregated/).

## Why do regulators focus on wallet policies?

Regulators focus on wallet policies primarily to protect client assets, prevent financial crime, and ensure the operational integrity and resilience of virtual asset service providers. Poor wallet management can lead to significant financial losses for customers and systemic risk.

The State Bank of Pakistan (SBP) and the Securities and Exchange Commission of Pakistan (SECP), working alongside PVARA, recognise that the security of virtual assets is paramount. The Financial Action Task Force (FATF) Recommendation 15 specifically addresses virtual assets and VASPs, highlighting the need for robust risk management. This includes measures to prevent misuse for money laundering and terrorist financing. Therefore, a firm's wallet policy is a cornerstone of its overall risk management framework and a key component of its licence application, as detailed in our guidance on [VASP licensing services](/vasp-licensing/).

## What are PVARA's expectations for hot wallet management?

PVARA expects hot wallets to be managed with robust cybersecurity controls, strict access protocols, and conservative limits on the amount of virtual assets held in them. These measures aim to minimise the risk of theft and unauthorised access.

Firms should implement a multi-layered security approach for hot wallets. This includes:

*   **Multi-Factor Authentication (MFA):** Mandatory for all access points, including internal systems.
*   **Regular Security Audits:** Independent penetration testing and vulnerability assessments are expected. Our article on [penetration testing expectations for exchanges](/blog/penetration-testing-expectations-for-exchanges/) provides further details.
*   **Access Controls:** Strict "least privilege" principles, ensuring only authorised personnel have access, and only to the specific functions required for their role.
*   **Encryption:** All data related to hot wallets, including private keys (if stored online, even temporarily), must be encrypted both in transit and at rest.
*   **Transaction Monitoring:** Real-time monitoring for suspicious activities and automated alerts. This ties into broader [crypto transaction monitoring in Pakistan](/blog/transaction-monitoring-for-crypto-setting-rules-and-thresholds/).
*   **Limits and Thresholds:** Clearly defined maximum amounts of virtual assets allowed in hot wallets at any given time, with automated alerts and procedures for exceeding these thresholds.
*   **Key Management:** Secure generation, storage, and rotation of private keys, often using Hardware Security Modules (HSMs). More on this is available in our analysis of [crypto key management and multi-signature governance in Pakistan](/blog/key-management-and-multi-signature-governance/).
*   **Incident Response Plan:** A clear plan for detecting, responding to, and recovering from security incidents, including reporting obligations to PVARA. Firms should understand [what VASPs must tell PVARA and when](/blog/incident-reporting-what-must-be-told-to-the-regulator-and-when/).

## What are PVARA's expectations for cold wallet management?

PVARA expects cold wallets to be managed with the highest level of physical and digital security, ensuring they remain offline and are protected against both cyber and physical threats. Access must be severely restricted and controlled by multi-signature schemes.

Key expectations for cold wallet management include:

*   **Physical Security:** Storage in secure, geographically dispersed vaults with restricted access, surveillance, and environmental controls.
*   **Air-Gapped Systems:** Ensuring that the systems used to generate and manage cold wallet keys are never connected to the internet.
*   **Multi-Signature (Multi-Sig) Requirements:** Implementing multi-signature schemes where multiple independent parties must authorise transactions, preventing a single point of failure. This is a critical aspect of [crypto key management and multi-signature governance in Pakistan](/blog/key-management-and-multi-signature-governance/).
*   **Segregation of Duties:** Separating the responsibilities for key generation, storage, and transaction authorisation among different individuals or teams to prevent collusion. Our article on [segregation of duties in a small compliance team](/blog/segregation-of-duties-in-a-small-compliance-team/) offers relevant guidance.
*   **Regular Audits and Reconciliation:** Periodic audits of cold storage procedures and reconciliation of cold wallet balances with internal records and client liabilities. This links to [client asset reconciliation: frequencies and methods for crypto operators](/blog/client-asset-reconciliation-frequency-and-method/).
*   **Disaster Recovery:** Robust plans for recovering cold wallet access in case of unforeseen events, such as natural disasters or loss of key personnel, without compromising security. This is part of broader [VASP business continuity planning](/blog/business-continuity-planning-for-vasps-what-the-regulator-wants-to-see/).
*   **Insurance:** Firms acting as custodians of client assets may be required to hold adequate insurance coverage for potential losses from theft or operational failures. Our analysis of [crypto custody insurance requirements for VASPs](/blog/insurance-requirements-for-custodians/) elaborates on this.

## How should firms manage the balance between hot and cold storage?

Firms must strike a careful balance between the accessibility of hot wallets and the security of cold wallets, typically by holding a minimal amount of assets in hot storage for operational needs and the vast majority in cold storage. This balance must be documented and justified.

PVARA will expect to see a clear policy outlining the firm's strategy for allocating assets between hot and cold storage. This policy should be risk-based, considering the firm's specific business model, transaction volumes, and the types of virtual assets handled. Generally, the principle is to keep only the absolute minimum required for immediate operational liquidity in hot wallets. Any excess should be moved to cold storage promptly.

This strategy requires:

1.  **Defined Thresholds:** Clear, quantifiable thresholds for when assets are moved between hot and cold storage. For example, if a hot wallet balance exceeds a certain amount, an automated or manual transfer to cold storage is triggered.
2.  **Automated Processes:** Where possible, automated systems for transferring assets from hot to cold storage to reduce human error and increase efficiency.
3.  **Regular Review:** Periodic review and adjustment of these thresholds and processes based on market conditions, business growth, and risk assessments.
4.  **Transparency:** Clear internal documentation of the rationale behind these decisions and the procedures in place.

## What are the key security and operational requirements?

Key security and operational requirements for wallet management include robust cyber defences, stringent access controls, comprehensive audit trails, and detailed business continuity and disaster recovery plans. These ensure asset safety and operational resilience.

Regulators require a holistic approach to security that goes beyond just the wallets themselves. It encompasses the entire operational environment.

*   **Cybersecurity Framework:** Implementation of an internationally recognised cybersecurity framework (e.g., NIST, ISO 27001) adapted to the virtual asset context.
*   **Access Management:** Granular access controls, multi-factor authentication, and regular review of user privileges for all systems interacting with wallets.
*   **Audit Trails:** Comprehensive logging of all wallet-related activities, including key generation, access attempts, transaction authorisations, and asset transfers. These logs must be immutable and regularly reviewed.
*   **Business Continuity Planning (BCP):** Detailed plans for how the firm will continue critical operations, including asset management, in the event of major disruptions. This includes recovery point objectives (RPOs) and recovery time objectives (RTOs). More information is available in our article on [VASP business continuity planning](/blog/business-continuity-planning-for-vasps-what-the-regulator-wants-to-see/).
*   **Disaster Recovery (DR):** Specific plans for restoring systems and data, including wallet access, after a catastrophic event.
*   **Personnel Vetting and Training:** Thorough background checks for all personnel involved in wallet operations and regular training on security protocols, incident response, and anti-money laundering (AML) obligations. Our guide on [AML training requirements for VASPs in Pakistan](/blog/training-obligations-for-staff-at-a-licensed-vasp/) is relevant here.
*   **Regular Audits:** Independent audits of security systems, wallet management procedures, and compliance with internal policies and regulatory requirements. This is distinct from the independent audit of the AML programme, which is also a requirement for licensed VASPs.

## How do these policies relate to client asset protection?

Wallet policies are fundamental to client asset protection by ensuring the secure segregation, storage, and accessibility of virtual assets, even in scenarios like insolvency or security breaches. They prevent commingling and facilitate orderly asset returns.

PVARA, in conjunction with the SECP, places a high emphasis on client asset protection. The framework aims to ensure that client virtual assets are clearly identifiable and recoverable. This is crucial for maintaining market integrity and consumer confidence.

*   **Segregation of Client Assets:** The wallet policy must clearly outline how client assets are segregated from the firm's own operational funds. This typically involves using distinct wallets or sub-accounts. Our article on [protecting client assets during VASP insolvency in Pakistan](/blog/client-asset-return-on-insolvency/) provides more context on this critical area.
*   **Proof of Reserves:** While not universally mandated, some regulators internationally are exploring "Proof of Reserves" requirements. This mechanism allows for independent verification that a firm holds the virtual assets it claims to hold on behalf of clients. While specific requirements are still under consultation in Pakistan, firms should understand the concept, as discussed in our piece on [Proof of Reserves for virtual asset exchanges in Pakistan](/blog/proof-of-reserves-what-it-is-and-whether-regulators-require-it/).
*   **Wind-Down Planning:** A robust wallet policy is an integral part of a firm's wind-down plan, detailing how client assets would be securely returned or transferred in the event of business failure. For more on this, refer to our article on [crypto wind-down plans in Pakistan](/blog/wind-down-planning-what-happens-if-the-business-fails/).
*   **Transparency to Clients:** Firms are expected to clearly communicate their asset protection measures to clients, fostering trust and demonstrating their commitment to security.

## What documentation and audit trails are required?

Firms must maintain comprehensive documentation of their wallet policies, procedures, and security controls, along with detailed, immutable audit trails of all related activities. This provides transparency, accountability, and evidence of compliance.

Regulators require a clear paper trail to assess a firm's adherence to its obligations. This includes:

*   **Policy Documents:** Formal, approved documents outlining the firm's hot and cold wallet policies, risk assessments, and internal controls.
*   **Procedure Manuals:** Detailed step-by-step guides for all operational aspects of wallet management, including key generation, storage, asset transfers, and incident response.
*   **Risk Assessments:** Regular assessments identifying, evaluating, and mitigating risks associated with wallet management, including cyber, operational, and financial crime risks.
*   **Audit Logs:** Records of all transactions, access attempts (successful and failed), system changes, and security events. These logs must be tamper-proof and retained for a specified period, in line with [VASP record keeping obligations in Pakistan](/blog/record-keeping-obligations-what-a-vasp-must-retain-and-for-how-long/).
*   **Reconciliation Records:** Documentation of all client asset reconciliations, demonstrating that client virtual assets held match recorded liabilities.
*   **Security Audit Reports:** Reports from independent security audits, penetration tests, and vulnerability assessments.
*   **Training Records:** Documentation of all staff training on wallet security and operational procedures.

The PVARA will scrutinise these documents during the [VASP licensing process](https://pvara.org/vasp-licensing/) and during ongoing supervision. Incomplete or inadequate documentation is a common reason for licence application delays or rejections, as highlighted in our analysis of [common reasons licence applications fail](/blog/common-reasons-licence-applications-fail/).

## About this analysis

This analysis was prepared by Sarzif Policy, an independent research desk, based on publicly available consultation papers, international regulatory guidance from bodies like FATF, and general principles of financial services regulation applicable to virtual assets. It is intended to provide general information and insights for crypto business operators. The regulatory framework for virtual assets in Pakistan is still under consultation and development. Specific requirements, thresholds, and deadlines must be verified directly with PVARA, the State Bank of Pakistan, the SECP, or other relevant authorities. This article does not constitute legal, financial, or regulatory advice. Firms should seek professional counsel tailored to their specific circumstances. For more information about our research and editorial standards, please review our [editorial policy](/editorial-policy/).