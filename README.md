#  EGX Stock Breakout Detection (Python Project)

This project analyzes historical stock data from the **Egyptian Exchange (EGX)** to **predict breakout opportunities** before they happen. It uses technical indicators like **Z-Score**, **ATR**, **volume spikes**, and **volatility ratio** to rate breakout signals on a confidence scale of 1 to 5.

---

##  How It Works

- **Cleans the dataset**: removes summary rows like “Highest”, “Change”, etc.
- **Calculates**:
  - Price vs. 5-day high (breakout detection)
  - Z-score (momentum)
  - Volume spike vs. 5-day average
  - Volatility ratio (current vs. historical std)
  - ATR-to-price ratio (user input)
- **Final Score**: Gives a signal strength from 1 to 5 based on indicators

---

##  Input Requirements

- A `.csv` file with **at least 56 rows**
- Must include columns:
  - `Date`
  - `Price` (closing price)
  - `Vol.` (daily volume)

>  Designed for files exported from **Investing.com** for EGX stocks.

---

##  How to Run

```bash
python breakout.py
You will be prompted to:

Enter your CSV file path
(e.g. C:/Users/YourName/Desktop/stockdata.csv)

Enter today’s ATR manually

 Sample Output

Today volume: 2,000,000
5-day average volume: 1,200,000
Breakout likely to happen!
Z-score: 1.1
Volatility ratio: 1.3
Confidence score: 4/5
📌 Notes
This script is tailored for EGX (Egyptian Exchange) data

Built using Python 3.11.0, pandas, and math

#Made by Youssef Soliman
