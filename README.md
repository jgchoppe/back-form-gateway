# How to deploy

## Requirements

### AWS Credentials

All the steps requires you to have [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) installed.

It also needs your credentials to be set inside `~/.aws/credentials`. If your profile isn't the default profile don't forget to specify it when it's necessary.

### Serverless

Make sure you have [Serverless](https://www.serverless.com/framework/docs/providers/aws/guide/installation/) installed.

## Deployment

All you have to do is deploying the app with the following command (default profile):

```bash
$ serverless deploy
```

If you want to specify the AWS profile:

```bash
$ serverless deploy --aws-profile $profileName
```

# Development purpose

## Create API route

### Python Function

Considering that the API is in python, you'll have to create python files.
For good development purpose, you will have to create a new folder if you want to add a new type of routes (e.g.: users):

```bash
$ mkdir users
```

You can now create python file inside this new folder.
Because our route will be AWS Lambda, you don't have to create a main function.

### Add the new route to Serverless

You can open serverless.yml:

```bash
$ nano serverless.yml
```

At the end of the file you will find the `functions` part.

#### Add the new route without authorization

You can add the following part to the yml file in functions part:

```
  ...
  users:
    handler: users/users.get_users # folder/py_file/function_name
    events:
      - http:
          path: users                       # path to the route
          method: get                       # method to use (get, post, delete...)
```

#### Add the new route with authorization

Note: A route with authorization mean that if you want to call the route you will have to put an `Authorization` in the header of the request where the value is the tokenID provided by Cognito.

You can add the following part to the yml file in functions part:

```
  ...
  users:
    handler: users/users.delete_user 
    events:
      - http:
          path: users/{id}
          method: delete
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
```
