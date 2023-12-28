import json
import os

import stripe

import pytest

import create_payment_intent.app

RETURN_URL = "https://brewerdigital.com"

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


class TestApiGateway:

    @pytest.fixture(scope="class")
    def payment_intent_creation_result_for_capture(self):
        """ Create a payment intent event for testing """
        return self.generate_payment_intent()

    @pytest.fixture(scope="class")
    def payment_intent_creation_result_for_cancellation(self):
        """ Create a payment intent event for testing """
        return self.generate_payment_intent()

    def generate_payment_intent(self):
        event = \
            {
                "body": "{\"amount\": 100}",
            }
        return create_payment_intent.app.lambda_handler(event, None)

    def test_create_payment_intent(self, payment_intent_creation_result_for_capture):
        response = payment_intent_creation_result_for_capture
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'paymentIntentId' in body
        assert 'clientSecret' in body
        assert 'amount' in body
        assert body['amount'] == 100

    def test_capture_payment_intent(self, payment_intent_creation_result_for_capture):
        body = json.loads(payment_intent_creation_result_for_capture["body"])
        payment_intent_id = body['paymentIntentId']
        payment_methods = ['pm_card_visa_chargeDeclined', 'pm_card_visa']
        for payment_method in payment_methods:
            payment_intent = stripe.PaymentIntent.modify(payment_intent_id, payment_method=payment_method)
            if payment_method == payment_methods[-1]:
                payment_intent.confirm(return_url=RETURN_URL)
                assert 'status' in payment_intent
                assert payment_intent['status'] == 'requires_capture'
                payment_intent.capture()
                assert payment_intent.status == 'succeeded'
            else:
                with pytest.raises(stripe.error.CardError) as e:
                    payment_intent.confirm(return_url=RETURN_URL)
                assert e.value.code == 'card_declined'

    def test_cancel_payment_intent(self, payment_intent_creation_result_for_cancellation):
        body = json.loads(payment_intent_creation_result_for_cancellation["body"])
        payment_intent_id = body['paymentIntentId']
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        payment_intent.cancel()
        assert payment_intent.status == 'canceled'
