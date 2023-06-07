# Mortgage Simulator

This is a Python program that simulates a mortgage loan and calculates daily or monthly balances, payments, and interest.

## Limitations

It currently only works for mortgages where the interest is calculated daily. In fact that is why I wrote this program because
other mortgage calculators assumed interest was calculated monthly.

## Usage

To run the program, use the following command:

```plaintext
python mortgage_simulator.py START_DATE START_BALANCE INTEREST [--monthly] [--monthly-payment MONTHLY_PAYMENT] [--end-date END_DATE] [--payment-day PAYMENT_DAY]
```

- `START_DATE` should be the start date of the loan in the format `YYYY-MM-DD`.
- `START_BALANCE` is the starting balance of the loan.
- `INTEREST` is the annual interest rate as a decimal.
- The `--monthly` flag is optional. If present, the program will output monthly rows instead of daily rows.
- `MONTHLY_PAYMENT` is an optional argument that specifies the monthly payment amount.
- `END_DATE` is an optional argument that specifies the end date of the loan in the format `YYYY-MM-DD`.
- `PAYMENT_DAY` is an optional argument that specifies the day of the month on which payments are made. By default, it's set to the 16th day of the month.

Either `MONTHLY_PAYMENT` or `END_DATE` must be supplied.

The program will output a CSV file to stdout, with columns for date, balance, interest, and payment amount.

For example, to simulate a loan from January 1, 2023 with a starting balance of $200,000, an annual interest rate of 5%, a monthly payment of $1500, and output daily rows, you would run:

```plaintext
python mortgage_simulator.py 2023-01-01 200000 0.05 --monthly-payment 1500
```

To output monthly rows instead, you would add the `--monthly` flag:

```plaintext
python mortgage_simulator.py 2023-01-01 200000 0.05 --monthly --monthly-payment 1500
```

Output is written to the file mortgage.csv.

## Acknowledgments

This program was made with help from [ChatGPT](https://openai.com/research/chatgpt), an AI developed by OpenAI. You can view the conversation that led to the creation of this program [here](https://chat.openai.com/share/59e5a3e3-8cda-4018-aa4c-b7afa6f5bf60).

## License

[MIT](https://choosealicense.com/licenses/mit/)
