import pandas as pd
from datetime import timedelta, datetime
import argparse


def calculate_daily_balance(payment, start_date, end_date, start_balance, annual_interest_rate, payment_day=16):
    # Create initial dataframe with one row
    df = pd.DataFrame(index=[pd.to_datetime(start_date)])
    df.index.name = 'date'
    df['balance'] = start_balance
    df['interest'] = 0
    df['payment'] = 0

    # Calculate daily interest rate
    daily_rate = (1 + annual_interest_rate) ** (1 / 365) - 1

    next_work_day_is_payment_day = False

    # Continue until balance is less than payment or until end_date
    current_date = pd.to_datetime(start_date)
    while (end_date is None and df.loc[current_date, 'balance'] >= payment) or \
          (end_date is not None and current_date < pd.to_datetime(end_date)):
        current_date += pd.DateOffset(days=1)  # Move to the next day
        df.loc[current_date, 'interest'] = df.loc[current_date - pd.DateOffset(days=1), 'balance'] * daily_rate
        df.loc[current_date, 'payment'] = 0.0
        if current_date.day == payment_day or next_work_day_is_payment_day:
            if current_date.weekday() < 5:  # If it's a payment day and a working day
                df.loc[current_date, 'payment'] = payment
                next_work_day_is_payment_day = False
            else:
                next_work_day_is_payment_day = True
        new_balance = df.loc[current_date - pd.DateOffset(days=1), 'balance'] + df.loc[current_date, 'interest'] - df.loc[current_date, 'payment']
        df.loc[current_date, 'balance'] = new_balance

    return df


def find_monthly_payment(start_date, end_date, start_balance, annual_interest_rate, payment_day=16, epsilon=1):
    lower_payment = 0
    upper_payment = start_balance  # This is obviously too high

    while upper_payment - lower_payment > epsilon:
        mid_payment = (upper_payment + lower_payment) / 2
        print(f'Trying {mid_payment}')
        df = calculate_daily_balance(mid_payment, start_date, end_date, start_balance, annual_interest_rate, payment_day)
        if df.loc[end_date, 'balance'] > 0:  # Mid payment is too low
            lower_payment = mid_payment
        else:  # Mid payment is too high
            upper_payment = mid_payment

    return (upper_payment + lower_payment) / 2


def aggregate_by_month(df):
    # Resample to get sum of payments and interest for each month
    monthly_df = df.resample('M').sum()

    # Find the payment day for each month
    payment_days = df[df['payment'] > 0].resample('M').last()

    # Replace the balance in the monthly dataframe with the balance on the payment day
    monthly_df['balance'] = payment_days['balance']

    return monthly_df


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():
    parser = argparse.ArgumentParser(description='Simulate a mortgage loan and calculate daily or monthly balances.')
    parser.add_argument('start_date', type=valid_date, help='Start date of the loan in YYYY-MM-DD format')
    parser.add_argument('start_balance', type=float, help='Start balance of the loan')
    parser.add_argument('interest', type=float, help='Annual interest rate as a decimal')
    parser.add_argument('--monthly', action='store_true', help='Output monthly rows instead of daily rows')
    parser.add_argument('--monthly-payment', type=float, help='Monthly payment amount')
    parser.add_argument('--end-date', type=valid_date, help='End date of the loan in YYYY-MM-DD format')
    parser.add_argument('--payment-day', default=16, type=int, help='Day of the month on which payments are made')

    args = parser.parse_args()

    if args.end_date is not None:
        if args.start_date >= args.end_date:
            parser.error('End date must be after start date')
        if not 0 <= args.interest < 1:
            parser.error('Interest rate must be a decimal between 0 and 1')
    elif args.monthly_payment is None:
        parser.error('Specify either end date or a monthly payment amount')

    # Call your functions here with the arguments, for example:
    # find_monthly_payment(args.start_date, args.end_date, start_balance, args.interest)
    monthly_payment = args.monthly_payment if args.monthly_payment else find_monthly_payment(
        start_date=args.start_date,
        end_date=args.end_date,
        start_balance=args.start_balance,
        annual_interest_rate=args.interest,
        payment_day=args.payment_day,
    ) if args.monthly_payment is None else args.monthly_payment
    print(f'Monthly payment = {monthly_payment}')
    df = calculate_daily_balance(
        monthly_payment,
        start_date=args.start_date,
        end_date=args.end_date,
        start_balance=args.start_balance,
        annual_interest_rate=args.interest,
        payment_day=args.payment_day,
    )

    if args.monthly:
        df = aggregate_by_month(df)

    df.to_csv('mortgage.csv')


if __name__ == '__main__':
    main()

