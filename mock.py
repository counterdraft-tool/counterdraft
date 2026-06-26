# -*- coding: utf-8 -*-
"""Bundled sample output for dry-run / demo (no API key needed)."""

MOCK_AUDIT = {
    "contract_label": "Vendor / Master Services Agreement",
    "overall_risk": "high",
    "summary": "Drafted heavily in the vendor's favor. Four clauses transfer "
               "almost all risk and cost onto the client. All are negotiable.",
    "counts": {"critical": 3, "caution": 4, "minor": 0},
    "issues": [
        {"clause_ref": "Section 9.2", "title": "Unlimited / one-sided liability",
         "severity": "critical",
         "quote": "Client shall indemnify and hold Vendor harmless from any and all claims... without limitation.",
         "why_it_matters": "Uncapped exposure could exceed your annual revenue, while the vendor caps its own liability at fees paid.",
         "demand": "Mutual liability cap at 12 months of fees; carve-outs only for gross negligence and willful misconduct."},
        {"clause_ref": "Section 3.1", "title": "Auto-renewal with 90-day opt-out",
         "severity": "critical",
         "quote": "This Agreement renews automatically for successive 12-month terms unless terminated 90 days prior to renewal.",
         "why_it_matters": "Miss the narrow window and you are locked in for another full year.",
         "demand": "30-day notice; renewal reminder 60 days out; or month-to-month after the initial term."},
        {"clause_ref": "Section 7.4", "title": "Vendor owns deliverables and your data",
         "severity": "critical",
         "quote": "All deliverables, materials, and data processed hereunder shall remain the exclusive property of Vendor.",
         "why_it_matters": "You could lose ownership of work you paid for and access to your own data on exit.",
         "demand": "Client owns deliverables and data upon payment; vendor gets a limited license; guaranteed data export on termination."},
        {"clause_ref": "Section 4.3", "title": "Unilateral price increases",
         "severity": "caution",
         "quote": "Vendor may increase fees upon 30 days' notice.",
         "why_it_matters": "Your costs can rise at the vendor's discretion.",
         "demand": "Cap annual increases at the lesser of 5% or CPI; none during the initial term."},
        {"clause_ref": "Section 11.1", "title": "One-sided termination for convenience",
         "severity": "caution",
         "quote": "Vendor may terminate this Agreement for convenience upon thirty (30) days' notice.",
         "why_it_matters": "The vendor can exit but you cannot, and may forfeit prepaid fees.",
         "demand": "Make termination-for-convenience mutual with pro-rata refund of prepaid fees."},
        {"clause_ref": "missing", "title": "No service-level guarantees",
         "severity": "caution", "quote": "",
         "why_it_matters": "No uptime, response time, or remedies are defined, so you have no recourse for poor service.",
         "demand": "Add an SLA with measurable targets and service credits for misses."},
        {"clause_ref": "Section 14.2", "title": "Governing law in vendor's home state",
         "severity": "caution",
         "quote": "This Agreement shall be governed by the laws of the State of Delaware, and disputes resolved in its courts.",
         "why_it_matters": "Raises your cost to enforce or defend a dispute.",
         "demand": "Use your state, or neutral arbitration."},
    ],
}

MOCK_LETTER = """Subject: [Your Business] - proposed revisions to the Master Services Agreement

Hi [Counterparty contact],

Thanks for sending the MSA - we're excited to move forward. Before signing, we need a few standard revisions to balance the terms:

1. Liability (Sec. 9.2-9.3): make liability mutual and cap both parties at 12 months of fees paid, carve-outs limited to gross negligence and willful misconduct.
2. Renewal (Sec. 3.1): reduce the opt-out notice from 90 to 30 days and add a 60-day pre-renewal reminder.
3. Ownership (Sec. 7.4): deliverables and our data should be our property upon payment, with a limited license to you and a guaranteed data export on termination.
4. Fees (Sec. 4.3): cap annual increases at the lesser of 5% or CPI, with no increase during the initial term.
5. Termination (Sec. 11.1): make termination-for-convenience mutual, with a pro-rata refund of prepaid fees.
6. Governing law (Sec. 14.2): change venue to [Your state], or neutral arbitration.

Happy to hop on a quick call to finalize. Looking forward to working together.

Best,
[Your name]"""


MOCK_AUDIT_UA = {
    "contract_label": "Договір про надання послуг",
    "overall_risk": "high",
    "summary": "Договір складено на користь виконавця. Кілька умов перекладають "
               "ризик і витрати на клієнта. Усі вони підлягають перегляду.",
    "counts": {"critical": 3, "caution": 2, "minor": 0},
    "issues": [
        {"clause_ref": "п. 5.2", "title": "Асиметрична пеня", "severity": "critical",
         "quote": "За прострочення оплати Замовник сплачує пеню 1% за кожен день прострочення.",
         "why_it_matters": "Пеня 1%/день значно перевищує подвійну облікову ставку НБУ і встановлена лише проти клієнта.",
         "demand": "Обмежити пеню подвійною обліковою ставкою НБУ та зробити санкції взаємними (ст. 549, 551 ЦКУ; ЗУ № 543/96-ВР)."},
        {"clause_ref": "п. 8.1", "title": "Одностороння зміна ціни виконавцем", "severity": "critical",
         "quote": "Виконавець має право в односторонньому порядку змінювати вартість послуг.",
         "why_it_matters": "Узгоджена ціна може зрости без твоєї згоди протягом дії договору.",
         "demand": "Зміна ціни - лише за взаємною письмовою згодою (ст. 525, 651 ЦКУ)."},
        {"clause_ref": "відсутнє", "title": "Немає порядку приймання послуг", "severity": "critical",
         "quote": "",
         "why_it_matters": "Без акта і критеріїв приймання важко довести належне виконання й оскаржити оплату.",
         "demand": "Додати акт наданих послуг, критерії якості та строк для вмотивованих заперечень."},
        {"clause_ref": "п. 9.3", "title": "Виключення відповідальності виконавця", "severity": "caution",
         "quote": "Виконавець не несе відповідальності за будь-які збитки Замовника.",
         "why_it_matters": "Усю відповідальність перекладено на клієнта.",
         "demand": "Зробити відповідальність взаємною; зберегти відповідальність за умисел і грубу необережність."},
        {"clause_ref": "п. 11.2", "title": "Підсудність за місцем виконавця", "severity": "caution",
         "quote": "Усі спори розглядаються за місцезнаходженням Виконавця.",
         "why_it_matters": "Зростають твої витрати на участь у спорі.",
         "demand": "Підсудність за місцем клієнта або нейтральний форум."},
    ],
}

MOCK_LETTER_UA = """Тема: [Ваша компанія] - пропозиції щодо правок до Договору про надання послуг

Доброго дня, [Контакт контрагента]! Дякуємо за надісланий проєкт - ми налаштовані на співпрацю. Перед підписанням просимо внести кілька стандартних правок для балансу умов:

1. Пеня (п. 5.2): обмежити пеню подвійною обліковою ставкою НБУ і зробити санкції взаємними.
2. Ціна (п. 8.1): зміна вартості - лише за взаємною письмовою згодою, без односторонньої зміни в межах строку.
3. Приймання (новий пункт): додати акт наданих послуг, критерії якості та строк для вмотивованих заперечень.
4. Відповідальність (п. 9.3): зробити відповідальність взаємною, зберігши відповідальність за умисел і грубу необережність.
5. Підсудність (п. 11.2): розгляд спорів за місцем [Ваша компанія] або в нейтральному форумі.

Будемо раді коротко обговорити це телефоном і фіналізувати. З повагою, [Ваше імʼя]."""
