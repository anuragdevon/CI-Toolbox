import argparse
import requests
import subprocess
import os
import socket
import time

def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",
                        help="dispatcher's host, by default it uses localhost",
                        default="localhost",
                        action="store")
    parser.add_argument("--port",
                        help="dispatcher's host, by default it uses localhost",
                        default=8888,
                        action="store")
    args = parser.parse_args()

    server = ThreadingTCPServer((args.host, int(args.port)), DispatcherHandler)
    print("serving on {} {}".format(args.host, int(args.port)))
    
    runner_heartbeat.start()
    redistrbutor.start()

    # Activate the server
    server.dead = True
    runner_heartbeat.join()
    redistributor.join()

def runner_checker(server):
    def manage_commit_lists(runner):
        for commit, assigned_runner in server.dispatched_commits.iteritems():
            