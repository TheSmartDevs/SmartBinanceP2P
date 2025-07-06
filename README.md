# SmartBinanceP2P - Ultimate Binance P2P API ❤️

![GitHub stars](https://img.shields.io/github/stars/TheSmartDevs/SmartBinanceP2P) ![GitHub license](https://img.shields.io/github/license/TheSmartDevs/SmartBinanceP2P) ![GitHub issues](https://img.shields.io/github/issues/TheSmartDevs/SmartBinanceP2P)

Welcome to **SmartBinanceP2P**, the ultimate, lightning-fast, and **free** API that unlocks Binance's P2P trading platform for everyone! ✅ No 2000 USDT balance or merchant status needed! Developed with ❤️ by **@ISmartCoder**, this open-source gem at [github.com/TheSmartDevs/SmartBinanceP2P](https://github.com/TheSmartDevs/SmartBinanceP2P) empowers developers, traders, and crypto fans to access real-time P2P buy/sell data with unmatched speed and flexibility. Currently hosted on Railway's $5 Hobby Plan at [https://smartbinance-production.up.railway.app/](https://smartbinance-production.up.railway.app/) 🚀.

## 🌟 Features

- **Free Access** ✅: No 2000 USDT or merchant requirements.
- **Blazing Fast** ⚡: Sub-second responses with caching and concurrent requests.
- **Rich Data** 📊: Seller details like prices, payment methods, and completion rates.
- **Flexible Filters** 🔍: Customize by asset, fiat, trade type, and more.
- **Global Support** 🌍: Supports fiat (BDT 🇧🇩, INR, USD, etc.) and crypto (USDT, BTC, ETH, etc.).
- **Reliable** 🛡️: Robust error handling for uninterrupted service.
- **Open Source** ❤️: Transparent code with community contributions.
- **Easy Deployment** 🚀: One-click deploy to Heroku, Render, or Railway.

## 🚀 Getting Started

### Prerequisites ✅

- Python 3.8+
- Git
- `pip` package manager
- Optional: Heroku, Render, or Railway account for cloud deployment

### Installation

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/TheSmartDevs/SmartBinanceP2P.git
   cd SmartBinanceP2P
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Locally**:
   ```bash
   python app.py
   ```
   Access at `http://localhost:5000` ✅.

### Project Structure

```
SmartBinanceP2P/
├── Procfile              # Deployment config 🚀
├── app.py                # Main FastAPI app ❤️
├── requirements.txt      # Python dependencies 📦
├── status.html           # Root endpoint page 🌐
├── README.md             # This file 📖
```

## 📚 API Endpoints

### Base URL
The API is live at [SmartDev-Binance](https://smartbinance-production.up.railway.app/) ✅.

### 1. Root Endpoint (`GET /`)
Displays a status page (`status.html`).

**Example**:
```bash
curl https://smartbinance-production.up.railway.app/
```

**Response**: HTML status page ✅.

---

### 2. Health Check (`GET /health`)
Verify API health and runtime info.

**Example**:
```bash
curl https://smartbinance-production.up.railway.app/health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-06T08:49:00.123456",
  "version": "2.0.0",
  "cache_size": 0,
  "uptime": 1623456789.123
}
```

---

### 3. P2P Data (`GET /api/v1/p2p`)
Fetch P2P buy/sell offers with customizable filters.

**Parameters**:
| Parameter              | Type   | Default | Description                                                                 |
|------------------------|--------|---------|-----------------------------------------------------------------------------|
| `asset`                | String | USDT    | Crypto asset (e.g., USDT, BTC, ETH) ✅                                      |
| `pay_type`             | String | BDT     | Fiat currency (e.g., BDT 🇧🇩, INR, USD) ✅                                  |
| `pay_method`           | String | ALL     | Payment method (e.g., BKASH, UPI, BANK) ✅                                  |
| `trade_type`           | String | SELL    | Trade type (BUY or SELL) ✅                                                 |
| `limit`                | Integer| 100     | Number of results (max 1000) ✅                                             |
| `sort_by`              | String | price   | Sort by: price, completion_rate, available_amount, monthly_orders ✅         |
| `order`                | String | asc     | Sort order: asc or desc ✅                                                  |
| `min_completion_rate`  | Float  | None    | Min seller completion rate (0-100) ✅                                       |
| `min_orders`           | Integer| None    | Min monthly orders by seller ✅                                             |
| `online_only`          | Boolean| false   | Filter for online merchants only ✅                                         |

**Example**:
```bash
curl "https://smartbinance-production.up.railway.app/api/v1/p2p?asset=USDT&pay_type=BDT&pay_method=BKASH&trade_type=BUY&limit=10&sort_by=price&order=asc"
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "123456789",
      "seller_name": "TraderX",
      "price": 110.5,
      "fiat_unit": "BDT",
      "available_amount": 500.0,
      "min_order_amount": 1000.0,
      "max_order_amount": 50000.0,
      "completion_rate": 98.5,
      "monthly_orders": 150,
      "payment_methods": ["bKash"],
      "user_type": "merchant",
      "online_status": "online"
    },
    ...
  ],
  "count": 10,
  "total_found": 25,
  "total_sellers": 25,
  "time_taken": 0.235,
  "trade_type": "BUY",
  "api_dev": "@ISmartCoder",
  "updates_channel": "t.me/TheSmartDev",
  "statistics": {
    "avg_price": 112.3,
    "min_price": 110.5,
    "max_price": 115.0,
    "total_available": 2500.0
  },
  "parameters": {
    "asset": "USDT",
    "pay_type": "BDT",
    "pay_method": "BKASH",
    "trade_type": "BUY",
    "limit": 10,
    "sort_by": "price",
    "order": "asc",
    "filters_applied": {}
  },
  "timestamp": "2025-07-06T08:49:00.123456",
  "cache_status": "served"
}
```

---

### 4. Payment Methods (`GET /api/v1/p2p/methods`)
List fiat currencies and payment methods.

**Example**:
```bash
curl https://smartbinance-production.up.railway.app/api/v1/p2p/methods
```

**Response**:
```json
{
  "success": true,
  "data": {
    "BDT": {
      "BKASH": "bKash",
      "NAGAD": "Nagad",
      "ROCKET": "Rocket",
      "UPAY": "Upay",
      "BANK": "BANK"
    },
    ...
  },
  "timestamp": "2025-07-06T08:49:00.123456"
}
```

---

### 5. Supported Currencies (`GET /api/v1/p2p/currencies`)
List crypto assets, fiat currencies, and trade types.

**Example**:
```bash
curl https://smartbinance-production.up.railway.app/api/v1/p2p/currencies
```

**Response**:
```json
{
  "success": true,
  "data": {
    "crypto_assets": ["USDT", "BTC", "ETH", "BNB", "BUSD", "ADA", "DOT", "MATIC", "SHIB", "DOGE"],
    "fiat_currencies": ["BDT", "INR", "PKR", "USD", "EUR", "GBP", "AED", "SAR", "TRY", "RUB", ...],
    "trade_types": ["BUY", "SELL"]
  },
  "total_currencies": 21,
  "total_assets": 10,
  "timestamp": "2025-07-06T08:49:00.123456"
}
```

## 🛠️ Supported Assets & Currencies

### Crypto Assets ✅
- USDT, BTC, ETH, BNB, BUSD, ADA, DOT, MATIC, SHIB, DOGE

### Fiat Currencies & Payment Methods ✅
| Fiat | Payment Methods                              |
|------|----------------------------------------------|
| BDT 🇧🇩 | bKash, Nagad, Rocket, Upay, BANK          |
| INR  | UPI, IMPS, Paytm, PhonePe, GooglePay, BANK  |
| USD  | Wise, Paypal, BANK, Zelle                   |
| EUR  | SEPA, Wise, BANK                            |
| ...  | Check `/api/v1/p2p/methods` for all ✅       |

## ⚙️ Deployment 🚀

Deploy instantly with one click or follow the tutorials. The API is currently hosted on Railway's $5 Hobby Plan at [https://smartbinance-production.up.railway.app/](https://smartbinance-production.up.railway.app/) ✅.

### One-Click Deployment ✅

| Platform | Deploy Button |
|----------|---------------|
| **Heroku** | [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TheSmartDevs/SmartBinanceP2P) |
| **Render** | [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/TheSmartDevs/SmartBinanceP2P) |
| **Railway** | [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/TheSmartDevs/SmartBinanceP2P) |

> **Railway Note** ⚠️: Update `Procfile` to `start: python3 app.py` (not `python3 app.py`) for Railway's Nix environment. See Railway tutorial below.

### Deployment Tutorials

#### Heroku Deployment ✅
1. Install Heroku CLI: [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
2. Log in:
   ```bash
   heroku login
   ```
3. Clone repo and navigate to folder.
4. Create app:
   ```bash
   heroku create my-smartbinancep2p
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```
6. Scale:
   ```bash
   heroku ps:scale web=1
   ```
7. Open:
   ```bash
   heroku open
   ```

#### Render Deployment ✅
1. Sign up at [Render](https://render.com).
2. Create Web Service, connect `TheSmartDevs/SmartBinanceP2P`.
3. Configure:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `python app.py`
   - **Instance**: Free or paid
4. Deploy and access URL ✅.

#### Railway Deployment ✅
1. Sign up at [Railway](https://railway.app).
2. Create project, select "Deploy from GitHub."
3. Connect `TheSmartDevs/SmartBinanceP2P`.
4. Update `Procfile`:
   - Change `python3 app.py` to:
     ```
     start: python3 app.py
     ```
   - Commit:
     ```bash
     git add Procfile
     git commit -m "Update Procfile for Railway"
     git push origin main
     ```
5. Configure:
   - **Start Command**: `start: python3 app.py`
   - Add `PORT` env variable (e.g., `5000`).
6. Deploy and access URL ✅.

#### Local Deployment ✅
For testing:
```bash
python app.py
```
Access: `http://localhost:5000` ✅.

## 🔧 Configuration

- **Cache Duration** ⏱️: Set `CACHE_DURATION` in `app.py` (default: 30s).
- **Logging** 📜: Adjust logging in `app.py` for debug/production.
- **Limits** 📏: Max 1000 results per request for performance ✅.

## 🤝 Contributing ❤️

We love contributions! To join:

1. Fork the repo.
2. Create branch: `git checkout -b feature/my-feature`.
3. Commit: `git commit -m "Add my feature"`.
4. Push: `git push origin feature/my-feature`.
5. Open Pull Request.

See [Code of Conduct](https://github.com/TheSmartDevs/SmartBinanceP2P/blob/main/CODE_OF_CONDUCT.md).

## 📢 Community

- **Updates** 📣: Join [t.me/TheSmartDev](https://t.me/TheSmartDev) ✅.
- **Issues** 🐞: Report bugs at [GitHub Issues](https://github.com/TheSmartDevs/SmartBinanceP2P/issues).
- **Discussions** 💬: Chat at [GitHub Discussions](https://github.com/TheSmartDevs/SmartBinanceP2P/discussions).

## 📝 License

MIT License. See [LICENSE](https://github.com/TheSmartDevs/SmartBinanceP2P/blob/main/LICENSE).

## 🙌 Acknowledgments

- Built by **@ISmartCoder** with ❤️.
- Powered by [FastAPI](https://fastapi.tiangolo.com/), [aiohttp](https://docs.aiohttp.org/), and community ❤️.
- Dedicated to making Binance P2P accessible for all ✅.

---

⭐ **Star us** on [GitHub](https://github.com/TheSmartDevs/SmartBinanceP2P) to support! ❤️  
💬 Join [Telegram](https://t.me/TheSmartDev) for updates and help ✅.

