
Public
ENVIRONMENT
No Environment
LAYOUT
Double Column
LANGUAGE
cURL - cURL
NOWPayments API
Introduction
Authentication
NOWPayments Integration Guide
Integration Scenarios
Standard e-commerce flow for NOWPayments API:
API Documentation
Auth and API status
Currencies
Payments
Mass payouts
Conversions
Customer management
Fiat payouts
Recurring Payments API (Email Subscriptions feature)
Use cases
NOWPayments API
NOWPayments is a non-custodial cryptocurrency payment processing platform. Accept payments in a wide range of cryptos and get them instantly converted into a coin of your choice and sent to your wallet. Keeping it simple – no excess.

Authentication
To use the NOWPayments API you should do the following:

Sign up at nowpayments.io;

Specify your payout wallet;

Generate an API key and IPN secret key;
Please note: IPN secret key may be shown fully only upon creation. Make sure to save it after generation.

NOWPayments Integration Guide
For more detailed information on how to integrate and use the NOWPayments API, please refer to our comprehensive NOWPayments Integration Guide. This guide provides step-by-step instructions on setting up and managing payouts, API requests, and other features to help you get started quickly and effectively.

Integration Scenarios
For a deeper understanding of different integration possibilities, check out our Integration Scenarios Guide. This guide outlines possible integration methods, providing practical examples and insights to help you implement the best solution for your business needs.

Standard e-commerce flow for NOWPayments API:
API - Check API availability with the "GET API status" method. If required, check the list of available payment currencies with the "GET available currencies" method;

UI - Ask a customer to select item/items for purchase to determine the total sum;

UI - Ask a customer to select payment currency;

API - Get the minimum payment amount for the selected currency pair (payment currency to your payout wallet currency) with the "GET Minimum payment amount" method;

API - Get the estimate of the total amount in crypto with "GET Estimated price" and check that it is larger than the minimum payment amount from step 4;

API - Call the "POST Create payment" method to create a payment and get the deposit address (in our example, the generated BTC wallet address is returned from this method);

UI - Ask a customer to send the payment to the generated deposit address (in our example, user has to send BTC coins);

UI - A customer sends coins, NOWPayments processes and exchanges them (if required), and settles the payment to your payout wallet (in our example, to your ETH address);

API - You can get the payment status either via our IPN callbacks or manually, using "GET Payment Status" and display it to a customer so that they know when their payment has been processed;

API - you call the list of payments made to your account via the "GET List of payments" method;

Additionally, you can see all of this information in your Account on NOWPayments website;

Alternative flow
API - Check API availability with the "GET API status" method. If required, check the list of available payment currencies with the "GET available currencies" method;

UI - Ask a customer to select item/items for purchase to determine the total sum;

UI - Ask a customer to select payment currency;

API - Get the minimum payment amount for the selected currency pair (payment currency to your payout wallet currency) with the "GET Minimum payment amount" method;

API - Get the estimate of the total amount in crypto with "GET Estimated price" and check that it is larger than the minimum payment amount from step 4;

API - Call the "POST Create Invoice method to create an invoice. Set "success_url" - parameter so that the user will be redirected to your website after successful payment;

UI - display the invoice url or redirect the user to the generated link;

NOWPayments - the customer completes the payment and is redirected back to your website (only if "success_url" parameter is configured correctly!);

API - You can get the payment status either via our IPN callbacks or manually, using "GET Payment Status" and display it to a customer so that they know when their payment has been processed;

API - you call the list of payments made to your account via the "GET List of payments" method;

Additionally, you can see all of this information in your Account on NOWPayments website;

API Documentation
Instant Payments Notifications
IPN (Instant payment notifications, or callbacks) are used to notify you when transaction status is changed.
To use them, you should complete the following steps:

Generate and save the IPN Secret key in Payment Settings tab at the Dashboard;

Insert your URL address where you want to get callbacks in create_payment request. The parameter name is ipn_callback_url. You will receive payment updates (statuses) to this URL address.**
Please, take note that we cannot send callbacks to your localhost unless it has dedicated IP address.**

important Please make sure that firewall software on your server (i.e. Cloudflare) does allow our requests to come through. It may be required to whitelist our IP addresses on your side to get it. The list of these IP addresses can be requested at partners@nowpayments.io;

You will receive all the parameters at the URL address you specified in (2) by POST request;
The POST request will contain the x-nowpayments-sig parameter in the header.
The body of the request is similiar to a get payment status response body.
You can see examples in "Webhook examples" section.

Sort the POST request by keys and convert it to string using
JSON.stringify (params, Object.keys(params).sort()) or the same function;

Sign a string with an IPN-secret key with HMAC and sha-512 key;

Compare the signed string from the previous step with the x-nowpayments-sig , which is stored in the header of the callback request;
If these strings are similar, it is a success.
Otherwise, contact us on support@nowpayments.io to solve the problem.

Example of creating a signed string at Node.JS

View More
Plain Text
function sortObject(obj) {
  return Object.keys(obj).sort().reduce(
    (result, key) => {
      result[key] = (obj[key] && typeof obj[key] === 'object') ? sortObject(obj[key]) : obj[key]
      return result
    },
    {}
  )
}
const hmac = crypto.createHmac('sha512', notificationsKey);
hmac.update(JSON.stringify(sortObject(params)));
const signature = hmac.digest('hex');
Example of comparing signed strings in PHP

View More
Plain Text
function tksort(&$array)
  {
  ksort($array);
  foreach(array_keys($array) as $k)
    {
    if(gettype($array[$k])=="array")
      {
      tksort($array[$k]);
      }
    }
  }
function check_ipn_request_is_valid()
    {
        $error_msg = "Unknown error";
        $auth_ok = false;
        $request_data = null;
        if (isset($_SERVER['HTTP_X_NOWPAYMENTS_SIG']) && !empty($_SERVER['HTTP_X_NOWPAYMENTS_SIG'])) {
            $recived_hmac = $_SERVER['HTTP_X_NOWPAYMENTS_SIG'];
            $request_json = file_get_contents('php://input');
            $request_data = json_decode($request_json, true);
            tksort($request_data);
            $sorted_request_json = json_encode($request_data, JSON_UNESCAPED_SLASHES);
            if ($request_json !== false && !empty($request_json)) {
                $hmac = hash_hmac("sha512", $sorted_request_json, trim($this->ipn_secret));
                if ($hmac == $recived_hmac) {
                    $auth_ok = true;
                } else {
                    $error_msg = 'HMAC signature does not match';
                }
            } else {
                $error_msg = 'Error reading POST data';
            }
        } else {
            $error_msg = 'No HMAC signature sent.';
        }
    }
Example comparing signed signatures in Python

View More
python
import json 
import hmac 
import hashlib
def np_signature_check(np_secret_key, np_x_signature, message):
    sorted_msg = json.dumps(message, separators=(',', ':'), sort_keys=True)
    digest = hmac.new(
    str(np_secret_key).encode(), 
    f'{sorted_msg}'.encode(),
    hashlib.sha512)
    signature = digest.hexdigest()
    if signature == np_x_signature:
        return
    else:
        print("HMAC signature does not match")
Usually you will get a notification per each step of processing payments, withdrawals, or transfers, related to custodial recurring payments.

The webhook is being sent automatically once the transaction status is changed.

You also can request an additional IPN notification using your NOWPayments dashboard.

Please note that you should set up an endpoint which can receive POST requests from our server.

Before going production we strongly recommend to make a test request to this endpoint to ensure it works properly.

Recurrent payment notifications
If an error is detected, the payment will be flagged and will receive additional recurrent notifications (number of recurrent notifications can be changed in your Payment Settings-> Instant Payment Notifications).

If an error is received again during the payment processing, recurrent notifications will be initiated again.

Example: "Timeout" is set to 1 minute and "Number of recurrent notifications" is set to 3.

Once an error is detected, you will receive 3 notifications at 1 minute intervals.

Webhooks Examples:
Payments:

View More
json
{
"payment_id":123456789,
"parent_payment_id":987654321,
"invoice_id":null,
"payment_status":"finished",
"pay_address":"address",
"payin_extra_id":null,
"price_amount":1,
"price_currency":"usd",
"pay_amount":15,
"actually_paid":15,
"actually_paid_at_fiat":0,
"pay_currency":"trx",
"order_id":null,
"order_description":null,
"purchase_id":"123456789",
"outcome_amount":14.8106,
"outcome_currency":"trx",
"payment_extra_ids":null
"fee": {
"currency":"btc",
"depositFee":0.09853637216235617,
"withdrawalFee":0,
"serviceFee":0
}
}
Withdrawals:

View More
json
{
"id":"123456789",
"batch_withdrawal_id":"987654321",
"status":"CREATING",
"error":null,
"currency":"usdttrc20",
"amount":"50",
"address":"address",
"fee":null,
"extra_id":null,
"hash":null,
"ipn_callback_url":"callback_url",
"created_at":"2023-07-27T15:29:40.803Z",
"requested_at":null,
"updated_at":null
}
Custodial recurring payments:

json
{
"id":"1234567890",
"status":"FINISHED",
"currency":"trx",
"amount":"12.171365564140688",
"ipn_callback_url":"callback_url",
"created_at":"2023-07-26T14:20:11.531Z",
"updated_at":"2023-07-26T14:20:21.079Z"
}
Repeated Deposits and Wrong-Asset Deposits
This section explains how we handle two specific types of deposits: repeated deposits (re-deposits) and wrong-asset deposits. These deposits may require special processing or manual intervention, and understanding how they work will help you manage your payments more effectively.

Repeated Deposits
Repeated deposits are additional payments sent to the same deposit address that was previously used by a customer to fully or partially pay an invoice. These deposits are processed at the current exchange rate at the time they are received. They are marked with either the "Partially paid" or "Finished" status. If you need to clarify your current repeated-deposit settings, please check with your payment provider regarding the default status.

In the Payments History section of the personal account, these payments are labeled as "Re-deposit". Additionally, in the payment details, the Original payment ID field will display the ID of the original transaction.

Recommendation:

Recommendation: When integrating, we recommend tracking the 'parent_payment_id' parameter in Instant Payment Notifications and being aware that the total amount of repeated deposits may differ from the expected payment amount. This helps avoid the risk of providing services in cases of underpayment.
We do not recommend configuring your system to automatically provide services or ship goods based on any repeated-deposit status. If you choose to configure it this way, you should be aware of the risk of providing services in cases of underpayment. For additional risk acceptance please refer to section 6 of our Terms of Service.

NB: Repeated deposits are always converted to the same asset as the original payment.
Note: To review the current flow or change the default status of repeated payments to "Finished" or "Partially paid", please contact us at support@nowpayments.io.

2. Wrong-Asset Deposits

Wrong-asset deposits occur when a payment is sent using the wrong network or asset (e.g. a user may mistakenly send USDTERC20 instead of ETH), and this network and asset are supported by our service.

These payments will appear in the Payments History section with the label "Wrong Asset" and, by default, will require manual intervention to resolve.

Recommendation: When integrating, we recommend configuring your system to check the amount, asset type and the 'parent_payment_id' param in Instant Payment Notifications of the incoming deposit to avoid the risks of providing services in case of insufficient funds.

If you want wrong-asset deposits to be processed automatically, you can enable the Wrong-Asset Deposits Auto-Processing option in your account settings (Settings -> Payment -> Payment details). Before enabling this option, please take into account that the final sum of the sent deposit may differ from the expected payment amount and by default these payments always receive "Finished" status.

If needed, we can also provide an option to assign a "partially paid" status to deposits processed through this feature. For more details, please contact support@nowpayments.io

Packages
Please find our out-of-the box packages for easy integration below:

JavaScript package

[PHP package]
(https://packagist.org/packages/nowpayments/nowpayments-api-php)

More coming soon!

Payments
Currencies
GET
Get available currencies
https://api.nowpayments.io/v1/currencies?fixed_rate=true
This is a method for obtaining information about all cryptocurrencies available for payments for your current setup of payout wallets.

HEADERS
x-api-key
{{api-key}}

(Required) Your NOWPayments API key

PARAMS
fixed_rate
true

(Optional) Returns avaliable currencies with minimum and maximum amount of the exchange.

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/currencies?fixed_rate=true' \
--header 'x-api-key: {{api-key}}'
200 OK
Example Response
Body
Headers (20)
View More
json
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
    "sxp",
    "uni",
    "okb",
    "btc"
  ]
}
Payments
Following methods will allow you to create payment links for your clients and white labeled payments if you prefer to keep us working under the hood.

Be sure to consider the details of repeated and wrong-asset deposits from 'Repeated Deposits and Wrong-Asset Deposits' section when processing payments.

Additionally, it's important to monitor the "outcome amount" and "outcome currency" parameters, especially if it's critical for your business to receive the full payment for services or goods. We advise against automatically providing goods or services when the payment status is "Partially paid," as discrepancies between the expected and actual amounts can be significant. If the difference is minor, you can update the payment status to "Finished" in the payment details section in Payments History.

GET
Get the minimum payment amount
https://api.nowpayments.io/v1/min-amount?currency_from=eth&currency_to=trx&fiat_equivalent=usd&is_fixed_rate=False&is_fee_paid_by_user=False
Get the minimum payment amount for a specific pair.

You can provide both currencies in the pair or just currency_from, and we will calculate the minimum payment amount for currency_from and currency which you have specified as the outcome in the Payment Settings.

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
HEADERS
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

Example Request
200
View More
curl
curl --location 'https://api.nowpayments.io/v1/min-amount?currency_from=eth&currency_to=trx&fiat_equivalent=usd&is_fixed_rate%20=False&is_fee_paid_by_user=False' \
--header 'x-api-key: <your_api_key>'
200 OK
Example Response
Body
Headers (20)
json
{
  "currency_from": "eth",
  "currency_to": "trx",
  "min_amount": 0.0078999,
  "fiat_equivalent": 35.40626584
}
POST
Get/Update payment estimate
https://api.nowpayments.io/v1/payment/:id/update-merchant-estimate
This endpoint is required to get the current estimate on the payment and update the current estimate.
Please note! Calling this estimate before expiration_estimate_date will return the current estimate, it won’t be updated.

:id - payment ID, for which you want to get the estimate

Response:
id - payment ID
token_id - id of api key used to create this payment (please discard this parameter)
pay_amount - payment estimate, the exact amount the user will have to send to complete the payment
expiration_estimate_date - expiration date of this estimate

HEADERS
x-api-key
{{api-key}}

(Required) Your NOWPayments API key

Content-Type
application/json

(Required) Your payload has to be JSON object

PATH VARIABLES
id
Payment ID, for which you want to get the estimate

Example Request
200
curl
curl --location --request POST 'https://api.nowpayments.io/v1/payment/4409701815/update-merchant-estimate' \
--header 'x-api-key: {{api-key}}' \
--header 'Content-Type: application/json'
200 OK
Example Response
Body
Headers (20)
json
{
  "id": "4455667788",
  "token_id": "5566778899",
  "pay_amount": 0.04671013,
  "expiration_estimate_date": "2022-08-12T13:14:28.536Z"
}
GET
Get estimated price
https://api.nowpayments.io/v1/estimate?amount=3999.5000&currency_from=usd&currency_to=btc
This is a method for calculating the approximate price in cryptocurrency for a given value in Fiat currency. You will need to provide the initial cost in the Fiat currency (amount, currency_from) and the necessary cryptocurrency (currency_to)
Currently following fiat currencies are available: USD, EUR, CAD, GBP, AUD, ILS, RON.

Please note that this method allows you to get estimates for crypto pairs as well.

HEADERS
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

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/estimate?amount=3999.5000&currency_from=usd&currency_to=btc' \
--header 'x-api-key: {{api-key}}'
200 OK
Example Response
Body
Headers (20)
json
{
  "currency_from": "usd",
  "amount_from": 3999.5,
  "currency_to": "btc",
  "estimated_amount": 0.17061637
}
GET
Get API status
https://api.nowpayments.io/v1/status
This is a method to get information about the current state of the API. If everything is OK, you will receive an "OK" message. Otherwise, you'll see some error.

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/status'
200 OK
Example Response
Body
Headers (15)
json
{
  "message": "OK"
}
POST
Authentication
https://api.nowpayments.io/v1/auth
Authentication method for obtaining a JWT token. You should specify your email and password which you are using for signing in into dashboard.
JWT token will be required for creating a payout request. For security reasons, JWT tokens expire in 5 minutes.

HEADERS
Content-Type
application/json

Body
raw (json)
json
{
    "email": "{{email}}",
    "password": "{{password}}" 
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/auth' \
--data '{
    "email": "your_email",
    "password": "your_password" 
}'
200 OK
Example Response
Body
Headers (21)
View More
json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU4MjYyNTkxMTUiLCJpYXQiOjE2MDUyODgzODQsImV4cCI6MTYwNTI4ODY4NH0.bk8B5AjoTt8Qfm1zHJxutAtgaTGW-2j67waGQ2DUHUI"
}
GET
Get all transfers
https://api.nowpayments.io/v1/sub-partner/transfers?id=111&status=CREATED&limit=10&offset=1&order=ASC
Returns the entire list of transfers created by your users.

The list of available statuses:

CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
HEADERS
Authorization
Bearer *your_jwt_token*

PARAMS
id
111

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

Example Request
200
View More
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/transfers?status=FINISHED&limit=10&offset=0&order=ASC'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
      "currency": "usdtbsc"
    },
    {
      "id": "1167886259",
      "from_sub_id": "5209391548",
      "to_sub_id": "111394288",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:22:17.125Z",
      "updated_at": "2022-10-09T21:24:00.662Z",
      "amount": "2",
      "currency": "usdtbsc"
    },
    {
      "id": "48471014",
      "from_sub_id": "111394288",
      "to_sub_id": "5209391548",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:25:29.231Z",
      "updated_at": "2022-10-09T21:27:00.676Z",
      "amount": "1",
      "currency": "usdtbsc"
    },
    {
      "id": "1304149238",
      "from_sub_id": "111394288",
      "to_sub_id": "5209391548",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:54:57.713Z",
      "updated_at": "2022-10-09T21:56:01.056Z",
      "amount": "1",
      "currency": "usdtbsc"
    },
    {
      "id": "327209161",
      "from_sub_id": "111394288",
      "to_sub_id": "1515573197",
      "status": "FINISHED",
      "created_at": "2022-10-09T22:09:02.181Z",
      "updated_at": "2022-10-09T22:10:01.853Z",
      "amount": "1",
      "currency": "usdtbsc"
    }
  ],
  "count": 7
}
GET
Get transfer
https://api.nowpayments.io/v1/sub-partner/transfer/:id
Get the actual information about certain transfer. You need to provide the transfer ID in the request.

The list of available statuses:

CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
HEADERS
Authorization
Bearer *your_jwt_token*

PATH VARIABLES
id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/transfer/327209161'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
POST
Create payout
https://api.nowpayments.io/v1/payout
This is the method to create a payout. You need to provide your data as a JSON-object payload. Next is a description of the required request fields:

address (required) - the address where you want to send funds;
currency (required) - payout currency;
amount (required) - amount of the payout. Must not exceed 6 decimals (i.e. 0.123456);
extra_id (optional) - memo, destination tag, etc.
ipn_callback_url(optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io". Please note: you can either set ipn_callback_url for each individual payout, or for all payouts in a batch (see example). In both cases IPNs will be sent for each payout separately;
payout_description(optional) - a description of the payout. You can set it for all payouts in a batch;
unique_external_id(optional) - a unique external identifier;
fiat_amount(optional) - used for setting the payout amount in fiat equivalent. Overrides "amount" parameter;
fiat_currency (optional) - used for determining fiat currency to get the fiat equivalent for. Required for "fiat_amount" parameter to work. DOES NOT override "currency" parameter. Payouts are made in crypto only, no fiat payouts are available;
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

HEADERS
x-api-key
<your_api_key>

Content-Type
application/json

Authorization
Bearer *your_jwt_token*

Body
raw (json)
View More
json
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
Example Request
200
View More
curl
curl --location 'https://api.nowpayments.io/v1/payout' \
--header 'x-api-key: <your_api_key>' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer *your_jwt_token*' \
--data '{
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
        },
        {
            "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
            "currency": "usdc",
            "amount": 1,
            "fiat_amount": 100,
            "fiat_currency": "usd",
            "ipn_callback_url": "https://nowpayments.io"
        }
    ]
}'
200 OK
Example Response
Body
Headers (0)
View More
json
{
  "id": "5000000713",
  "withdrawals": [
    {
      "is_request_payouts": false,
      "id": "5000000000",
      "address": "TEmGwPeRTPiLFLVfBxXkSP91yc5GMNQhfS",
      "currency": "trx",
      "amount": "200",
      "batch_withdrawal_id": "5000000000",
      "ipn_callback_url": "https://nowpayments.io",
      "status": "WAITING",
      "extra_id": null,
      "hash": null,
      "error": null,
      "payout_description": null,
      "unique_external_id": null,
      "created_at": "2020-11-12T17:06:12.791Z",
      "requested_at": null,
      "updated_at": null
    },
    {
      "is_request_payouts": false,
      "id": "5000000001",
      "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
      "currency": "eth",
      "amount": "0.1",
      "batch_withdrawal_id": "5000000000",
      "ipn_callback_url": "https://nowpayments.io",
      "status": "WAITING",
      "extra_id": null,
      "hash": null,
      "error": null,
      "payout_description": null,
      "unique_external_id": null,
      "createdAt": "2020-11-12T17:06:12.791Z",
      "requestedAt": null,
      "updatedAt": null
    },
    {
      "is_request_payouts": false,
      "id": "5000000002",
      "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
      "currency": "usdc",
      "amount": "99.84449793",
      "fiat_amount": "100",
      "fiat_currency": "usd",
      "batch_withdrawal_id": "5000000000",
      "ipn_callback_url": "https://nowpayments.io",
      "status": "WAITING",
      "extra_id": null,
      "hash": null,
      "error": null,
      "payout_description": null,
      "unique_external_id": null,
      "createdAt": "2020-11-12T17:06:12.791Z",
      "requestedAt": null,
      "updatedAt": null
    }
  ]
}
POST
Verify payout
https://api.nowpayments.io/v1/payout/:batch-withdrawal-id/verify
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

HEADERS
x-api-key
{{your_api_key}}

Authorization
Bearer *your_jwt_token*

PATH VARIABLES
batch-withdrawal-id
Body
raw (json)
json
{
  "verification_code": "123456"
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/payout/5000000191/verify' \
--header 'x-api-key: {{your_api_key}}' \
--header 'Authorization: Bearer *your_jwt_token*' \
--header 'Content-Type: application/json' \
--data '{
  "verification_code": "123456"
}'
200 OK
Example Response
Body
Headers (0)
OK
GET
Get payout status
https://api.nowpayments.io/v1/payout/<payout_id>
Get the actual information about the payout. You need to provide the ID of the payout in the request.

NOTE! You should make the get payout status request with the same API key that you used in the creat_payout request.

Here is the list of available statuses:

creating;
processing;
sending;
finished;
failed;
rejected;
HEADERS
x-api-key
{{your_api_key}}

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/payout/:payout_id' \
--header 'x-api-key: <your_api_key>' \
--header 'Authorization: Bearer *your_jwt_token*'
200 OK
Example Response
Body
Headers (0)
View More
json
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
GET
List of payouts
https://api.nowpayments.io/v1/payout
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
HEADERS
x-api-key
{{your_api_key}}

Example Request
List of payouts
curl
curl --location 'https://api.nowpayments.io/v1/payout'
200 OK
Example Response
Body
Headers (1)
View More
json
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

API - Call the "POST Deposit with payment" method to create a payment and get the deposit address (in our example, the generated BTC wallet address is returned from this method);

UI - Ask a customer to send the payment to the generated deposit address (in our example, user has to send BTC coins);

UI - A customer sends coins, NOWPayments processes and exchanges them (if required), and credit the payment to your players' balance;

API - You can get the payment status either via our IPN callbacks or manually, using "GET Payment Status" and display it to a customer so that they know when their payment has been processed;

API - you call the list of payments made to your account via the "GET List of payments" method;

Payouts:

UI - ask the user for desirable amount, coin and address for payout.

API - call the player balance with "GET user balance" method and check if player has enough balance.

API - call "POST validate address" to check if the provided address is valid on the blockchain.

API - call "POST write off your account" method to collect the requested amount from user balance to your master balance.

API - call "POST Create payout" to create a payout.

API - create an OTP password for 2fa validation using external libraries.

API - call "POST Verify payout" to validate a payout with 2fa code.

API - You can get the payout status either via our IPN callbacks or manually, using "GET Payout Status" and display it to a customer so that they know when their payment has been processed;

UI - NOWPayments processes payout and credit the payment to your players' wallet;

All related information about your operations will also be available in your NOWPayments dashboard.

If you have any additional questions about integration feel free to drop a message to partners@nowpayments.io for further guidance.

Auth and API status
This set of methods allows you to check API availability and get a JWT token which is requires as a header for some other methods.

GET
Get API status
https://api.nowpayments.io/v1/status
This is a method to get information about the current state of the API. If everything is OK, you will receive an "OK" message. Otherwise, you'll see some error.

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/status'
200 OK
Example Response
Body
Headers (15)
json
{
  "message": "OK"
}
POST
Authentication
https://api.nowpayments.io/v1/auth
Authentication method for obtaining a JWT token. You should specify your email and password which you are using for signing in into dashboard.
JWT token will be required for creating a payout request. For security reasons, JWT tokens expire in 5 minutes.

HEADERS
Content-Type
application/json

Body
raw (json)
json
{
    "email": "{{email}}",
    "password": "{{password}}" 
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/auth' \
--data '{
    "email": "your_email",
    "password": "your_password" 
}'
200 OK
Example Response
Body
Headers (21)
View More
json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU4MjYyNTkxMTUiLCJpYXQiOjE2MDUyODgzODQsImV4cCI6MTYwNTI4ODY4NH0.bk8B5AjoTt8Qfm1zHJxutAtgaTGW-2j67waGQ2DUHUI"
}
POST
Write off on your account
https://api.nowpayments.io/v1/sub-partner/write-off
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

HEADERS
Authorization
Bearer *your_jwt_token*

Content-Type
application/json

Body
raw (json)
json
{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403"
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/write-off' \
--header 'x-api-key: {{x-api-token}}' \
--data '{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403"
}'
Example Response
Body
Headers (0)
View More
Text
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

Using the API you can automate 2fa by implementing the OTP generation library in your code and set it up in your dashboard. "Dashboard" - "Account settings" - "Two step authentification" - "Use an app"

Save the secret key and set it up in your favorite 2FA application as well, otherwise you won't be able to get access to your dashboard!

Please note:

Payouts can be requested only using a whitelisted IP address, and to whitelisted wallet addresses. It's a security measure enabled for each partner account by default.

You can whitelist both of these anytime dropping a formal request using your registration email to partners@nowpayments.io.

For more information about whitelisting you can reach us at partners@nowpayments.io.

GET
Get payout status
https://api.nowpayments.io/v1/payout/<payout_id>
Get the actual information about the payout. You need to provide the ID of the payout in the request.

NOTE! You should make the get payout status request with the same API key that you used in the creat_payout request.

Here is the list of available statuses:

creating;
processing;
sending;
finished;
failed;
rejected;
HEADERS
x-api-key
{{your_api_key}}

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/payout/:payout_id' \
--header 'x-api-key: <your_api_key>' \
--header 'Authorization: Bearer *your_jwt_token*'
200 OK
Example Response
Body
Headers (0)
View More
json
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
GET
List of payouts
https://api.nowpayments.io/v1/payout
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
HEADERS
x-api-key
{{your_api_key}}

Example Request
List of payouts
curl
curl --location 'https://api.nowpayments.io/v1/payout'
200 OK
Example Response
Body
Headers (1)
View More
json
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
DAO
Basic DAO Integration Flow
Once you finished establishing your DAO you can use NOWPayments API to set up your daily operations just as easy as that:

Registration and getting deposits:

API - Integrate "POST Create new user account" into your registration process, so users will have dedicated balance right after completing registration.

UI - Ask a customer for desirable deposit amount to top up their balance, and desired currency for deposit.

API - Get the minimum payment amount for the selected currency pair (payment currency to your payout wallet currency) with the "GET Minimum payment amount" method;

API - Get the estimate of the total amount in crypto with "GET Estimated price" and check that it is larger than the minimum payment amount from step 4;

API - Call the "POST Deposit with payment" method to create a payment and get the deposit address (in our example, the generated BTC wallet address is returned from this method);

UI - Ask a customer to send the payment to the generated deposit address (in our example, user has to send BTC coins);

UI - A customer sends coins, NOWPayments processes and exchanges them (if required), and credit the payment to your players' balance;

API - You can get the payment status either via our IPN callbacks or manually, using "GET Payment Status" and display it to a customer so that they know when their payment has been processed;

API - you call the list of payments made to your account via the "GET List of payments" method;

Payouts:

UI - ask the user for desirable amount, coin and address for payout.

API - call the player balance with "GET user balance" method and check if player has enough balance.

API - call "POST validate address" to check if the provided address is valid on the blockchain.

API - call "POST write off your account" method to collect the requested amount from user balance to your master balance.

API - call "POST Create payout" to create a payout.

API - create an OTP password for 2fa validation using external libraries.

API - call "POST Verify payout" to validate a payout with 2fa code.

API - You can get the payout status either via our IPN callbacks or manually, using "GET Payout Status" and display it to a customer so that they know when their payment has been processed;

UI - NOWPayments processes payout and credit the payment to your players' wallet;

All related information about your operations will also be available in your NOWPayments dashboard.

If you have any additional questions about integration feel free to drop a message to partners@nowpayments.io for further guidance.

Auth and API status
This set of methods allows you to check API availability and get a JWT token which is requires as a header for some other methods.

GET
Get available checked currencies
https://api.nowpayments.io/v1/merchant/coins
This is a method for obtaining information about the cryptocurrencies available for payments. Shows the coins you set as available for payments in the "coins settings" tab on your personal account.
Optional parameters:

fixed_rate(optional) - boolean, can be true or false. Returns currencies avaliable for fixed rate exchanges with minimum and maximum amount of the exchange.
HEADERS
x-api-key
{{your_api_key}}

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/merchant/coins' \
--header 'x-api-key: <your_api_key>'
200 OK
Example Response
Body
Headers (20)
View More
json
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
    "sxp",
    "uni",
    "okb",
    "btc"
  ]
}
Custody
NOWPayments allows you to create deposit accounts for your users, enabling full-fledged crypto billing solution.

POST
Create new user account
https://api.nowpayments.io/v1/sub-partner/balance
This is a method to create an account for your user. After this you'll be able to generate a payment(/v1/sub-partner/payment) or deposit(/v1/sub-partner/deposit) for topping up its balance as well as withdraw funds from it.

Body:

Name : a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)

AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
Authorization
Bearer *your_jwt_token*

Content-Type
application/json

PARAMS
Body
raw (json)
json
{
    "name": "test1"
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/balance' \
--data '{
    "name": "test1"
}'
200 OK
Example Response
Body
Headers (0)
Text
{
  "result": {
    "id": "1515573197",
    "name": "test1",
    "created_at": "2022-10-09T21:56:33.754Z",
    "updated_at": "2022-10-09T21:56:33.754Z"
  }
}
POST
Create recurring payments
https://api.nowpayments.io/v1/subscriptions
This method creates a recurring charge from a user account.

The funds are transferred from a user account to your account when a new payment is generated or a paid period is coming to an end. The amount depends on the plan a customer chooses.
If you specify a particular currency your customer should pay in, and their account have enough funds stored in it, the amount will be charged automatically. In case a customer has other currency on their account, the equivalent sum will be charged.

Here is the list of available statuses:

WAITING_PAY - the payment is waiting for user's deposit;
PAID - the payment is completed;
PARTIALLY_PAID - the payment is completed, but the final amount is less than required for payment to be fully paid;
EXPIRED - is being assigned to unpaid payment after 7 days of waiting;
AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
x-api-key
{{your_api_key}}

Content-Type
application/json

Body
raw (json)
json
{
    "subscription_plan_id": 76215585,
    "sub_partner_id": 111111,
    "email": "your email"
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/subscriptions' \
--header 'x-api-key: {{your_api_key}}' \
--data '{
    "subscription_plan_id": 76215585,
    "sub_partner_id": 111111
}'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
GET
Get user balance
https://api.nowpayments.io/v1/sub-partner/balance/:id
This request can be made only from a whitelisted IP.
If IP whitelisting is disabled, this request can be made by any user that has an API key.

HEADERS
x-api-key
{{your_api_key}}

PATH VARIABLES
id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/balance/:id' \
--header 'x-api-key: {{your_api_key}}'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
GET
Get users
https://api.nowpayments.ioo/v1/sub-partner?id=111&offset=1&limit=10&order=DESC
This method returns the entire list of your users.

AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
Authorization
Bearer *your_jwt_token*

PARAMS
id
111

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

Example Request
200
View More
curl
curl --location 'https://api.nowpayments.ioo/v1/sub-partner?offset=0&limit=10&order=DESC'
Example Response
Body
Headers (0)
View More
Text
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
GET
Get all transfers
https://api.nowpayments.io/v1/sub-partner/transfers?id=111&status=CREATED&limit=10&offset=1&order=ASC
Returns the entire list of transfers created by your users.

The list of available statuses:

CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
HEADERS
Authorization
Bearer *your_jwt_token*

PARAMS
id
111

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

Example Request
200
View More
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/transfers?status=FINISHED&limit=10&offset=0&order=ASC'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
      "currency": "usdtbsc"
    },
    {
      "id": "1167886259",
      "from_sub_id": "5209391548",
      "to_sub_id": "111394288",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:22:17.125Z",
      "updated_at": "2022-10-09T21:24:00.662Z",
      "amount": "2",
      "currency": "usdtbsc"
    },
    {
      "id": "48471014",
      "from_sub_id": "111394288",
      "to_sub_id": "5209391548",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:25:29.231Z",
      "updated_at": "2022-10-09T21:27:00.676Z",
      "amount": "1",
      "currency": "usdtbsc"
    },
    {
      "id": "1304149238",
      "from_sub_id": "111394288",
      "to_sub_id": "5209391548",
      "status": "FINISHED",
      "created_at": "2022-10-09T21:54:57.713Z",
      "updated_at": "2022-10-09T21:56:01.056Z",
      "amount": "1",
      "currency": "usdtbsc"
    },
    {
      "id": "327209161",
      "from_sub_id": "111394288",
      "to_sub_id": "1515573197",
      "status": "FINISHED",
      "created_at": "2022-10-09T22:09:02.181Z",
      "updated_at": "2022-10-09T22:10:01.853Z",
      "amount": "1",
      "currency": "usdtbsc"
    }
  ],
  "count": 7
}
GET
Get transfer
https://api.nowpayments.io/v1/sub-partner/transfer/:id
Get the actual information about the transfer. You need to provide the transfer ID in the request.

The list of available statuses:

CREATED - the transfer is being created;
WAITING - the transfer is waiting for payment;
FINISHED - the transfer is completed;
REJECTED - for some reason, transaction failed;
HEADERS
Authorization
Bearer *your_jwt_token*

PATH VARIABLES
id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/transfer/327209161'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
POST
Transfer
https://api.nowpayments.io/v1/sub-partner/transfer
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

HEADERS
x-api-key
{{x-api-token}}

Content-Type
application/json

Body
raw (json)
json
{
    "currency": "trx",
    "amount": 0.3,
    "from_id": 1111111,
    "to_id":  1111111
}
Example Request
Transfer
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/transfer' \
--header 'x-api-key: {{x-api-token}}' \
--data '{
    "currency": "trx",
    "amount": 0.3,
    "from_id": 1111111,
    "to_id":  1111111
}'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
POST
Deposit from your master account
https://api.nowpayments.io/v1/sub-partner/deposit
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

HEADERS
x-api-key
{{x-api-token}}

Content-Type
application/json

Body
raw (json)
json
{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403"
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/deposit' \
--header 'x-api-key: {{x-api-token}}' \
--data '{
    "currency": "usddtrc20",
    "amount": 0.7,
    "sub_partner_id": "111394288"
}'
Example Response
Body
Headers (0)
View More
Text
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
GET
Get all plans
https://api.nowpayments.io/v1/subscriptions/plans
This method allows you to obtain information about all the payment plans you’ve created.

HEADERS
x-api-key
{{your_api_key}}

PARAMS
limit
10

Number

offset
3

Number

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/subscriptions/plans' \
--header 'x-api-key: <your_api_key>'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
POST
Create an email subscription
https://api.nowpayments.io/v1/subscriptions
This method allows you to send payment links to your customers via email. A day before the paid period ends, the customer receives a new letter with a new payment link.

subscription_plan_id - the ID of the payment plan your customer chooses; such params as the duration and amount will be defined by this ID;
email - your customer’s email to which the payment links will be sent;

AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
x-api-key
{{your_api_key}}

Content-Type
application/json

Body
raw (json)
json
{
    "subscription_plan_id": 76215585,
    "email": "test@example.com"
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/subscriptions' \
--header 'x-api-key: <enter_your_api_key>' \
--data-raw '{
    "subscription_plan_id": 76215585,
    "email": "test@example.com"
}'
200 OK
Example Response
Body
Headers (0)
View More
Text
{
  "result": {
    "id": "148427051",
    "subscription_plan_id": "76215585",
    "is_active": false,
    "status": "WAITING_PAY",
    "expire_date": "2022-10-10T13:46:18.476Z",
    "subscriber": {
      "email": "test@example.com"
    },
    "created_at": "2022-10-10T13:46:18.476Z",
    "updated_at": "2022-10-10T13:46:18.476Z"
  }
}
Conversions
Conversions API allows you to exchange coins within your custody user account.

POST
Create conversion
https://api.nowpayments.io/v1/conversion
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
HEADERS
x-api-key
{{your_api_key}}

Authorization
Bearer *your_jwt_token*

Content-Type
application/json

Body
raw
{
    "amount": 50,
    "from_currency": "usdttrc20",
    "to_currency": "USDTERC20"
}
Example Request
200
curl
curl --location --request GET 'https://api.nowpayments.io/v1/conversion' \
--header 'x-api-key: {{your_api_key}}' \
--header 'Authorization: Bearer *your_jwt_token*' \
--header 'Content-Type: application/json' \
--data '{
    "amount": "50",
    "from_currency": "usdttrc20",
    "to_currency": "USDTERC20"
}'
Example Response
Body
Headers (0)
View More
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
GET
Get conversion status
https://api.nowpayments.io/v1/conversion/:conversion_id
HEADERS
Authorization
Bearer *your_jwt_token*

PATH VARIABLES
conversion_id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/conversion/:conversion_id' \
--header 'Authorization: Bearer *your_jwt_token*'
Example Response
Body
Headers (0)
View More
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
GET
Get list of conversions
https://api.nowpayments.io/v1/conversion
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
HEADERS
Authorization
Bearer *your_jwt_token*

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/conversion'
Example Response
Body
Headers (0)
View More
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

Using the API you can automate 2fa by implementing the OTP generation library in your code and set it up in your dashboard. "Dashboard" - "Account settings" - "Two step authentification" - "Use an app"

Save the secret key and set it up in your favorite 2FA application as well, otherwise you won't be able to get access to your dashboard!

Please note:

Payouts can be requested only using a whitelisted IP address, and to whitelisted wallet addresses. It's a security measure enabled for each partner account by default.

You can whitelist both of these anytime dropping a formal request using your registration email to partners@nowpayments.io.

For more information about whitelisting you can reach us at partners@nowpayments.io.

GET
Get balance
https://api.nowpayments.io/v1/balance
This method returns your balance in different currencies.

The response contains a list of currencies with two parameters:

amount - avaliable currency amount;
pendingAmount - currently processing currency amount;
HEADERS
x-api-key
{{your_api_key}}

Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/balance' \
--header 'x-api-key: <your_api_key>' \
--header 'Authorization: Bearer *your_jwt_token*'
200 OK
Example Response
Body
Headers (0)
View More
json
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
POST
Validate address
https://api.nowpayments.io/v1/payout/validate-address
This endpoint allows you to check if your payout address is valid and funds can be received there.

Available parameters:

address - the payout address;
currency - the ticker of payout currency;
(optional) extra_id - memo or destination tag, if applicable;
HEADERS
x-api-key
{{your_api_key}}

Content-Type
application/json

Body
raw
{
    "address": "0g033BbF609Ed876576735a02fa181842319Dd8b8F", 
    "currency": "eth", 
    "extra_id":null
}
Example Request
400
curl
curl --location 'https://api.nowpayments.io/v1/payout/validate-address' \
--header 'x-api-key: {{your_api_key}}' \
--header 'Content-Type: application/json' \
--data '{
    "address": "0g033BbF609Ed876576735a02fa181842319Dd8b8F", 
    "currency": "eth", 
    "extra_id":null
}'
400 Bad Request
Example Response
Body
Headers (0)
{
  "status": false,
  "statusCode": 400,
  "code": "BAD_CREATE_WITHDRAWAL_REQUEST",
  "message": "Invalid payout_address: [currency] [address]"
}
POST
Create payout
https://api.nowpayments.io/v1/payout
This is the method to create a payout. You need to provide your data as a JSON-object payload. Next is a description of the required request fields:

address (required) - the address where you want to send funds;
currency (required) - payout currency;
amount (required) - amount of the payout. Must not exceed 6 decimals (i.e. 0.123456);
extra_id (optional) - memo, destination tag, etc.
ipn_callback_url(optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io". Please note: you can either set ipn_callback_url for each individual payout, or for all payouts in a batch (see example). In both cases IPNs will be sent for each payout separately;
payout_description(optional) - a description of the payout. You can set it for all payouts in a batch;
unique_external_id(optional) - a unique external identifier;
fiat_amount(optional) - used for setting the payout amount in fiat equivalent. Overrides "amount" parameter;
fiat_currency (optional) - used for determining fiat currency to get the fiat equivalent for. Required for "fiat_amount" parameter to work. DOES NOT override "currency" parameter. Payouts are made in crypto only, no fiat payouts are available;
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

HEADERS
x-api-key
<your_api_key>

Content-Type
application/json

Authorization
Bearer *your_jwt_token*

Body
raw (json)
View More
json
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
Example Request
200
View More
curl
curl --location 'https://api.nowpayments.io/v1/payout' \
--header 'x-api-key: <your_api_key>' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer *your_jwt_token*' \
--data '{
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
        },
        {
            "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
            "currency": "usdc",
            "amount": 1,
            "fiat_amount": 100,
            "fiat_currency": "usd",
            "ipn_callback_url": "https://nowpayments.io"
        }
    ]
}'
200 OK
Example Response
Body
Headers (0)
View More
json
{
  "id": "5000000713",
  "withdrawals": [
    {
      "is_request_payouts": false,
      "id": "5000000000",
      "address": "TEmGwPeRTPiLFLVfBxXkSP91yc5GMNQhfS",
      "currency": "trx",
      "amount": "200",
      "batch_withdrawal_id": "5000000000",
      "ipn_callback_url": "https://nowpayments.io",
      "status": "WAITING",
      "extra_id": null,
      "hash": null,
      "error": null,
      "payout_description": null,
      "unique_external_id": null,
      "created_at": "2020-11-12T17:06:12.791Z",
      "requested_at": null,
      "updated_at": null
    },
    {
      "is_request_payouts": false,
      "id": "5000000001",
      "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
      "currency": "eth",
      "amount": "0.1",
      "batch_withdrawal_id": "5000000000",
      "ipn_callback_url": "https://nowpayments.io",
      "status": "WAITING",
      "extra_id": null,
      "hash": null,
      "error": null,
      "payout_description": null,
      "unique_external_id": null,
      "createdAt": "2020-11-12T17:06:12.791Z",
      "requestedAt": null,
      "updatedAt": null
    },
    {
      "is_request_payouts": false,
      "id": "5000000002",
      "address": "0x1EBAeF7Bee7B3a7B2EEfC72e86593Bf15ED37522",
      "currency": "usdc",
      "amount": "99.84449793",
      "fiat_amount": "100",
      "fiat_currency": "usd",
      "batch_withdrawal_id": "5000000000",
      "ipn_callback_url": "https://nowpayments.io",
      "status": "WAITING",
      "extra_id": null,
      "hash": null,
      "error": null,
      "payout_description": null,
      "unique_external_id": null,
      "createdAt": "2020-11-12T17:06:12.791Z",
      "requestedAt": null,
      "updatedAt": null
    }
  ]
}
