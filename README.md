# Messaging Application Challenge

This repository contains the API for a simple text messaging application (with authentication, p2p messaging and group chat functionalities).

## Technology stack
The application is written in Python 3.10, using the Flask web framework.
The storage is done using SQLite 3
The deployment is done using Docker + DockerCompose
User passwords are hashed using the bcrypt library

## Data model
The application uses 3 entities:
 - User
 - Message
 - Chat
Chats are general entities that can apply to either group chats or P2P chats. In other words, P2P chats are just chats limited to 2 participants, automatically created when User A sends a message to User B for the first time.
Each of the entities has a corresponding repository and controller

## API Documentation
The following API endpoints are available, grouped in 3 categories:

### Authentication API Endpoints

 - [POST] /v1/auth/register
	 - Registers a new user account
	 - The request body should be a JSON dict of format:
		 - {"username":"USERNAME FOR THE CREATED USER", "password":"PASSWORD FOR THE CREATED USER"}
	 - Returns:
		 - 200 on Success
		 - 400 if the request body is malformed or the username is already in use
 - [POST] /v1/auth/login
	 - Logs in into an existing user account and saves the session
	 - The request body should be a JSON dict of format:
		 - {"username":"USERNAME FOR THE USER", "password":"PASSWORD FOR THE USER"}
	 - Returns:
		 - 200 on Success
		 - 400 if the request body is malformed, the username doesn't exist, or the password is invalid
- [POST] /v1/auth/logout
	- Logs out of an existing user account and clears the session
	- Requires the user to be authenticated
	 - Returns:
		 - 200 on Success
		 - 401 if the user is not authenticated

### Group Chat API Endpoints
 - [POST] /v1/group_chat
	 - Creates a new group chat
	- Requires the user to be authenticated
	 - Returns:
		 - 200 on Success, and the ID of the newly created group chat in the response body
		 - 401 if the user is not authenticated
 - [POST] /v1/group_chat/{int:group_chat_id}/participants
	 - Adds a user to a group chat
	- Requires the user to be authenticated
	- The request body should be a JSON dict of format:
		 - {"username":"USERNAME FOR USER TO BE ADDED"}
	 - Returns:
		 - 200 on Success
		 - 400 if the request body is malformed, the user does not exist, the chat ID refers to a P2P chat or the user is already part of that chat
		 -  401 if the user is not authenticated
		 - 403 if the user sending the request is not part of the given group chat (and thus, doesn't have authorization to add users to it)
 - [DELETE] /v1/group_chat/{int:group_chat_id}/participants/{str:user_id}
	 - Removes a user from a group chat
	- Requires the user to be authenticated
	 - Returns:
		 - 200 on Success
		 - 400 if the user does not exist or the user is not part of that chat
		- 401 if the user is not authenticated
		 - 403 if the user sending the request is not part of the given group chat (and thus, doesn't have authorization to remove users from it)

### Message API Endpoints
 - [POST] /v1/messages
	 - Sends a new message
	- Requires the user to be authenticated
	- The request body should be a JSON dict of one of these formats:
		 - {"group_chat_id":"ID OF THE GROUP CHAT WHERE THE MESSAGE SHOULD BE SENT", "message":"MESSAGE CONTENT"}
		- {"dest_username":"USERNAME THAT SHOULD RECEIVE THE P2P MESSAGE", "message":"MESSAGE CONTENT}
	- Returns:
		 - 200 on Success
		 - 400 if the body of the request is malformed or the destination P2P user does not exist
		 - 401 if the user is not authenticated
		 - 403 if the user sending the request is not part of the given group chat (and thus, doesn't have authorization to send messages to it)
 - [GET] /v1/group_chat/messages
	 - Gets all messages from all group and P2P chats for the user
	- Requires the user to be authenticated
	 - Returns:
		 - 200 on Success, with all of the messages in the response body (the list CAN be empty)
		 - 401 if the user is not authenticated
 - [GET] /v1/group_chat/messages/group/{int:group_chat_id}
	 - Gets all messages from a group chat
	- Requires the user to be authenticated
	 - Returns:
		 - 200 on Success, with all of the messages in the response body (the list CAN be empty)
		 - 401 if the user is not authenticated 
		 - 403 if the user sending the request is not part of the given group chat (and thus, doesn't have authorization to read messages in it)
- [GET] /v1/group_chat/messages/p2p/{string:dest_username}
	 - Gets all messages from the P2P conversation between the user sending the request and the one with the username dest_username
	- Requires the user to be authenticated
	 - Returns:
		 - 200 on Success, with all of the messages in the response body (the list CAN be empty)
		 - 400 if the destination user does not exist
		 - 401 if the user is not authenticated

## Deployment information
The project includes a Dockerfile that can be used for development deployment. After downloading the project, the container can be built using:

    `$ docker build --tag messaging-application-challenge src`

Afterwards, the container can be run most simply using docker-compose. The `docker-compose.yml` file should contain:

     version: "3.6"
        services:
          messaging-application-challenge:
            container_name: messaging-application-challenge
            image: messaging-application-challenge
            ports:
              - 12000:12000
            volumes:
              - ${USERDIR}/docker/MessagingApplicationChallenge/resources:/app/resources
            environment:
              - FLASK_SECRET_KEY=RANDOMLY GENERATED SECRET FLASK KEY GOES HERE

Then, the container can be started with:
`$ docker-compose -f ./docker-compose.yml up -d`

Alternatively, the container can be run from the command line using:

    $ docker run -d --name messaging-application-challenge 
    -p 12000:12000
    -e FLASK_SECRET_KEY=RANDOMLY_GENERATED_SECRET_FLASK_KEY_GOES_HERE 
    -v ${USERDIR}/docker/MessagingApplicationChallenge/resources:/app/resources 
    messaging-application-challenge

The given Dockerfile uses Flask's built-in webserver and is, thus, unsuitable for a production environment. This should only be used in a development environment.
For a production environment, an alternative web server should be used (such as Apache or Tomcat) in order to serve files securely and with full performance.
