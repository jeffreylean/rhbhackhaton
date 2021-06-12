from pandas import DataFrame


def vectorize(inputArray):
    data1 = DataFrame(inputArray, columns=['Current Balance',
                                           'Total Payment', 'Premise Type', 'Core Business Type',
                                           'Number of Staff', 'Loan Term', 'Collateral Type', 'Collateral Value', 'Interest Rate', 'Installment'])
    data1['Premise Type'] = data1['Premise Type'].str[0].str.upper().map({
        'R': 0, 'O': 1})
    data1['Collateral Type'] = data1['Collateral Type'].str[0].str.upper().map(
        {'F': 0, 'P': 1, 'G': 2, 'O': 3})
    data1['Core Business Type'] = data1['Core Business Type'].map({'Retail': 0, 'Wholesale': 1, 'Construction': 2, 'Warehousing': 3, 'Information Services': 4, 'Transportation': 5,
                                                                  'Accommodation and catering': 6, 'Leasing and business services': 7, 'Real estate development and management': 8, 'Software and information technology': 9})
    # data1['Loan Status'] = data1['Loan Status'].str[0].str.upper().map(
    # {'P': 0, 'F': 1, 'L': 2, 'D': 3})
    data1 = data1.fillna(0)
    processedinputs = data1
    return processedinputs
