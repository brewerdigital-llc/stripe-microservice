import json
import logging
import os

import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


def lambda_handler(event, _):
    """Lambda function to create a payment intent without confirming it."""
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info('Received event:\n%s', json.dumps(event, indent=2))

    try:
        body = json.loads(event['body'])
        amount = body['amount']
        # Create a payment intent without confirming it.
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            confirm=False,
            capture_method="manual",
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "amount": amount,
                "paymentIntentId": payment_intent.id,
                "clientSecret": payment_intent.client_secret,
            }),
        }
    except json.JSONDecodeError:
        # Handle JSON decode errors.
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid JSON format in event body.",
            }),
        }
    except stripe.error.StripeError as e:
        # Handle Stripe errors.
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e),
                "event": event,
            }),
        }

    except Exception as e:
        # Handle other unexpected errors.
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "event": event,
            }),
        }
