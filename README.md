# Social Network App


## Project Setup

1. Clone the repository using
```
https://github.com/destinysam/social_network.git
```
2. Setup the enviornment using
```
python3 -m venv env
```
4. Activate the environment (Linux only)
```
source env/bin/activate
```
4. install the dependency into it
```
pip install -r requirements.txt
```
5. Make migrations
```
python3 manage.py makemigrations
```
6. Migrate migrations
```
python3 manage.py migrate
```
7. To run server
```
python3 manage.py runserver
```

## Project Architect

### This project consists of 2 apps:

1. **users** -> Used to manage the user related stuff like api's, models.
   
2. **network** -> Used to send,update friend requests and much more.
  




## DataBase Schema

1. **User** -> Used to manage user details.

2. **FriendRequests** -> Used to manage friend requests.




## API's

### users app

1. **SignUpAPI** -> Used to register users.

2. **SigninAPI** -> Used to Signin users and get access token,refresh token.

3. **RefreshTokenAPI** -> Used to get access token using refresh token.


### network app

1. **SendFriendRequestAPI** -> Used to send friend requests.

2. **UpdateFriendRequestAPI** -> Used to accept/reject friend requests.

3. **AcceptedFriendRequestAPI** -> Used to list the accepted friend requests of a user.

4. **PendingFriendRequestAPI** -> Used to list the recieved pending friend requests.

5. **ListUserAPI** -> Used to list the users based on search keyword.


   




