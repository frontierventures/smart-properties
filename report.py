#!/usr/bin/env python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

doc = SimpleDocTemplate("files/paragraphs.pdf", pagesize=letter)

paragraphs = []

paragraphs.append('''<b>THIS LOAN AGREEMENT</b> made as of %s''' % 'DATETIME')
paragraphs.append('''<p>between</p>''')
paragraphs.append('''<b>BITCOIN REALTY MANAGEMENT LIMITED</b>, a body corporate incorporated under the laws of the Province of Nova Scotia, Canada (the \"Borrower\") OF THE FIRST PART''')
paragraphs.append('''   and''')
paragraphs.append('''<b>%s</b> (the \"Lender\") OF THE SECOND PART''' % 'LENDER')
paragraphs.append('''   and''')
paragraphs.append('''DEVIN PODGORSKI (\"Devin\") OF THE THIRD PART''')
paragraphs.append('''JAMES SUTTON (\"James\" and collectively, with Devin, the \"Guarantors\") OF THE FORTH PART''')
paragraphs.append(''' ''')

paragraphs.append('''WHEREAS the Lender has agreed to provide financing to the Borrower (the \"Loan\");''')
paragraphs.append('''AND WHEREAS the Guarantors have agreed to guarantee the Loan in accordance with the terms hereof;''')
paragraphs.append('''THEREFORE in consideration of the mutual covenants and agreements herein contained, the sum of One Dollar ($1.00) and other good and valuable consideration, the receipt and sufficiency of which is hereby acknowledged, the parties covenant and agree as follows:''')
#!/usr/bin/env python
paragraphs.append('''1. INTERPRETATION''')
paragraphs.append('''(a) Definitions. In this Agreement, unless the context otherwise requires the following terms shall have the following meanings:''')
paragraphs.append('''\"Agreement\" means this agreement and any amendments, schedules and supplements thereto that are agreed on by the parties in writing from time to time;''')
paragraphs.append('''\"Bitcoin Amount\" means the amount of <b>%s</b> bitcoins, to be advanced by the Lender to the Borrower in accordance with the terms of this Agreement.''')
paragraphs.append('''\"Closing Date\" means the date of this Agreement;''')
paragraphs.append('''\"Interest Rate\" means an annual interest rate of 9.30 percent;''')
paragraphs.append('''\"Loan Amount\" means the amount advanced by the Lender to the Borrower, expressed in Canadian Dollars and determined in accordance with Sections 2(b)(ii) and (iii) hereof; and''')
paragraphs.append('''\"Term\" means twenty five years.''')
paragraphs.append('''(b) Currency Conversion. Any conversion of bitcoin to Canadian Dollars, or Canadian Dollars to bitcoin, shall be done in accordance with Section 4 hereof.''')
paragraphs.append('''2. LOAN TO THE BORROWER''')
paragraphs.append('''(c) Agreement to Lend.  Subject to the terms and conditions of this Agreement, the Lender agrees to lend to the Borrower the Loan Amount.''') 
paragraphs.append('''(d) Advance. The loan advance shall be made in accordance with the following terms:''')
paragraphs.append('''(i) Advance. The Lender will advance the Bitcoin Amount to the Borrower, in a single advance on the Closing Date without set-off, holdbacks or other deductions.''')
paragraphs.append('''(ii) Conversion to Loan Amount. The Borrower shall convert the Bitcoin Amount to Canadian Dollars within 2 business days of receipt thereof (the \"Conversion Date\").''')
paragraphs.append('''(iii) Exchange Statement. Within 2 business days of the Conversion Date, the Borrower will provide an exchange statement to the Lender setting out the Loan Amount (expressed in Canadian Dollars), together with notice of the applicable bitcoin exchange rate at the time of conversion of the Bitcoin Amount (the \"Exchange Statement\"). The Loan Amount, as set out in the Exchange Statement, shall be conclusive evidence of the indebtedness of the Borrower to the Lender.''') 
paragraphs.append('''3. PROMISE TO REPAY. The Borrower promises to repay the Loan Amount in accordance with the terms of this Agreement.''')
paragraphs.append('''(e) Place of Payment.  All amounts due under this Agreement shall be paid to Lender by electronic transmission and shall be deemed to have been paid in Halifax, Province of Nova Scotia, Canada.''')
paragraphs.append('''(f) Interest Adjustment Date: The Interest Adjustment Date shall be the first day of the month immediately following the Loan advance. In addition to any other payments required pursuant to section 3(c), interest from the Conversion Date to the Interest Adjustment Date shall be payable in bitcoin on the seventh business day of the first calendar month following the Interest Adjustment Date.''')
paragraphs.append('''(g) Payment.  Equal monthly payments of principal and interest based on the Term shall be calculated in Canadian Dollars as of the first day of each calendar month (each such amount being a \"Payment Amount\"). Subject to this section 3, the Payment Amount shall be payable in bitcoin on the seventh business day of each calendar month commencing on the seventh business day of the calendar month immediately following the Interest Adjustment Date.''')
paragraphs.append('''(h) Conversion. On the fifth business day of each month (each, a \"Repayment Conversion Date\") the Borrower shall convert the Payment Amount into bitcoin at the then current bitcoin exchange rate (the \"Bitcoin Exchange Rate\").''')
paragraphs.append('''(i) Prepayment. The Borrower may prepay any or all of the Loan Amount at its absolute discretion provided that any such prepayment shall be made in bitcoin and shall be converted in accordance wit section 3 hereof (the \"Prepayment Amount\").''')
paragraphs.append('''(j) Expenses. Any expenses incurred by the Borrower to convert any Payment Amount or Prepayment amount into bitcoin shall be for the expense of the Borrower.''')
paragraphs.append('''(k) Reduction of Loan Amount. Following any payments hereunder, the Loan Amount shall be reduced  by the applicable Payment Amount or Prepayment Amount, as determined in Canadian Dollars at the applicable Repayment Conversion Date.''')
paragraphs.append('''4. CONVERSION. Any conversion of Canadian Dollars into bitcoin or bitcoin into Canadian Dollars pursuant to this Agreement shall be completed in accordance with the following terms and conditions:''')
paragraphs.append('''(l) Bitcoin Exchange Operator. The Borrower may determine, at its absolute discretion, which bitcoin exchange operator (the \"Bitcoin Exchange Operator\") completes the conversion of any amounts payable hereunder.''')
paragraphs.append('''(m) Expenses. All expenses for any conversion shall be for the account of the Borrower.''')
paragraphs.append('''(n) Determination Final. The Lender shall be deemed to accept (i) the posted exchange rate used by the Bitcoin Exchange Operator for the conversion of the Payment Amount to bitcoin; and (ii) any and all Exchange Fees, as determined by the Bitcoin Exchange Operator together with any third party fees reasonably necessary to complete the conversion of any payable amounts hereunder.''')
paragraphs.append('''5. COVENANTS, REPRESENTATIONS AND WARRANTIES''')
paragraphs.append('''(o) Borrower. The Borrower covenants and agrees with and represents and warrants to the Lender (and acknowledges and confirms that the Lender is relying on such covenants, agreements, representations and warranties in connection with entering this Agreement and in connection with the financing to be provided pursuant hereto by the Lender to the Borrower) that as of the date of this Agreement, and as of the Closing Date, and as of the time of the loan advance hereunder and throughout the period during which any part of the Loan Amount advanced to the Borrower remains outstanding as follows:''')
paragraphs.append('''(i) The Borrower is and will continue to be a body corporate duly incorporated and organized and validly subsisting in good standing under the laws of the Province of Nova Scotia. The Borrower has and will continue to have the corporate power to own property and to carry on the Business, is and will be duly qualified as a company to do business and is and will be in good standing in each jurisdiction in which the nature of the business makes such qualification necessary.''')
paragraphs.append('''(ii) The entering into of this Agreement and the carrying out of the transactions contemplated hereby have been duly authorized by all necessary corporate action and will not result in the violation of any of the terms and provisions of the constituting documents or articles of association of the Borrower or any indenture or other agreement, written or oral, to which the Borrower may be a party or otherwise bound.''')
paragraphs.append('''(iii) The Borrower has all requisite power and authority which has been properly exercised to enter into this Agreement, to carry out the transactions herein provided for and to perform its obligations under this Agreement.''')
paragraphs.append('''(iv) The Borrower shall take or cause to be taken all necessary or desirable actions, steps and corporate proceedings to approve or authorize validly and effectively the execution and delivery of this Agreement and all other arrangements and documents contemplated hereby and shall cause all necessary meetings of directors of the Borrower to be held for such purpose.''')
paragraphs.append('''(v) The Borrower will duly and punctually pay or cause to be paid to the Lender the principal Loan Amount pursuant to and in accordance with the terms of this Agreement.''')
paragraphs.append('''(p) Confidentiality. In the event that any governmental or quasi-governmental authority with jurisdiction over the Loan (a \"Governing Authority\") requires the disclosure of any information concerning any party hereto, the Parties agree to cooperative with such Governing Authority to the extent required by law, and agrees that no information required by such Governing Authority in the possession of the disclosing party will be confidential with respect to such Governing Authority.''')
paragraphs.append('''(q) Survival of Representations, Warranties and Covenants. The obligations, representations and warranties contained in this Agreement, in any document to be executed and delivered pursuant to this Agreement and in any documents executed and delivered in connection with the completion of the transaction contemplated herein shall survive the closing of such transaction notwithstanding any investigations made by or on behalf of the parties hereto.''')
paragraphs.append('''6. DEFAULT. Notwithstanding anything to the contrary contained herein, the principal Loan Amount advanced  shall, at the option of the Lender, become immediately due and payable in each and every of the following events:''')
paragraphs.append('''(i) if the Borrower makes any default in the payment of any indebtedness or obligation to the Lender or defaults in repayment of the principal Loan Amount payable under this Agreement and such default is not remedied within ten (10) days of the Borrower receiving notice in writing from the Lender of the default;''')
paragraphs.append('''(ii) if the Borrower fails to perform or observe any covenant or obligation contained herein, and such default is not remedied within ten (10) days of the Borrower receiving notice in writing from the Lender of the default;''')
paragraphs.append('''(iii) if the Borrower becomes insolvent or bankrupt or subject to provisions of the Bankruptcy and Insolvency Act or goes into liquidation, either voluntarily or under an order by a court of competent jurisdiction, or makes a general assignment for the benefit of its creditors or otherwise acknowledges itself insolvent; and ''')
paragraphs.append('''(iv) if the Borrower abandons its undertaking or ceases or threatens to cease to carry on Business or threatens to commit any act of bankruptcy.''')
paragraphs.append('''Provided that it shall not be an Event of Default if an inability to make any payment required pursuant to this Agreement is a result of an error incurred by a Bitcoin Exchange Operator. Should such a delay occur, the parties will negotiate alternative payment options. In the event that the parties are unable to agree on an alternative payment method, either Party may refer the matter to arbitration by providing the other Party with a notice to proceed to arbitrate (\"Notice of Arbitration\"). Upon either Party providing a Notice of Arbitration, the matter (or such matters as remain in dispute, if the Parties agree they have resolved some but not all of the original dispute) shall not later than thirty (30) days from issuance of the Notice of Arbitration be submitted to final and binding arbitration in accordance with the Nova Scotia Commercial Arbitration Act. Any matter in dispute that is submitted for arbitration shall be heard by a single arbitrator chosen by the Parties. The cost of the arbitration, excluding a Party's legal fees and disbursements shall, unless otherwise ordered by the arbitrator or the panel, be borne equally by the Parties. The Lender agrees that the Borrower may, at its discretion, include such other creditors of the Borrower as may be affected by the Bitcoin Exchange Operator error in the foregoing arbitration.''') 
paragraphs.append('''7. GUARANTEE. The Guarantors hereby severally guarantee payment to the Lender of the Loan Amount provided that no sum in excess of one half of the Loan Amount then outstanding, and interest therein as herein provided, calculated from the date demand is made shall be recoverable from  may be recovered from any one of the Guarantors. The Borrower may release any one of the Guarantors without affecting the liability of the remaining Guarantor.''')
paragraphs.append('''8. MISCELLANEOUS PROVISIONS''')
paragraphs.append('''(r) Notices. All notices, requests, demands or other communications by the terms hereof required or permitted to be given by one party to another shall be given electronically at the last known address of any of the parties or as otherwise directed by the parties, in writing.''')
paragraphs.append('''(s) Governing Law. This Agreement shall be interpreted in accordance with the laws of the Province of Nova Scotia and the laws of Canada applicable therein.''')
paragraphs.append('''(t) Electronic Transmissions. This Agreement may be signed in counterparts, and by electronic transmission or facimilie.''')
paragraphs.append('''(u) Time of Essence. Time shall be of the essence of this Agreement and of every part hereof and no extension or variation of this Agreement shall operate as a waiver of this provision.''')
paragraphs.append('''(v) Survival. The representations and warranties herein, and the covenants to act by the parties post-closing shall survive the closing and loan advances contemplated in this Agreement.''')
paragraphs.append('''(w) Entire Agreement. This Agreement shall constitute the entire agreement between the parties hereto with respect to all of the matters herein and this Agreement shall not be amended except by a memorandum in writing signed by all of the parties hereto and any amendment hereof shall be null and void and shall not be binding upon any party which has not given its consent as aforesaid.''') 
paragraphs.append('''(x) Enurement. This Agreement shall enure to the benefit of and be binding upon the parties hereto and their respective heirs, executors, administrators, personal representatives, successors and assigns.''')
paragraphs.append('''IN WITNESS WHEREOF the parties have executed this Agreement as of the day and year first above written.''')
paragraphs.append('''SIGNED, SEALED AND DELIVERED in the presence of''')
paragraphs.append('''<b>BITCOIN REALTY MANAGEMENT LIMITED</b>''')
paragraphs.append('''Lender: <b>%s</b>''' % 'LENDER') 
paragraphs.append('''Bitcoin Address: <b>%s</b>''' % 'BITCOIN_ADDRESS')
paragraphs.append('''GPG Signature: <b>%s</b>''' % 'LENDER')
paragraphs.append('''Devin Podgorski''')
paragraphs.append('''James Sutton''')
    

style = ParagraphStyle(
    name='Normal',
    fontName='Helvetica',
    fontSize=9,
)

parts = []

for paragraph in paragraphs:
    parts.append(Paragraph(paragraph, style))
    parts.append(Spacer(1, 0.2 * inch))
doc.build(parts)
