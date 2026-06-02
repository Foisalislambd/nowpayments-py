# NOWPayments API — Full Reference

> Consolidated from official Postman exports (`docs/raw/`) and package docs.
> Production: `https://api.nowpayments.io` · Sandbox: `https://api-sandbox.nowpayments.io`

## Table of contents

1. [Overview & authentication](#overview--authentication)
2. [SDK method checklist](#sdk-method-checklist)
3. [Endpoint reference (Postman)](#endpoint-reference-postman)
4. [IPN (webhooks)](#ipn-webhooks)
5. [Links](#links)

---

## Overview & authentication

> Source: https://documenter.getpostman.com/view/7907941/2s93JusNJt
> Last Updated: March 2025

## Overview

NOWPayments is a non-custodial cryptocurrency payment processing platform. Accept payments in 300+ cryptos with auto-conversion to your preferred currency.

- **Base URL (Production)**: `https://api.nowpayments.io`
- **Base URL (Sandbox)**: `https://api-sandbox.nowpayments.io`
- **API Version**: v1

## Authentication

All API requests require the `x-api-key` header with your API key.

```
x-api-key: YOUR_API_KEY
```

## API Products

- **Payment API** - Integrate crypto payments into your service
- **Mass Payouts API** - Initiate thousands of transactions in a single call
- **Custody API** - Manage funds within custody balance
- **Customer Management API** - Manage customer accounts & balances
- **Recurring Payments API** - Crypto subscriptions & billing
- **Fiat Withdrawals API** - Accept crypto, settle in fiat

---

**Headers (typical):**

| Header | When |
|--------|------|
| `x-api-key` | Almost all requests |
| `Content-Type: application/json` | POST/PATCH bodies |
| `Authorization: Bearer <jwt>` | Payouts, custody, some lists (JWT from `POST /v1/auth`, expires in 5 min) |

---

## SDK method checklist

> Maps each API route to `nowpayments-node` methods (same coverage in other SDKs).

Based on Postman exports in [`raw/copied-docs.md`](./raw/copied-docs.md). ✅ = implemented in this package.

### Auth & Status

| API | Method | Package | Notes |
|-----|--------|---------|-------|
| GET /v1/status | getStatus | ✅ `getStatus()` | |
| POST /v1/auth | getAuthToken | ✅ `getAuthToken(email, password)` | Returns JWT (expires 5 min) |

### Currencies

| API | Method | Package | Notes |
|-----|--------|---------|-------|
| GET /v1/currencies | getCurrencies | ✅ `getCurrencies(fixedRate?)` | fixed_rate param optional |
| GET /v1/full-currencies | getFullCurrencies | ✅ `getFullCurrencies()` | Detailed currency info |
| GET /v1/currencies/{currency} | getCurrency | ✅ `getCurrency(currency)` | |
| GET /v1/merchant/coins | getMerchantCoins | ✅ `getMerchantCoins(fixedRate?)` | Coins from dashboard settings |

### Payments

| API | Method | Package | Notes |
|-----|--------|---------|-------|
| GET /v1/min-amount | getMinAmount | ✅ `getMinAmount(params)` | + fiat_equivalent, is_fixed_rate, is_fee_paid_by_user |
| POST /v1/payment/:id/update-merchant-estimate | updatePaymentEstimate | ✅ | |
| GET /v1/estimate | getEstimatePrice | ✅ | |
| POST /v1/payment | createPayment | ✅ | |
| GET /v1/payment/:id | getPaymentStatus | ✅ | |
| GET /v1/payment/ | getPayments | ✅ `getPayments(params?, jwtToken?)` | JWT recommended |

### Invoices

| API | Method | Package |
|-----|--------|---------|
| POST /v1/invoice | createInvoice | ✅ |
| POST /v1/invoice-payment | createInvoicePayment | ✅ |

### Payouts (JWT required)

| API | Method | Package | Notes |
|-----|--------|---------|-------|
| POST /v1/payout | createPayout | ✅ `createPayout(params, jwtToken)` | |
| POST /v1/payout/:id/verify | verifyPayout | ✅ `verifyPayout(id, verificationCode, jwtToken)` | 2FA code in body |
| POST /v1/payout/w_id/cancel | cancelPayout | ✅ `cancelPayout(id, jwtToken)` | Cancel scheduled payout |
| GET /v1/payout/fee | getPayoutFee | ✅ `getPayoutFee(currency, amount)` | Network fee estimate |
| GET /v1/payout/:id | getPayoutStatus | ✅ `getPayoutStatus(id, jwtToken?)` | |
| GET /v1/payout | getPayouts | ✅ `getPayouts(params?)` | |
| POST /v1/payout/validate-address | validatePayoutAddress | ✅ | |

### Fiat Payouts (JWT required)

| API | Method | Package |
|-----|--------|---------|
| GET /v1/fiat-payouts/crypto-currencies | getFiatPayoutsCryptoCurrencies | ✅ `getFiatPayoutsCryptoCurrencies(params?, jwtToken?)` |
| GET /v1/fiat-payouts/payment-methods | getFiatPayoutsPaymentMethods | ✅ `getFiatPayoutsPaymentMethods(params?, jwtToken?)` |
| GET /v1/fiat-payouts | getFiatPayouts | ✅ `getFiatPayouts(params?, jwtToken?)` |

### Balance & Custody

| API | Method | Package |
|-----|--------|---------|
| GET /v1/balance | getBalance | ✅ `getBalance(jwtToken?)` |

### Sub-Partner / Custody (JWT for most)

| API | Method | Package |
|-----|--------|---------|
| POST /v1/sub-partner/balance | createSubPartner | ✅ `createSubPartner(name, jwtToken)` |
| POST /v1/sub-partner/payment | createSubPartnerPayment | ✅ `createSubPartnerPayment(params, jwtToken)` |
| GET /v1/sub-partner/balance/:id | getSubPartnerBalance | ✅ |
| GET /v1/sub-partner | getSubPartners | ✅ `getSubPartners(params?, jwtToken?)` |
| GET /v1/sub-partner/transfers | getTransfers | ✅ `getTransfers(params?, jwtToken?)` |
| GET /v1/sub-partner/transfer/:id | getTransfer | ✅ `getTransfer(id, jwtToken?)` |
| POST /v1/sub-partner/transfer | createTransfer | ✅ `createTransfer(params, jwtToken)` |
| POST /v1/sub-partner/write-off | writeOff | ✅ `writeOff(params, jwtToken)` |
| POST /v1/sub-partner/deposit | deposit | ✅ `deposit(params, jwtToken)` |

### Subscriptions (JWT required)

| API | Method | Package | Notes |
|-----|--------|---------|-------|
| GET /v1/subscriptions | getSubscriptions | ✅ `getSubscriptions(params?)` | status, subscription_plan_id, is_active, limit, offset |
| GET /v1/subscriptions/:id | getSubscription | ✅ | |
| DELETE /v1/subscriptions/:id | deleteSubscription | ✅ `deleteSubscription(id, jwtToken?)` | |
| POST /v1/subscriptions | createSubscription | ✅ `createSubscription(params, jwtToken)` | |
| GET /v1/subscriptions/plans | getSubscriptionPlans | ✅ `getSubscriptionPlans(params?)` | limit, offset |
| GET /v1/subscriptions/plans/:id | getSubscriptionPlan | ✅ | |
| PATCH /v1/subscriptions/plans/:id | updateSubscriptionPlan | ✅ | |

### Conversions (JWT required)

| API | Method | Package |
|-----|--------|---------|
| POST /v1/conversion | createConversion | ✅ `createConversion(params, jwtToken)` |
| GET /v1/conversion/:id | getConversionStatus | ✅ `getConversionStatus(id, jwtToken)` |
| GET /v1/conversion | getConversions | ✅ `getConversions(params?, jwtToken?)` |

### IPN & Helpers

| Feature | Package |
|---------|---------|
| verifyIpn / verifyIpnSignature | ✅ |
| createIpnSignature | ✅ |
| isPaymentComplete, getStatusLabel, etc. | ✅ |


---

## Endpoint reference (Postman)

Parsed **42** unique endpoints from raw exports.

## Auth & status

### POST `/v1/auth`

**Authentication**

- **URL:** `https://api.nowpayments.io/v1/auth`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Authentication method for obtaining a JWT token. You should specify your email and password which you are using for signing in into dashboard.
JWT token will be required for creating a payout request. For security reasons, JWT tokens expire in 5 minutes.
Content-Type
application/json
{
    "email": "{{email}}",
    "password": "{{password}}"
}
    "email": "your_email",
    "password": "your_password"
}'
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU4MjYyNTkxMTUiLCJpYXQiOjE2MDUyODgzODQsImV4cCI6MTYwNTI4ODY4NH0.bk8B5AjoTt8Qfm1zHJxutAtgaTGW-2j67waGQ2DUHUI"
}
Custody
This section describes our custody feature.
In order to do that you need:
To show the balance at the frontend you can get it with "GET user balance" method. It will return you an array of user balances you can list in the back office.
For payouts administration you will need to collect funds from your players' balance and withdraw it using payouts API.
```

</details>

### GET `/v1/status`

**Get API status**

- **URL:** `https://api.nowpayments.io/v1/status`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This is a method to get information about the current state of the API. If everything is OK, you will receive an "OK" message. Otherwise, you'll see some error.
{
  "message": "OK"
}
```

</details>

## Balance

### GET `/v1/balance`

**Get balance**

- **URL:** `https://api.nowpayments.io/v1/balance`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This method returns your balance in different currencies.
The response contains a list of currencies with two parameters:
amount - avaliable currency amount;
pendingAmount - currently processing currency amount;
x-api-key
{{your_api_key}}
{
  "eth": {
    "amount": 0.0001817185463659148,
    "pendingAmount": 0
  },
  "trx": {
    "amount": 0,
    "pendingAmount": 0
  },
  "xmr": {
    "amount": 0,
    "pendingAmount": 0
  }
}
```

</details>

## Conversions

### GET `/v1/conversion`

**Get list of conversions**

- **URL:** `https://api.nowpayments.io/v1/conversion`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This endpoint returns you the list of your conversions with the essential info for each one.
You can query only for certain conversions using the following parameters to filter the result:
id: int or array of int (optional) - filter by id of the conversion;
status: string or array of string(optional) - filter conversions by certain status;
from_currency: string(optional) - filter by initial currency of the conversion;
to_currency: string(optional), - filter by outcome currency of the conversion;
created_at_from: Date(optional), - filter by date;
created_at_to: Date(optional) - filter by date;
limit: (optional) default 10 - set the limit of shown results;
offset: (optional) default 0;
order: ASC / DESC (optional) - set the sorting order of provided data;
Authorization
Bearer *your_jwt_token*
{
    "result": [
        {
            "id": "148427051",
            "status": "REJECTED",
            "from_currency": "TRX",
            "to_currency": "ETH",
            "from_amount": 0.1,
            "to_amount": null,
            "created_at": "2023-02-10T13:01:52.521Z",
            "updated_at": "2023-02-10T14:46:22.419Z"
        },
       {
            "id": "2065223244",
            "status": "FINISHED",
            "from_currency": "TRX",
            "to_currency": "ETH",
            "from_amount": 1,
            "to_amount": 0.000041013900000000004,
            "created_at": "2023-02-10T16:38:10.675Z",
            "updated_at": "2023-02-10T16:39:30.308Z"
        },
   ],
    "count": 2
}
Mass payouts
This set of methods will allow you to make payouts from your custody to unlimited number of wallets. Fast and secure.
Recommended payouts requesting flow using API:
Check if your payout address is valid using POST Validate address endpoint;
If it's valid, create a withdrawal using POST Create payout endpoint;
Verify your payout with 2fa (by default it's mandatory) using POST Verify payout endpoint;
2FA automation:
Save the secret key and set it up in your favorite 2FA application as well, otherwise you won't be able to get access to your dashboard!
Please note:
Payouts can be requested only using a whitelisted IP address, and to whitelisted wallet addresses. It's a security measure enabled for each partner account by default.
You can whitelist both of these anytime dropping a formal request using your registration email to partners@nowpayments.io.
For more information about whitelisting you can reach us at partners@nowpayments.io.
```

</details>

### POST `/v1/conversion`

**Create conversion**

- **URL:** `https://api.nowpayments.io/v1/conversion`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This endpoint allows you to create conversions within your custody account.
Parameters:
amount(required) - the amount of your conversion;
from_currency(required) - the currency you're converting your funds from;
to_currency(required) - the currency you're converting your funds to;
The list of available statuses:
WAITING - the conversion is created and waiting to be executed;
PROCESSING - the conversion is in processing;
FINISHED - the conversion is completed;
REJECTED - for some reason, conversion failed;
x-api-key
{{your_api_key}}
Authorization
Bearer *your_jwt_token*
Content-Type
application/json
raw
{
    "amount": 50,
    "from_currency": "usdttrc20",
    "to_currency": "USDTERC20"
}
    "amount": "50",
    "from_currency": "usdttrc20",
    "to_currency": "USDTERC20"
}'
{
  "result": {
    "id": "1327866232",
    "status": "WAITING",
    "from_currency": "USDTTRC20",
    "to_currency": "USDTERC20",
    "from_amount": 50,
    "to_amount": 50,
    "created_at": "2023-03-05T08:18:30.384Z",
    "updated_at": "2023-03-05T08:18:30.384Z"
  }
}
```

</details>

### GET `/v1/conversion/{id}`

**Get conversion status**

- **URL:** `https://api.nowpayments.io/v1/conversion/:conversion_id`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
Authorization
Bearer *your_jwt_token*
PATH VARIABLES
conversion_id
{
  "result": {
    "id": "1327866232",
    "status": "WAITING",
    "from_currency": "USDTTRC20",
    "to_currency": "USDTERC20",
    "from_amount": 50,
    "to_amount": 50,
    "created_at": "2023-03-05T08:18:30.384Z",
    "updated_at": "2023-03-05T08:41:30.201Z"
  }
}
```

</details>

## Currencies

### GET `/v1/currencies`

**Get available currencies**

- **URL:** `https://api.nowpayments.io/v1/currencies`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This is a method for obtaining information about all cryptocurrencies available for payments for your current setup of payout wallets.
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PARAMS
fixed_rate
true
(Optional) Returns avaliable currencies with minimum and maximum amount of the exchange.
{
  "currencies": [
    "btg",
    "eth",
    "xmr",
    "zec",
    "xvg",
    "ada",
    "ltc",
    "bch",
    "qtum",
    "dash",
    "xlm",
    "xrp",
    "xem",
    "dgb",
    "lsk",
    "doge",
    "trx",
    "kmd",
    "rep",
    "bat",
    "ark",
    "waves",
    "bnb",
    "xzc",
    "nano",
    "tusd",
    "vet",
    "zen",
    "grs",
    "fun",
    "neo",
    "gas",
    "pax",
    "usdc",
    "ont",
    "xtz",
    "link",
    "rvn",
    "bnbmainnet",
    "zil",
    "bcd",
    "usdt",
    "usdterc20",
    "cro",
    "dai",
    "ht",
    "wabi",
    "busd",
    "algo",
    "usdttrc20",
... (truncated)
```

</details>

### GET `/v1/full-currencies`

**Get available currencies (2nd method)**

- **URL:** `https://api.nowpayments.io/v1/full-currencies`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This is a method to obtain detailed information about all cryptocurrencies available for payments.
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
"currencies": [
 {
 "id": 121,
 "code": "AAVE",
 "name": "Aave",
 "enable": true,
 "wallet_regex": "^(0x)[0-9A-Fa-f]{40}$",
 "priority": 127,
 "extra_id_exists": false,
 "extra_id_regex": null,
 "logo_url": "/images/coins/aave.svg",
 "track": true,
 "cg_id": "aave",
 "is_maxlimit": false,
 "network": "eth",
 "smart_contract": null,
 "network_precision": null
 }
]
```

</details>

### GET `/v1/merchant/coins`

**Get available checked currencies**

- **URL:** `https://api.nowpayments.io/v1/merchant/coins`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This is a method for obtaining information about the cryptocurrencies available for payments. Shows the coins you set as available for payments in the "coins settings" tab on your personal account.
Optional parameters:
fixed_rate(optional) - boolean, can be true or false. Returns currencies avaliable for fixed rate exchanges with minimum and maximum amount of the exchange.
x-api-key
{{your_api_key}}
{
  "currencies": [
    "btg",
    "eth",
    "xmr",
    "zec",
    "xvg",
    "ada",
    "ltc",
    "bch",
    "qtum",
    "dash",
    "xlm",
    "xrp",
    "xem",
    "dgb",
    "lsk",
    "doge",
    "trx",
    "kmd",
    "rep",
    "bat",
    "ark",
    "waves",
    "bnb",
    "xzc",
    "nano",
    "tusd",
    "vet",
    "zen",
    "grs",
    "fun",
    "neo",
    "gas",
    "pax",
    "usdc",
    "ont",
    "xtz",
    "link",
    "rvn",
    "bnbmainnet",
    "zil",
    "bcd",
    "usdt",
    "usdterc20",
    "cro",
    "dai",
    "ht",
    "wabi",
    "busd",
    "algo",
    "usdttrc20",
    "gt",
    "stpt",
    "ava",
... (truncated)
```

</details>

## Custody & sub-partners

### GET `/v1/sub-partner`

**Get customers**

- **URL:** `https://api.nowpayments.io/v1/sub-partner`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This method returns the entire list of your customers.
AUTHORIZATION
Bearer Token
Token
{{token}}
Authorization
Bearer {{token}}
(Required) Your authorization token
PARAMS
id
int or array of int (optional)
offset
1
(optional) default 0
limit
10
(optional) default 10
order
DESC
ASC / DESC (optional) default ASC
{
  "result": [
    {
      "id": "111394288",
      "name": "test",
      "created_at": "2022-10-06T16:42:47.352Z",
      "updated_at": "2022-10-06T16:42:47.352Z"
    },
    {
      "id": "1515573197",
      "name": "test1",
      "created_at": "2022-10-09T21:56:33.754Z",
      "updated_at": "2022-10-09T21:56:33.754Z"
    }
  ],
  "count": 2
}
```

</details>

### POST `/v1/sub-partner/balance`

**Create new user account**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/balance`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
You can integrate this endpoint into the registration process on your service so upon registration, players will already have dedicated NOWPayments balance as your sub-user.
Name : a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)
AUTHORIZATION
Bearer Token
Token
{{token}}
Authorization
Bearer *your_jwt_token*
Content-Type
application/json
PARAMS
{
    "name": "test1"
}
    "name": "test1"
}'
{
  "result": {
    "id": "1515573197",
    "name": "test1",
    "created_at": "2022-10-09T21:56:33.754Z",
    "updated_at": "2022-10-09T21:56:33.754Z"
  }
}
```

</details>

### GET `/v1/sub-partner/balance/{id}`

**Get customer balance**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/balance/:id`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This request can be made only from a whitelisted IP.
If IP whitelisting is disabled, this request can be made by any user that has an API key.
You can whitelist your IP address in the 'Whitelist IPs' section in 'Whitelist Settings'.
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PATH VARIABLES
id
ID of sub-user for balance request
{
  "result": {
    "subPartnerId": "111394288",
    "balances": {
      "usddtrc20": {
        "amount": 0.7,
        "pendingAmount": 0
      },
      "usdtbsc": {
        "amount": 1.0001341847350678,
        "pendingAmount": 0
      }
    }
  }
}
```

</details>

### POST `/v1/sub-partner/deposit`

**Deposit from your master account**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/deposit`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This is a method for transferring funds from your master account to a user's one.
The actual information about the transfer's status can be obtained via Get transfer method.
The list of available statuses:
CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
AUTHORIZATION
Bearer Token
Token
{{token}}
x-api-key
{{x-api-token}}
Content-Type
application/json
{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403"
}
    "currency": "usddtrc20",
    "amount": 0.7,
    "sub_partner_id": "111394288"
}'
{
    "result": {
        "id": "19649354",
        "from_sub_id": "5209391548", //main account
        "to_sub_id": "111394288", //sub account
        "status": "WAITING",
        "created_at": "2022-10-11T10:01:33.323Z",
        "updated_at": "2022-10-11T10:01:33.323Z",
        "amount": "0.7",
        "currency": "usddtrc20"
    }
}
```

</details>

### POST `/v1/sub-partner/payment`

**Deposit with payment**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/payment`
- **Source:** `copied-docs-2.md`

<details>
<summary>Postman export details</summary>

```
This method allows you to top up a sub-partner account with a general payment.
You can check the actual payment status by using GET 9 Get payment status request.
AUTHORIZATION
Bearer Token
Token
{{token}}
x-api-key
{{x-api-token}}
{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403",
    "fixed_rate": false
}
Deposit with payment
    "currency": "trx",
    "amount": 50,
    "sub_partner_id": "1631380403",
    "fixed_rate": false
}'
{
  "result": {
    "payment_id": "5250038861",
    "payment_status": "waiting",
    "pay_address": "TSszwFcbpkrZ2H85ZKsB6bEV5ffAv6kKai",
    "price_amount": 50,
    "price_currency": "trx",
    "pay_amount": 50,
    "amount_received": 0.0272467,
    "pay_currency": "trx",
    "order_id": null,
    "order_description": null,
    "ipn_callback_url": null,
    "created_at": "2022-10-11T10:49:27.414Z",
    "updated_at": "2022-10-11T10:49:27.414Z",
    "purchase_id": "5932573772",
    "smart_contract": null,
    "network": "trx",
    "network_precision": null,
    "time_limit": null,
    "burning_percent": null,
    "expiration_estimate_date": "2022-10-11T11:09:27.418Z"
  }
}
```

</details>

### POST `/v1/sub-partner/transfer`

**Transfer**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/transfer`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This method allows creating transfers between users' accounts.
You can check the transfer's status using Get transfer method.
The list of available statuses:
CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
AUTHORIZATION
Bearer Token
Token
{{token}}
x-api-key
{{x-api-token}}
Content-Type
application/json
{
    "currency": "trx",
    "amount": 0.3,
    "from_id": 1111111,
    "to_id":  1111111
}
Transfer
    "currency": "trx",
    "amount": 0.3,
    "from_id": 1111111,
    "to_id":  1111111
}'
{
    "result": {
        "id": "327209161",
        "from_sub_id": "111394288", //sub account
        "to_sub_id": "1515573197", //sub account
        "status": "WAITING",
        "created_at": "2022-10-09T22:09:02.181Z",
        "updated_at": "2022-10-09T22:09:02.181Z",
        "amount": "1",
        "currency": "usdtbsc"
    }
}
```

</details>

### GET `/v1/sub-partner/transfer/{id}`

**Get transfer**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/transfer/:id`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Get the actual information about the transfer. You need to provide the transfer ID in the request.
The list of available statuses:
CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
Authorization
Bearer {{token}}
(Required) Your authorization token
PATH VARIABLES
id
{
  "result": {
    "id": "327209161",
    "from_sub_id": "111394288",
    "to_sub_id": "1515573197",
    "status": "FINISHED",
    "created_at": "2022-10-09T22:09:02.181Z",
    "updated_at": "2022-10-09T22:10:01.853Z",
    "amount": "1",
    "currency": "usdtbsc"
  }
}
```

</details>

### GET `/v1/sub-partner/transfers`

**Get all transfers**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/transfers`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
Returns the entire list of transfers created by your users.
The list of available statuses:
CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
Authorization
Bearer *your_jwt_token*
PARAMS
id
int or array of int (optional)
status
CREATED
string or array of string "WAITING"/"CREATED"/"FINISHED"/"REJECTED" (optional)
limit
10
(optional) default 10
offset
1
(optional) default 0
order
ASC
ASC / DESC (optional) default ASC
{
  "result": [
    {
      "id": "111394288",
      "from_sub_id": "5209391548",
      "to_sub_id": "111394288",
      "status": "FINISHED",
      "created_at": "2022-10-09T18:53:21.975Z",
      "updated_at": "2022-10-09T18:55:00.696Z",
      "amount": "1",
      "currency": "usdtbsc"
    },
    {
      "id": "148427051",
      "from_sub_id": "111394288",
      "to_sub_id": "5209391548",
      "status": "FINISHED",
      "created_at": "2022-10-09T19:08:32.440Z",
      "updated_at": "2022-10-09T19:10:01.209Z",
      "amount": "1",
      "currency": "usdtbsc"
    },
    {
      "id": "1631380403",
      "from_sub_id": "5209391548",
      "to_sub_id": "111394288",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:19:51.936Z",
      "updated_at": "2022-10-09T21:21:00.671Z",
      "amount": "2",
```

</details>

### POST `/v1/sub-partner/write-off`

**Write off on your account**

- **URL:** `https://api.nowpayments.io/v1/sub-partner/write-off`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
With this method you can withdraw funds from a user's account and transfer them to your master account.
The actual status of the transaction can be checked with Get transfer method.
The list of available statuses:
CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
AUTHORIZATION
Bearer Token
Token
{{token}}
Authorization
Bearer *your_jwt_token*
Content-Type
application/json
{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403"
}
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403"
}'
{
    "result": {
        "id": "19649354",
        "from_sub_id": "111394288", //sub account
        "to_sub_id": "5209391548", //main account
        "status": "WAITING",
        "created_at": "2022-10-11T10:01:33.323Z",
        "updated_at": "2022-10-11T10:01:33.323Z",
        "amount": "0.7",
        "currency": "usddtrc20"
    }
}
Payouts
This set of methods will allow you to set up fully automated payouts-on-demand for your players.
Recommended payouts requesting flow using API:
Check if your payout address is valid using POST Validate address endpoint;
If it's valid, create a withdrawal using POST Create payout endpoint;
Verify your payout with 2fa (by default it's mandatory) using POST Verify payout endpoint;
2FA automation:
Save the secret key and set it up in your favorite 2FA application as well, otherwise you won't be able to get access to your dashboard!
Please note:
Payouts can be requested only using a whitelisted IP address, and to whitelisted wallet addresses. It's a security measure enabled for each partner account by default.
You can whitelist both of these anytime dropping a formal request using your registration email to partners@nowpayments.io.
For more information about whitelisting you can reach us at partners@nowpayments.io.
```

</details>

## Fiat payouts

### GET `/v1/fiat-payouts`

**Get payouts**

- **URL:** `https://api.nowpayments.io/v1/fiat-payouts`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This enpoint shows you the list of previously created payouts from your account.
Authorization
Bearer *your jwt token*
PARAMS
id
provider
requestId
fiatCurrency
cryptoCurrency
status
filter
provider_payout_id
limit
page
orderBy
sortBy
dateFrom
dateTo
Get payouts
{
  "result": {
    "rows": [
      {
        "id": "12345678909",
        "provider": "transfi",
        "requestId": "1234567890",
        "status": "FINISHED",
        "fiatCurrencyCode": "EUR",
        "fiatAmount": "12.59",
        "cryptoCurrencyCode": "BNBBSC",
        "cryptoCurrencyAmount": "0.067",
        "fiatAccountCode": "sepa_bank",
        "fiatAccountNumber": "1234567890",
        "payoutDescription": null,
        "error": null,
        "createdAt": "2023-10-27T16:25:59.977Z",
        "updatedAt": "2023-10-27T16:25:59.977Z"
      }
    ]
  }
}
Recurring Payments API (Email Subscriptions feature)
Streamline your workflows by assigning payments to your customers on a regular basis with NOWPayments.
This feature involves creating a plan for payments and individual recurring payments for each user.
Be sure to consider the details of repeated and wrong-asset deposits from 'Repeated Deposits and Wrong-Asset Deposits' section when processing payments.
First you need to create a Recurring Payment plan:
```

</details>

### GET `/v1/fiat-payouts/crypto-currencies`

**Get crypto currencies**

- **URL:** `https://api.nowpayments.io/v1/fiat-payouts/crypto-currencies`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This endpoint shows you the list of available crypto currencies for your cashout.
Authorization
Bearer *your_jwt_token*
PARAMS
provider
currency
Get crypto currencies
{
  "result": [
    {
      "provider": "transfi",
      "currencyCode": "USDC",
      "currencyNetwork": "eth",
      "enabled": true
    },
    {
      "provider": "transfi",
      "currencyCode": "USDT",
      "currencyNetwork": "btc",
      "enabled": true
    },
    {
      "provider": "transfi",
      "currencyCode": "USDTERC20",
      "currencyNetwork": "eth",
      "enabled": true
    },
    {
      "provider": "transfi",
      "currencyCode": "USDTTRC20",
      "currencyNetwork": "trx",
      "enabled": true
    }
  ]
}
```

</details>

### GET `/v1/fiat-payouts/payment-methods`

**Get available payment methods**

- **URL:** `https://api.nowpayments.io/v1/fiat-payouts/payment-methods`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This endpoint shows you the list of available payment methods for chosen provider and currency.
Authorization
Bearer *your jwt token*
PARAMS
provider
currency
Get available payment methods
{
    "result": [
        {
            "name": "Bdo Network Bank",
            "paymentCode": "ph_onb",
            "fields": [
                {
                    "name": "accountNumber",
                    "type": "String",
                    "mandatory": true,
                    "description": "Beneficiary account number"
                }
            ],
            "provider": "transfi"
        },
        ************************
        more options here
        ************************
                {
            "name": "Mega Intl Comml Bank Co Ltd",
            "paymentCode": "ph_mega",
            "fields": [
                {
                    "name": "accountNumber",
                    "type": "String",
                    "mandatory": true,
                    "description": "Beneficiary account number"
                }
            ],
            "provider": "transfi"
        }
    ]
}
```

</details>

## Invoices

### POST `/v1/invoice`

**Create invoice**

- **URL:** `https://api.nowpayments.io/v1/invoice`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Creates a payment link. With this method, the customer is required to follow the generated url to complete the payment. Data must be sent as a JSON-object payload.
Request fields:
price_currency (required) - the fiat currency in which the price_amount is specified (usd, eur, etc);
pay_currency (optional) - the specified crypto currency (btc, eth, etc), or one of available fiat currencies if it's enabled for your account (USD, EUR, ILS, GBP, AUD, RON);
If not specified, can be chosen on the invoice_url
ipn_callback_url (optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io";
order_id (optional) - internal store order ID, e.g. "RGDBP-21314";
order_description (optional) - internal store order description, e.g. "Apple Macbook Pro 2019 x 1";
success_url(optional) - url where the customer will be redirected after successful payment;
cancel_url(optional) - url where the customer will be redirected after failed payment;
is_fixed_rate(optional) - boolean, can be true or false. Required for fixed-rate exchanges;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";
is_fee_paid_by_user(optional) - boolean, can be true or false. Required for fixed-rate exchanges with all fees paid by users;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";
SUCCESSFUL RESPONSE FIELDS
Name	Type	Description
id	String	Invoice ID
token_id	String	Internal identifier
order_id	String	Order ID specified in request
order_description	String	Order description specified in request
price_amount	String	Base price in fiat
price_currency	String	Ticker of base fiat currency
pay_currency	String	Currency your customer will pay with. If it's 'null' your customer can choose currency in web interface.
ipn_callback_url	String	Link to your endpoint for IPN notifications catching
invoice_url	String	Link to the payment page that you can share with your customer
success_url	String	Customer will be redirected to this link once the payment is finished
cancel_url	String	Customer will be redirected to this link if the payment fails
partially_paid_url	String	Customer will be redirected to this link if the payment gets partially paid status
payout_currency	String	Ticker of payout currency
created_at	String	Time of invoice creation
updated_at	String	Time of latest invoice information update
is_fixed_rate	Boolean	This parameter is 'True' if Fixed Rate option is enabled and 'false' if it's disabled
is_fee_paid_by_user	Boolean	This parameter is 'True' if Fee Paid By User option is enabled and 'false' if it's disabled
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
Content-Type
application/json
(Required) Your payload has to be JSON object
{
  "price_amount": 1000,
  "price_currency": "usd",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io",
  "partially_paid_url": "https://nowpayments.io",
  "is_fixed_rate": true,
  "is_fee_paid_by_user": false
}
  "price_amount": 1000,
  "price_currency": "usd",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "success_url": "https://nowpayments.io",
```

</details>

### POST `/v1/invoice-payment`

**Create payment by invoice**

- **URL:** `https://api.nowpayments.io/v1/invoice-payment`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Creates payment by invoice. With this method, your customer will be able to complete the payment without leaving your website.
Be sure to consider the details of repeated and wrong-asset deposits from 'Repeated Deposits and Wrong-Asset Deposits' section when processing payments.
Data must be sent as a JSON-object payload.
Required request fields:
iid (required) - invoice id. You can get invoice ID in response of POST Create_invoice method;
order_description (optional) - inner store order description, e.g. "Apple Macbook Pro 2019 x 1";
customer_email (optional) - user email to which a notification about the successful completion of the payment will be sent;
payout_address (optional) - usually the funds will go to the address you specify in your Personal account. In case you want to receive funds on another address, you can specify it in this parameter;
payout_extra_id(optional) - extra id or memo or tag for external payout_address;
payout_currency (optional) - currency of your external payout_address, required when payout_adress is specified;
Here the list of available statuses of payment:
waiting - waiting for the customer to send the payment. The initial status of each payment;
confirming - the transaction is being processed on the blockchain. Appears when NOWPayments detect the funds from the user on the blockchain;
confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations;
sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you;
partially_paid - it shows that the customer sent the less than the actual price. Appears when the funds have arrived in your wallet;
finished - the funds have reached your personal address and the payment is finished;
failed - the payment wasn't completed due to the error of some kind;
refunded - the funds were refunded back to the user;
expired - the user didn't send the funds to the specified address in the 7 days time window;
Please note: when you're creating a fiat2crypto payment you also should include additional header to your request - "origin-ip : xxx", where xxx is your customer IP address.
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
Content-Type
application/json
(Required) Your payload has to be JSON object
{
  "iid": {{invoice_id}},
  "pay_currency": "btc",
  "purchase_id": {{purchase_id}},
  "order_description": "Apple Macbook Pro 2019 x 1",
  "customer_email": "test@gmail.com",
  "payout_address": "0x...",
  "payout_extra_id": null,
  "payout_currency": "usdttrc20"
}
  "iid": {{invoice_id}},
  "pay_currency": "btc",
  "purchase_id": {{purchase_id}},
  "order_description": "Apple Macbook Pro 2019 x 1",
```

</details>

## Payments

### GET `/v1/estimate`

**Get estimated price**

- **URL:** `https://api.nowpayments.io/v1/estimate`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
Currently following fiat currencies are available: USD, EUR, CAD, GBP, AUD, ILS, RON.
Please note that this method allows you to get estimates for crypto pairs as well.
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PARAMS
amount
3999.5000
Set the amount for calculations
currency_from
usd
currency_to
btc
{
  "currency_from": "usd",
  "amount_from": 3999.5,
  "currency_to": "btc",
  "estimated_amount": 0.17061637
}
```

</details>

### GET `/v1/min-amount`

**Get the minimum payment amount**

- **URL:** `https://api.nowpayments.io/v1/min-amount`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
Get the minimum payment amount for a specific pair.
You can also specify one of the fiat currencies in the currency_from. In this case, the minimum payment will be calculated in this fiat currency.
You can also add field fiat_equivalent (optional field) to get the fiat equivalent of the minimum amount.
"is_fixed_rate", and "is_fee_paid_by_user" parameters allows you to see current minimum amounts for corresponsing flows (it may differ from the standard flow!)
In the case of several outcome wallets we will calculate the minimum amount in the same way we route your payment to a specific wallet.
SUCCESSFUL RESPONSE FIELDS
Name	Type	Description
currency_from	String	Payin currency
currency_to	String	Outcome currency
min_amount	Float	Minimal amount for payment using mentioned currencies
fiat_equivalent	Float	(Optional) Get the fiat equivalent for calculated minimal amount
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PARAMS
currency_from
eth
(Required) Payin currency
currency_to
trx
(Required) Outcome currency
fiat_equivalent
usd
(Optional) Mentioning ticker of any supported fiat currency you can get fiat equivalent of calculated minimal amount
is_fixed_rate
False
(Optional) Set this as true if you're using fixed rate flow
is_fee_paid_by_user
False
(Optional) Set this as true if you're using fee paid by user flow
{
  "currency_from": "eth",
  "currency_to": "trx",
  "min_amount": 0.0078999,
  "fiat_equivalent": 35.40626584
}
```

</details>

### POST `/v1/payment`

**Create payment**

- **URL:** `https://api.nowpayments.io/v1/payment`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Creates payment. With this method, your customer will be able to complete the payment without leaving your website.
Data must be sent as a JSON-object payload.
Required request fields:
price_currency (required) - the fiat currency in which the price_amount is specified (usd, eur, etc);
pay_amount (optional) - the amount that users have to pay for the order stated in crypto. You can either specify it yourself, or we will automatically convert the amount you indicated in price_amount;
pay_currency (required) - the crypto currency in which the pay_amount is specified (btc, eth, etc), or one of available fiat currencies if it's enabled for your account (USD, EUR, ILS, GBP, AUD, RON);
ipn_callback_url (optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io";
order_id (optional) - inner store order ID, e.g. "RGDBP-21314";
order_description (optional) - inner store order description, e.g. "Apple Macbook Pro 2019 x 1";
payout_address (optional) - usually the funds will go to the address you specify in your Personal account. In case you want to receive funds on another address, you can specify it in this parameter;
payout_currency (optional) - currency of your external payout_address, required when payout_adress is specified;
payout_extra_id(optional) - extra id or memo or tag for external payout_address;
is_fixed_rate(optional) - boolean, can be true or false. Required for fixed-rate exchanges;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired".
is_fee_paid_by_user(optional) - boolean, can be true or false. Required for fixed-rate exchanges with all fees paid by users;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";
Here the list of available statuses of payment:
waiting - waiting for the customer to send the payment. The initial status of each payment;
confirming - the transaction is being processed on the blockchain. Appears when NOWPayments detect the funds from the user on the blockchain;
Please note: each currency has its own amount of confirmations requires to start the processing.
confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations;
sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you;
partially_paid - it shows that the customer sent the less than the actual price. Appears when the funds have arrived in your wallet;
finished - the funds have reached your personal address and the payment is finished;
failed - the payment wasn't completed due to the error of some kind;
expired - the user didn't send the funds to the specified address in the 7 days time window;
Please note: when you're creating a fiat2crypto payment you also should include additional header to your request - "origin-ip : xxx", where xxx is your customer IP address.
x-api-key
{{your_api_key}}
Content-Type
application/json
{
  "price_amount": 3999.5,
  "price_currency": "usd",
  "pay_currency": "btc",
  "ipn_callback_url": "https://nowpayments.io",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "is_fixed_rate": true,
  "is_fee_paid_by_user": false
}
  "price_amount": 3999.5,
  "price_currency": "usd",
  "pay_currency": "btc",
  "ipn_callback_url": "https://nowpayments.io",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1"
}'
```

</details>

### GET `/v1/payment/{id}`

**Get payment status**

- **URL:** `https://api.nowpayments.io/v1/payment/:payment_id`
- **Source:** `copied-docs-2.md`

<details>
<summary>Postman export details</summary>

```
Get the actual information about the payment. You need to provide the ID of the payment in the request.
NOTE! You should make the get payment status request with the same API key that you used in the create payment request. Here is the list of avalable statuses:
waiting - waiting for the customer to send the payment. The initial status of each payment.
confirming - the transaction is being processed on the blockchain. Appears when NOWPayments detect the funds from the user on the blockchain.
confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations.
sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you.
partially_paid - it shows that the customer sent the less than the actual price. Appears when the funds have arrived in your wallet.
finished - the funds have reached your personal address and the payment is finished.
failed - the payment wasn't completed due to the error of some kind.
refunded - the funds were refunded back to the user.
expired - the user didn't send the funds to the specified address in the 24 hour time window.
Additional info:
outcome_amount - this parameter shows the amount that will be (or is already) received on your Outcome Wallet once the transaction is settled.
outcome_currency - this parameter shows the currency in which the transaction will be settled.
invoice_id - this parameter shows invoice ID from which the payment was created
x-api-key
<enter_your_api_key>
PATH VARIABLES
payment_id
{
  "payment_id": 5524759814,
  "payment_status": "finished",
  "pay_address": "TNDFkiSmBQorNFacb3735q8MnT29sn8BLn",
  "price_amount": 5,
  "price_currency": "usd",
  "pay_amount": 165.652609,
  "actually_paid": 180,
  "pay_currency": "trx",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "purchase_id": "4944856743",
  "created_at": "2020-12-16T14:30:43.306Z",
  "updated_at": "2020-12-16T14:40:46.523Z",
  "outcome_amount": 178.9005,
  "outcome_currency": "trx"
}
Currencies
```

</details>

### POST `/v1/payment/{id}/update-merchant-estimate`

**Get/Update payment estimate**

- **URL:** `https://api.nowpayments.io/v1/payment/:id/update-merchant-estimate`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This endpoint is required to get the current estimate on the payment and update the current estimate.
Please note! Calling this estimate before expiration_estimate_date will return the current estimate, it won’t be updated.
:id - payment ID, for which you want to get the estimate
Response:
id - payment ID
token_id - id of api key used to create this payment (please discard this parameter)
pay_amount - payment estimate, the exact amount the user will have to send to complete the payment
expiration_estimate_date - expiration date of this estimate
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
Content-Type
application/json
(Required) Your payload has to be JSON object
PATH VARIABLES
id
Payment ID, for which you want to get the estimate
{
  "id": "4455667788",
  "token_id": "5566778899",
  "pay_amount": 0.04671013,
  "expiration_estimate_date": "2022-08-12T13:14:28.536Z"
}
```

</details>

## Payouts

### GET `/v1/payout`

**List of payouts**

- **URL:** `https://api.nowpayments.io/v1/payout`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This endpoint allows you to get a list of your payouts.
The list of available parameters:
batch_id: batch ID of enlisted payouts;
status: the statuses of enlisted payouts;
order_by: can be id, batchId, dateCreated, dateRequested, dateUpdated, currency, status;
order: 'asc' or 'desc' order;
date_from: beginning date of the requested payouts;
date_to: ending date of the requested payouts;
limit: how much results to show;
page: the current page;
x-api-key
{{your_api_key}}
List of payouts
{
  "payouts": [
    {
      "id": "5000248325",
      "batch_withdrawal_id": "5000145498",
      "status": "FINISHED",
      "error": null,
      "currency": "trx",
      "amount": "94.088939",
      "address": "[payout address]",
      "extra_id": null,
      "hash": "[hash]",
      "ipn_callback_url": null,
      "payout_description": null,
      "is_request_payouts": true,
      "unique_external_id": null,
      "created_at": "2023-04-06T14:44:59.684Z",
      "requested_at": "2023-04-06T14:45:55.505Z",
      "updated_at": "2023-04-06T14:49:08.031Z"
    },
    {
      "id": "5000247307",
      "batch_withdrawal_id": "5000144539",
      "status": "FINISHED",
      "error": null,
      "currency": "trx",
      "amount": "10.000000",
      "address": "[payout address]",
      "extra_id": null,
      "hash": "[hash]",
      "ipn_callback_url": null,
      "payout_description": null,
      "is_request_payouts": true,
      "unique_external_id": null,
      "created_at": "2023-04-05T19:21:40.836Z",
      "requested_at": "2023-04-05T19:23:17.111Z",
      "updated_at": "2023-04-05T19:27:30.895Z"
    }
  ]
}
Trading platforms
Standard Trading platform Flow
Registration and getting deposits:
API - Integrate "POST Create new user account" into your registration process, so users will have dedicated balance right after completing registration.
UI - Ask a customer for desirable deposit amount to top up their balance, and desired currency for deposit.
API - Get the minimum payment amount for the selected currency pair (payment currency to your payout wallet currency) with the "GET Minimum payment amount" method;
API - Get the estimate of the total amount in crypto with "GET Estimated price" and check that it is larger than the minimum payment amount from step 4;
... (truncated)
```

</details>

### POST `/v1/payout`

**Create payout**

- **URL:** `https://api.nowpayments.io/v1/payout`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This is the method to create a payout. You need to provide your data as a JSON-object payload. Next is a description of the required request fields:
address (required) - the address where you want to send funds;
currency (required) - payout currency;
amount (required) - amount of the payout. Must not exceed 6 decimals (i.e. 0.123456);
extra_id (optional) - memo, destination tag, etc.
payout_description(optional) - a description of the payout. You can set it for all payouts in a batch;
unique_external_id(optional) - a unique external identifier;
fiat_amount(optional) - used for setting the payout amount in fiat equivalent. Overrides "amount" parameter;
Here the list of the available payout statuses:
creating;
processing;
sending;
finished;
failed;
rejected;
Please, take note that you may request a single payout, but it still should be formatted as an array with the single element.
AUTHORIZATION
Bearer Token
Token
{{token}}
x-api-key
<your_api_key>
Content-Type
application/json
Authorization
Bearer *your_jwt_token*
{
    "payout_description": "description",
    "ipn_callback_url": "https://nowpayments.io",
    "withdrawals": [
        {
            "address": "TEmGwPeRTPiLFLVfBxXkSP91yc5GMNQhfS",
            "currency": "trx",
            "amount": 200,
            "ipn_callback_url": "https://nowpayments.io"
        },
        {
           "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
            "currency": "eth",
            "amount": 0.1,
            "ipn_callback_url": "https://nowpayments.io"
        }
    ]
}
    "ipn_callback_url": "https://nowpayments.io",
    "withdrawals": [
        {
            "address": "TEmGwPeRTPiLFLVfBxXkSP91yc5GMNQhfS",
            "currency": "trx",
            "amount": 200,
            "ipn_callback_url": "https://nowpayments.io"
        },
        {
            "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
            "currency": "eth",
            "amount": 0.1,
```

</details>

### GET `/v1/payout/fee`

**Get payout fee**

- **URL:** `https://api.nowpayments.io/v1/payout/fee`
- **Source:** `METHODS_CHECKLIST.md (Zendesk API docs)`

<details>
<summary>Postman export details</summary>

```
Query: currency (required), amount (required)
Estimates network fee for a payout.
```

</details>

### POST `/v1/payout/validate-address`

**Validate address**

- **URL:** `https://api.nowpayments.io/v1/payout/validate-address`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This endpoint allows you to check if your payout address is valid and funds can be received there.
Available parameters:
address - the payout address;
currency - the ticker of payout currency;
(optional) extra_id - memo or destination tag, if applicable;
x-api-key
{{your_api_key}}
Content-Type
application/json
raw
{
    "address": "0g033BbF609Ed876576735a02fa181842319Dd8b8F",
    "currency": "eth",
    "extra_id":null
}
    "address": "0g033BbF609Ed876576735a02fa181842319Dd8b8F",
    "currency": "eth",
    "extra_id":null
}'
{
  "status": false,
  "statusCode": 400,
  "code": "BAD_CREATE_WITHDRAWAL_REQUEST",
  "message": "Invalid payout_address: [currency] [address]"
}
```

</details>

### POST `/v1/payout/w_id/cancel`

**Cancel a scheduled payout**

- **URL:** `https://api.nowpayments.io/v1/payout/w_id/cancel`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Please note: You must specify the payout id of the individual payout you wish to cancel, not the batch id.
Params:
w_id - the unique identifier of the planned payout you want to cancel. This should be the ID of the individual payout, not the batch ID.
Content-Type
application/json
Cancel a scheduled payout
  "payout_id": "12345"
}
'
No response body
This request doesn't return any response body
Conversions
Conversions API allows you to exchange coins within your custody user account.
```

</details>

### GET `/v1/payout/{id}`

**Get payout status**

- **URL:** `https://api.nowpayments.io/v1/payout/<payout_id>`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
Get the actual information about the payout. You need to provide the ID of the payout in the request.
NOTE! You should make the get payout status request with the same API key that you used in the creat_payout request.
Here is the list of available statuses:
creating;
processing;
sending;
finished;
failed;
rejected;
x-api-key
{{your_api_key}}
[
  {
    "id": "<payout_id>",
    "address": "<payout_address>",
    "currency": "trx",
    "amount": "200",
    "batch_withdrawal_id": "<batchWithdrawalId>",
    "status": "WAITING",
    "extra_id": null,
    "hash": null,
    "error": null,
    "is_request_payouts": false,
    "ipn_callback_url": null,
    "unique_external_id": null,
    "payout_description": null,
    "created_at": "2020-11-12T17:06:12.791Z",
    "requested_at": null,
    "updated_at": null
  }
]
```

</details>

### POST `/v1/payout/{id}-id/verify`

**Verify payout**

- **URL:** `https://api.nowpayments.io/v1/payout/:withdrawals-id/verify`
- **Source:** `copied-docs-2.md`

<details>
<summary>Postman export details</summary>

```
This method is required to verify payouts by using your 2fa code.
You’ll have 10 attempts to verify the payout. If it is not verified after 10 attempts, the payout will remain in ‘creating’ status.
Payout will be processed only when it is verified.
Make sure to have your 2fa authentication enabled in your NOWPayments Account (in Account Settings).
When 2fa is disabled, the code automatically goes to your registration email.
The code sent by email is valid for one hour.
Next is a description of the required request fields:
:batch-withdrawal-id - payout id you received in 2. Create payout method
verification_code - 2fa code you received with your Google Auth app or via email
In order to establish an automatic verification of payouts, you should switch 2FA through the application.
There are several libraries for different frameworks aimed on generating a 2FA codes based on a secret key from your account settings.
e.g: Speakeasy for JavaScript.
We do not recommend to change any default settings.
Plain Text
const 2faVerificationCode = speakeasy.totp({
      your_2fa_secret_key,
      encoding: 'base32',
})
AUTHORIZATION
Bearer Token
Token
{{token}}
x-api-key
<enter_your_api_key>
PATH VARIABLES
withdrawals-id
5000000191
{
  "verification_code": "123456"
}
OK
```

</details>

### POST `/v1/payout/{id}-withdrawal-id/verify`

**Verify payout**

- **URL:** `https://api.nowpayments.io/v1/payout/:batch-withdrawal-id/verify`
- **Source:** `copied-docs.md`

<details>
<summary>Postman export details</summary>

```
This method is required to verify payouts by using your 2FA code.
You’ll have 10 attempts to verify the payout. If it is not verified after 10 attempts, the payout will remain in ‘creating’ status.
Payout will be processed only when it is verified.
If you have 2FA app enabled in your dashboard, payouts will accept 2FA code from your app. Otherwise the code for payouts validation will be sent to your registration email.
Please take a note that unverified payouts will be automatically rejected in an hour after creation.
Next is a description of the required request fields:
:batch-withdrawal-id - payout id you received in 2. Create payout method;
verification_code - 2fa code you received with your Google Auth app or via email;
In order to establish an automatic verification of payouts, you should switch 2FA through the application.
There are several libraries for different frameworks aimed on generating a 2FA codes based on a secret key from your account settings, for example, Speakeasy for JavaScript.
We do not recommend to change any default settings.
Plain Text
const 2faVerificationCode = speakeasy.totp({
      your_2fa_secret_key,
      encoding: 'base32',
})
AUTHORIZATION
Bearer Token
Token
{{token}}
x-api-key
{{your_api_key}}
Authorization
Bearer *your_jwt_token*
PATH VARIABLES
batch-withdrawal-id
{
  "verification_code": "123456"
}
  "verification_code": "123456"
}'
OK
```

</details>

## Subscriptions

### GET `/v1/subscriptions`

**Get many recurring payments**

- **URL:** `https://api.nowpayments.io/v1/subscriptions`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
The method allows you to view the entire list of recurring payments filtered by payment status and/or payment plan id
Available parameters:
limit - the amount of shown items
offset - setting the offset
is_active - status of the recurring payment
status - filter by status of recurring payment
subscription_plan_id - filter results by subscription plan id.
Here is the list of available statuses:
WAITING_PAY - the payment is waiting for user's deposit;
PAID - the payment is completed;
PARTIALLY_PAID - the payment is completed, but the final amount is less than required for payment to be fully paid;
EXPIRED - is being assigned to unpaid payment after 7 days of waiting;
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PARAMS
status
PAID
"WAITING_PAY" / "PAID" / "PARTIALLY_PAID" / "EXPIRED"
subscription_plan_id
111394288
is_active
false
true / false
limit
10
offset
0
{
  "result": [
    {
      "id": "1515573197",
      "subscription_plan_id": "111394288",
      "is_active": true,
      "status": "PAID",
      "expire_date": "2022-10-11T00:02:00.025Z",
      "subscriber": {
        "sub_partner_id": "111394288"
      },
      "created_at": "2022-10-09T22:15:50.808Z",
      "updated_at": "2022-10-09T22:15:50.808Z"
    },
    {
      "id": "111394288",
      "subscription_plan_id": "111394288",
      "is_active": false,
      "status": "WAITING_PAY",
      "expire_date": "2022-10-07T16:46:00.910Z",
      "subscriber": {
        "email": "test@example.com"
      },
      "created_at": "2022-10-06T16:40:28.880Z",
      "updated_at": "2022-10-06T16:40:28.880Z"
    }
```

</details>

### POST `/v1/subscriptions`

**Create recurring payments**

- **URL:** `https://api.nowpayments.io/v1/subscriptions`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This method creates a recurring charge from a user account.
The funds are transferred from a user account to your account when a new payment is generated or a paid period is coming to an end. The amount depends on the plan a customer chooses.
Here is the list of available statuses:
WAITING_PAY - the payment is waiting for user's deposit;
PAID - the payment is completed;
PARTIALLY_PAID - the payment is completed, but the final amount is less than required for payment to be fully paid;
EXPIRED - is being assigned to unpaid payment after 7 days of waiting;
Please note:
You can convert it manually using our conversions endpoints through api or in your Custody dashboard.
Authorization
Bearer {{token}}
(Required) Your authorization token
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
Content-Type
application/json
(Required) Your payload has to be JSON object
{
    "subscription_plan_id": 76215585,
    "sub_partner_id": 111111,
    "email": "your email"
}
    "subscription_plan_id": 76215585,
    "sub_partner_id": 111111
}'
{
  "result": {
    "id": "1515573197",
    "subscription_plan_id": "76215585",
    "is_active": false,
    "status": "WAITING_PAY",
    "expire_date": "2022-10-09T22:15:50.808Z",
    "subscriber": {
      "sub_partner_id": "111111"
    },
    "created_at": "2022-10-09T22:15:50.808Z",
    "updated_at": "2022-10-09T22:15:50.808Z"
  }
}
```

</details>

### GET `/v1/subscriptions/plans`

**Get all plans**

- **URL:** `https://api.nowpayments.io/v1/subscriptions/plans`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
This method allows you to obtain information about all the payment plans you’ve created.
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PARAMS
limit
10
Number
offset
3
Number
{
  "result": [
    {
      "id": "76215585",
      "title": "second sub plan",
      "interval_day": "3",
      "ipn_callback_url": null,
      "success_url": null,
      "cancel_url": null,
      "partially_paid_url": null,
      "amount": 0.1,
      "currency": "USD",
      "created_at": "2022-10-04T16:10:06.214Z",
      "updated_at": "2022-10-04T16:10:06.214Z"
    },
    {
      "id": "1062307590",
      "title": "second sub plan",
      "interval_day": "1",
      "ipn_callback_url": null,
      "success_url": null,
      "cancel_url": null,
      "partially_paid_url": null,
      "amount": 0.5,
      "currency": "USD",
      "created_at": "2022-10-04T16:28:55.423Z",
      "updated_at": "2022-10-04T16:28:55.423Z"
    }
  ],
  "count": 2
}
```

</details>

### GET `/v1/subscriptions/plans/{id}-id`

**Get one plan**

- **URL:** `https://api.nowpayments.io/v1/subscriptions/plans/:plan-id`
- **Source:** `copied-docs-2.md`

<details>
<summary>Postman export details</summary>

```
This method allows you to obtain information about your payment plan.
(you need to specify your payment plan id in the request).
x-api-key
<enter_your_api_key>
PATH VARIABLES
plan-id
{
  "result": {
    "id": "76215585",
    "title": "test plan",
    "interval_day": "1",
    "ipn_callback_url": null,
    "success_url": null,
    "cancel_url": null,
    "partially_paid_url": null,
    "amount": 2,
    "currency": "USD",
    "created_at": "2022-10-04T16:10:06.214Z",
    "updated_at": "2022-10-04T16:10:06.214Z"
  }
}
```

</details>

### DELETE `/v1/subscriptions/{id}`

**Delete recurring payment**

- **URL:** `https://api.nowpayments.io/v1/subscriptions/:sub_id`
- **Source:** `copied-docs-2.md`

<details>
<summary>Postman export details</summary>

```
Completely removes a particular payment from the recurring payment plan.
You need to specify the payment plan id in the request.
AUTHORIZATION
Bearer Token
Token
{{token}}
PATH VARIABLES
sub_id
{
  "result": "ok"
}
Billing (sub-partner API)
NOWPayments allows you to create sub-partner accounts for your users, enabling full-fledged crypto billing solution.
```

</details>

### GET `/v1/subscriptions/{id}`

**Get one recurring payment**

- **URL:** `https://api.nowpayments.io/v1/subscriptions/:sub_id`
- **Source:** `copied-docs-3.md`

<details>
<summary>Postman export details</summary>

```
Get information about a particular recurring payment via its ID.
Here is the list of available statuses:
WAITING_PAY - the payment is waiting for user's deposit;
PAID - the payment is completed;
PARTIALLY_PAID - the payment is completed, but the final amount is less than required for payment to be fully paid;
EXPIRED - is being assigned to unpaid payment after 7 days of waiting;
x-api-key
{{api-key}}
(Required) Your NOWPayments API key
PATH VARIABLES
sub_id
{
  "result": {
    "id": "1515573197",
    "subscription_plan_id": "111394288",
    "is_active": true,
    "status": "PAID",
    "expire_date": "2022-10-12T00:02:00.025Z",
    "subscriber": {
      "sub_partner_id": "111394288"
    },
    "created_at": "2022-10-09T22:15:50.808Z",
    "updated_at": "2022-10-09T22:15:50.808Z"
  }
}
Auth and API status
This set of methods allows you to check API availability and get a JWT token which is requires as a header for some other methods.
```

</details>

---

## IPN (webhooks)

1. Set `ipn_callback_url` when creating a payment or invoice.
2. Save **IPN Secret** from Dashboard → Store Settings (shown once at creation).
3. On callback: recursively **sort JSON keys**, `JSON.stringify`, HMAC-SHA512 with IPN secret.
4. Compare with header `x-nowpayments-sig` (timing-safe).
5. **Use the raw HTTP body** for verification when possible (parsed frameworks may change types).

**Payment statuses:** `waiting`, `confirming`, `confirmed`, `spending`, `sending`, `partially_paid`, `finished`, `failed`, `refunded`, `expired`

---

## Links

- [Postman — Production](https://documenter.getpostman.com/view/7907941/2s93JusNJt)
- [Postman — Sandbox](https://documenter.getpostman.com/view/7907941/T1LSCRHC)
- [Help Center — API](https://nowpayments.io/help/payments/api)
- [Zendesk — Endpoints](https://nowpayments.zendesk.com/hc/en-us/articles/21345824322717-API-and-endpoint-description)
