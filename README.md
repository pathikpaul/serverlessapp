# My First Serverless App Used Flask to Deploy to HTML

## For the HTML Flask Code details refer :
- https://github.com/pathikpaul/firstflaskapp

## Deploying the AWS Lambda Code
- https://github.com/pathikpaul/firstflaskapp

## Using the AWS API Gateway
- https://github.com/pathikpaul/firstflaskapp

## Enabling Cognito Pools
- Ref https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6
- Cognito -> Manage User Pools -> Button(Create a user pool)
    - Name: serverlessdemo
    - **Create Role: "serverlessdemo-SMS-Role"**
    - App Client: serverlessclient
        - [] Generate client secret **disabled**
- Grant Permissions for Cognito
   - AmazonCognitoPowerUser
- AWS API Gateway -> Authorizers -> Button(Create New Authorizer)
   - Name: MyCognitoAutorizer
   - Ref: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-enable-cognito-user-pool.html
       - Token source: Authorization (use this header name to pass the token in your code)
