import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
 
 
########################################################################
class LetterMaker(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, pdf_file, org, seconds):
        self.c = canvas.Canvas(pdf_file, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter
        self.organization = org
        self.seconds  = seconds
 
 
    #----------------------------------------------------------------------
    def createDocument(self):
        """"""
        voffset = 65
 
        # create return address
        address = """<font size="9">
        Jack Spratt<br/>
        222 Ioway Blvd, Suite 100<br/>
        Galls, TX 75081-4016</font>
        """
        p = Paragraph(address, self.styles["Normal"])        
 
        # add a logo and size it
#        logo = Image("")
#        logo.drawHeight = 2*inch
#        logo.drawWidth = 2*inch
##        logo.wrapOn(self.c, self.width, self.height)
##        logo.drawOn(self.c, *self.coord(140, 60, mm))
##        
 
#        data = [[p, logo]]
#        table = Table(data, colWidths=4*inch)
#        table.setStyle([("VALIGN", (0,0), (0,0), "TOP")])
#        table.wrapOn(self.c, self.width, self.height)
#        table.drawOn(self.c, *self.coord(18, 60, mm))
 
        Story = []
        timestamp = time.ctime()
        ptext = """
        <b>THIS LOAN AGREEMENT</b> made as of %s
        <b>BETWEEN:</b>
        <b>BITCOIN REALTY MANAGEMENT LIMITED</b>, a body corporate incorporated under the laws of the Province of Nova Scotia, Canada
        """ % timestamp 
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.c, self.width-170, self.height)
        p.drawOn(self.c, *self.coord(20, voffset, mm))

        t=Preformatted(text,normalStyle,newLinesChars=>)#maxLineLength=80)
        # insert body of letter
        ptext = "Dear Sir or Madam:"
        self.createParagraph(ptext, 20, voffset+35)
 
        ptext = """
        The document you are holding is a set of requirements for your next mission, should you
        choose to accept it. In any event, this document will self-destruct <b>%s</b> seconds after you
        read it. Yes, <b>%s</b> can tell when you're done...usually.
        """ % (self.seconds, self.organization)
        p = Paragraph(ptext, self.styles["Normal"])
        p.wrapOn(self.c, self.width-170, self.height)
        p.drawOn(self.c, *self.coord(20, voffset+48, mm))
 
#text='''
#<p><b>THIS LOAN AGREEMENT</b> made as of %s</p>
#<p><b>BETWEEN:</b></p>
#<p><b>BITCOIN REALTY MANAGEMENT LIMITED</b>, a body corporate incorporated under the laws of the Province of Nova Scotia, Canada</p> 
#
#(the \"Borrower\")
#OF THE FIRST PART
#    - and -
#
#[INSERT BITCOIN ADDRESS or GPG Signature]
#    
#(the \"Lender\")
#OF THE SECOND PART
#
#- and -
#
#DEVIN PODGORSKI
#    
#(\"Devin\")
#OF THE THIRD PART
#
#JAMES SUTTON
#    
#(\"James\" and collectively, with Devin, the \"Guarantors\")
#OF THE FORTH PART
#
#
#
#    WHEREAS the Lender has agreed to provide financing to the Borrower (the \"Loan\");
#
#    AND WHEREAS the Guarantors have agreed to guarantee the Loan in accordance with the terms hereof;
#
#    THEREFORE in consideration of the mutual covenants and agreements herein contained, the sum of One Dollar ($1.00) and other good and valuable consideration, the receipt and sufficiency of which is hereby acknowledged, the parties covenant and agree as follows:
#1. INTERPRETATION
#(a) Definitions. In this Agreement, unless the context otherwise requires the following terms shall have the following meanings:
#\"Agreement\" means this agreement and any amendments, schedules and supplements thereto that are agreed on by the parties in writing from time to time;
#
#\"Bitcoin Amount\" means the amount of [auto-populate quantity] bitcoins, to be advanced by the Lender to the Borrower in accordance with the terms of this Agreement.
#
#\"Closing Date\" means the date of this Agreement;
#
#\"Interest Rate\" means an annual interest rate of 9.30 percent;
#
#\"Loan Amount\" means the amount advanced by the Lender to the Borrower, expressed in Canadian Dollars and determined in accordance with Sections 2(b)(ii) and (iii) hereof; and
#    
#\"Term\" means twenty five years.
#    
#(b) Currency Conversion. Any conversion of bitcoin to Canadian Dollars, or Canadian Dollars to bitcoin, shall be done in accordance with Section 4 hereof.
#2. LOAN TO THE BORROWER
#(c) Agreement to Lend.  Subject to the terms and conditions of this Agreement, the Lender agrees to lend to the Borrower the Loan Amount. 
#(d) Advance. The loan advance shall be made in accordance with the following terms:
#(i) Advance. The Lender will advance the Bitcoin Amount to the Borrower, in a single advance on the Closing Date without set-off, holdbacks or other deductions.
#(ii) Conversion to Loan Amount. The Borrower shall convert the Bitcoin Amount to Canadian Dollars within 2 business days of receipt thereof (the \"Conversion Date\").
#(iii) Exchange Statement. Within 2 business days of the Conversion Date, the Borrower will provide an exchange statement to the Lender setting out the Loan Amount (expressed in Canadian Dollars), together with notice of the applicable bitcoin exchange rate at the time of conversion of the Bitcoin Amount (the \"Exchange Statement\"). The Loan Amount, as set out in the Exchange Statement, shall be conclusive evidence of the indebtedness of the Borrower to the Lender. 
#3. Promise to Repay. The Borrower promises to repay the Loan Amount in accordance with the terms of this Agreement.
#(e) Place of Payment.  All amounts due under this Agreement shall be paid to Lender by electronic transmission and shall be deemed to have been paid in Halifax, Province of Nova Scotia, Canada.
#(f) Interest Adjustment Date: The Interest Adjustment Date shall be the first day of the month immediately following the Loan advance. In addition to any other payments required pursuant to section 3(c), interest from the Conversion Date to the Interest Adjustment Date shall be payable in bitcoin on the seventh business day of the first calendar month following the Interest Adjustment Date.
#(g) Payment.  Equal monthly payments of principal and interest based on the Term shall be calculated in Canadian Dollars as of the first day of each calendar month (each such amount being a \"Payment Amount\"). Subject to this section 3, the Payment Amount shall be payable in bitcoin on the seventh business day of each calendar month commencing on the seventh business day of the calendar month immediately following the Interest Adjustment Date.
#(h) Conversion. On the fifth business day of each month (each, a \"Repayment Conversion Date\") the Borrower shall convert the Payment Amount into bitcoin at the then current bitcoin exchange rate (the \"Bitcoin Exchange Rate\").
#(i) Prepayment. The Borrower may prepay any or all of the Loan Amount at its absolute discretion provided that any such prepayment shall be made in bitcoin and shall be converted in accordance with section 3 hereof (the \"Prepayment Amount\").
#(j) Expenses. Any expenses incurred by the Borrower to convert any Payment Amount or Prepayment amount into bitcoin shall be for the expense of the Borrower.
#(k) Reduction of Loan Amount. Following any payments hereunder, the Loan Amount shall be reduced by the applicable Payment Amount or Prepayment Amount, as determined in Canadian Dollars at the applicable Repayment Conversion Date.
#4. CONVERSION. Any conversion of Canadian Dollars into bitcoin or bitcoin into Canadian Dollars pursuant to this Agreement shall be completed in accordance with the following terms and conditions:
#(l) Bitcoin Exchange Operator. The Borrower may determine, at its absolute discretion, which bitcoin exchange operator (the \"Bitcoin Exchange Operator\") completes the conversion of any amounts payable hereunder.
#(m) Expenses. All expenses for any conversion shall be for the account of the Borrower.
#(n) Determination Final. The Lender shall be deemed to accept (i) the posted exchange rate used by the Bitcoin Exchange Operator for the conversion of the Payment Amount to bitcoin; and (ii) any and all Exchange Fees, as determined by the Bitcoin Exchange Operator together with any third party fees reasonably necessary to complete the conversion of any payable amounts hereunder.
#5. COVENANTS, REPRESENTATIONS AND WARRANTIES
#(o) Borrower. The Borrower covenants and agrees with and represents and warrants to the Lender (and acknowledges and confirms that the Lender is relying on such covenants, agreements, representations and warranties in connection with entering this Agreement and in connection with the financing to be provided pursuant hereto by the Lender to the Borrower) that as of the date of this Agreement, and as of the Closing Date, and as of the time of the loan advance hereunder and throughout the period during which any part of the Loan Amount advanced to the Borrower remains outstanding as follows:
#(i) The Borrower is and will continue to be a body corporate duly incorporated and organized and validly subsisting in good standing under the laws of the Province of Nova Scotia.  The Borrower has and will continue to have the corporate power to own property and to carry on the Business, is and will be duly qualified as a company to do business and is and will be in good standing in each jurisdiction in which the nature of the business makes such qualification necessary.
#(ii) The entering into of this Agreement and the carrying out of the transactions contemplated hereby have been duly authorized by all necessary corporate action and will not result in the violation of any of the terms and provisions of the constituting documents or articles of association of the Borrower or any indenture or other agreement, written or oral, to which the Borrower may be a party or otherwise bound.
#(iii) The Borrower has all requisite power and authority which has been properly exercised to enter into this Agreement, to carry out the transactions herein provided for and to perform its obligations under this Agreement.
#(iv) The Borrower shall take or cause to be taken all necessary or desirable actions, steps and corporate proceedings to approve or authorize validly and effectively the execution and delivery of this Agreement and all other arrangements and documents contemplated hereby and shall cause all necessary meetings of directors of the Borrower to be held for such purpose.
#(v) The Borrower will duly and punctually pay or cause to be paid to the Lender the principal Loan Amount pursuant to and in accordance with the terms of this Agreement.
#(p) Confidentiality. In the event that any governmental or quasi-governmental authority with jurisdiction over the Loan (a \"Governing Authority\") requires the disclosure of any information concerning any party hereto, the Parties agree to cooperative with such Governing Authority to the extent required by law, and agrees that no information required by such Governing Authority in the possession of the disclosing party will be confidential with respect to such Governing Authority.
#(q) Survival of Representations, Warranties and Covenants. The obligations, representations and warranties contained in this Agreement, in any document to be executed and delivered pursuant to this Agreement and in any documents executed and delivered in connection with the completion of the transaction contemplated herein shall survive the closing of such transaction notwithstanding any investigations made by or on behalf of the parties hereto.
#6. DEFAULT. Notwithstanding anything to the contrary contained herein, the principal Loan Amount advanced  shall, at the option of the Lender, become immediately due and payable in each and every of the following events:
#(i) if the Borrower makes any default in the payment of any indebtedness or obligation to the Lender or defaults in repayment of the principal Loan Amount payable under this Agreement and such default is not remedied within ten (10) days of the Borrower receiving notice in writing from the Lender of the default;
#(ii) if the Borrower fails to perform or observe any covenant or obligation contained herein, and such default is not remedied within ten (10) days of the Borrower receiving notice in writing from the Lender of the default;
#(iii) if the Borrower becomes insolvent or bankrupt or subject to provisions of the Bankruptcy and Insolvency Act or goes into liquidation, either voluntarily or under an order by a court of competent jurisdiction, or makes a general assignment for the benefit of its creditors or otherwise acknowledges itself insolvent; and 
#(iv) if the Borrower abandons its undertaking or ceases or threatens to cease to carry on Business or threatens to commit any act of bankruptcy.
#Provided that it shall not be an Event of Default if an inability to make any payment required pursuant to this Agreement is a result of an error incurred by a Bitcoin Exchange Operator. Should such a delay occur, the parties will negotiate alternative payment options. In the event that the parties are unable to agree on an alternative payment method, either Party may refer the matter to arbitration by providing the other Party with a notice to proceed to arbitrate (\"Notice of Arbitration\"). Upon either Party providing a Notice of Arbitration, the matter (or such matters as remain in dispute, if the Parties agree they have resolved some but not all of the original dispute) shall not later than thirty (30) days from issuance of the Notice of Arbitration be submitted to final and binding arbitration in accordance with the Nova Scotia Commercial Arbitration Act. Any matter in dispute that is submitted for arbitration shall be heard by a single arbitrator chosen by the Parties. The cost of the arbitration, excluding a Party's legal fees and disbursements shall, unless otherwise ordered by the arbitrator or the panel, be borne equally by the Parties. The Lender agrees that the Borrower may, at its discretion, include such other creditors of the Borrower as may be affected by the Bitcoin Exchange Operator error in the foregoing arbitration. 
#7. GUARANTEE. The Guarantors hereby severally guarantee payment to the Lender of the Loan Amount provided that no sum in excess of one half of the Loan Amount then outstanding, and interest therein as herein provided, calculated from the date demand is made shall be recoverable from  may be recovered from any one of the Guarantors. The Borrower may release any one of the Guarantors without affecting the liability of the remaining Guarantor.
#8. MISCELLANEOUS PROVISIONS
#(r) Notices. All notices, requests, demands or other communications by the terms hereof required or permitted to be given by one party to another shall be given electronically at the last known address of any of the parties or as otherwise directed by the parties, in writing.
#
#(s) Governing Law. This Agreement shall be interpreted in accordance with the laws of the Province of Nova Scotia and the laws of Canada applicable therein.
#
#(t) Electronic Transmissions. This Agreement may be signed in counterparts, and by electronic transmission or facimilie.
#(u) Time of Essence. Time shall be of the essence of this Agreement and of every part hereof and no extension or variation of this Agreement shall operate as a waiver of this provision.
#(v) Survival. The representations and warranties herein, and the covenants to act by the parties post-closing shall survive the closing and loan advances contemplated in this Agreement.
#(w) Entire Agreement. This Agreement shall constitute the entire agreement between the parties hereto with respect to all of the matters herein and this Agreement shall not be amended except by a memorandum in writing signed by all of the parties hereto and any amendment hereof shall be null and void and shall not be binding upon any party which has not given its consent as aforesaid.  
#(x) Enurement. This Agreement shall enure to the benefit of and be binding upon the parties hereto and their respective heirs, executors, administrators, personal representatives, successors and assigns.
#IN WITNESS WHEREOF the parties have executed this Agreement as of the day and year first above written.
#
#SIGNED, SEALED AND DELIVERED    BITCOIN REALTY MANAGEMENT LIMITED 
#in the presence of              )                                                   )
#                        )   Per:                    
#                        )   Name:   
#                        )   Title:
#                        )
#                        )       [INSERT LENDER NAME/IDENTIFIER]
#                        )   
#                        )                       
#                        )   GPG Signature
#                        )
#                        )
#                        )                       
#                        )   Devin Podgorski
#                        )
#                        )
#                        )                       
#                        )   James Sutton
#    ''' % formatted_time
    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y    
 
    #----------------------------------------------------------------------
    def createParagraph(self, ptext, x, y, style=None):
        """"""
        if not style:
            style = self.styles["Normal"]
        p = Paragraph(ptext, style=style)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))
 
    #----------------------------------------------------------------------
    def savePDF(self):
        """"""
        self.c.save()   
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    doc = LetterMaker("files/example.pdf", "The MVP", 10)
    doc.createDocument()
    doc.savePDF()

