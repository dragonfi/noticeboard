# noticeboard
A simple non-authenticated HTML notice board.

I mainly wrote this as a practice example to learm more about Flask and AngularJS.

It provides a web page showing a list of messages, updated near-realtime. Users can add/remove messages.

Note that this is completely unmoderated and doesn't scale well. (As in, the queries return all messages.)

## Setup

It is assumed that python3, pip3, nodejs, jasmine and karma are installed.

It is recommended to create a python virtual environment in order not to clutter up the global site directory.

    pip3 install -r requirements.txt
    npm install angular angular-mocks --prefix noticeboard/static
  
## Test

run `start_karma.sh` for javascript and `start_unittest.sh` for python unit test runners.
These will continually check your source files for changes and automatically re-run the necessary tests.

## Run developement server

    python3 noticeboard/noticeboard.py

  
