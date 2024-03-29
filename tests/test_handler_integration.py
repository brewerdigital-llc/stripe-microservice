import json
import os
from http import HTTPStatus

import pytest
import stripe

import create_payment_intent.app
import capture_payment_intent.app
import cancel_payment_intent.app

TEST_PAYMENT_AMOUNT = 100
RETURN_URL = "https://brewerdigital.com"

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test.
"""

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


class TestHandlerIntegration:
    """Test handler integration."""

    @pytest.fixture(scope="class")
    def payment_intent_creation_result_for_capture(self):
        """Create a payment intent event for testing."""
        return self.generate_payment_intent()

    @pytest.fixture(scope="class")
    def payment_intent_creation_result_for_cancellation(self):
        """Create a payment intent event for testing."""
        return self.generate_payment_intent()

    @staticmethod
    def generate_payment_intent() -> dict:
        """Generate a payment intent event for testing."""
        event = \
            {
                'body': f'{{"amount": {TEST_PAYMENT_AMOUNT}}}',
            }
        return create_payment_intent.app.lambda_handler(event, None)

    def test_create_payment_intent(self, payment_intent_creation_result_for_capture):
        """Test that the payment intent is created."""
        response = payment_intent_creation_result_for_capture
        assert response['statusCode'] == HTTPStatus.OK
        body = json.loads(response['body'])
        assert 'paymentIntentId' in body
        assert 'clientSecret' in body
        assert 'amount' in body
        assert body['amount'] == TEST_PAYMENT_AMOUNT

    def test_capture_payment_intent(self, payment_intent_creation_result_for_capture):
        """Test that the payment intent is captured."""
        body = json.loads(payment_intent_creation_result_for_capture["body"])
        payment_intent_id = body['paymentIntentId']
        payment_methods = ['pm_card_visa_chargeDeclined', 'pm_card_visa']
        payment_intent_event = {'body': f'{{"id": "{payment_intent_id}"}}'}
        for payment_method in payment_methods:
            payment_intent = stripe.PaymentIntent.modify(payment_intent_id, payment_method=payment_method)
            if payment_method == payment_methods[-1]:
                payment_intent.confirm(return_url=RETURN_URL)
                assert 'status' in payment_intent
                assert payment_intent['status'] == 'requires_capture'
                response = capture_payment_intent.app.lambda_handler(payment_intent_event, None)
                assert response['statusCode'] == HTTPStatus.OK
                body = json.loads(response['body'])
                assert 'paymentIntentId' in body
                assert 'status' in body
                assert body['status'] == 'succeeded'
            else:
                with pytest.raises(stripe.error.CardError) as e:
                    payment_intent.confirm(return_url=RETURN_URL)
                assert e.value.code == 'card_declined'

    def test_cancel_payment_intent(self, payment_intent_creation_result_for_cancellation):
        """Test that the payment intent is canceled."""
        body = json.loads(payment_intent_creation_result_for_cancellation["body"])
        payment_intent_id = body['paymentIntentId']
        payment_intent_event = {'body': f'{{"id": "{payment_intent_id}"}}'}
        response = cancel_payment_intent.app.lambda_handler(payment_intent_event, None)
        assert response['statusCode'] == HTTPStatus.OK
        body = json.loads(response['body'])
        assert 'paymentIntentId' in body
        assert 'status' in body
        assert body['status'] == 'canceled'
