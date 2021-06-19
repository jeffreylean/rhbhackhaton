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
            "Commercial Services": 0,
            "Communications": 1,
            "Consumer Durables": 2,
            "Consumer Non-Durables": 3,
            "Consumer Services": 4,
            "Distribution Services": 5,
            "Electronic Technology": 6,
            "Energy Minerals": 7,
            "Finance": 8,
            "Health Services": 9,
            "Health Technology": 10,
            "Industrial Services": 11,
            "Miscellaneous": 12,
            "Non-Energy Minerals": 13,
            "Process Industries": 14,
            "Producer Manufacturing": 15,
            "Retail Trade": 16,
            "Technology Services": 17,
            "Transportation": 18,
            "Utilities": 19,
        }
    )
    # data1['Loan Status'] = data1['Loan Status'].str[0].str.upper().map(
    # {'P': 0, 'F': 1, 'L': 2, 'D': 3})
    data1 = data1.fillna(0)
    processedinputs = data1
    return processedinputs


def calculate_score(
    loandefaultpred, interest_rate, market_trend, loan_amount, configuration
):
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
