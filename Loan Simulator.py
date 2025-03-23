import math


def amortized_loan(loan_amount, interest_rate, loan_term_year, loan_term_month, compounding_frequency, payback_frequency):

    global payments_per_year, m

    interest_rate =interest_rate/100

    loan_months = (loan_term_year*12) + loan_term_month

    #establishing compounded frequency based on selection
    if compounding_frequency == 'Annually (APR)':
        m = 1
    elif compounding_frequency == 'Semi-annually':
        m = 2
    elif compounding_frequency == 'Quarterly':
        m = 4
    elif compounding_frequency == 'Monthly':
        m = 12
    elif compounding_frequency == 'Semi-monthly':
        m = 24
    elif compounding_frequency == 'Weekly':
        m = 52
    elif compounding_frequency == 'Biweekly':
        m = 26

    #establishing payback_frequency based on selection
    if payback_frequency == 'Every Year':
        payments_per_year = 1
    elif payback_frequency == 'Every 6 Months':
        payments_per_year = 2
    elif payback_frequency == 'Every Quarter':
        payments_per_year = 4
    elif payback_frequency == 'Every Month':
        payments_per_year = 12
    elif payback_frequency == 'Every Half Month':
        payments_per_year = 24


    number_payments = (loan_months/12) * payments_per_year
    period_rate = (1 + interest_rate / m) ** (m / payments_per_year) - 1

    # Calculate periodic interest rate
    if period_rate == 0:
        period_rate = 0
    else:
        period_rate = (1+interest_rate/m) ** (m/payments_per_year) -1

    if period_rate == 0:
        payment = loan_amount / number_payments
    else:
        numerator = loan_amount * period_rate * math.exp(number_payments * math.log1p(period_rate))
        denominator = math.exp(number_payments * math.log1p(period_rate)) - 1
        payment = numerator / denominator

    print(f"Your payment per period ({payback_frequency}) is: ${payment:.2f}")

amortized_loan(
    loan_amount=100000,
    loan_term_year=10,
    loan_term_month=0,
    interest_rate =6,
    compounding_frequency = 'Biweekly',
    payback_frequency= 'Every Half Month'
)