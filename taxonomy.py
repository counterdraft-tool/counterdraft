"""
Counterdraft risk taxonomy — US business / commercial contract law.

This is the legal "moat": expert checklists of dangerous clauses per contract
type, written from the perspective of the CLIENT (the party RECEIVING the draft).
The taxonomy is injected into the audit prompt so the model checks against a
real attorney's playbook instead of generic web knowledge.

Each item:
  id        - stable key
  title     - short label
  severity  - default severity if found unbalanced (critical | caution)
  check     - what to look for
  why       - plain-English business impact (for non-lawyers)
  demand    - the standard negotiating ask
"""

CONTRACT_TYPES = {
    "vendor_msa": "Vendor / Master Services Agreement",
    "commercial_lease": "Commercial Lease",
    "nda": "NDA / Confidentiality Agreement",
    "contractor_employment": "Independent Contractor / Employment Agreement",
}

# ---- Cross-cutting checks applied to every contract type ----
COMMON = [
    {
        "id": "liability_uncapped",
        "title": "Uncapped or one-sided liability / indemnity",
        "severity": "critical",
        "check": "Indemnification or liability that is unlimited, or where only the client indemnifies, or where the counterparty caps its liability but the client's is open-ended.",
        "why": "Uncapped exposure can exceed your annual revenue from a single dispute. One-sided indemnity shifts all risk onto you.",
        "demand": "Make liability mutual; cap both parties at 12 months of fees paid; carve-outs limited to gross negligence and willful misconduct.",
    },
    {
        "id": "auto_renewal",
        "title": "Auto-renewal with long opt-out window",
        "severity": "critical",
        "check": "Automatic renewal where the notice-to-cancel window is long (e.g., 60-90 days) or buried.",
        "why": "Miss the narrow window and you are locked in for another full term. The most common SMB trap.",
        "demand": "Reduce opt-out notice to 30 days; require a renewal reminder 60 days out; or switch to month-to-month after the initial term.",
    },
    {
        "id": "termination_asymmetry",
        "title": "One-sided termination rights",
        "severity": "caution",
        "check": "Counterparty may terminate for convenience but the client may not, or unequal cure periods.",
        "why": "You can be dropped on short notice with no equivalent exit, and may forfeit prepaid amounts.",
        "demand": "Mutual termination-for-convenience with equal notice and pro-rata refund of prepaid fees.",
    },
    {
        "id": "governing_law_venue",
        "title": "Governing law / venue in counterparty's home state",
        "severity": "caution",
        "check": "Disputes governed by and litigated in the counterparty's state, far from the client.",
        "why": "Raises your cost to enforce or defend; home-court advantage to them.",
        "demand": "Use the client's state, a neutral state, or neutral arbitration (e.g., AAA) with a convenient seat.",
    },
    {
        "id": "unilateral_amendment",
        "title": "Unilateral changes to terms / fees",
        "severity": "caution",
        "check": "Counterparty can change terms, fees, or policies on notice without client consent.",
        "why": "The deal you signed can change under you at any time.",
        "demand": "Changes require mutual written consent; cap fee increases at the lesser of 5% or CPI; none during the initial term.",
    },
    {
        "id": "assignment",
        "title": "One-sided assignment rights",
        "severity": "caution",
        "check": "Counterparty may assign the contract (e.g., on acquisition) but the client may not, with no consent right.",
        "why": "You could end up bound to a competitor or unknown third party.",
        "demand": "Assignment requires the other party's consent (not unreasonably withheld); allow assignment in a bona fide M&A by either side.",
    },
]

# ---- Type-specific checks ----
BY_TYPE = {
    "vendor_msa": [
        {
            "id": "ip_ownership",
            "title": "Vendor retains ownership of deliverables / client data",
            "severity": "critical",
            "check": "Work product, deliverables, or client data declared the property of the vendor.",
            "why": "You could lose ownership of work you paid for and access to your own data on exit.",
            "demand": "Client owns deliverables and data upon payment; vendor gets a limited license to perform; guaranteed data export on termination.",
        },
        {
            "id": "no_sla",
            "title": "No service levels / remedies",
            "severity": "caution",
            "check": "No uptime, response-time, or performance commitments and no remedies/credits.",
            "why": "You have no recourse when the service underperforms.",
            "demand": "Add an SLA with measurable targets and service credits for misses.",
        },
        {
            "id": "payment_terms",
            "title": "Aggressive payment / late fees",
            "severity": "caution",
            "check": "Short payment windows, high interest on late payment, or fees due regardless of performance.",
            "why": "Cash-flow risk and penalties even when delivery is poor.",
            "demand": "Net-30, reasonable late interest, right to withhold disputed amounts in good faith.",
        },
        {
            "id": "warranty_disclaimer",
            "title": "Full warranty disclaimer ('as is')",
            "severity": "caution",
            "check": "Vendor disclaims all warranties; services provided 'as is'.",
            "why": "No guarantee the service even does what was promised.",
            "demand": "Add a basic warranty that services conform to the documentation/SOW and applicable law.",
        },
    ],
    "commercial_lease": [
        {
            "id": "personal_guarantee",
            "title": "Personal guarantee",
            "severity": "critical",
            "check": "Owner personally guarantees the lease obligations.",
            "why": "Your personal assets (home, savings) are on the hook if the business fails.",
            "demand": "Remove the personal guarantee; if unavoidable, cap it (e.g., 'good-guy' guarantee limited to amounts due until surrender).",
        },
        {
            "id": "rent_escalation",
            "title": "Uncapped rent escalation / CAM charges",
            "severity": "critical",
            "check": "Annual increases without a cap, or open-ended common-area maintenance (CAM)/operating-expense pass-throughs.",
            "why": "Costs can balloon unpredictably and dwarf the base rent.",
            "demand": "Cap annual increases (e.g., 3%); cap controllable CAM growth; right to audit CAM statements.",
        },
        {
            "id": "repair_obligations",
            "title": "Tenant responsible for structural / HVAC repairs",
            "severity": "caution",
            "check": "Tenant carries roof, structure, or major HVAC repair/replacement obligations.",
            "why": "A single major repair can cost tens of thousands.",
            "demand": "Landlord responsible for structure, roof, and HVAC replacement; tenant only for routine maintenance.",
        },
        {
            "id": "assignment_sublease",
            "title": "No right to assign / sublease",
            "severity": "caution",
            "check": "Absolute prohibition on assignment or subletting.",
            "why": "You cannot exit or downsize if circumstances change.",
            "demand": "Allow assignment/sublease with landlord consent not to be unreasonably withheld.",
        },
        {
            "id": "exclusive_use",
            "title": "Missing exclusive-use / co-tenancy protection",
            "severity": "caution",
            "check": "No exclusive-use clause (retail) or co-tenancy protection.",
            "why": "Landlord could lease next door to a direct competitor.",
            "demand": "Add exclusive-use for your category; co-tenancy remedy if anchor tenants leave.",
        },
    ],
    "nda": [
        {
            "id": "one_way_vs_mutual",
            "title": "One-way NDA where it should be mutual",
            "severity": "caution",
            "check": "Only the client is bound to confidentiality while the counterparty is not.",
            "why": "You protect them but share your own information unprotected.",
            "demand": "Make the NDA mutual if both sides exchange confidential information.",
        },
        {
            "id": "overbroad_definition",
            "title": "Over-broad definition of 'Confidential Information'",
            "severity": "caution",
            "check": "Definition covers everything, including publicly available or independently developed info, with no standard exclusions.",
            "why": "You could be in breach for using knowledge you already had or that is public.",
            "demand": "Add standard carve-outs: public, already known, independently developed, lawfully received, required by law.",
        },
        {
            "id": "perpetual_term",
            "title": "Perpetual or excessive duration",
            "severity": "caution",
            "check": "Confidentiality obligations last forever or for an unreasonably long time.",
            "why": "Indefinite obligations are hard to manage and risky long-term.",
            "demand": "Limit to 2-5 years (longer only for trade secrets, which can remain protected while secret).",
        },
        {
            "id": "non_solicit_noncompete",
            "title": "Hidden non-compete / non-solicit",
            "severity": "critical",
            "check": "NDA smuggles in non-compete or employee/customer non-solicit clauses.",
            "why": "Restricts your business well beyond confidentiality; may be unenforceable but chilling.",
            "demand": "Remove non-compete/non-solicit from the NDA; negotiate separately and narrowly if at all.",
        },
        {
            "id": "ip_in_nda",
            "title": "IP assignment buried in NDA",
            "severity": "critical",
            "check": "NDA assigns ownership of ideas/feedback/IP disclosed during discussions.",
            "why": "You could hand over rights to your own concepts just by talking.",
            "demand": "Strike IP assignment; each party retains its own IP; no license granted by disclosure.",
        },
    ],
    "contractor_employment": [
        {
            "id": "ip_assignment_scope",
            "title": "Over-broad IP assignment",
            "severity": "critical",
            "check": "Assigns all inventions, including those created on own time and unrelated to the work.",
            "why": "You could lose rights to side projects and pre-existing work.",
            "demand": "Limit assignment to work product created for this engagement; carve out prior inventions and unrelated personal projects (per state law, e.g., CA Labor Code 2870).",
        },
        {
            "id": "non_compete",
            "title": "Non-compete restriction",
            "severity": "critical",
            "check": "Post-engagement non-compete limiting future work.",
            "why": "Can block your livelihood; many states limit or ban these (e.g., California void; FTC scrutiny).",
            "demand": "Remove the non-compete; if any restriction, narrow to true trade-secret protection and confirm enforceability in the governing state.",
        },
        {
            "id": "misclassification",
            "title": "Misclassification risk (contractor vs employee)",
            "severity": "caution",
            "check": "Labeled 'independent contractor' but terms impose employee-like control, exclusivity, set hours.",
            "why": "Misclassification creates tax and legal liability and can void protections.",
            "demand": "Align terms with genuine contractor status (control over how/when), or convert to proper employment with benefits.",
        },
        {
            "id": "termination_pay",
            "title": "Termination without notice / unpaid work",
            "severity": "caution",
            "check": "Either side can terminate instantly; no payment for work in progress; forfeiture of earned fees.",
            "why": "You could do work and not get paid.",
            "demand": "Reasonable notice; payment for all work performed and approved through termination.",
        },
        {
            "id": "non_solicit",
            "title": "Broad non-solicitation",
            "severity": "caution",
            "check": "Bars soliciting any clients/employees for a long period.",
            "why": "Limits your future business relationships broadly.",
            "demand": "Narrow to clients/employees you actually worked with; limit to 12 months.",
        },
    ],
}


# ---------------------------------------------------------------------------
# Jurisdiction registry (US + Ukraine)
# ---------------------------------------------------------------------------
from taxonomy_ua import CONTRACT_TYPES_UA, COMMON_UA, BY_TYPE_UA

JURISDICTIONS = {"us": "United States", "ua": "Ukraine (ЦКУ)"}

_REGISTRY = {
    "us": {"types": CONTRACT_TYPES, "common": COMMON, "by_type": BY_TYPE},
    "ua": {"types": CONTRACT_TYPES_UA, "common": COMMON_UA, "by_type": BY_TYPE_UA},
}


def contract_types(jurisdiction: str = "us") -> dict:
    return _REGISTRY[jurisdiction]["types"]



def all_contract_types() -> dict:
    out = {}
    for j in _REGISTRY.values():
        out.update(j["types"])
    return out


def taxonomy_for(contract_type: str, jurisdiction: str = "us"):
    reg = _REGISTRY.get(jurisdiction, _REGISTRY["us"])
    items = list(reg["common"])
    items += reg["by_type"].get(contract_type, [])
    return items


def taxonomy_as_prompt(contract_type: str, jurisdiction: str = "us") -> str:
    items = taxonomy_for(contract_type, jurisdiction)
    lines = []
    for it in items:
        lines.append(
            "- [%s] %s: %s (Impact: %s | Standard ask: %s)" % (
                it["severity"].upper(), it["title"], it["check"],
                it["why"], it["demand"])
        )
    return "\n".join(lines)
