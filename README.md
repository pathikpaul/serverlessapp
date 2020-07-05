# My First Serverless App Used Flask to Deploy to HTML

## For the HTML Flask Code refer :
- https://github.com/pathikpaul/firstflaskapp

## Installed Flask using below commands
```bash
  sudo yum install python-virtualenv
  cd ~
  python2 -m virtualenv venv
  cd ~
  . venv/bin/activate
  pip install Flask==1.1.2
  pip install boto3==1.14.16
  mkdir serverlessapp
  cd serverlessapp
```
## Ran using the below
```bash
  export  FLASK_ENV=development
  export  FLASK_APP=application  ##
  flask run --host=192.168.77.10 ## since the machine does not have a browser I had to use below flask command instead of "flask run"
```
## Tested at below URL
```bash
  http://192.168.77.10:5000/
```
## Uses AWS Resources
- Lambda
- API Gateway
- SSM Parameter Store

## Storing the API Key in the AWS SSM Parameter Store
Ref:
- https://aws.amazon.com/systems-manager/pricing/
- Standard Pricing – Free – (upto 10,000 Parameter Store API interactions per month)

"Systems Manager" -> "Parameter Store" -> "button[Create parameter]"
```bash
     Name:            APIKey
     Type:            SecureString
     KMS key source:  My current account
     Value:  ..       **** value obatined from API Key Store… ***
```
