import json
import stripe
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def lambda_handler(event, context):
    """Lambda function to create a payment intent without confirming it"""

    print("Received event: " + json.dumps(event, indent=2))
    try:
        amount = event['body']['amount']

        # Create a payment intent without confirming it
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            confirm=False
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "amount": amount,
                "paymentIntentId": payment_intent.id,
            }),
        }
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e),
                "event": event,
            }),
        }

    except Exception as e:
        # Handle other unexpected errors
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "An unexpected error occurred.",
                "event": event,
            }),
        }