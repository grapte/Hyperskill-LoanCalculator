import argparse, math

# Create the ArgumentParser object
parser = argparse.ArgumentParser(description="Calculate loan details.")

# Add arguments
parser.add_argument('--payment', type=float, help='Monthly payment amount')
parser.add_argument('--principal', type=float, help='Principal loan amount')
parser.add_argument('--periods', type=int, help='Number of payment periods')
parser.add_argument('--interest', type=float, help='Loan interest rate as a percentage')
parser.add_argument('--type', choices=['annuity', 'diff'], help='Type of payment: "annuity" or "diff"')

# Parse the arguments
args = parser.parse_args()

payment, principal, periods, interest, mode = args.payment, args.principal, args.periods, args.interest, args.type


def annuity(payment, principal, periods, interest):
    i = (interest * 0.01) / 12

    if not principal:
        principal = p = payment / ((i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1))
        print(f'Your loan principal = {principal}')
    elif not periods:
        n = math.log(payment / (payment - i * principal), 1 + i)
        fractional, periods = math.modf(n)
        if fractional:
            periods += 1
        if periods == 1:
            print('It will take 1 month to repay the loan')
        else:
            years, months = divmod(periods, 12)
            if months != 0 and years == 0:
                print(f'It will take {months} months to repay the loan')
            elif months == 0 and years != 0:
                print(f'It will take {years} years to repay the loan')
            elif months != 0 and years != 0:
                print(f'It will take {years} years and {months} months to repay this loan')
    elif not payment:
        a = principal * (i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1)

        fractional, payment = math.modf(a)
        if fractional != 0:
            payment, remain = payment + 1, (principal - (payment + 1) * (periods - 1))
            print(f'Your monthly payment = {payment} and the last payment = {remain}.')
        else:
            print(f'Your monthly payment = {payment}')


def differentiated(principal, periods, interest):
    p = principal
    n = periods
    i = (interest * 0.01) / 12
    total = 0
    for m in range(1, n + 1):
        d = p/n + i * (p - (p*(m-1))/n)
        d = math.ceil(d)
        total += d
        print(f'Month {m}: payment is {d}')
    print(f'Overpayment = {total - principal}')


def valid_annuity_args():
    none_args = [None for a in [payment, principal, periods] if a is None]
    return len(none_args) == 1


if mode == 'annuity' and valid_annuity_args() and interest:
    annuity(payment, principal, periods, interest)
elif mode == 'diff' and not payment and principal and periods and interest:
    differentiated(principal, periods, interest)
else:
    print('Incorrect parameters')
