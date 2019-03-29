import random
import time
import argparse

from stem import Signal
from stem.control import Controller
import stem.control

__parser = argparse.ArgumentParser("A script tool for getting multiple IPs from Tor.")
__parser.add_argument('-c', dest='circuits', type=int, default='128', help='Number of Circuits with sorted exit addresses.')
__parser.add_argument('-ca', type=str, dest='tor_control_address', default='127.0.0.1', help='Tor control port address.')
__parser.add_argument('-cp', dest='tor_control_port', type=int, default='9051', help='Tor control port.')
__parser.add_argument('-cpp', type=str, dest='tor_control_password', default='', help='Tor control password.')
args = __parser.parse_args()

with Controller.from_port(address = args.tor_control_address, port = args.tor_control_port) as controller:
    controller.authenticate(password = args.tor_control_password)
    controller.signal(Signal.NEWNYM)
    controller.set_conf('__LeaveStreamsUnattached', '1')

    avail_circuits = list()

    def attach_stream(stream):
        if stream.status == 'NEW' or stream.status == 'NEWRESOLVE':
            print("Detected new connection.")
            try:
                controller.attach_stream(stream.id, random.choice(avail_circuits))
            except:
                print("Error servicing request")

    controller.add_event_listener(attach_stream, stem.control.EventType.STREAM)

    def circuit_destroyed(circuit):
        if circuit.status == 'FAILED' or circuit.status == 'CLOSED':
            if circuit.id in avail_circuits:
                print("Circuit %s has failed." % (circuit.id))
                avail_circuits.remove(circuit.id)

    controller.add_event_listener(circuit_destroyed, stem.control.EventType.CIRC)

    while True:
        if len(avail_circuits) < args.circuits:
            while len(avail_circuits) < args.circuits:
                try:
                    circuit_id = controller.new_circuit(await_build=True)
                    avail_circuits.append(circuit_id)
                    print("Built circuit (%d/%d)" % (len(avail_circuits), args.circuits))
                except:
                    print("Failed to establish circuit!")
                time.sleep(1)

            print("Operating at peak performance.")

        time.sleep(5)
