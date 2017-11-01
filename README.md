# ev3-generic-api
A generic REST API exposing motors and sensors on an ev3dev-enabled brick. Makes use of Flask to serve the API.

# Running
The ev3dev Python language bindings require Python 3 so you cannot simply run `flask run`. Use `python3 -m flask run` instead.

For local debug mode run with `FLASK_DEBUG=1`.

```
export FLASK_APP=ev3api.py
export FLASK_DEBUG=1
python3 -m flask run
```
To make development easier the API currently uses RPyC to connect to the Mindstorms brick. Be sure to follow the instructions at http://python-ev3dev.readthedocs.io/en/stable/rpyc.html for setting it up on the brick and your local machine.

# Resources
Working:
 * `GET /motors` - list all currently connected motors with their state

To be implemented:
 * `PUT /motors/{port}` - modify the state of the motor connected to `{port}`
 * `GET /sensors` - list all sensors currently connected to the brick
 * `GET /sensors/{port}` - read the current value of the sensor connected to `{port}`