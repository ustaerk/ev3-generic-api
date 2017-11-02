#!/usr/bin/env python3


# import ev3dev.ev3 as ev3
# import ev3dev.core as core

import rpyc
from flask import json
from flask import jsonify
from flask import Flask
from flask import request
app = Flask(__name__)
conn = rpyc.classic.connect('192.168.0.40')
ev3 = conn.modules['ev3dev.ev3']
core = conn.modules['ev3dev.core']

@app.route('/motors', methods=['GET'])
def list_motors():
    attached_motors = list(core.list_motors())
    motors = [motor_to_dict(attached_motor) for attached_motor in attached_motors]
    return jsonify(motors)

@app.route('/motors/<string:port>', methods=['PUT'])
def change_motor(port):
    payload = request.json
    handle_payload(port, payload)
    return jsonify({})

def handle_payload(port, payload):
    motor = ev3.Motor(port); assert motor.connected
    if not payload['state']:
        motor.reset()
    elif payload['state'] == 'running':
        if 'running' not in motor.state:
            motor.run_direct(duty_cycle_sp = 100)
        handle_attributes(motor, payload)
    else:
        raise InvalidUsage('Unsupported state.')

def handle_attributes(motor, payload):
    assert motor.connected
    if 'duty_cycle_sp' in payload:
        motor.duty_cycle_sp = payload['duty_cycle_sp']

def motor_to_dict(motor):
    return dict(address = motor.address,
                commands = motor.commands,
                driver_name = motor.driver_name,
                duty_cycle = motor.duty_cycle,
                duty_cycle_sp = motor.duty_cycle_sp,
                is_holding = motor.is_holding,
                is_overloaded = motor.is_overloaded,
                is_ramping = motor.is_ramping,
                is_running = motor.is_running,
                is_stalled = motor.is_stalled,
                max_speed = motor.max_speed,
                polarity = motor.polarity,
                position = motor.position,
                position_sp = motor.position_sp,
                ramp_down_sp = motor.ramp_down_sp,
                ramp_up_sp = motor.ramp_up_sp,
                speed = motor.speed,
                speed_sp = motor.speed_sp,
                state = motor.state,
                stop_action = motor.stop_action,
                stop_actions = motor.stop_actions,
                time_sp = motor.time_sp
                )

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response