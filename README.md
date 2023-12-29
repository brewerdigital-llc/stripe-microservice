# stripe-ms: FHIR Stripe Microservice

This project contains source code and supporting files for the FHIR Stripe serverless microservice application that you can deploy
with the SAM CLI. It includes the following files and folders.

- create_payment_intent, capture_payment_intent, and cancel_payment_intent - Code for the application's Lambda functions.
- events - Invocation events that you can use to invoke the functions.
- tests - Integration tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the
`template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that
updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. 
The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get
started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Use the Brewer-deployed microservice

### Base URL

The base URL for the Brewer-deployed microservice is https://gozj2why30.execute-api.us-east-2.amazonaws.com/Prod.  You can use this
URL to make requests to the microservice by appending the below endpoints and applying the corresponding HTTP methods upon invocation.

### Service endpoints

The following table lists the endpoints of the microservice.

| HTTP method | Endpoint          | Description              | Request body example                    | Response body example                                                                                                                               |
|-------------|-------------------|--------------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `POST`      | `/payment_intent` | Create a payment intent  | `{"amount": 200}`                       | `{"amount": 100, "paymentIntentId": "pi_000000000000000000000000", "clientSecret": "pi_000000000000000000000000_secret_0000000000000000000000000"}` |
| `PUT`       | `/payment_intent` | Confirm a payment intent | `{"id": "pi_000000000000000000000000"}` | `{"paymentIntentId": "pi_000000000000000000000000", "status": "succeeded"}`                                                                         |
| `DELETE`    | `/payment_intent` | Cancel a payment intent  | `{"id": "pi_000000000000000000000000"}` | `{"paymentIntentId": "pi_000000000000000000000000", "status": "canceled"}`                                                                          |

### Error responses

All error responses will have an appropriate HTTP status code other than `2nn` (typically in the `4nn` or `5nn` ranges) and a body
with the following format:

```json
{
   "error": "error_message",
   "event": {...}
}
```

Note that only some error responses include the `event` property, as appropriate.

### Workflow

The following workflow is used for payment operations with the microservice:

1. Create a payment intent by sending a `POST` request to the `/payment_intent` endpoint. The response will contain the payment intent ID and client secret.
2. Either:
   1. Send a `PUT` request to the `/payment_intent` endpoint with the payment intent ID returned in the `POST` response to confirm the payment intent with Stripe; or
   2. Send a `DELETE` request to the `/payment_intent` endpoint with the payment intent ID returned in the `POST` response to cancel the payment intent with Stripe.

### Authentication and Authorization

You must supply the AWS API Gateway with a valid API key in the `X-Api-Key` header of the request. The API key is defined under API
Keys at https://us-east-2.console.aws.amazon.com/apigateway/main/api-keys?api=unselected&region=us-east-2, and associated with the
API via a Usage Plan at https://us-east-2.console.aws.amazon.com/apigateway/main/usage-plans?region=us-east-2.

## Build, configure, deploy, and test the microservice

### Prerequisites

You must create a Stripe account for each provider at https://dashboard.stripe.com/register.  You must also create an API key
at https://dashboard.stripe.com/test/apikeys.

### Deploy the microservice

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for
building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda.
It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS,
with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

### Environment variables

The following environment variables are required to run the application:

* `STRIPE_SECRET_KEY` - The API key you created according to the instructions under **Prerequisites** above to use for the Stripe API calls.

For cloud operation, you can define these environment variables in the AWS Lambda console under each relevant function at
https://us-east-2.console.aws.amazon.com/lambda/home?functions&region=us-east-2#/functions. For testing, you should define these
either in your shell or via your IDE's runtime configuration.

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
stripe-ms$ sam build --use-container
```

The SAM CLI installs dependencies defined in `*/requirements.txt`, creates a deployment package, and saves it in the
`.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the
function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
stripe-ms$ sam local invoke CreatePaymentIntentFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
stripe-ms$ sam local start-api
stripe-ms$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property
on each function's definition includes the route and method for each path.

```yaml
      Events:
        CreatePaymentIntentApi:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /payment_intent
            Method: post
```

### Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of
AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and
APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

### Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed
Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features
to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
stripe-ms$ sam logs -n CreatePaymentIntentFunction --stack-name "fhir-stripe-ms" --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

### Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
stripe-ms$ pip install -r tests/requirements.txt --user
# Integration test, requiring deploying the stack first and setting the STRIPE_SECRET_KEY environment variable.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
stripe-ms$ AWS_SAM_STACK_NAME="fhir-stripe-ms" python -m pytest tests/test_handler_integration.py -v
```

### Cleanup

To delete the microservice that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run
the following:

```bash
sam delete --stack-name "fhir-stripe-ms"
```

### Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy other ready-to-use Apps and learn how authors developed their
applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
