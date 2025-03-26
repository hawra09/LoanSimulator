import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


pd.set_option('display.max_rows', None)
def amortized_loan(loan_amount, interest_rate, loan_term_year, loan_term_month, compounding_frequency, payback_frequency, extra_payment):
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

    if period_rate == 0:
        period_rate = 0
        payment = loan_amount / number_payments
    else:
        numerator = loan_amount * period_rate * math.exp(number_payments * math.log1p(period_rate))
        denominator = math.exp(number_payments * math.log1p(period_rate)) - 1
        payment = numerator / denominator
    print(f"Your payment per period ({payback_frequency}) is: ${payment:.2f}.")

    #no extra payments
    loan_amount_no_extra = loan_amount
    remaining_balance_no_extra = loan_amount_no_extra
    interest_paid_no_extra = 0
    principal_paid_no_extra = 0


    #extra payments
    loan_amount_extra = loan_amount
    remaining_balance_extra = loan_amount_extra
    interest_paid_extra = 0
    principal_paid_extra = 0

    amortization_data = []

    #without extra payment
    for i in range(1, int(number_payments) + 1):
        #no extra payments
        if remaining_balance_no_extra > 0:
            beginning_balance_no_extra = remaining_balance_no_extra  # Beginning balance is the remaining balance from the previous period
            interest_paid_no_extra = beginning_balance_no_extra * period_rate
            principal_paid_no_extra = payment - interest_paid_no_extra
            remaining_balance_no_extra -= principal_paid_no_extra

        else:
            interest_no_extra = principal_no_extra = 0

        #extra payments
        if remaining_balance_extra > 0:
            beginning_balance_extra = remaining_balance_extra  # Beginning balance is the remaining balance from the previous period
            interest_paid_extra = beginning_balance_extra * period_rate
            remaining_balance_extra -= extra_payment
            principal_paid_extra = payment - interest_paid_extra
        else:
            interest_paid_extra = principal_paid_extra = 0

        amortization_data.append({'Payment Number': i,
                                  'Ending Balance No Extra': remaining_balance_no_extra,
                                  'Interest No Extra': interest_paid_no_extra,
                                  'Principal No Extra': principal_paid_no_extra,
                                  'Ending Balance Extra': remaining_balance_extra,
                                  'Interest Extra': interest_paid_extra,
                                  'Principal Extra': principal_paid_extra,
                                  })
    amortization_data = pd.DataFrame(amortization_data)

    print(amortization_data)
    return amortization_data


def amortization_plot(amortization_data):
    fig, axes = plt.subplots(2,2, figsize=(8,8))
    fig.suptitle('Visualization: Amortization Analysis', fontsize=16, fontweight='bold')
    #first plot
    sns.lineplot(data=amortization_data, x='Payment Number', y='Ending Balance No Extra', ax=axes[0,0], label='Ending Balance No Extra')
    sns.lineplot(data=amortization_data, x='Payment Number', y='Ending Balance Extra', ax=axes[0, 0], label='Ending Balance No Extra')
    axes[0,0].set_title('End Balance Over Time')
    axes[0, 0].legend(loc='upper left')

    #second plot
    amortization_data.plot.bar(x='Payment Number', y=['Interest No Extra', 'Principal No Extra'], stacked=True, ax=axes[0,1])
    x_ticks = (range(0, amortization_data['Payment Number'].iloc[-1]+1, 10))
    axes[0,1].set_xticks(x_ticks)
    axes[0,1].set_xticklabels([str(i) for i in x_ticks])
    axes[0,1].legend(loc='upper right', bbox_to_anchor=(1.3,1))
    axes[0,1].set_title('Total Interest and Principal Paid Over Time')

    #third plot
    amortization_data['Cumulative Interest No Extra'] = amortization_data['Interest No Extra'].cumsum()
    amortization_data['Cumulative Principal No Extra'] = amortization_data['Principal No Extra'].cumsum()
    amortization_data['Cumulative Interest Extra'] = amortization_data['Interest Extra'].cumsum()
    amortization_data['Cumulative Principal Extra'] = amortization_data['Principal Extra'].cumsum()

    axes[1, 0].plot(amortization_data['Payment Number'], amortization_data['Cumulative Interest No Extra'],
                    label='Interest No Extra')
    axes[1, 0].plot(amortization_data['Payment Number'], amortization_data['Cumulative Principal No Extra'],
                    label='Principal No Extra')
    axes[1, 0].plot(amortization_data['Payment Number'], amortization_data['Cumulative Interest Extra'],
                    label='Interest Extra')
    axes[1, 0].plot(amortization_data['Payment Number'], amortization_data['Cumulative Principal Extra'],
                    label='Principal Extra')
    axes[1, 0].set_title('Cumulative Interest and Principal Paid')
    axes[1, 0].legend(loc='upper left')

    #fourth plot
    Interest_No_Extra_Sum = amortization_data['Interest No Extra'].sum()
    Interest_Extra_Sum = amortization_data['Interest Extra'].sum()
    axes[1, 1].pie([Interest_No_Extra_Sum, Interest_Extra_Sum], labels=['Interest No Extra', 'Interest Extra'])
    plt.tight_layout()
    plt.show()

def export_amortization_data(amortization_data, filename='amortization.csv'):
    amortization_data.to_csv(filename, index='False')
    print(f'Data has been exported to {filename}')

amortized_data = amortized_loan(
    loan_amount=100000,
    loan_term_year=10,
    loan_term_month=0,
    interest_rate =6,
    compounding_frequency = 'Biweekly',
    payback_frequency= 'Every Half Month',
    extra_payment=500
)
export_amortization_data(amortized_data)
amortization_plot(amortized_data)
