# Copyright @ISmartCoder
# Updates Channel: https://t.me/TheSmartDev
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import aiohttp
import asyncio
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import time
from functools import wraps
import threading
from datetime import datetime
import os  

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

BINANCE_API_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
HEADERS = {
    "Content-Type": "application/json",
    "clienttype": "web",
    "lang": "en",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

cache = {}
cache_lock = threading.Lock()
CACHE_DURATION = 30

PAYMENT_METHODS = {
    "BHD": {
        "BANK": "BANK",
        "BBK": "Bank of Bahrain and Kuwait B.S.C.",
        "DENIZBANK": "DenizBank A.Ş. Bahrain",
        "AIC": "The Arab Investment Company S.A.A.",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "AED": {
        "BANK": "BANK",
        "CIB": "CIB",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "SAR": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "EGP": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "JOD": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "KWD": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "LBP": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "MAD": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "OMR": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "QAR": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "TND": {
        "BANK": "BANK",
        "CASHU": "CashU",
        "MONEYGRAM": "MoneyGram"
    },
    "BDT": {
        "BKASH": "bKash",
        "NAGAD": "Nagad",
        "ROCKET": "Rocket",
        "UPAY": "Upay",
        "BANK": "BANK"
    },
    "INR": {
        "UPI": "UPI",
        "IMPS": "IMPS",
        "PAYTM": "Paytm",
        "PHONEPE": "PhonePe",
        "GPAY": "GooglePay",
        "BANK": "BANK"
    },
    "PKR": {
        "EASYPAISA": "EasyPaisa",
        "JAZZCASH": "JazzCash",
        "BANK": "BANK"
    },
    "USD": {
        "WISE": "Wise",
        "PAYPAL": "Paypal",
        "BANK": "BANK",
        "ZELLE": "Zelle"
    },
    "EUR": {
        "SEPA": "SEPA",
        "WISE": "Wise",
        "BANK": "BANK"
    },
    "GBP": {
        "FASTERPAYMENTS": "FasterPayments",
        "WISE": "Wise",
        "BANK": "BANK"
    },
    "TRY": {
        "BANK": "BANK",
        "PAPARA": "Papara",
        "ZIRAAT": "ZiraatBank"
    },
    "RUB": {
        "BANK": "BANK",
        "TINKOFF": "TinkoffBank",
        "SBERBANK": "Sberbank"
    },
    "NGN": {
        "BANK": "BANK",
        "OPAY": "Opay",
        "PALMPAY": "PalmPay"
    },
    "KES": {
        "MPESA": "M-Pesa",
        "BANK": "BANK"
    },
    "ZAR": {
        "BANK": "BANK",
        "CAPITEC": "Capitec",
        "FNB": "FNB"
    },
    "PHP": {
        "GCASH": "GCash",
        "PAYMAYA": "PayMaya",
        "BANK": "BANK"
    },
    "THB": {
        "BANK": "BANK",
        "PROMPTPAY": "PromptPay"
    },
    "MYR": {
        "BANK": "BANK",
        "TOUCHNGO": "TouchNGo"
    },
    "SGD": {
        "BANK": "BANK",
        "PAYNOW": "PayNow"
    },
    "HKD": {
        "BANK": "BANK",
        "FPS": "FPS"
    },
    "JPY": {
        "BANK": "BANK"
    },
    "KRW": {
        "BANK": "BANK"
    },
    "CNY": {
        "BANK": "BANK",
        "ALIPAY": "Alipay",
        "WECHAT": "WeChatPay"
    },
    "VND": {
        "BANK": "BANK",
        "MOMO": "MoMo",
        "ZALOPAY": "ZaloPay"
    },
    "IDR": {
        "BANK": "BANK",
        "GOPAY": "GoPay",
        "OVO": "OVO",
        "DANA": "DANA"
    },
    "BRL": {
        "BANK": "BANK",
        "PIX": "Pix"
    },
    "ARS": {
        "BANK": "BANK",
        "MERCADOPAGO": "MercadoPago"
    },
    "CLP": {
        "BANK": "BANK"
    },
    "COP": {
        "BANK": "BANK",
        "NEQUI": "Nequi",
        "DAVIPLATA": "DaviPlata"
    },
    "MXN": {
        "BANK": "BANK",
        "SPEI": "SPEI"
    },
    "PEN": {
        "BANK": "BANK",
        "YAPE": "Yape",
        "PLIN": "Plin"
    },
    "GHS": {
        "BANK": "BANK",
        "MTN": "MTN Mobile Money",
        "VODAFONE": "Vodafone Cash"
    },
    "UGX": {
        "BANK": "BANK",
        "AIRTEL": "Airtel Money",
        "MTN": "MTN Mobile Money"
    },
    "TZS": {
        "BANK": "BANK",
        "MPESA": "M-Pesa",
        "TIGO": "Tigo Pesa"
    },
    "LRD": {
        "BANK": "BANK",
        "MOOV": "Moov Money"
    },
    "SLL": {
        "BANK": "BANK",
        "ORANGE": "Orange Money"
    },
    "GMD": {
        "BANK": "BANK",
        "QMoney": "QMoney"
    },
    "MRO": {
        "BANK": "BANK"
    },
    "CVE": {
        "BANK": "BANK"
    }
}

CRYPTO_ASSETS = ["USDT", "BTC", "ETH", "BNB", "BUSD", "ADA", "DOT", "MATIC", "SHIB", "DOGE"]

def get_cache_key(params):
    return f"{params.get('asset', 'USDT')}_{params.get('pay_type', 'BDT')}_{params.get('trade_type', 'SELL')}_{params.get('pay_method', 'ALL')}_{params.get('limit', '100')}"

def cache_response(duration=CACHE_DURATION):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = get_cache_key(kwargs.get('request').query_params)
            current_time = time.time()
            
            with cache_lock:
                if cache_key in cache:
                    cached_data, timestamp = cache[cache_key]
                    if current_time - timestamp < duration:
                        logger.info(f"Cache hit for {cache_key}")
                        return cached_data
                
                keys_to_remove = [
                    key for key, (_, timestamp) in cache.items()
                    if current_time - timestamp > duration
                ]
                for key in keys_to_remove:
                    del cache[key]
            
            result = await func(*args, **kwargs)
            
            with cache_lock:
                cache[cache_key] = (result, current_time)
            
            return result
        return wrapper
    return decorator

async def fetch_page_async(session, asset, fiat, trade_type, pay_method, page, rows=20):
    payload = {
        "asset": asset,
        "fiat": fiat,
        "tradeType": trade_type,
        "page": page,
        "rows": rows,
        "payTypes": [pay_method] if pay_method and pay_method != "ALL" else [],
        "publisherType": None,
        "merchantCheck": False
    }
    
    try:
        async with session.post(BINANCE_API_URL, headers=HEADERS, json=payload, timeout=15) as response:
            if response.status != 200:
                logger.error(f"Error fetching page {page}: {response.status}")
                return []
            
            data = await response.json()
            return data.get('data', [])
    except asyncio.TimeoutError:
        logger.error(f"Timeout fetching page {page}")
        return []
    except Exception as e:
        logger.error(f"Exception fetching page {page}: {e}")
        return []

async def fetch_all_sellers_async(asset, fiat, trade_type, pay_method, max_results=1000):
    connector = aiohttp.TCPConnector(
        limit=30,
        limit_per_host=15,
        ttl_dns_cache=300,
        use_dns_cache=True
    )
    timeout = aiohttp.ClientTimeout(total=45)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        pages_needed = min((max_results // 20) + 1, 50) 
        
        logger.info(f"Fetching {pages_needed} pages concurrently...")
        
        tasks = [
            fetch_page_async(session, asset, fiat, trade_type, pay_method, page)
            for page in range(1, pages_needed + 1)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_sellers = []
        for result in results:
            if isinstance(result, list):
                all_sellers.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Task failed: {result}")
        
        logger.info(f"Fetched {len(all_sellers)} total sellers")
        return all_sellers[:max_results]

def process_sellers_data(sellers, filters=None):
    processed = []
    filters = filters or {}
    
    for ad in sellers:
        try:
            adv = ad.get('adv', {})
            advertiser = ad.get('advertiser', {})
            
            if not adv or not advertiser:
                continue
            
            payment_methods = []
            for method in adv.get('tradeMethods', []):
                method_name = method.get('tradeMethodName', '')
                payment_methods.append(method_name)
            
            if filters.get('min_completion_rate'):
                completion_rate = advertiser.get('monthFinishRate', 0) * 100
                if completion_rate < filters['min_completion_rate']:
                    continue
            
            if filters.get('min_orders'):
                if advertiser.get('monthOrderCount', 0) < filters['min_orders']:
                    continue
            
            if filters.get('online_only') and advertiser.get('userType') != 'merchant':
                continue
            
            processed_seller = {
                "id": adv.get('advNo', ''),
                "seller_name": advertiser.get("nickName", "Unknown"),
                "price": float(adv.get('price', 0)),
                "fiat_unit": adv.get('fiatUnit', ''),
                "available_amount": float(adv.get('surplusAmount', 0)),
                "min_order_amount": float(adv.get('minSingleTransAmount', 0)),
                "max_order_amount": float(adv.get('maxSingleTransAmount', 0)),
                "completion_rate": round(advertiser.get('monthFinishRate', 0) * 100, 2),
                "monthly_orders": advertiser.get('monthOrderCount', 0),
                "payment_methods": payment_methods,
                "user_type": advertiser.get('userType', 'user'),
                "online_status": "online" if advertiser.get('userType') == 'merchant' else "offline"
            }
            
            processed.append(processed_seller)
            
        except Exception as e:
            logger.error(f"Error processing seller: {e}")
            continue
    
    return processed

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("status.html", "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="status.html file not found")
    except Exception as e:
        logger.error(f"Error reading status.html: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "cache_size": len(cache),
        "uptime": time.time()
    }

@app.get("/api/v1/p2p")
@cache_response(30)
async def get_p2p_data(request: Request):
    start_time = time.time()  
    try:
        params = request.query_params
        asset = params.get('asset', 'USDT').upper()
        pay_type = params.get('pay_type', 'BDT').upper()
        pay_method = params.get('pay_method', 'ALL').upper()
        trade_type = params.get('trade_type', 'SELL').upper()
        limit = int(params.get('limit', 100))
        sort_by = params.get('sort_by', 'price').lower()
        order = params.get('order', 'asc').lower()
        
        min_completion_rate = params.get('min_completion_rate')
        min_orders = params.get('min_orders')
        online_only = params.get('online_only', 'false').lower() == 'true'

        if limit > 1000:
            raise HTTPException(
                status_code=400,
                detail="Sorry Max Limit Exceeded. Maximum limit is 1000."
            )
        
        limit = min(limit, 1000)  
        
        if asset not in CRYPTO_ASSETS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported asset. Supported: {', '.join(CRYPTO_ASSETS)}"
            )
        
        if trade_type not in ['BUY', 'SELL']:
            raise HTTPException(
                status_code=400,
                detail="trade_type must be BUY or SELL"
            )
        
        if pay_type not in PAYMENT_METHODS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported pay_type. Supported: {', '.join(PAYMENT_METHODS.keys())}"
            )
        
        if pay_method != 'ALL' and pay_method not in PAYMENT_METHODS[pay_type]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid pay_method for {pay_type}. Supported: {', '.join(PAYMENT_METHODS[pay_type].keys())}"
            )
        
        api_pay_method = PAYMENT_METHODS[pay_type].get(pay_method) if pay_method != 'ALL' else None
        
        filters = {}
        if min_completion_rate:
            filters['min_completion_rate'] = float(min_completion_rate)
        if min_orders:
            filters['min_orders'] = int(min_orders)
        if online_only:
            filters['online_only'] = True
        
        logger.info(f"Fetching P2P data: {asset}/{pay_type} - {trade_type} - {pay_method}")
        
        sellers = await fetch_all_sellers_async(asset, pay_type, trade_type, api_pay_method, limit)
        
        if not sellers:
            return {
                "success": False,
                "message": "No sellers found",
                "data": [],
                "count": 0,
                "total_sellers": 0,
                "time_taken": round(time.time() - start_time, 3),
                "trade_type": trade_type,
                "api_dev": "@ISmartCoder",
                "updates_channel": "t.me/TheSmartDev",
                "parameters": {
                    "asset": asset,
                    "pay_type": pay_type,
                    "pay_method": pay_method,
                    "trade_type": trade_type
                }
            }
        
        processed_sellers = process_sellers_data(sellers, filters)
        
        reverse = order == 'desc'
        sort_keys = {
            'price': lambda x: x['price'],
            'completion_rate': lambda x: x['completion_rate'],
            'available_amount': lambda x: x['available_amount'],
            'monthly_orders': lambda x: x['monthly_orders']
        }
        
        if sort_by in sort_keys:
            processed_sellers.sort(key=sort_keys[sort_by], reverse=reverse)
        
        limited_sellers = processed_sellers[:limit]
        
        stats = {
            "avg_price": round(sum(s['price'] for s in limited_sellers) / len(limited_sellers), 2) if limited_sellers else 0,
            "min_price": min(s['price'] for s in limited_sellers) if limited_sellers else 0,
            "max_price": max(s['price'] for s in limited_sellers) if limited_sellers else 0,
            "total_available": sum(s['available_amount'] for s in limited_sellers)
        }
        
        return {
            "success": True,
            "data": limited_sellers,
            "count": len(limited_sellers),
            "total_found": len(processed_sellers),
            "total_sellers": len(processed_sellers), 
            "time_taken": round(time.time() - start_time, 3),  
            "trade_type": trade_type, 
            "api_dev": "@ISmartCoder",  
            "updates_channel": "t.me/TheSmartDev",  
            "statistics": stats,
            "parameters": {
                "asset": asset,
                "pay_type": pay_type,
                "pay_method": pay_method,
                "trade_type": trade_type,
                "limit": limit,
                "sort_by": sort_by,
                "order": order,
                "filters_applied": filters
            },
            "timestamp": datetime.now().isoformat(),
            "cache_status": "served"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter value: {str(e)}")
    except Exception as e:
        logger.error(f"Error in get_p2p_data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/p2p/methods")
async def get_payment_methods():
    return {
        "success": True,
        "data": PAYMENT_METHODS,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/p2p/currencies")
async def get_supported_currencies():
    return {
        "success": True,
        "data": {
            "crypto_assets": CRYPTO_ASSETS,
            "fiat_currencies": list(PAYMENT_METHODS.keys()),
            "trade_types": ["BUY", "SELL"]
        },
        "total_currencies": len(PAYMENT_METHODS),
        "total_assets": len(CRYPTO_ASSETS),
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "available_endpoints": [
                "/api/v1/p2p",
                "/api/v1/p2p/methods",
                "/api/v1/p2p/currencies",
                "/health"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
