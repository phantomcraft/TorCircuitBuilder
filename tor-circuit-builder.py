import random
import time

from stem import Signal
from stem.control import Controller
import stem.control

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)
    controller.set_conf('__LeaveStreamsUnattached', '1')

    avail_circuits = list()

    def attach_stream(stream):
        if stream.status == 'NEW' or stream.status == 'NEWRESOLVE':
            print "Detected new connection."
            try:
                controller.attach_stream(stream.id, random.choice(avail_circuits))
            except:
                print "Error servicing request"

    controller.add_event_listener(attach_stream, stem.control.EventType.STREAM)

    def circuit_destroyed(circuit):
        if circuit.status == 'FAILED' or circuit.status == 'CLOSED':
            if circuit.id in avail_circuits:
                print "Circuit %s has failed." % (circuit.id)
                avail_circuits.remove(circuit.id)

    controller.add_event_listener(circuit_destroyed, stem.control.EventType.CIRC)

    while True:
        if len(avail_circuits) < 128:
            while len(avail_circuits) < 128:
                try:
                    circuit_id = controller.new_circuit(await_build=True)
                    avail_circuits.append(circuit_id)
                    print "Built circuit (%d/%d)" % (len(avail_circuits), 128)
                except:
                    print "Failed to establish circuit!"
                time.sleep(1)

            print "Operating at peak performance."

        time.sleep(5)
