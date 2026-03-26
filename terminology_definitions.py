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
7. Member cannot access online portal due to moving/relocation (geographic restrictions)
8. Member no longer a resident in original state and cannot use state-specific portal
9. Unauthorized access to an account — someone not on the account gained access
10. Card issued on the wrong account, sending account information to the wrong member, or providing account information to someone not authorized
11. Any instance where unauthorized access to an account occurs in any form
KEYWORDS TO WATCH FOR: "unauthorized access", "someone accessed", "wrong member", "account information sent to", "not on the account", "locked out", "can't access", "account security"
NOTE: Card fraud/stolen cards do NOT qualify as account access issues - a stolen card does not provide access to the member's actual account.
IMPORTANT:
- This tag is commonly MISSED — look for any mention of unauthorized access, account information shared with wrong person, or account security breaches
- If member's card doesn't work after an account conversion, the primary issue is "card block" (not account access) — unless they also can't access the account itself
- If member is calling about being yelled at by an agent, that is "agent behavior", NOT account access
- Only use this tag when the member has trouble accessing THEIR ACCOUNT (online, in-branch, locked out), not when a specific product (card, loan) has an issue""",

    "agent behavior": """
1. Any member complaint that includes a lack of proper decorum from the agent (rudeness, unprofessional conduct, inappropriate comments)
2. Agent is seen as being rude, dismissive, disinterested, unresponsive, or unattentive to the member
3. Agent is acting unscrupulously — such as pressuring members to open a certain account, apply for a certain loan, or otherwise pushing them towards an action against their wishes
4. Agent gossips about members or other employees
5. Agent provides deliberately poor service or is intentionally unhelpful
KEYWORDS TO WATCH FOR: "rude", "unprofessional", "dismissive", "disinterested", "unresponsive", "pressured", "pushed me to", "agent was", "hung up on me", "wouldn't help", "attitude"
CRITICAL RULES:
- This tag is commonly MISSED — look for any indication of agent misconduct in demeanor OR unscrupulous conduct
- ONLY use when the AGENT behaves improperly in DEMEANOR or CONDUCT (agent was rude, agent hung up inappropriately, agent was unprofessional, agent gossiped, agent pressured member)
- If MEMBER is rude, abusive, or uses profanity, that is NOT agent behavior - the agent did nothing wrong
- If case mentions "member was using profanity" or "member said [insult]", do NOT tag agent behavior
- If agent hung up because MEMBER was abusive, that is NOT agent behavior (agent was right to disconnect)
- Look for clear agent misconduct in CONDUCT/DEMEANOR, not member complaints about service quality
- If agent shared member's personal information without authorization, that is "unauthorized action", NOT "agent behavior" (the issue is the unauthorized disclosure, not rudeness)
- Agent making a processing mistake is "processing error", not "agent behavior" — behavior is about demeanor/conduct, not errors""",

    "application": """
1. Any issue that arises during the APPLICATION PROCESS itself, including difficulty completing an application, undue burden placed on member during the application process, and/or incorrect information given during the application process
2. Application sent to wrong address or wrong person
3. Incorrect information entered on an application by agent (wrong email, wrong address, etc.)
IMPORTANT: 
- "App" in case notes usually means MOBILE APP, not application process
- A loan being denied is NOT an application issue unless the application PROCESS itself was problematic
- Only use when there's an actual problem with HOW the application was submitted or processed
- If application was sent to wrong address, also add "delivery"
- If agent entered wrong info on the application, also add "processing error\"""",

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
3. Member believes the balance should be different than what they are being told — checking, savings, money market, loan, or any account
4. Member disagrees with the stated balance on any financial product
5. After a deposit (cash or check), member believes the credited amount is wrong
KEYWORDS TO WATCH FOR: "balance is wrong", "balance should be", "incorrect balance", "doesn't match", "balance dispute", "account shows wrong amount"
NOTE: Use when member believes the BALANCE is wrong, not when a payment went to the wrong place (that's payment misapplied).
IMPORTANT:
- This is one of the most commonly MISSED tags — always check if the member is disagreeing with a stated balance
- If a cash deposit amount doesn't match what member expected, include "balance dispute"
- If member says "my balance should be X but it shows Y", this IS a balance dispute""",

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
3. Card not working after account conversion or account change
NOTE: Use when the card itself is physically fine but won't work due to blocks or system issues. If the chip is malfunctioning or card is worn, use "card quality" instead.
IMPORTANT: 
- If member says card is "not working" with no clear physical defect mentioned, default to "card block"
- If card doesn't work specifically at ATMs, tag BOTH "card block" AND "atm"
- If card doesn't work after account conversion, the issue is "card block" (not account access)""",

    "card fraud": """
1. Issues being flagged as fraud, requiring a call in to resolve
2. Actual fraudulent transactions on the card, requiring member to call in to resolve
3. Any fraudulent charges appearing on credit/debit card
4. Member upset about potential fraudulent transactions posting to account
NOTE: Use this for REPORTING fraud involving credit/debit CARD transactions.
IMPORTANT:
- Use when member is REPORTING or IDENTIFYING card fraud
- If member wants to DISPUTE a transaction or is upset about the OUTCOME of a fraud claim (claim denied, can't dispute pending txns), use "transaction dispute" instead
- "card fraud" = reporting/identifying fraud; "transaction dispute" = disputing a transaction or claim outcome
- If member wants to dispute pending transactions they believe are fraud but can't yet, the issue is "transaction dispute" (the dispute process), NOT "card fraud"
- If the fraud involves card transactions or pending card charges, use "card fraud", NOT "fraud - general\"""",

    "card quality": """
1. Card quality is poor, chip malfunctions, swipe functionality is spotty (physical card defects)
2. Members are constantly requiring cards to be reissued or reprinted due to physical defects
3. Card that wears down and needs replacement
4. Chip not working, strip having issues
NOTE: Use when there are PHYSICAL defects with the card. If card is blocked/declined but NOT physically defective, use "card block".
IMPORTANT: If the card is "not working" but NO specific physical defect is mentioned (chip, strip, tap, wear), default to "card block". Only use "card quality" when physical defect is explicitly described (e.g., "chip quit working", "tap stopped working", "card worn out").""",

    "certificate (CD)": """
1. Communication around withdrawal penalties or other fees regarding the closing or transfer of a CD is poor
2. CD auto renews without the member's knowledge or consent or without proper communication of auto renewal
3. Communication about rates, interest earned, or other concerning CDs is not good
IMPORTANT: Only use when the issue is WITH the CD itself. If member wants a CD-secured loan that gets denied, the issue is "loan denial", not CD.""",

    "check deposit": """
1. Check cannot be deposited or cashed due to check being printed improperly or not having all required information on it, typically the MICR Line
2. Check was cashed incorrectly, either incorrect amount, in the wrong account, or other
3. Check cannot be cashed or deposited due to technical issues, improper endorsement or failed identity verification
4. Check that has been sent is not deposited in a timely manner, inciting fears of the check being lost
5. A check deposit was processed with incorrect amounts (e.g., extra money taken from customer's account during deposit)
6. A check deposit triggered account restrictions, fraud flags, or access issues
IMPORTANT: 
- This is for CHECK deposits only. Cash deposits with issues should use "balance dispute" (if amount is wrong) and/or "processing error" (if teller counted incorrectly)
- A check deposit is NOT a payment — member depositing a check they received is "check deposit", NOT "payment misapplied"
- If a check deposit triggers fraud restrictions or account access issues, include "check deposit" as the root cause tag alongside other relevant tags""",

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
6. Dropped calls, phone tag, or difficulty reaching the right person/department
7. Communication is very difficult due to phone issues, language barriers, or other communication obstacles
8. Member left messages that were never returned
9. Promises to call back that were not kept
KEYWORDS TO WATCH FOR: "not told", "didn't communicate", "no one called back", "couldn't reach", "dropped call", "phone tag", "didn't inform", "wasn't aware", "never notified", "no communication"
NOTE: Use when information was NOT communicated or was unclear. If WRONG information was given, use "misinformation given" instead.
IMPORTANT:
- This tag is commonly MISSED — always check if information was not communicated, was unclear, or if communication was very difficult
- Dropped calls and phone tag are communication issues
- Lack of follow-up or returned calls is a communication issue""",

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
1. Financial product (card, check, title) was lost in delivery or never reached its intended destination
2. Delivery for financial product (card, check, title) was extremely slow
3. Improper delivery type (e.g. standard instead of expedited)
4. Title mailed but never received
5. Item (application, document, card) sent to the wrong address
NOTE: Use alongside item-specific tags (e.g., "titles" + "delivery" when title wasn't delivered).
IMPORTANT:
- Only use when a physical item was ACTUALLY SENT/MAILED and there was a delivery problem
- If a title was never printed or never mailed (e.g., lien release issue), that is NOT a delivery issue — use "titles" only
- Sending an application or document to the wrong address IS a delivery issue
- The item must have been in transit or intended to be delivered for this tag to apply""",

    "discrimination": """
1. Member makes a claim that racism, sexism, classism, or other -ism has occurred""",

    "documentation": """
1. An issue with documentation being different than what is required
2. An issue with documentation being completed or filled out improperly, leading to issues
3. A member has not received a required form, like tax form, that they are expecting
4. A member requests documentation from member services regarding their accounts
5. Required documentation preventing account opening (SSA letter for rep payee, etc.)
6. Member unable to provide required documents for account action
7. Member's statement or year-end document displays information incorrectly or in a misleading way (e.g., fees showing that were already refunded, incorrect totals)
8. Member wants a statement or document corrected/updated
NOTE: Use alongside specific account type tags (e.g., "rep payee" + "documentation").
IMPORTANT: If the issue is about what a STATEMENT or DOCUMENT shows (even if fees are involved), use "documentation" — the problem is with the document, not the fee itself.""",

    "duplicate transaction": """
1. A transaction that has occurred twice or more than twice on a member's account WITH THE SAME AMOUNT
2. Double payment posted to a loan that needs adjustment
IMPORTANT:
- Amounts MUST be the same to be a duplicate
- Different amounts (e.g., $198.85 and $177.22) are separate transactions, NOT duplicates
- Third-party charges (Comcast, etc.) with different amounts = use "transaction dispute" instead
- When double payment needs correction, also add "adjustment" tag""",

    "escalation request": """
1. Member fails to get a resolution to their problem through first line service and so request escalation
2. Member asks to speak to a supervisor/manager/lead
3. Call became an escalation call
4. Member was transferred to escalations/helpdesk
5. MACU employee escalates a call to assist the member (employee-initiated escalation)
6. Member demands to speak with someone higher up or with more authority
KEYWORDS TO WATCH FOR: "escalate", "supervisor", "manager", "speak to a lead", "transferred to", "wants to escalate", "escalation"
NOTE: 
- This tag is commonly MISSED — always check if the member requested escalation OR if the call was escalated by an employee
- There are TWO scenarios to watch for: (1) member ASKS for escalation, or (2) MACU employee escalates the call
- Staff internally consulting other teams (fraud, payments) is NOT an escalation request
- Member disconnecting in frustration is NOT an escalation request""",

    "fee disclosure": """
1. Member has a question regarding fees that are linked to an account, not understanding why they were charged or their origin
2. Member feels that the payment of fees was not properly communicated to them
3. Member is upset that fees are being charged that had never been charged for similar or the same transaction in the past
4. Member inquiring about what a fee is for
5. Member wants to understand account fees or charges
6. Member wants better returns/dividends (fee/interest related)""",

    "fraud - general": """
1. A catch-all for fraud complaints OUTSIDE of credit card fraud, including identity theft, account takeover, check fraud, wire fraud, etc.
2. Member is attempting to commit fraud themselves (e.g., falsely claiming money was stolen when evidence shows otherwise)
IMPORTANT: 
- If the fraud involves CARD transactions (credit/debit card charges, pending card transactions), use "card fraud" instead
- Only use "fraud - general" for non-card fraud like identity theft, check fraud, wire fraud, account takeover without card involvement
- Also use when the MEMBER is the one committing fraud (filing false claims, making false accusations against employees when evidence contradicts their story)""",

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
3. GAP insurance claim issues
4. Issues with loan relief / loan relief plan / debt protection products (these ARE insurance)
5. Member upset about how loan relief charges were explained or added
IMPORTANT: "Loan relief" and "debt protection" are insurance products - use this tag, NOT "auto loan" for loan relief issues.""",

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
1. A MACU representative provides incorrect/WRONG information VERBALLY to a member, upon which the member then acts
IMPORTANT: 
- Only use when agent TOLD the member WRONG information (wrong date, wrong amount, wrong process)
- If information was simply not communicated, use "communication issue" instead
- If an agent entered wrong data into a system (wrong account number for a recall, wrong email on application), that is "processing error", NOT misinformation — the error was in DATA ENTRY, not in what the member was TOLD
- Misinformation = told wrong info; Processing error = did wrong action""",

    "missed payment": """
1. Payment was missed and member wants to know if MACU can work with them in some way
2. Payment was missed due to slow processing times on MACU's end
3. Payment missed due to other reasons, such as UX or inability to access account
4. Member failed to make a required payment on time
5. Autopay failed to pull a payment, resulting in a missed payment
6. Member was unaware of a payment due date and missed the payment
KEYWORDS TO WATCH FOR: "missed payment", "didn't pay", "failed to pay", "payment was missed", "didn't make payment", "payment not made", "past due"
IMPORTANT:
- This tag is commonly MISSED — always check if the complaint involves a payment that was not made on time
- If autopay failure caused the missed payment, tag BOTH "missed payment" AND "autopay"
- If a late fee resulted from the missed payment, tag BOTH "missed payment" AND "late fee"
- Primary causes: autopay issues, member failing to make payment when required, system issues preventing payment""",

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
- Balance showing incorrectly is NOT payment misapplied (use "balance dispute")
- Check deposits are NOT payments — if a check deposit was processed incorrectly, use "check deposit" (and "processing error" if agent error)
- Autopay set up in reverse or to the wrong account is a PROCESSING ERROR, not payment misapplied (the setup was wrong, not the payment itself)
- An extra amount taken during a deposit is "check deposit" + "processing error", NOT payment misapplied""",

    "processing error": """
1. A transaction was processed incorrectly BY A HUMAN AGENT
2. Member receives a notice or other communication from MACU in error about an issue that does not exist on their account or meant for another Member
3. Changes are made to an account where the requestor for the change is unknown or where it originated from
4. Documents processed with incorrect information
5. Loan booked to wrong account (even if loan was requested, wrong account = processing error)
6. Cash deposit counted incorrectly by teller
7. Product (insurance, loan relief) not cancelled when member requested cancellation
8. Autopay set up incorrectly (e.g., reversed direction, wrong account, wrong amount)
9. Agent entered incorrect data in a system (wrong account number for recall, wrong email on application, etc.)
10. Payment processed through wrong account
IMPORTANT: 
- Only use when a HUMAN AGENT processed something incorrectly
- ATM errors are NOT processing errors (use "atm")
- IVR/phone system errors are NOT processing errors (use "interactive voice response (IVR)")
- System working as designed is NOT processing error
- Don't use if we don't know whether an error occurred
- If member REQUESTED an action but it was done to WRONG account = processing error, NOT unauthorized action
- Autopay set up backwards or to wrong account = processing error (the SETUP was wrong)
- Wrong data entered into system (recall info, application info) = processing error, NOT misinformation""",

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
1. Member upset with changes in rewards offered
2. Member did not receive a promotional bonus or reward that was promised
3. Member has issues with points, cashback, or other reward program benefits
4. Member is complaining about a marketing promotion that was not honored
5. Member expected a reward or bonus for opening an account, signing up for a product, or meeting certain criteria
KEYWORDS TO WATCH FOR: "promo", "promotion", "reward", "points", "bonus", "cashback", "incentive", "offer"
IMPORTANT:
- This tag is commonly MISSED — look for any mention of promotions, rewards, points, or bonuses
- Even if the complaint is primarily about something else, if a missed reward/promo is part of the issue, include this tag""",

    "skip payment": """
1. The member wants to initiate a skip payment
2. The member is not able to use a skip payment for some reason
3. The member is confused about how a skip pay works or has concerns about the results of their skip payment
4. Payment still initializes even after a skip payment is requested or activated
5. Member seeking loan extension due to not making payments (also add "loan payment" in this case)
NOTE: When member is behind on payments and seeking extension, tag BOTH skip payment AND "loan payment".""",

    "stop payment": """
1. Member calls in because of an issue that arises with a stop payment request or to initiate a stop payment request
2. Member wants to stop a check payment that has been initiated but not yet applied
3. Member placed a stop payment but the payment still went through
4. Issues with stop payment fees or the stop payment process
5. Member requests to cancel or halt a pending payment (typically a check payment)
KEYWORDS TO WATCH FOR: "stop payment", "stop the check", "cancel payment", "halt payment", "stop a check", "stop the payment"
IMPORTANT:
- This tag is commonly MISSED — always check if the member is requesting to stop or cancel a pending payment
- A stop payment is specifically about a payment that has been INITIATED but NOT YET APPLIED
- If the payment already went through, this is not a stop payment issue (may be "transaction dispute" or "refund")""",

    "technical issue": """
1. Member has technical issues with online banking or the mobile app
2. Member does not receive proper notifications when using the online system
3. MACU has internal technical issues that affect the member in some way
4. Member is generally unhappy with the way technology at MACU works or is configured. They find it confusing or difficult to use
5. SMS/text message system not recognizing member's response (fraud alert texts, verification texts)
6. System failed to process member's response correctly
IMPORTANT:
- System working as designed is NOT a technical issue
- Loan product not offered is NOT a technical issue
- IVR issues should use "interactive voice response (IVR)" instead
- "App" in case notes usually means mobile APP (potential technical issue), not application process
- Fraud text alerts where system didn't recognize response = technical issue""",

    "titles": """
1. Issue where a title cannot be released or has not been released
2. Member is having trouble gaining access to a title
3. Title has incorrect information (wrong VIN, etc.)""",

    "transaction dispute": """
1. Member calls in to dispute a transaction, either a credit card payment, a wire transfer/bill pay, account offsets, or other transactions
2. Member disputing an offset payment that was made from their account
3. Member disputes any transaction that occurred on their account
4. Member upset about claim credit reversal (disputed fraud claim that was denied and provisional credit reversed)
5. Third-party charges that member wants refunded (even if amounts are different)
NOTE: 
- Use when member is DISPUTING a transaction
- Account offsets per loan agreement terms are disputable transactions
- "Claim credit reversal" or denied fraud claim = transaction dispute, NOT card fraud
- Card fraud is for REPORTING fraud, this is for DISPUTING outcomes of claims or transactions""",

    "transfers": """
1. Transfer issues, including transfers from visa debit/credit cards, ODP, or other issues
2. Member not able to make transfers
3. Transfers are not showing up in a timely manner
4. Transfers happening when not requested or money disappearing without the member knowing where it went
5. Member calls in having issues with transfer limits
NOTE: Transfers are different from payments. If money was transferred to wrong account, use this tag, NOT "payment misapplied".""",

    "unauthorized action": """
1. Any disputed transaction where the member claims that MACU took unilateral action on doing something that was NOT REQUESTED by the member
2. Account converted without member's knowledge or consent (e.g., share type changed)
3. Account changes made without proper notification or authorization
4. Credit pull done without member's direct authorization (wife authorized but member didn't)
5. Agent shared member's personal information with a third party without member's authorization
6. Product/service (e.g., overdraft protection) enrolled or set up without member's knowledge or consent
7. Mortgage deferment or other loan modification applied without member signing documents or consenting
IMPORTANT: 
- Actions permitted by loan agreement terms (like account offsets for past due loans) are NOT unauthorized, even if member is upset about them
- Account conversions/changes without notification ARE unauthorized
- If member REQUESTED an action but it was done to the WRONG account = "processing error", NOT unauthorized
- If action was never requested at all = "unauthorized action"
- Credit pull where member didn't personally authorize = unauthorized action
- Unauthorized disclosure of personal information to third parties = unauthorized action (NOT "agent behavior")
- Setting up overdraft protection when member specifically said not to = unauthorized action""",

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

    "account charge off": """
1. Member is disputing a charge off on their account
2. Member received notice about a charged off account
3. Member upset about charge off affecting their credit
4. Charge off dispute, regardless of whether member claims fraud
NOTE: If member claims a charge off is fraud, still use "account charge off" as the primary tag (not fraud - general).""",

    "garnishment": """
1. Member's account has been garnished
2. Member upset about garnishment on their account
3. Member not notified about garnishment
4. Funds taken from account due to court-ordered garnishment
NOTE: Use when funds are taken from account due to legal garnishment order.""",

    "adjustment": """
1. Member requesting an adjustment to their account
2. Payment adjustment is taking longer than expected
3. Transaction needs to be adjusted/corrected
4. Member was told incorrect timeframe for adjustment
5. Double payment posted that needs adjustment
NOTE: Use when a correction/adjustment needs to be made to fix a transaction or payment issue.""",

    "rep payee": """
1. Member attempting to open a representative payee account
2. Issues with rep payee account setup or requirements
3. SSA letter requirements for rep payee accounts
4. Problems with representative payee arrangements
NOTE: Representative payee accounts have specific documentation requirements (SSA letter).""",

    "account offset": """
1. Member's account is offset (funds moved from one account to cover a debt on another) and calls in about it
2. Member disputes an account offset
3. Member upset about an offset being applied to their account
4. Call was triggered by an account offset being performed on the member's account
NOTE: Use specifically when the complaint is triggered by an account offset. Offsets per loan agreement terms are permitted by MACU but are still disputable — pair with "transaction dispute" if member is disputing the offset.""",

    "overdraft protection": """
1. Member has concerns about being opted in or out of overdraft protection (ODP) without their knowledge or consent
2. Member expected their card to decline transactions but overdraft protection was active
3. Member disputes their enrollment in overdraft protection/privilege
4. Issues with overdraft protection setup, enrollment, or opt-in/opt-out status
IMPORTANT:
- Use when the core issue is about ENROLLMENT in or STATUS of overdraft protection, NOT about the fees themselves
- If member is complaining about overdraft FEES they were charged, use "overdraft fee"
- If member never authorized ODP enrollment, also add "unauthorized action"
- "overdraft fee" = about the FEE charged; "overdraft protection" = about the ENROLLMENT/OPT-IN status""",

    "late fee": """
1. Member has been assessed a late fee for any reason, primarily late and/or missed payments
2. Member is disputing or complaining about a late fee charged to their account
3. Member is upset that a late fee was assessed when they believe the payment was on time
4. Member is calling about late fees resulting from autopay failure or processing delays
5. Late fee assessed after a skip payment or deferment period
KEYWORDS TO WATCH FOR: "late fee", "late charge", "late penalty", "charged late", "fee for being late", "assessed a fee"
IMPORTANT:
- Use when a late fee is a component of the complaint, even if the member is also complaining about a missed payment or autopay issue
- If the member also missed a payment, tag BOTH "late fee" AND "missed payment"
- If the late fee resulted from an autopay failure, tag BOTH "late fee" AND "autopay"
- If member is requesting a refund of the late fee, also add "refund\"""",

    "NSF": """
1. Member has been assessed an NSF (non-sufficient funds) fee
2. A payment or transaction was rejected because the member did not have enough funds in the account
3. Member is disputing an NSF fee or complaining about the fee amount
4. Member is calling because a check or payment bounced due to insufficient funds
5. Member had a transaction declined and was charged an NSF fee
KEYWORDS TO WATCH FOR: "NSF", "non-sufficient funds", "insufficient funds", "bounced check", "returned item", "not enough funds", "rejected payment"
IMPORTANT:
- NSF is DIFFERENT from overdraft: NSF = payment is REJECTED and fee is charged; overdraft = payment goes through but account goes negative
- If the payment was rejected AND the member was charged a fee, use "NSF"
- If the payment went through despite insufficient funds (overdraft), use "overdraft fee" instead
- If member is requesting a refund of the NSF fee, also add "refund\"""",

    "cash deposit": """
1. Member is depositing cash into a personal or business account (checking, savings, CD, etc.)
2. Cash deposit was placed into the wrong account
3. Cash was counted incorrectly by teller during deposit
4. Issues with the amount credited from a cash deposit
5. Cash deposit not reflecting correctly in account balance
KEYWORDS TO WATCH FOR: "cash deposit", "deposited cash", "cash into account", "teller deposit"
IMPORTANT:
- A cash deposit is NOT a payment — do NOT tag as "payment misapplied"
- If cash was deposited into the wrong account, use "cash deposit" + "processing error" (the teller made the error)
- If the teller counted the cash incorrectly, use "cash deposit" + "processing error"
- If the cash deposit amount doesn't match what member expected, use "cash deposit" + "balance dispute"
- "payment misapplied" is ONLY for actual PAYMENTS (loan payments, credit card payments) going to the wrong place, NOT deposits""",
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

### MOST IMPORTANT: Do NOT Miss Relevant Tags
- The #1 error is MISSING tags — returning fewer tags than are relevant to the complaint
- Read the ENTIRE complaint carefully and identify ALL issues present, not just the most obvious one
- If a complaint mentions multiple issues (e.g., missed payment AND late fee AND autopay failure), tag ALL of them
- When in doubt about whether a tag applies, lean towards INCLUDING it — missing a relevant tag is worse than including a borderline one
- Pay special attention to these commonly missed tags: balance dispute, late fee, missed payment, NSF, rewards, stop payment, overdraft protection, processing error, escalation request, account access & security, agent behavior, communication issue, cash deposit

### Focus on PRIMARY Complaint (but include secondary issues too)
- Tag based on WHY the member called, but also include secondary issues mentioned in the complaint
- If member called to pay a loan but couldn't verify identity, the issue is "identity verification", not "loan payment"
- If member mentions escalation while complaining about fees, tag BOTH the fee issue AND "escalation request"

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
- If misinformation was given about CDs (rates, limits, interest) = include "certificate (CD)" along with "misinformation given"

### Duplicate Transaction - BE PRECISE
- ONLY use when the SAME amount is charged multiple times
- Different amounts = NOT a duplicate (e.g., Comcast charging $198.85 and $177.22 are separate charges, not duplicates)
- Third-party duplicate charges (not MACU's fault) may still need "transaction dispute" instead
- When in doubt about different amounts, use "transaction dispute" instead

### Skip Payment / Loan Extension + Loan Payment
- When member is seeking an extension because they have NOT made payments, tag BOTH the extension issue AND "loan payment"
- Member behind on payments seeking extension = add "loan payment"

### Overdraft Fee + Refund
- When member is BOTH upset about overdraft fees AND specifically seeking a refund, tag BOTH "overdraft fee" AND "refund"
- Just asking about fees = "overdraft fee" only
- Asking for fees to be waived/refunded = add "refund"

### Fee Disclosure - Already Covers Confusing Fees
- When fees are confusing or unclear, use "fee disclosure" - do NOT also add "communication issue"
- "communication issue" is for when information was NOT communicated at all
- Confusing fee structure or unclear fee explanation = just "fee disclosure"

### Claim Credit Reversal / Disputed Claims
- "claim credit reversal" or denied fraud claim = "transaction dispute", NOT "card fraud"
- Card fraud is for REPORTING fraud, not for disputing the outcome of a claim
- If member is disputing denial of their fraud claim = "transaction dispute"

### Loan Relief / Debt Protection = Insurance
- "Loan relief", "loan relief plan", "debt protection" = these are INSURANCE products
- Issues with loan relief charges or cancellation = "insurance", NOT "auto loan"
- If loan relief should have been cancelled but wasn't = add "processing error"

### Cash Deposit vs Check Deposit vs Payment Misapplied
- "cash deposit" = member depositing CASH into an account — this is NOT a payment
- "check deposit" = member depositing a CHECK into an account — this is NOT a payment
- "payment misapplied" = an actual PAYMENT (loan payment, credit card payment) going to the wrong place
- CRITICAL: Deposits (cash or check) are NOT payments. Do NOT tag deposits as "payment misapplied"
- Cash deposit into wrong account = "cash deposit" + "processing error"
- Cash counted incorrectly by teller = "cash deposit" + "processing error"
- Check deposit processed incorrectly = "check deposit" + "processing error"
- If a deposit also involves incorrect balance = add "balance dispute"

### Auto Loan Setup Through Dealer
- When dealer fails to communicate important loan info (due date, account info) = add "communication issue" AND "auto loan"
- Missing payment information at loan setup = "communication issue"

### Check Return Causing Interest
- If a payoff check is returned and causes additional interest = tag BOTH "check return" AND "interest dispute"
- Don't forget the interest component when check issues cause interest charges

### Escalation Request - Member Must Request
- ONLY use when MEMBER explicitly asks to speak to supervisor/manager OR is transferred to escalations
- Staff internally consulting other departments (fraud team, etc.) is NOT an escalation request
- Member disconnecting in frustration is NOT an escalation request

### Delivery - Items Not Arriving
- When a title, card, or check never arrives or was lost in delivery = add "delivery"
- Use alongside the item-specific tag (e.g., "titles" + "delivery")

### Portal Access Due to Relocation
- Member can't access online portal because they moved/changed state = "account access & security"
- Geographic restrictions preventing portal access = account access issue

### Double Payment Needing Adjustment
- Payment posted twice to an account that needs correction = BOTH "duplicate transaction" AND "adjustment"
- Focus on both the duplication AND the need for correction

### Account Charge Off
- Use for charge off disputes, NOT "fraud - general"
- Even if member claims charge off is fraud, primary issue is "account charge off"
- Often paired with "credit check" when affecting credit report

### Documentation for Account Opening
- When specific documentation is required to open an account (SSA letter for rep payee, etc.) = add "documentation"
- Missing required documents preventing account action = "documentation"

### Documentation vs Adjustment for Statement Issues
- If member wants their statement corrected because it shows fees that were refunded = "documentation" (the document is wrong)
- If member wants a transaction adjusted/corrected = "adjustment"
- Statement display issues = "documentation"; transaction corrections = "adjustment"

### Payment Misapplied vs Check Deposit vs Processing Error
- A check deposit processed incorrectly (wrong amount, extra money taken) = "check deposit" + "processing error"
- A check deposit is NOT a payment — member depositing a check is "check deposit", NOT "payment misapplied"
- Autopay set up in the wrong direction or to the wrong account = "processing error" + "autopay", NOT "payment misapplied"
- "payment misapplied" requires an actual PAYMENT going to the wrong place, not a setup error

### Agent Behavior vs Unauthorized Action
- Agent was rude, gossiping, unprofessional in DEMEANOR = "agent behavior"
- Agent shared member's personal information without authorization = "unauthorized action" (the harm is the unauthorized disclosure, not rudeness)
- Agent actions that violate member privacy or authorization = "unauthorized action"

### Card Quality vs Card Block — Unknown Cause Defaults to Card Block
- Card has KNOWN physical defect (chip quit, tap stopped, strip worn) = "card quality"
- Card not working but reason is UNKNOWN = "card block" (cannot assume physical defect without evidence)
- Key: "card quality" requires explicit mention of physical malfunction

### Overdraft Fee vs Overdraft Protection
- Member upset about FEES from overdraft = "overdraft fee"
- Member upset about being ENROLLED in overdraft protection without consent = "overdraft protection"
- If ODP was set up when member explicitly said not to, add "unauthorized action"
- If enrollment was unauthorized AND fees resulted = "overdraft protection" + "unauthorized action" + "overdraft fee"

### Card Fraud vs Transaction Dispute — Reporting vs Disputing
- Member REPORTING fraud on their card (identifying unauthorized charges) = "card fraud"
- Member wanting to DISPUTE transactions (even fraud-related) but can't because they're pending = "transaction dispute"
- Member disputing the OUTCOME of a fraud claim (claim denied) = "transaction dispute"
- The distinction: reporting/identifying = card fraud; disputing process/outcome = transaction dispute

### Member-Initiated Fraud
- When evidence shows the MEMBER is committing fraud (false claim against employee, fabricated story contradicted by evidence) = "fraud - general"
- This is NOT "unauthorized action" or "transaction dispute" — the member is the fraudster

### Misinformation vs Processing Error — What Was Said vs What Was Done
- Agent TOLD member wrong information = "misinformation given"
- Agent ENTERED wrong data into system (wrong account for recall, wrong email on app) = "processing error"
- Key question: Was the error in COMMUNICATION (told wrong info) or in DATA ENTRY (did wrong action)?

### Card Block at ATMs
- If card doesn't work specifically at ATMs, tag BOTH "card block" AND "atm"
- The ATM tag captures the location; card block captures the card issue

### Delivery — Must Involve Actual Transit
- Only use "delivery" when an item was ACTUALLY SENT/MAILED
- Title never printed or mailed (lien release issue) = "titles" only, NOT "delivery"
- Application sent to wrong address = "application" + "delivery"
- Item must have been in transit for delivery tag to apply

### Account Access vs Card Block After Conversion
- After account conversion, if card doesn't work = "card block" (card issue, not account access)
- After account conversion, if member can't log in to online banking = "account access & security"
- Focus on WHAT isn't working: card = card block; account login = account access

### Check Deposit as Root Cause
- When a check deposit triggers downstream issues (fraud flags, account restrictions) = include "check deposit" as a root cause tag
- Tag the downstream effects too (e.g., "account access & security", "communication issue")

### Account Offset
- When member's complaint is triggered by an account offset = add "account offset"
- If member is disputing the offset = add "transaction dispute" alongside "account offset"
- Account offsets per loan terms are permitted but still disputable

### Interest Dispute as Secondary Tag
- When unauthorized action or payment issue causes interest to accrue = add "interest dispute"
- Example: unauthorized deferment that caused 6k in interest = "unauthorized action" + "mortgage" + "interest dispute"
- Example: can't pay full balance causing interest = "interest dispute" + "loan payment"

### Late Fee — Commonly Missed
- When member is assessed a late fee, ALWAYS include "late fee" as a tag
- Late fees often co-occur with "missed payment" — tag BOTH when a missed payment led to a late fee
- Late fees from autopay failure = "late fee" + "autopay" (+ "missed payment" if applicable)
- If member wants the late fee refunded, also add "refund"

### NSF (Non-Sufficient Funds) — Commonly Missed
- NSF = payment REJECTED due to insufficient funds + fee charged
- Overdraft = payment goes THROUGH despite insufficient funds + fee charged
- "bounced check" or "returned item" = NSF
- If member wants the NSF fee refunded, also add "refund"

### Missed Payment — Commonly Missed
- Any time a payment was not made when it should have been = "missed payment"
- Autopay failure causing missed payment = "missed payment" + "autopay"
- Missed payment causing late fee = "missed payment" + "late fee"

### Processing Error vs Payment Misapplied — Critical Distinction
- Processing error is about a HUMAN AGENT making an error in processing
- When a deposit (cash or check) is processed incorrectly, use "processing error" + the deposit type tag, NOT "payment misapplied"
- "payment misapplied" requires an actual PAYMENT going to the wrong place — deposits are NOT payments
- When in doubt between processing error and payment misapplied with a deposit, choose "processing error"

### Escalation Request — Two Scenarios
- Scenario 1: MEMBER asks to speak to supervisor/manager = "escalation request"
- Scenario 2: MACU EMPLOYEE escalates the call = "escalation request"
- Both scenarios should be tagged — don't miss employee-initiated escalations

### Balance Dispute — Commonly Missed
- Any time a member disagrees with a stated balance on ANY account = "balance dispute"
- This applies to checking, savings, money market, loan, credit card — any financial product
- If deposit amount doesn't match what was expected = include "balance dispute"
"""


if __name__ == "__main__":
    # Quick test
    test_tags = ["card block", "card fraud", "card quality", "fraud - general"]
    print("Testing tag definitions:")
    print(get_tag_definitions_prompt(test_tags))
    print("\n" + "=" * 60)
    print("Confusion guidance:")
    print(get_confusion_guidance())
