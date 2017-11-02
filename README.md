# ev3-generic-api
A generic REST API exposing motors and sensors on an ev3dev-enabled brick. Makes use of Flask to serve the API.

# Running
Requires Flask to be installed. Follow the Flask installation instructions or run e.g. `sudo pip3 install flask`.
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
 * `GET /motors` - list all currently connected motors with their states
 * `PUT /motors/{port}` - modify the state of the motor connected to `{port}` (see below)

To be implemented:
 * `GET /sensors` - list all sensors currently connected to the brick
 * `GET /sensors/{port}` - read the current value of the sensor connected to `{port}`

# Interacting with motors
This API aims to be truly RESTful so instead of calling actions you specify the desired state of the motor in question and let the API handle the rest. E.g. for running the motor at 100% you `PUT` the following JSON object to `/motors/{port}`:

```
{
    "state": "running",
    "duty_cycle_sp": "100"
}
```

Similarily for stopping the motor you would `PUT`

```
{
    "state": []
}
```
## States
The following states are currently supported
 * `running` - starts the motor using `run-direct`. Runs at 100% if `duty_cycle_sp` is not provided
 * `[]` - stops the motor using the default stop action (`coast`)

In the future, the following additional states could be possible
 * `holding` - stops the motor using the `hold` stop action
 * `running` in combination with `time_sp` - start the motor using `run-timed`

## Attributes
The only attribute currently supported is `duty_cycle_sp` and only in combination with starting the motor (changing its state to `running`). 

All other attributes (e.g. `stop_action` or `speed_sp`) are currently unsupported. This will hopefully change in later versions.