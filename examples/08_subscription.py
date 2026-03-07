"""
Example: Subscription plans and create subscription
Run: python examples/08_subscription.py
Env: NOWPAYMENTS_API_KEY, EMAIL, PASSWORD (for create_subscription)
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    # List plans (no auth)
    plans = np.get_subscription_plans()
    plans_list = plans.get("result", [])
    print("Plans:", len(plans_list))

    if plans_list:
        plan = plans_list[0]
        plan_id = plan.get("id")
        print("Plan:", plan)

        # Create subscription (requires JWT)
        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        if email and password and plan_id:
            auth = np.get_auth_token(email, password)
            token = auth["token"]
            sub = np.create_subscription(
                params={"subscription_plan_id": plan_id, "email": "customer@example.com"},
                jwt_token=token,
            )
            print("Subscription:", sub.get("result"))
        else:
            print("Set EMAIL and PASSWORD to create subscription")


if __name__ == "__main__":
    main()
