"""
terminology_definitions.py - Tag definitions from the Complaints Tags Terminology Guide.

These definitions help the LLM classifier understand when to apply each tag.
Updated with feedback from classification reviews.
"""

# Dictionary mapping each tag to its definition and criteria for when to use it
TAG_DEFINITIONS = {
    "account access & security": """
1. Member cannot access account, either due to failing verification, technical issues, account blocks, account closures, or other account access issues
2. Non-authorized members have access to an account
3. Account security is weak or proper steps not taken to secure or verify account
4. Issues arising due to joint account ownership
5. Issues arising to opening an account or linking accounts
6. Issues regarding accessing accounts post transfer of accounts to Sunward
NOTE: Card fraud/stolen cards do NOT qualify as account access issues - a stolen card does not provide access to the member's actual account.""",

    "agent behavior": """
1. Any member complaint that includes a lack of proper decorum from the agent (rudeness, unprofessional conduct, inappropriate comments)
CRITICAL RULES:
- ONLY use when the AGENT behaves improperly (agent was rude, agent hung up inappropriately, agent was unprofessional)
- If MEMBER is rude, abusive, or uses profanity, that is NOT agent behavior - the agent did nothing wrong
- If case mentions "member was using profanity" or "member said [insult]", do NOT tag agent behavior
- If agent hung up because MEMBER was abusive, that is NOT agent behavior (agent was right to disconnect)
- Look for clear agent misconduct, not member complaints about service quality""",

    "application": """
1. Any issue that arises during the APPLICATION PROCESS itself, including difficulty completing an application, undue burden placed on member during the application process, and/or incorrect information given during the application process
IMPORTANT: 
- "App" in case notes usually means MOBILE APP, not application process
- A loan being denied is NOT an application issue unless the application PROCESS itself was problematic
- Only use when there's an actual problem with HOW the application was submitted or processed""",

    "atm": """
1. Issues where ATM dispenses incorrect amount to the receiver
2. Member has issues with ATM limits
3. Concerns with ATM fees or no partner ATMs available
4. Issues with ATM deposits""",

    "auto loan": """
1. Auto loan has been denied or given unfavorable terms
2. Member has quality issues with an automobile that is financed through MACU
3. Member is having issues with payments on auto loans
4. Member has unexpected charges on his auto loan not related to the auto purchase""",

    "autopay": """
1. Autopay issues where autopay didn't pull correctly, had been turned off, or otherwise failed to go through
2. Autopay was improperly set up
3. Difficulty in setting up autopay
4. Autopay was not authorized
5. Autopay dates were changed""",

    "balance dispute": """
1. Member has concern that balance in their account is incorrect
2. Member is disputing the balance shown after a payment was made
NOTE: Use when member believes the BALANCE is wrong, not when a payment went to the wrong place (that's payment misapplied).""",

    "balance inquiry": """
1. Member is inquiring about any account balance available
2. Member is seeking clarification for transactions made on their account
3. Member is seeking to pay off a negative balance on an account
4. Member does not understand why balances don't match between app/online and statement
5. Member confused about balance discrepancies between different views of their account
NOTE: When member calls because balances shown on mobile app don't match statement, this is balance inquiry.""",

    "card block": """
1. Card stops working or payment is declined due to system blocks, freezes, authorization failures, or unknown reasons
2. Card is declined when used but there is NO physical defect with the card
NOTE: Use when the card itself is physically fine but won't work due to blocks or system issues. If the chip is malfunctioning or card is worn, use "card quality" instead.""",

    "card fraud": """
1. Issues being flagged as fraud, requiring a call in to resolve
2. Actual fraudulent transactions on the card, requiring member to call in to resolve
3. Fraudulent transaction disputes are declined
4. Any fraudulent charges appearing on credit/debit card
5. Member upset about potential fraudulent transactions posting to account
6. Disputes about fraud on card transactions
NOTE: Use this for ANY fraud involving credit/debit CARD transactions. If the fraud involves card transactions or pending card charges, use "card fraud", NOT "fraud - general".""",

    "card quality": """
1. Card quality is poor, chip malfunctions, swipe functionality is spotty (physical card defects)
2. Members are constantly requiring cards to be reissued or reprinted due to physical defects
3. Card that wears down and needs replacement
4. Chip not working, strip having issues
NOTE: Use when there are PHYSICAL defects with the card. If card is blocked/declined but NOT physically defective, use "card block".""",

    "certificate (CD)": """
1. Communication around withdrawal penalties or other fees regarding the closing or transfer of a CD is poor
2. CD auto renews without the member's knowledge or consent or without proper communication of auto renewal
3. Communication about rates, interest earned, or other concerning CDs is not good
IMPORTANT: Only use when the issue is WITH the CD itself. If member wants a CD-secured loan that gets denied, the issue is "loan denial", not CD.""",

    "check deposit": """
1. Check cannot be deposited or cashed due to check being printed improperly or not having all required information on it, typically the MICR Line
2. Check was cashed incorrectly, either incorrect amount, in the wrong account, or other
3. Check cannot be cashed or deposited due to technical issues, improper endorsement or failed identity verification
4. Check that has been sent is not deposited in a timely manner, inciting fears of the check being lost""",

    "check hold": """
1. Check holds happen frequently, regardless of amount, member longevity, or frequency of deposit
2. Member calls in to get a hold released that is based on the monetary amount of the check""",

    "check return": """
1. Funds from a deposited check were subsequently credited back against the account, due to insufficient funds, duplicate transactions, or other""",

    "communication issue": """
1. MACU fails to communicate or reply to a member's inquiry in a timely manner
2. Members have a difficult time contacting or otherwise being able to get a hold of MACU or their point of contact
3. Communication from MACU to the member omits or otherwise obfuscates important information
4. Communication to the member is confusing or conveys a different message to the member than intended
5. Member was NOT TOLD about something (loan terms, fees, account changes, etc.)
NOTE: Use when information was NOT communicated or was unclear. If WRONG information was given, use "misinformation given" instead.""",

    "loan consolidation": """
1. An issue arises during the loan consolidation process""",

    "credit check": """
1. Member has had a credit score drop due to multiple credit pulls
2. Credit was pulled without authorization
3. Credit was pulled based on a misrepresentation of the facts
4. Inquiry about negative credit reporting based on late payments
5. Member is calling to file a credit dispute
6. Accounts were closed involuntarily negatively affecting credit""",

    "delay": """
1. The lag between payoff amount provided and actual payment resulted in an additional balance being owed
2. The lag between a payment issuance and actual payment resulted in late fees being assessed""",

    "delivery": """
1. Financial product (card, check) was lost in delivery or never reached its intended destination
2. Delivery for financial product (card, check) was extremely slow
3. Improper delivery type (e.g. standard instead of expedited)""",

    "discrimination": """
1. Member makes a claim that racism, sexism, classism, or other -ism has occurred""",

    "documentation": """
1. An issue with documentation being different than what is required
2. An issue with documentation being completed or filled out improperly, leading to issues
3. A member has not received a required form, like tax form, that they are expecting
4. A member requests documentation from member services regarding their accounts""",

    "duplicate transaction": """
1. A transaction that has occurred twice or more than twice on a member's account""",

    "escalation request": """
1. Member fails to get a resolution to their problem through first line service and so request escalation
2. Member asks to speak to a supervisor/manager/lead
3. Call became an escalation call
4. Member was transferred to escalations/helpdesk
NOTE: Always include this tag when member explicitly asks to speak to a supervisor/manager or when call is transferred to escalations.""",

    "fee disclosure": """
1. Member has a question regarding fees that are linked to an account, not understanding why they were charged or their origin
2. Member feels that the payment of fees was not properly communicated to them
3. Member is upset that fees are being charged that had never been charged for similar or the same transaction in the past
4. Member inquiring about what a fee is for
5. Member wants to understand account fees or charges
6. Member wants better returns/dividends (fee/interest related)""",

    "fraud - general": """
1. A catch-all for fraud complaints OUTSIDE of credit card fraud, including identity theft, account takeover, check fraud, wire fraud, etc.
IMPORTANT: If the fraud involves CARD transactions (credit/debit card charges, pending card transactions), use "card fraud" instead. Only use "fraud - general" for non-card fraud like identity theft, check fraud, wire fraud, account takeover without card involvement.""",

    "HELOC": """
1. Issues with a HELOC payments being in arrears
2. Issues with members having issues with the HELOC application process
3. Issues with making payments or understanding how payments post with a HELOC""",

    "identity verification": """
1. Member's identity or business identity information is incorrectly entered, causing verification issues
2. At the heart of the issue is the member's failure to verify at the T1 or T2 level
3. Member has a different name or additional name as to the one on the account
4. Member frustrated that they cannot verify their identity through available methods
NOTE: Focus on the PRIMARY complaint. If member called to make a payment but couldn't verify, the issue is identity verification.""",

    "insurance": """
1. Member is being denied for insurance that was purchased as part of a loan, either auto, ISTL, or other insurance protection
2. Member was opted into insurance unknowingly or applied for insurance coverage due to poor communication
3. GAP insurance claim issues""",

    "interest dispute": """
1. Member has a dispute as to interest balances accrued that must be paid
2. Member makes payment to payoff loan then finds out there is a remaining balance due to accrued interest that was not properly disclosed or communicated
3. Member has a dispute with the interest rate they were given relative to expectations
4. Member wants MACU to pay interest charges that accrued due to MACU error/delay
5. Member upset about interest charges on credit card or loan
NOTE: Use when interest charges are a core part of the complaint.""",

    "issuance": """
1. Member or someone linked to member is issued a credit card they are not supposed to have
2. Credit card is issued to the wrong account or wrong person
3. Member has a problem with being issued a credit card in some way
4. Member had checks printed or issued on their account incorrectly, e.g. wrong account, wrong name, or other printing issues such as missing information so that checks cannot be processed
5. Card was ordered to the wrong share/account causing issues
IMPORTANT: Only use when there's a problem with HOW the card/check was issued. If a new card is printed as a resolution to another problem, that is NOT an issuance issue.""",

    "interactive voice response (IVR)": """
1. IVR is not functioning correctly
2. Interactions/IVR system misunderstood what member said, causing errors
3. Phone system issues when member calls in""",

    "loan denial": """
1. Loan is denied, even though previous applications had been approved
2. Loan is denied after member was led to believe that it would be approved
3. Loan is denied, but certain actions such as a hard credit pull took place during the process, negatively affecting the member
4. Loan process or steps being taken are not properly identified or explained so loan denial is disruptive or more detrimental than anticipated
5. Loan is denied and member is upset due to previous history or longevity with MACU
6. Reasons for loan denial are not clearly explained to member
7. Loan product is not offered/available (e.g., CD-secured loans no longer offered)
NOTE: Use for loan denials regardless of whether the application process had issues. If the application PROCESS was problematic, also add "application".""",

    "loan payment": """
1. Member has an issue with a loan payoff: Cashier's check issues, wrong account numbers, etc.
2. General issues making loan payments
NOTE: Focus on WHY the member called. If they called about interest dispute but mentioned making a payment, the main issue is interest dispute, not loan payment.""",

    "loan payoff": """
1. Member has an issue with a loan payoff: Cashier's check issues, wrong account numbers, getting payoff amount, etc.""",

    "wait time": """
1. Member gets passed around from department to department, leaving them on the phone or in branch for long periods of time
2. Member waits for a call back that for days or even weeks before finally being contacted
3. Mailed checks or documents take an inordinate amount of time to reach the member
4. Member is waiting for a check or deposit to clear
5. Member has been on the phone for hours trying to resolve an issue
6. Process is taking an inordinate amount of time (e.g., title release, insurance settlement)
7. Member had to speak to multiple agents to resolve an issue
NOTE: Use when time spent waiting/on phone is a significant part of the complaint.""",

    "misinformation given": """
1. A MACU representative provides incorrect/WRONG information to a member, upon which the member then acts
IMPORTANT: Only use when agent gave WRONG information. If information was simply not communicated, use "communication issue" instead.""",

    "missed payment": """
1. Payment was missed and member wants to know if MACU can work with them in some way
2. Payment was missed due to slow processing times on MACU's end
3. Payment missed due to other reasons, such as UX or inability to access account""",

    "mobile deposit": """
1. Issues with mobile deposits that range from deposit holds, technical issues, missing funds, and more
2. Issues with deposit limits through the mobile banking app""",

    "mortgage": """
1. Member having difficulty making a mortgage payment for non MACU reasons
2. Member having a difficulty making a mortgage payment for MACU reasons""",

    "overdraft fee": """
1. Member gets hit with overdraft fees, prompting a call in or visit and causing a complaint ticket to be generated
2. Overdraft protection was improperly set up or set up without member's consent
3. ODP (overdraft protection) started unexpectedly after being suspended
IMPORTANT: If member is calling to request a refund of previous fees due to financial hardship (not specifically complaining about overdraft fees), use "refund" tag instead.""",

    "payment misapplied": """
1. Payment is deposited into or made to the wrong account or withdrawn from the wrong account
2. Payment is made on the wrong financial product, either through MACU or Member error
IMPORTANT: 
- Only use for actual PAYMENTS going to wrong place
- Transfers are NOT payments (use "transfers" tag)
- Balance showing incorrectly is NOT payment misapplied (use "balance dispute")""",

    "processing error": """
1. A transaction was processed incorrectly BY A HUMAN AGENT
2. Member receives a notice or other communication from MACU in error about an issue that does not exist on their account or meant for another Member
3. Changes are made to an account where the requestor for the change is unknown or where it originated from
4. Documents processed with incorrect information
IMPORTANT: 
- Only use when a HUMAN AGENT processed something incorrectly
- ATM errors are NOT processing errors (use "atm")
- IVR/phone system errors are NOT processing errors (use "interactive voice response (IVR)")
- System working as designed is NOT processing error
- Don't use if we don't know whether an error occurred""",

    "refinance": """
1. Member initiates a request to refinance a loan
2. Issues arise in the processing of refinancing a loan or loans""",

    "refund": """
1. Member wants a fee refunded due to a MACU error
2. Member wants a fee refunded due to their error
3. Member requesting money back for fees charged
4. Member asking for help with fees due to financial hardship/difficult situation
5. Member requesting fees be waived or reversed
NOTE: Use this when member is requesting refund/help with fees, even if overdraft fees are involved - focus on the refund request itself.""",

    "rewards": """
1. Member upset with changes in rewards offered""",

    "skip payment": """
1. The member wants to initiate a skip payment
2. The member is not able to use a skip payment for some reason
3. The member is confused about how a skip pay works or has concerns about the results of their skip payment
4. Payment still initializes even after a skip payment is requested or activated""",

    "stop payment": """
1. Member calls in because of an issue that arises with a stop payment request or to initiate a stop payment request""",

    "technical issue": """
1. Member has technical issues with online banking or the mobile app
2. Member does not receive proper notifications when using the online system
3. MACU has internal technical issues that affect the member in some way
4. Member is generally unhappy with the way technology at MACU works or is configured. They find it confusing or difficult to use
IMPORTANT:
- System working as designed is NOT a technical issue
- Loan product not offered is NOT a technical issue
- IVR issues should use "interactive voice response (IVR)" instead
- "App" in case notes usually means mobile APP (potential technical issue), not application process""",

    "titles": """
1. Issue where a title cannot be released or has not been released
2. Member is having trouble gaining access to a title
3. Title has incorrect information (wrong VIN, etc.)""",

    "transaction dispute": """
1. Member calls in to dispute a transaction, either a credit card payment, a wire transfer/bill pay, account offsets, or other transactions
2. Member disputing an offset payment that was made from their account
3. Member disputes any transaction that occurred on their account
NOTE: Use when member is DISPUTING a transaction. Account offsets per loan agreement terms are disputable transactions.""",

    "transfers": """
1. Transfer issues, including transfers from visa debit/credit cards, ODP, or other issues
2. Member not able to make transfers
3. Transfers are not showing up in a timely manner
4. Transfers happening when not requested or money disappearing without the member knowing where it went
5. Member calls in having issues with transfer limits
NOTE: Transfers are different from payments. If money was transferred to wrong account, use this tag, NOT "payment misapplied".""",

    "unauthorized action": """
1. Any disputed transaction where the member claims that MACU took unilateral action on doing something that was not approved or requested by the member
2. Account converted without member's knowledge or consent (e.g., share type changed)
3. Account changes made without proper notification or authorization
IMPORTANT: Actions permitted by loan agreement terms (like account offsets for past due loans) are NOT unauthorized, even if member is upset about them. BUT account conversions/changes without notification ARE unauthorized.""",

    "unresolved complaint": """
1. A complaint has been pending resolution for long periods of time, spanning days or weeks without resolution requiring multiple call ins and interactions
2. Member has called in multiple times without getting resolution
3. Member had to call back because previous agent didn't resolve the issue
NOTE: Use when the complaint has history of not being resolved, requiring multiple interactions.""",

    "wire issue": """
1. Members having issues with wire transfers
2. Members having bill pay issues that directly relate to the transfer or payment of funds""",

    "withdrawal": """
1. Member has issues while making a withdrawal or depositing a check to cash
IMPORTANT: Only use when a withdrawal ACTUALLY OCCURRED and there was an issue. Wanting to withdraw but not doing it is NOT a withdrawal issue.""",

    "zelle": """
1. Member having issues with Zelle transactions
2. Member not eligible for or have issues being denied Zelle increases""",
}


def get_tag_definitions_prompt(allowed_tags: list) -> str:
    """
    Build a formatted string of tag definitions for use in the classifier prompt.
    
    Args:
        allowed_tags: List of allowed tag names (should match keys in TAG_DEFINITIONS)
    
    Returns:
        Formatted string with tag names and their definitions
    """
    lines = []
    for tag in allowed_tags:
        tag_lower = tag.lower()
        if tag_lower in TAG_DEFINITIONS:
            definition = TAG_DEFINITIONS[tag_lower].strip()
            lines.append(f"### {tag}\n{definition}")
        else:
            # Tag not found in definitions - just include the name
            lines.append(f"### {tag}\n(No specific definition available)")
    
    return "\n\n".join(lines)


def get_confusion_guidance() -> str:
    """
    Return guidance for commonly confused tags based on classification feedback.
    """
    return """
## CRITICAL CLASSIFICATION RULES - Read carefully before classifying:

### Focus on PRIMARY Complaint
- Tag based on WHY the member called, not everything mentioned in the case
- If member called to pay a loan but couldn't verify identity, the issue is "identity verification", not "loan payment"
- If member mentions escalation while complaining about fees, tag the fee issue as primary

### Card Block vs Card Quality
- "card block": Card is DECLINED or won't work, but card is PHYSICALLY FINE (system blocks, authorization issues)
- "card quality": Card has PHYSICAL DEFECTS (chip not working, worn out, strip issues, needs replacement due to wear)
- Key question: Is the problem with the physical card itself, or with the system/authorization?

### Card Fraud vs Fraud - General vs Account Access & Security
- "card fraud": ANY fraud involving credit/debit CARD transactions (fraudulent charges, pending fraud transactions on card)
- "fraud - general": ONLY for NON-card fraud (identity theft, account takeover, check fraud, wire fraud)
- If case mentions "fraud transactions" on card or "pending transactions that are fraud" → use "card fraud"
- "account access & security": Issues accessing the ACCOUNT itself - NOT card fraud (stolen card doesn't give account access)

### Application vs Mobile App ("app")
- "application": Problems with loan/account APPLICATION PROCESS
- When case mentions "app", it usually means MOBILE APP, not application
- Balance discrepancies on the "app" = "balance inquiry", NOT "application"
- Technical problems with the "app" = "technical issue", NOT "application"

### Misinformation Given vs Communication Issue
- "misinformation given": Agent gave WRONG/INCORRECT information
- "communication issue": Information was NOT TOLD or unclear (omitted, not communicated)
- "Not told about loan terms" = communication issue
- "Told payment was X but it was Y" = misinformation given

### Processing Error - Use Sparingly
- ONLY use when a HUMAN AGENT made an error in processing
- ATM errors = "atm", NOT processing error
- IVR errors = "interactive voice response (IVR)", NOT processing error  
- System working as designed = NOT processing error
- If uncertain whether error occurred, do NOT use processing error

### Payment Misapplied vs Transfers vs Balance Dispute
- "payment misapplied": A PAYMENT went to the wrong account
- "transfers": A TRANSFER issue (not a payment)
- "balance dispute": Member thinks BALANCE is wrong (not that payment went to wrong place)

### Agent Behavior - BE VERY CAREFUL
- ONLY use when the AGENT clearly behaved improperly (agent was rude to member, agent made inappropriate comments)
- If MEMBER was abusive/rude/used profanity, that is NOT agent behavior - the agent did nothing wrong
- If agent hung up because member was using profanity, that is NOT agent behavior (agent was justified)
- "member said my voice was annoying" = NOT agent behavior (member being rude)
- "agents dropped the ball" or "agents couldn't help" = NOT agent behavior unless agent was actually rude
- When in doubt, do NOT tag agent behavior

### Overdraft Fee vs Refund
- "overdraft fee": Member is complaining about getting hit with overdraft fees specifically
- "refund": Member is requesting a refund/help with fees due to financial hardship
- If member is asking for help due to tough financial situation, use "refund" NOT "overdraft fee"

### Wait Time and Unresolved Complaint
- "wait time": Use when member spent hours on phone, passed around departments, or process taking too long
- "unresolved complaint": Use when member had to call back multiple times because previous agents didn't resolve it
- These often appear together when member has had ongoing issues

### Issuance
- Only for problems with HOW card/check was issued
- New card printed as resolution = NOT issuance issue
- Card ordered to wrong share = IS issuance issue

### Transaction Dispute vs Unauthorized Action
- "transaction dispute": Member disputes ANY transaction (including account offsets)
- "unauthorized action": MACU took action NOT permitted by agreements
- Offset payments per loan terms = disputable transaction, NOT unauthorized (MACU has the right per agreement)

### Unresolved Complaint
- Only when complaint pending for EXTENDED TIME (days/weeks)
- If the specific complaint is clear, tag that issue instead

### Withdrawal
- Only when withdrawal ACTUALLY OCCURRED with issues
- Wanting to withdraw but not doing it = NOT withdrawal issue

### Certificate (CD)
- Only when issue is WITH the CD itself
- CD-secured loan denied = "loan denial", NOT CD issue
"""


if __name__ == "__main__":
    # Quick test
    test_tags = ["card block", "card fraud", "card quality", "fraud - general"]
    print("Testing tag definitions:")
    print(get_tag_definitions_prompt(test_tags))
    print("\n" + "=" * 60)
    print("Confusion guidance:")
    print(get_confusion_guidance())
