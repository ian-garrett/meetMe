import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging
import uuid

# Imports to handle dates
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Google API for services
from apiclient import discovery

# OAuth2  - Google library implementation for convenience
from oauth2client import client
import httplib2   # used in oauth2 flow

# generate number
import random

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)


# Mongo database
from pymongo import MongoClient

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)


try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.meetme
    collection = db.dated
    print("Succesfully opened database!")

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = CONFIG.GOOGLE_LICENSE_KEY  ## You'll need this
APPLICATION_NAME = 'MeetMe'

#############################
#
#  Pages (routed from URLs)
#
#############################

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Entering index")
  if 'begin_date' not in flask.session:
    init_session_values()
  return render_template('index.html')

@app.route("/planner")
def planner():
    print("in planner")
    app.logger.debug("Entering planner")
    meetID = request.args.get('id')
    flask.session['finalMeet'] = meetID
    return render_template('index.html')

@app.route('/finalize', methods=['POST'])
def finalize():
    key = request.form.get("final")
    print (key)
    print("mergedate")
    dateRange = mergeDateRanges(key)
    print("mergeevents")
    busyTimes = mergeBusyTimes(key)
    # print("finish helpers")
    # print(type(dateRange['start']))
    # print(type(dateRange['end']))
    print("BEGIN")
    start = dateRange['startDate']
    print(start)
    end = dateRange['endDate']
    print(end)
    print("END")
    generateFreeTimes(busyTimes, start, end)

    return flask.redirect(flask.url_for("index"))

def mergeDateRanges(key):
    # loop through objects in mongo db
    starts = []
    ends = []
    for record in collection.find( { "type": "date_range" } ):
        if record['id'] == key:
            start = record['startDate']
            end = record['endDate']
            starts.append(start)
            ends.append(end)
 
    # sort lists
    starts.sort()
    ends.sort()
    # assemble date rate
    start = starts[-1]
    end = ends[0] #add 24 h
    end = arrow.get(end).isoformat()
    if start <= end:
        modifiedDateRange = {'startDate':start,'endDate':end}
        return modifiedDateRange
    else:
        return False

def mergeBusyTimes(key):
    # loop through objects in mongo db
    records = [ ]
    print("here1")
    for record in collection.find( { "type": "busyTimes" } ):
        #print(record)
        if record['id'] == key:
            start = arrow.get(record['start'])
            end = arrow.get(record['end'])
            blah = {'start':start, 'end':end}
            records.append(blah)
    print (records)
    return records

@app.route("/choose")
def choose():
    # Authorize list
    app.logger.debug("Checking credentials for Gooasgle calendar access")
    credentials = valid_credentials()
    if not credentials:
      app.logger.debug("Redirecting to authorization")
      return flask.redirect(flask.url_for('oauth2callback'))
    global gcal_service #used in busyTimes
    gcal_service = get_gcal_service(credentials)
    app.logger.debug("Returned from get_gcal_service")
    flask.session['calendars'] = list_calendars(gcal_service)
    return render_template('index.html')

####
#
#  Google calendar authorization:
#      Returns us to the main /choose screen after inserting
#      the calendar_service object in the session state.  May
#      redirect to OAuth server first, and may take multiple
#      trips through the oauth2 callback function.
#
#  Protocol for use ON EACH REQUEST:
#     First, check for valid credentials
#     If we don't have valid credentials
#         Get credentials (jump to the oauth2 protocol)
#         (redirects back to /choose, this time with credentials)
#     If we do have valid credentials
#         Get the service object
#
#  The final result of successful authorization is a 'service'
#  object.  We use a 'service' object to actually retrieve data
#  from the Google services. Service objects are NOT serializable ---
#  we can't stash one in a cookie.  Instead, on each request we
#  get a fresh serivce object from our credentials, which are
#  serializable.
#
#  Note that after authorization we always redirect to /choose;
#  If this is unsatisfactory, we'll need a session variable to use
#
####

def valid_credentials():
    """
    Returns OAuth2 credentials if we have valid
    credentials in the session.  This is a 'truthy' value.
    Return None if we don't have credentials, if not, return 
    a 'falsy' value.
    """
    if 'credentials' not in flask.session:
      return None

    credentials = client.OAuth2Credentials.from_json(
        flask.session['credentials'])

    if (credentials.invalid or
        credentials.access_token_expired):
      return None
    return credentials


def get_gcal_service(credentials):
  """
  We need a Google calendar 'service' object to obtain
  list of calendars, busy times, etc.  This requires
  authorization. If authorization is already in effect,
  we'll just return with the authorization. Otherwise,
  control flow will be interrupted by authorization, and we'll
  end up redirected back to /choose *without a service object*.
  Then the second call will succeed without additional authorization.
  """
  app.logger.debug("Entering get_gcal_service")
  http_auth = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http_auth)
  app.logger.debug("Returning service")
  return service

@app.route('/oauth2callback')
def oauth2callback():
  """
  The 'flow' has this one place to call back to.  We'll enter here
  more than once as steps in the flow are completed, and need to keep
  track of how far we've gotten. The first time we'll do the first
  step, the second time we'll skip the first step and do the second,
  and so on.
  """
  print("no break")
  app.logger.debug("Entering oauth2callback")
  flow =  client.flow_from_clientsecrets(
      CLIENT_SECRET_FILE,
      scope= SCOPES,
      redirect_uri=flask.url_for('oauth2callback', _external=True))

  ## The *second* time we enter here, it's a callback
  ## with 'code' set in the URL parameter.  If we don't
  ## see that, it must be the first time through, so we
  app.logger.debug("Got flow")
  if 'code' not in flask.request.args:
    app.logger.debug("Code not in flask.request.args")
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
    ## This will redirect back here, but the second time through
    ## we'll have the 'code' parameter set
  else:
    ## It's the second time through ... we can tell because
    ## we got the 'code' argument in the URL.
    app.logger.debug("Code was in flask.request.args")
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    ## Now I can build the service and execute the query,
    ## but for the moment I'll just log it and go back to
    ## the main screen
    app.logger.debug("Got credentials")
    return flask.redirect(flask.url_for('choose'))

#####
#
#  Option setting:  Buttons or forms that add some
#     information into session state.  Don't do the
#     computation here; use of the information might
#     depend on what other information we have.
#   Setting an option sends us back to the main display
#      page
#
#####

@app.route('/setrange', methods=['POST'])
def setrange():
    """
    User chose a date range with the bootstrap daterange
    widget.
    """

    daterange = request.form.get('daterange')
    flask.session['daterange'] = daterange
    daterange_parts = daterange.split()
    flask.session['begin_date'] = interpret_date(daterange_parts[0])
    flask.session['end_date'] = interpret_date(daterange_parts[2])
    key = str(random.randint(1000000000000, 9999999999999))
    flask.session['key'] = key
    try:
        #print("in try")
        key = flask.session['finalMeet']
        #print("KEY:",flask.session['finalMeet'])
        flask.session['key'] = key

    except:
        print ("still first user")

    record = {"type": "date_range",
                    "id": key,
                    "startDate":flask.session['begin_date'],
                    "endDate":flask.session['end_date']
                }
    collection.insert(record)
    app.logger.debug("Setrange parsed {} - {}  dates as {} - {}".format(
      daterange_parts[0], daterange_parts[1],
      flask.session['begin_date'], flask.session['end_date']))
    returnRange = flask.redirect(flask.url_for("choose"))

    return returnRange

@app.route('/select_calendars', methods=['POST'])
def getCalendars():
    app.logger.debug("Get selected caldendars")
    selectedCalendars = request.form.getlist('calendar')
    allCalendars = []
    for cal in flask.session['calendars']:
        if cal['id'] in selectedCalendars:
            allCalendars.append(cal)

    #put event times into a collective list
    allLists = []
    for cal in calendarEventsList(allCalendars):
        if cal: #In case list is empty
            for event in cal:
                start = arrow.get(event['start']).to('local')
                end = arrow.get(event['end']).to('local')
                allLists.append({'start':start, 'end':end})
                record = {"type":"busyTimes",
                            "start": start.isoformat(),
                            "end": end.isoformat(),
                            "id": flask.session['key']
                            }
                collection.insert(record)

    try:
        flask.session['finalMeet']
        flask.flash("Thanks for submitting. Please let the proposer know that you have submitted your times and wait for them to get back to you!")
    except:
        meetID = flask.session['key']
        instruct1 = "Thank you for entering you're schedule! Send the URL to the person(s) you want to meet with."
        instruct2 = "Once the person(s) you sent the link have entered their free times, you can use the key to view potential meeting times." 
        label1 = "The URL you are to send is below"
        url = "http://ix.cs.uoregon.edu:6048/planner?id="+meetID
        label2 = "The key you are enter into the box below upon recieving confirmation from those you have sent the URL to is below"
        flask.flash(instruct1)
        flask.flash(instruct2)
        flask.flash(label1)
        flask.flash(url)
        flask.flash(label2)
        flask.flash(meetID)



    # startDate = arrow.get(flask.session['begin_date'])
    # endDate = arrow.get(flask.session['end_date'])
    # print(startDate,type(startDate))
    # print(endDate,type(endDate))

    # generateFreeTimes(allLists, startDate, endDate)
    return flask.redirect(flask.url_for("index"))

####
#
#   Initialize session variables
#
####

def init_session_values():
    """
    Start with some reasonable defaults for date and time ranges.
    """
    # Default date span = tomorrow to 1 week from now
    now = arrow.now('local')
    tomorrow = now.replace(days=+1)
    nextweek = now.replace(days=+7)
    flask.session["begin_date"] = tomorrow.floor('day').isoformat()
    flask.session["end_date"] = nextweek.ceil('day').isoformat()
    flask.session["daterange"] = "{} - {}".format(
        tomorrow.format("MM/DD/YYYY"),
        nextweek.format("MM/DD/YYYY"))
    # Default time span each day, 8 to 5
    flask.session["begin_time"] = interpret_time("9am")
    flask.session["end_time"] = interpret_time("5pm")

def interpret_time( text ):
    """
    Read time in a human-compatible format and
    interpret as ISO format with local timezone.
    May throw exception if time can't be interpreted. In that
    case it will also flash a message explaining accepted formats.
    """
    app.logger.debug("Decoding time '{}'".format(text))
    time_formats = ["ha", "h:mma",  "h:mm a", "H:mm"]
    try:
        as_arrow = arrow.get(text, time_formats).replace(tzinfo=tz.tzlocal())
        app.logger.debug("Succeeded interpreting time")
    except:
        app.logger.debug("Failed to interpret time")
        flask.flash("Time '{}' didn't match accepted formats 13:30 or 1:30pm"
              .format(text))
        raise
    return as_arrow.isoformat()

def interpret_date( text ):
    """
    Convert text of date to ISO format used internally,
    with the local time zone.
    """
    try:
      as_arrow = arrow.get(text, "MM/DD/YYYY").replace(
          tzinfo=tz.tzlocal())
    except:
        flask.flash("Date '{}' didn't fit expected format 12/31/2001")
        raise
    return as_arrow.isoformat()

def next_day(isotext):
    """
    ISO date + 1 day (used in query to Google calendar)
    """
    as_arrow = arrow.get(isotext)
    return as_arrow.replace(days=+1).isoformat()

####
#
#  Functions (NOT pages) that return some information
#
####


def calendarEventsList(calendarList):
    # gets events from selected calendars
    app.logger.debug("ENTERING CALENDAREVENTSLISTS")
    busyTimes = []
    beginDate = flask.session['begin_date']
    endDate = flask.session['end_date']
    endDate = arrow.get(endDate).replace(hours=+24).isoformat() # 24 hours added is to split into days
    for calendar in calendarList:
        ID = calendar['id']
        freebusy_query = {
            "timeMin" : beginDate,
            "timeMax" : endDate,
            "items" : [{ "id" : ID }]
        }
        result = gcal_service.freebusy().query(body=freebusy_query).execute()
        resultTimes = result['calendars'][ID]['busy']
        busyTimes.append(resultTimes)

    app.logger.debug("EXIT CALENDAREVENTSLISTS")
    return busyTimes

def sortEvents(eventList):
    # sort list by start time and return sorted list
    startTimes = []
    sortedTimes = []
    for event in eventList: # loop through events and add all start times to startTimes
        print (event)
        startTimes.append(event['start'])
    startTimes.sort() # sort by start time
    for times in startTimes: # loop through start times and create events to append to sortedTimes
        for event in eventList:
            if (times == event['start']):
                sortedTimes.append({'start':event['start'], 'end':event['end']})
    return sortedTimes

def addNights(eventList, startDate, endDate):
    # add busy events every day from 7am-9pm
    startDate = arrow.get(startDate)
    endDate = arrow.get(endDate)
    for day in arrow.Arrow.span_range('day', startDate, endDate): # loop through days in range
        startOfDay= {'start':day[0], 'end':day[0].replace(hours=+7)}
        endOfDay = {'start':day[1].replace(hours=-3).replace(seconds=+.000001), 'end':day[1].replace(seconds=+.000001)}
        eventList.append(startOfDay)
        eventList.append(endOfDay)
    return eventList

def generateFreeTimes(allLists, startDate, endDate):
    # bring the whole shabang together

    allLists = addNights(allLists, startDate, endDate) #add all times between 9pm-7am as a busy event
    sortedEvents = sortEvents(allLists) #sort the events
    freeTimes = fetchFreeTimes(sortedEvents) #fetch the list of free times

    displayTimes(freeTimes)

def displayTimes(freeTimes):
    # format time-ranges in a easy-to-read, easy-to-analyze format
    for times in freeTimes:
        message = []
        message.append("From ")
        message.append(times['start'].format('MM/DD/YYYY h:mm A'))
        message.append(" until ")
        message.append(times['end'].format('MM/DD/YYYY h:mm A'))
        message = ''.join(message)
        flask.flash(message)

def fetchFreeTimes(sortedList):
    correctedSortedList = duplicateRemover(sortedList) # call to remove duplicates

    freeTimes = []
    length = len(correctedSortedList)-1
    for i in range(length): # loop through events, and create free times out of gaps between busy events
        event = correctedSortedList[i]
        nextEvent = correctedSortedList[i+1]
        if nextEvent['start'] > event['end']: # if the start of the next event occurs after the end of the current event
            freeTimes.append({'start':event['end'], 'end':nextEvent['start']}) # append the time between to free times
    return freeTimes

def duplicateRemover(eventList): 
    #corrects overlaps in busy times
    correctedList = []
    for i in range(len(eventList)-1):
        event = eventList[i]
        nextEvent = eventList[i+1]
        event['end'].replace
        if (event['end'] > nextEvent['end'] and nextEvent['start'] < event['end']):
            correctedList.append({'start':event['start'], 'end':event['end']})
            eventList[i+1]['end'] = event['end'] # correctly iterates
        elif (event['end'] > nextEvent['start']):
            correctedList.append({'start':event['start'], 'end':nextEvent['start']})
        else:
            correctedList.append({'start':event['start'], 'end':event['end']})
    correctedList.append(eventList[len(eventList)-1]) # event is added to correctedList
    return correctedList


def list_calendars(service):
    """
    Given a google 'service' object, return a list of
    calendars.  Each calendar is represented by a dict, so that
    it can be stored in the session object and converted to
    json for cookies. The returned list is sorted to have
    the primary calendar first, and selected (that is, displayed in
    Google Calendars web app) calendars before unselected calendars.
    """
    app.logger.debug("Entering list_calendars")
    calendar_list = service.calendarList().list().execute()["items"]
    result = [ ]
    for cal in calendar_list:
        kind = cal["kind"]
        id = cal["id"]
        if "description" in cal:
            desc = cal["description"]
        else:
            desc = "(no description)"
        summary = cal["summary"]
        # Optional binary attributes with False as default
        selected = ("selected" in cal) and cal["selected"]
        primary = ("primary" in cal) and cal["primary"]


        result.append(
          { "kind": kind,
            "id": id,
            "summary": summary,
            "selected": selected,
            "primary": primary
            })
    return sorted(result, key=cal_sort_key)


def cal_sort_key( cal ):
    """
    Sort key for the list of calendars:  primary calendar first,
    then other selected calendars, then unselected calendars.
    (" " sorts before "X", and tuples are compared piecewise)
    """
    if cal["selected"]:
       selected_key = " "
    else:
       selected_key = "X"
    if cal["primary"]:
       primary_key = " "
    else:
       primary_key = "X"
    return (primary_key, selected_key, cal["summary"])


#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try:
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try:
        normal = arrow.get( time )
        return normal.format("HH:mm")
    except:
        return "(bad time)"

#############


if __name__ == "__main__":
  # App is created above so that it will
  # exist whether this is 'main' or not
  # (e.g., if we are running in a CGI script)

  app.secret_key = str(uuid.uuid4())
  app.debug=CONFIG.DEBUG
  app.logger.setLevel(logging.DEBUG)
  # We run on localhost only if debugging,
  # otherwise accessible to world
  if CONFIG.DEBUG:
    # Reachable only from the same computer
    app.run(port=CONFIG.PORT)
  else:
    # Reachable from anywhere
    app.run(port=CONFIG.PORT,host="0.0.0.0")
