import os

import boto3
import pytest
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "CreatePaymentIntentApi"]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs


    def test_payment_intent_creation(self, api_gateway_url):
        """ Call the API Gateway endpoint responsible for creating a payment intent and check the response """

        # Define the data for the payment intent
        data = {
            "amount": 1000,  # Amount in cents
            # Add more fields as required by your API
        }

        # Make a POST request to the API Gateway endpoint
        print(f"{api_gateway_url}/create_payment_intent")
        response = requests.post(f"{api_gateway_url}payment_intent", json=data)

        # Check the status code
        assert response.status_code == 200

        # Check the response body
        response_body = response.json()

        # Assert that the response body has a 'paymentIntentId' field
        assert "paymentIntentId" in response_body

        # Assert that the 'paymentIntentId' field is not None or empty
        assert response_body["paymentIntentId"]