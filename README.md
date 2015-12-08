# MeetMe

The MeetMe app allows a user to schedule a meeting with other users by finding common free times by pulling data from Google Calendars.
MeetMe is live at http://ix.cs.uoregon.edu:6048

# How it Works

The user who proposes the meeting selects a date range and a calendar(s). Upon submitting this data, the application saves their
free times and provided that user with a link to send to other users and a key to submit once all users have inputted their schedules.

When a second, third, ect. user load the link provided by the meeting proposer (user 1), they are taken to a page where they submit
a date range and calendar(s). These free times are combined and compared with the free times of the other users to find mutual
free times between all users.

Once all users have submitted their free times, the meeting proposer can insert their key, which will display all mutual free times.
It is then up to the proposer to contact and share these times with other users and decide on a meeting time. 

<b>NOTE</b> This repo includes a test suite, called test.py. To run the 10 included test, install nosetests (pip install nosetests), then run "nosetests tests.py (I know that all it should take is "nosetests" but I could not get this working so please include the file name)

# Future Work/Potential improvements
1. <b>Add error-handling for when users enter incorrect URL or key</b> (This should best done ASAP! Currently too busy with finals)
2. Add email functionality to automatically notify users of invitations and updates to the free times
3. Add a way for users to vote on times and display what the most popular meeting times are
4. Add a button for the proposer to confirm a meeting time, which will send an email to all users letting them know of the time and date
5. Improve interface to be more intuitive on mobile devices
6. Algorithm for getting free times from busy times currently runs in O(n), could potentially look into a new, more efficient method

Please contact me with any other suggestions! igarrett@uoregon.edu

