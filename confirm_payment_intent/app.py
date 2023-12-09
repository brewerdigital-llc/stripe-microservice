import json
import stripe
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def lambda_handler(event, context):
    """Lambda function to confirm a payment intent"""

    print("Received event: " + json.dumps(event, indent=2))
    try:
        body = json.loads(event['body'])
        payment_intent_id = body['payment_intent_id']

        # Retrieve the payment intent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Confirm the payment intent
        payment_intent.confirm()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "paymentIntentId": payment_intent.id,
                "status": payment_intent.status,
            }),
        }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid JSON format in event body.",
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
                "error": str(e),
                "event": event,
            }),
        }