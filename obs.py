# Imports
import argparse
import requests
import subprocess
import os
import socket
import time

def poll():
    """
    Pulls main repo and updates commits
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
                        "--dispatcher-server",
                        help="dispatcher host:port, "\
                        "by default it uses localhost:8888",
                        default="localhost:8888",
                        action="store"
    )

    parser.add_argument("repo", metavar="REPO", type=str,
                        help="path to the repository this will observe")
    args = parser.parse_args()
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(":")
    print("Observing repo: {}".format(args.repo))
    print("Dispatcher: {}:{}".format(dispatcher_host, dispatcher_port))
    print("Waiting for changes...")
    
    # Observe repo changes
    while True:
        try:
            subprocess.call(["git", "pull"])
            print("Commit: {}".format(subprocess.check_output(["git", "rev-parse", "HEAD"])))
            requests.post("http://{}:{}/commit".format(dispatcher_host, dispatcher_port),
                            data={"repo": args.repo, "commit": subprocess.check_output(["git", "rev-parse", "HEAD"])})
        except Exception as e:
            raise Exception("Could not update repo and check commit => {}".format(e))

        if os.path.exists(".commit_id"):
            try:
                response = helpers.communicate(dispatcher_host,
                                                int(dispatcher_port),
                                                "status")
            except socket.error as e:
                raise Exception("Could not communicate with dispatcher => {}".format(e))

            if response == "OK":
                commit = ""
                with open(".commit_id", "r") as f:
                    commit = f.readline()
                response = helpers.communicate(dispatcher_host,
                                                int(dispatcher_port),
                                                "dispatch:{}".format(commit))
                if response != "OK":
                    raise Exception("Could not dispatch commit => {}".format(response))
                
                print("Dispatched commit: {}".format(commit))
                
            else:
                raise Exception("Could not dispatch the test => {}".format(response))
        
        # Delay
        time.sleep(2)





        # if os.path.isfile(".commit_id"):
            # with open(".commit_id", "r") as f:
                # commit_id = f.read()
            # requests.post("http://{}:{}/commit".format(dispatcher_host, dispatcher_port),
                            # data={"repo": args.repo, "commit": commit_id})
            # os.remove(".commit_id")