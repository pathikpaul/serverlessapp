# My First Serverless App Used Flask to Deploy to HTML

## For the HTML Flask Code details refer :
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
## Ran the Front End Using the below
```bash
  export  FLASK_ENV=development
  export  FLASK_APP=application  ##
  flask run --host=192.168.77.10 ## since the machine does not have a browser I had to use below flask command instead of "flask run"
```
```bash
  http://192.168.77.10:5000/
```
## Deploying the AWS Lambda Code
- ReadNotes
     - lambda_read_notes.py
     - Will need S3 Read IAM role for the Read
     - Test with default template since no inputs are needed
- WriteNotes
     - lambda_write_notes.py
     - Will need S3 Full IAM role for the Read
     - test using below 
```json
{
  "list_of_notes": [
    {
      "topic": "Topic5",
      "comment": "Test 55555"
    }
  ],
  "key2": "value2",
  "key3": "value3"
}
```
## Deploying the AWS API Gateway
- Used two functions GET PUT
- GET
    - Authorization NONE
    - Lambda ReadNotes
    - Tested successfully (No inputs needed)
    - Please Hit the End Poing using the Browser .. you should get some output
- PUT
    - Authorization NONE
    - Lambda WriteNotes
    - tested using
```json
{
	"list_of_notes": [{
		"topic": "Topic6",
		"comment": "Test 66666"
	}]
}
```
## Adding the API Key to the API
- Create Usage Plan
   - Associate Usage Plan to API:Stage
- Create API Key
   - Associate Usage Plan to API Key
- Update GET  : Method Request : API Key Required true
- Update POST : Method Request : API Key Required true
- Deploy API 
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
