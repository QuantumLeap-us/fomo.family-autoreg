# FOMO Family Waitlist Registration Tool

This tool automates the registration process for the FOMO Family waitlist

## 🔗 Referral Link

Join the waitlist using this link:
[https://fomo.family/waitlist?ref_id=DSNDSJ97Q](https://fomo.family/waitlist?ref_id=DSNDSJ97Q)

## 🚀 Quick Start

1. **Install dependencies:**

   Make sure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

2. **Add proxy servers:**

   Add your proxy servers to `proxies.txt`, one per line, in the following format:

   ```
   http://username:password@host:port
   ```

3. **Run the script:**

   Execute the script with:

   ```bash
   python register.py
   ```

## ⚙️ Configuration

- **Referral Code:** Update the `referral_code` variable in `register.py` with your referral code.
- **Delay:** Adjust the delay between requests by modifying `random.uniform(3, 7)`.
- **Retries:** Change the `max_retries` parameter to set the number of retry attempts.

## 🔧 Features

- Automatic email generation
- Proxy support
- Request retry mechanism
- Progress tracking
- Success rate monitoring

## 📝 Notes

- Use high-quality proxies for better success rates.
- Set appropriate delays to avoid rate limiting.
- Private proxies are recommended over public ones.
- Regularly check proxy availability.

## 🛡️ Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with applicable terms of service and regulations.
