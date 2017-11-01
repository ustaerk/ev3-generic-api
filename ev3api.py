#!/usr/bin/env python3


# import ev3dev.ev3 as ev3
# import ev3dev.core as core

import rpyc
from flask import json
from flask import jsonify
from flask import Flask
app = Flask(__name__)
conn = rpyc.classic.connect('192.168.0.40')
ev3 = conn.modules['ev3dev.ev3']
core = conn.modules['ev3dev.core']

@app.route('/motors')
def list_motors():
    attached_motors = list(core.list_motors())
    motors = [motor_to_dict(attached_motor) for attached_motor in attached_motors]
    return jsonify(motors)

def motor_to_dict(motor):
    return dict(address = motor.address,
                # TODO: find out why this cannot be encoded as JSON
                # commands = motor.commands,
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
                # state = motor.state,
                stop_action = motor.stop_action,
                # stop_actions = motor.stop_actions,
                time_sp = motor.time_sp
                )