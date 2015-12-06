# MeetMe

The MeetMe app allows a user to schedule a meeting with other users by finding common free times by pulling data from Google Calendars.
This application allows you to schedule a meeting with a group of people
App can be found on http://ix.cs.uoregon.edu:6048 (Not currently running, contact me and I will launch it for use)

# How it Works

The user who proposes the meeting selects a date range and a calendar(s). Upon submitting this data, the application saves their
free times and provided that user with a link to send to other users and a key to submit once all users have inputted their schedules.

When a second, third, ect. user load the link provided by the meeting proposer (user 1), they are taken to a page where they submit
a date range and calendar(s). These free times are combined and compared with the free times of the other users to find mutual
free times between all users.

Once all users have submitted their free times, the meeting proposer can insert their key, which will display all mutual free times.
It is then up to the proposer to contact and share these times with other users and agree on a meeting time. 

<b>NOTE</b>Remove function and test suites in progress.
