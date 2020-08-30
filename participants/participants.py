import json
import boto3
import decimal
import json

dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
table = dynamodb.Table('Form')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def generate_response(status, body):
    return {
        "statusCode": status,
        "body": json.dumps(body, indent=4, cls=DecimalEncoder),
        "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True}
    }


def add_participant(event, context):
    try:
        table.put_item(Item={"userName": event['userName'], "activity": event['activity'], "email": event['email'],
                             "phone": event['phone'], "rulantica": event['rulantica'], "school": event['school']},
                       ConditionExpression="attribute_not_exists(userName)")
    except Exception as e:
        return generate_response(400, e)
    return generate_response(200, {"Status": True})


def get_participants(event, context):
    response = table.scan()
    return generate_response(200, response['Items'])


def get_participants_by_activity(event, context):
    response = table.get_item(Key={'Activity': 'PUT ACTIVITY'})
    return generate_response(200, response)


def edit_participant(event, context):
    try:
        table.update_item(
            Key={
                'UserName': 'PUT USERNAME HERE',
            },
            UpdateExpression="set activity=:a, email=:e, phone=:p, rulantica=:r, school=:s",
            ExpressionAttributeValues={
                ':a': '',
                ':e': '',
                ':p': '',
                ':r': '',
                ':s': ''
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        return generate_response(400, e)
    return generate_response(200, {"Status": True})


def delete_participant(event, context):
    try:
        table.delete_item(
            Key={
                'UserName': "PUT USERNAME HERE"
            }
        )
    except Exception as e:
        return generate_response(400, e)
    return generate_response(200, {"Status": True})
