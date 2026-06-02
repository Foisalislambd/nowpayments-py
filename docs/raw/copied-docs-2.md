
Public
ENVIRONMENT
No Environment
LAYOUT
Double Column
LANGUAGE
cURL - cURL
NOWPayments API
Introduction
Sandbox
Authentication
Standard e-commerce flow for NOWPayments API:
API Documentation
Recurring Payments API (Email Subscriptions feature)
Billing (sub-partner API)
Payments API
Currencies
Payouts API
GET
Get API status
POST
Authentication
NOWPayments API
NOWPayments is a non-custodial cryptocurrency payment processing platform. Accept payments in a wide range of cryptos and get them instantly converted into a coin of your choice and sent to your wallet. Keeping it simple – no excess.

Sandbox
Before production usage, you can test our API using the Sandbox. Details can be found here

Authentication
To use the NOWPayments API you should do the following:

Sign up at nowpayments.io
Specify your outcome wallet
Generate an API key
Standard e-commerce flow for NOWPayments API:
API - Check API availability with the "GET API status" method. If required, check the list of available payment currencies with the "GET available currencies" method.
UI - Ask a customer to select item/items for purchase to determine the total sum;
UI - Ask a customer to select payment currency
API - Get the minimum payment amount for the selected currency pair (payment currency to your Outcome Wallet currency) with the "GET Minimum payment amount" method;
API - Get the estimate of the total amount in crypto with "GET Estimated price" and check that it is larger than the minimum payment amount from step 4;
API - Call the "POST Create payment" method to create a payment and get the deposit address (in our example, the generated BTC wallet address is returned from this method);
UI - Ask a customer to send the payment to the generated deposit address (in our example, user has to send BTC coins);
UI - A customer sends coins, NOWPayments processes and exchanges them (if required), and settles the payment to your Outcome Wallet (in our example, to your ETH address);
API - You can get the payment status either via our IPN callbacks or manually, using "GET Payment Status" and display it to a customer so that they know when their payment has been processed.
API - you call the list of payments made to your account via the "GET List of payments" method. Additionally, you can see all of this information in your Account on NOWPayments website.
Alternative flow
API - Check API availability with the "GET API status" method. If required, check the list of available payment currencies with the "GET available currencies" method.
UI - Ask a customer to select item/items for purchase to determine the total sum;
UI - Ask a customer to select payment currency
API - Get the minimum payment amount for the selected currency pair (payment currency to your Outcome Wallet currency) with the "GET Minimum payment amount" method;
API - Get the estimate of the total amount in crypto with "GET Estimated price" and check that it is larger than the minimum payment amount from step 4;
API - Call the "POST Create Invoice method to create an invoice. Set "success_url" - parameter so that the user will be redirected to your website after successful payment.
UI - display the invoice url or redirect the user to the generated link.
NOWPayments - the customer completes the payment and is redirected back to your website (only if "success_url" parameter is configured correctly!).
API - You can get the payment status either via our IPN callbacks or manually, using "GET Payment Status" and display it to a customer so that they know when their payment has been processed.
API - you call the list of payments made to your account via the "GET List of payments" method. Additionally, you can see all of this information in your Account on NOWPayments website.
API Documentation
Instant Payments Notifications
IPN (Instant payment notifications, or callbacks) are used to notify you when transaction status is changed.
To use them, you should complete the following steps:

Generate and save the IPN Secret key in Store Settings tab at the Dashboard.
Insert your URL address where you want to get callbacks in create_payment request. The parameter name is ipn_callback_url. You will receive payment updates (statuses) to this URL address.
You will receive all the parameters at the URL address you specified in (2) by POST request.
The POST request will contain the x-nowpayments-sig parameter in the header.
The body of the request is similiar to a get payment status response body.
Example:
{"payment_id":5077125051,"payment_status":"waiting","pay_address":"0xd1cDE08A07cD25adEbEd35c3867a59228C09B606","price_amount":170,"price_currency":"usd","pay_amount":155.38559757,"actually_paid":0,"pay_currency":"mana","order_id":"2","order_description":"Apple Macbook Pro 2019 x 1","purchase_id":"6084744717","created_at":"2021-04-12T14:22:54.942Z","updated_at":"2021-04-12T14:23:06.244Z","outcome_amount":1131.7812095,"outcome_currency":"trx"}
Sort all the parameters from the POST request in alphabetical order.
Convert them to string using
JSON.stringify (params, Object.keys(params).sort()) or the same function.
Sign a string with an IPN-secret key with HMAC and sha-512 key
Compare the signed string from the previous step with the x-nowpayments-sig , which is stored in the header of the callback request.
If these strings are similar it is a success.
Otherwise, contact us on support@nowpayments.io to solve the problem.
Example of creating a signed string at Node.JS

Plain Text
const hmac = crypto.createHmac('sha512', notificationsKey);
hmac.update(JSON.stringify(params, Object.keys(params).sort()));
const signature = hmac.digest('hex');
Example of comparing signed strings in PHP

View More
Plain Text
function check_ipn_request_is_valid()
    {
        $error_msg = "Unknown error";
        $auth_ok = false;
        $request_data = null;
        if (isset($_SERVER['HTTP_X_NOWPAYMENTS_SIG']) && !empty($_SERVER['HTTP_X_NOWPAYMENTS_SIG'])) {
            $recived_hmac = $_SERVER['HTTP_X_NOWPAYMENTS_SIG'];
            $request_json = file_get_contents('php://input');
            $request_data = json_decode($request_json, true);
            ksort($request_data);
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
Recurrent payment notifications
If an error is detected, the payment is flagged and will receive additional recurrent notifications (number of recurrent notifications can be changed in your Store Settings-> Instant Payment Notifications).

If an error is received again during processing of the payment, recurrent notifications will be initiated again.

Example: "Timeout" is set to 1 minute and "Number of recurrent notifications" is set to 3.

Once an error is detected, you will receive 3 notifications at 1 minute intervals.

Several payments for one order
If you want to create several payments for one Order you should do the following:

Create a payment for the full order amount.
Save "purchase_id" which will be in "create_payment" response
Create next payment or payments with this "purchase_id" in "create_payment" request.
Only works for partially_paid payments
It may be useful if you want to give your customers opportunity to pay a full order with several payments, for example, one part in BTC and one part in ETH. Also, if your customer accidentally paid you only part of a full amount, you can automatically ask them to make another payment.

Packages
Please find our out-of-the box packages for easy integration below:

JavaScript package

[PHP package]
(https://packagist.org/packages/nowpayments/nowpayments-api-php)

More coming soon!

Payments
GET
Get one plan
https://api.nowpayments.io/v1/subscriptions/plans/:plan-id
This method allows you to obtain information about your payment plan.
(you need to specify your payment plan id in the request).

HEADERS
x-api-key
<enter_your_api_key>

PATH VARIABLES
plan-id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/subscriptions/plans/76215585' \
--header 'x-api-key: <your_api_key>'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
GET
Get many plans
https://api.nowpayments.io/v1/subscriptions/plans
This method allows you to obtain information about all the payment plans you’ve created.

HEADERS
x-api-key
<enter_your_api_key>

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
GET
Get one recurring payment
https://api.nowpayments.io/v1/subscriptions/:sub_id
Get information about a particular recurring payment via its ID.

Here’s the list of available statuses:
- WAITING_PAY
- PAID
- PARTIALLY_PAID
- EXPIRED

HEADERS
x-api-key
<enter_your_api_key>

PATH VARIABLES
sub_id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/subscriptions/1515573197' \
--header 'x-api-key: <enter_your_api_key>'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
DELETE
Delete recurring payment
https://api.nowpayments.io/v1/subscriptions/:sub_id
Completely removes a particular payment from the recurring payment plan.
You need to specify the payment plan id in the request.

AUTHORIZATION
Bearer Token
Token
{{token}}

PATH VARIABLES
sub_id
Example Request
200
curl
curl --location --request DELETE 'https://api.nowpayments.io/v1/subscriptions/:sub_id' \
--data ''
200 OK
Example Response
Body
Headers (0)
Text
{
  "result": "ok"
}
Billing (sub-partner API)
NOWPayments allows you to create sub-partner accounts for your users, enabling full-fledged crypto billing solution.

POST
Create new sub-partner
https://api.nowpayments.io/v1/sub-partner/balance
This is a method to create a sub-partner account for your user. After this you'll be able to generate a payment(/v1/sub-partner/payment) or deposit(/v1/sub-partner/deposit) for topping up its balance as well as withdraw funds from it.

Body:

Name : a unique user identifier; you can use any string which doesn’t exceed 30 characters (but NOT an email)

AUTHORIZATION
Bearer Token
Token
{{token}}

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
Create sub-partner recurring payments
https://api.nowpayments.io/v1/subscriptions
This method creates a recurring charge from a sub-account.

The funds are transferred from a sub-account to the main account when a new payment is generated or a paid period is coming to an end. The amount depends on the plan a customer chooses.
If you specify a particular currency your customer should pay in, and the sub-account has enough funds stored in it, the amount will be charged automatically. In case a customer has other currency on their sub-account, the equivalent sum will be charged.

AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
x-api-key
<enter_your_api_key>

Body
raw (json)
json
{
    "subscription_plan_id": 76215585,
    "sub_partner_id": 111111
}
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/subscriptions' \
--header 'x-api-key: <enter_your_api_key>' \
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
POST
Transfer
https://api.nowpayments.io/v1/sub-partner/transfer
This method allows creating transfers between sub-partners' accounts.
You can check the transfer's status using Get transfer method.

AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
x-api-key
{{x-api-token}}

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
Deposit with payment
https://api.nowpayments.io/v1/sub-partner/payment
This method allows you to top up a sub-partner account with a general payment.
You can check the actual payment status by using GET 9 Get payment status request.

AUTHORIZATION
Bearer Token
Token
{{token}}

HEADERS
x-api-key
{{x-api-token}}

Body
raw (json)
json
{
    "currency": "trx",
    "amount": 0.3,
    "sub_partner_id": "1631380403",
    "fixed_rate": false
}
Example Request
Deposit with payment
curl
curl --location 'https://api.nowpayments.io/v1/sub-partner/payment' \
--header 'x-api-key: {{x-api-token}}' \
--data '{
    "currency": "trx",
    "amount": 50,
    "sub_partner_id": "1631380403",
    "fixed_rate": false
}'
200 OK
Example Response
Body
Headers (0)
View More
Text
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
POST
Get/Update payment estimate
https://api.nowpayments.io/v1/payment/:id/update-merchant-estimate
This endpoint is required to get the current estimate on the payment, and update the current estimate.
Please note! Calling this estimate before expiration_estimate_date will return the current estimate, it won’t be updated.

:id - payment ID, for which you want to get the estimate

Response:
id - payment ID
token_id - id of api key used to create this payment (please discard this parameter)
pay_amount - payment estimate, the exact amount the user will have to send to complete the payment
expiration_estimate_date - expiration date of this estimate

HEADERS
x-api-key
<enter_your_api_key>

Content-Type
application/json

PATH VARIABLES
id
payment ID, for which you want to get the estimate

Example Request
200
curl
curl --location --request POST 'https://api.nowpayments.io/v1/payment/4409701815/update-merchant-estimate' \
--header 'x-api-key: <your_api_key>' \
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
Get payment status
https://api.nowpayments.io/v1/payment/:payment_id
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
HEADERS
x-api-key
<enter_your_api_key>

PATH VARIABLES
payment_id
Example Request
200
curl
curl --location 'https://api.nowpayments.io/v1/payment/5524759814' \
--header 'x-api-key: <your_api_key>'
200 OK
Example Response
Body
Headers (20)
View More
json
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
GET
Get available checked currencies
https://api.nowpayments.io/v1/merchant/coins
This is a method for obtaining information about the cryptocurrencies available for payments. Shows the coins you set as available for payments in the "coins settings" tab on your personal account.
Optional parameters:

fixed_rate(optional) - boolean, can be true or false. Returns avaliable currencies with minimum and maximum amount of the exchange.
HEADERS
x-api-key
<enter_your_api_key>

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
Payouts API
POST
Verify payout
https://api.nowpayments.io/v1/payout/:withdrawals-id/verify
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

HEADERS
x-api-key
<enter_your_api_key>

PATH VARIABLES
withdrawals-id
5000000191

Body
raw (json)
json
{
  "verification_code": "123456"
}
Example Request
200
curl
curl --location 'https://api.staging.nowpayments.io/v1/payout/5000000191/verify'
200 OK
Example Response
Body
Headers (0)
OK
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
Authentication method for obtaining a JWT token. You should specify your email and password which you are using for signing in into dashboard. JWT token will be required for creating a payout request. For security reasons, JWT tokens expire after 5 minutes.

Body
raw (json)
json
{
    "email": "<enter_your_email>",
    "password": "<enter_your_password>" 
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