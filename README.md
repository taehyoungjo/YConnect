# Yale Connect
## Overview
YConnect is a website that allows Yale students to connect with each other based on college specific criteria such as major, graduation year, and residential college. After finding a someone’s profile the user is then able to “connect” with them which allows the user to easily find that person’s profile again. The user of the website is able to keep their profile up to date if anything changes through the update profile tab.

## Startup
The project is implemented as a flask website, therefore the website can be started using `flask run` .

When the website first initializes the login page is displayed. From this page you can either log in or register for an account. Test accounts are available to use as an alternative to testing the registration feature:

```
username: abc
password: 123

username: test1
password: test
```

## Using the App
### Home Screen
After logging in the user is presented with the search screen where they are able to find other users based on criteria located at the top of the screen. After searching based on criteria cards that contain profile information are presented and the user is able to select them. Opening the profile shows the user’s profile picture (or a default if none was uploaded) along with the information that the user gave at sign up or updated later. This screen is also where users are able to connect with each other. If the user decides to “Add a Connection” with a user they are able to see these “connected” people through the connections screen.

### User Profile
Moving along the menu bar to profile shows the users profile. This page is not able to be edited and just shows the information that is associated with the user.

### Connections
Connections is a page that shows all the other users that the primary user has connected with through using the app. From this page the primary user is able to see basic information about connections including name, major, and year. They are also able to easily go to the users profile and remove the connection.

### Update Profile
The final tab on the menu bar is update profile. This is used both to create new profiles and update the information of the current user. From this page the user is able to provide all the information such as name, major, class, and residential college. The user is also able to upload a profile picture and provide a bio for other users to see. This information composes the basic information that is associated with the user.

Aside from this information, the user is also able to selected and deselect the classes that they are registered for. The search bar allows the user to input Class ID and a list of classes are generated. The user is then able to select classes using the check box which will then display in the selected classes. Finally, the user is then able to deregister from classes that they have already selected.

## Summary
YConnect is an app that seeks to allow Yale students to connect based on things that matter to Yale students. It seeks to fill the void between purely information apps (such as Yale’s current facebook directory) and full-fledged social apps. Through highlighting important aspects of the college experience and allowing users to find others who are like them, YConnect helps make the Yale college experience more interconnected.

### Project by John Brockmeier, John Kim, Tae Hyoung Jo







