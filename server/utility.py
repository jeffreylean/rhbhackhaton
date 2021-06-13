from pandas import DataFrame


def vectorize(inputArray):
    data1 = DataFrame(
        inputArray,
        columns=[
            "Current Balance",
            "Total Payment",
            "Premise Type",
            "Core Business Type",
            "Number of Staff",
            "Loan Term",
            "Collateral Type",
            "Collateral Value",
            "Installment",
        ],
    )
    data1["Premise Type"] = (
        data1["Premise Type"].str[0].str.upper().map({"R": 0, "O": 1})
    )
    data1["Collateral Type"] = (
        data1["Collateral Type"]
        .str[0]
        .str.upper()
        .map({"F": 0, "P": 1, "G": 2, "O": 3})
    )
    data1["Core Business Type"] = data1["Core Business Type"].map(
        {
            "Retail": 0,
            "Wholesale": 1,
            "Construction": 2,
            "Warehousing": 3,
            "Information Services": 4,
            "Transportation": 5,
            "Accommodation and catering": 6,
            "Leasing and business services": 7,
            "Real estate development and management": 8,
            "Software and information technology": 9,
        }
    )
    # data1['Loan Status'] = data1['Loan Status'].str[0].str.upper().map(
    # {'P': 0, 'F': 1, 'L': 2, 'D': 3})
    data1 = data1.fillna(0)
    processedinputs = data1
    return processedinputs


def calculate_score(loandefaultpred, interest_rate, market_trend, loan_amount):
    # target loan amount
    max_loan = 2500000
    amount_risk = (loan_amount / max_loan) * 100

    if amount_risk > 50:
        loanrisk = 100
    else:
        loanrisk = amount_risk

    # loan default
    if loandefaultpred == 1:
        predpercentage = 100
    else:
        predpercentage = (amount_risk / 50) * 100

    if interest_rate > 13:
        interestrisk = 100
    elif interest_rate > 9 and interest_rate <= 13:
        interestrisk = 75
    else:
        interestrisk = (amount_risk / 50) * 100

    finalscore = (predpercentage / 60) + ((loanrisk + interestrisk + market_trend) / 40)
    return finalscore
