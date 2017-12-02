""""""
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from qp_simulate import QPSimulator
    QPSimulator().simulate_1(QPSimulator.simulate_start_at_c_only)

    print "-- Auto Turret and Cockpit Station --"
    QPSimulator().simulate_many(QPSimulator.simulate_start_at_c_only, 1000)
    print "-- Auto Turret and Life Support Station --"
    QPSimulator().simulate_many(QPSimulator.simulate_start_at_ls_only, 1000)
    print "-- Cockpit and Life Support Station --"
    QPSimulator().simulate_many(QPSimulator.simulate_start_c_ls_only, 1000)
    print "-- Random Stations (LS, AT, or C) --"
    QPSimulator().simulate_many(QPSimulator.simulate_start_random, 1000)
    print "-- Based on Life Support State --"
    QPSimulator().simulate_many(QPSimulator.simulate_start_smartish, 1000)
