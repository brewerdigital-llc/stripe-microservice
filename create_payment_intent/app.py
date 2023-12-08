import json
import stripe
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def lambda_handler(event, context):
    """Lambda function to create a payment intent without confirming it"""

    amount = event['amount']

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