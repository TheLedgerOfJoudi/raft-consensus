import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2
import grpc
from concurrent import futures
import random
import sys
from enum import Enum
from threading import Timer
import time

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

leader_id = 0
term_number = 0
timer = None
leader_timer = None
timer_interval = 0
nodes = {}
id = sys.argv[1]
state = State.FOLLOWER
votes = {}
voted = False
lock = False

class RaftServiceHandler(pb2_grpc.RaftServiceServicer):
    def RequestVote(self, request, context):
        reset_timer()
        sender_term = request.term
        sender_id = request.id
        global term_number
        global voted
        if sender_term > term_number:
            term_number = sender_term
            voted = False
        my_vote = not voted
        if my_vote:
            print_to_console("Voted for node " + str(sender_id))
        reply = {"term": term_number, "vote": my_vote}
        voted = True
        return pb2.RequestVoteResponse(**reply)

    def AppendEntries(self, request, context):
        reset_timer()
        global leader_id
        sender_term = request.term
        leader_id = request.id
        ack = False
        if sender_term > term_number:
            ack = True
        reply = {"term": term_number, "ack": ack}
        return pb2.AppendEntriesResponse(**reply)

    def GetLeader(self, request, context):
        msg = request.message
        i = leader_id
        addr = nodes[str(i)]
        print_to_console("Command from client: getleader")
        print_to_console(str(id) + " " + nodes[str(i)])
        reply = {"id": i, "address": addr}
        return pb2.GetLeaderResponse(**reply)

    def Suspend(self, request, context):
        global lock
        timeout = request.timeout
        print_to_console("Command from client: suspend " + str(timeout))
        lock = True
        time.sleep(timeout)
        lock = False
        reply = {}
        return pb2.SuspendResponse(**reply)

def print_to_console(msg):
    print("From server " + id + ": " + msg)

def print_whoami():
    if state == State.FOLLOWER:
        print_to_console("I am a follower. Term " + str(term_number))
    if state == State.CANDIDATE:
        print_to_console("I am a candidate. Term " + str(term_number))
    if state == State.LEADER:
        print_to_console("I am a leader. Term " + str(term_number))

def send_heartbeat():
    if lock:
        return
    for addr in nodes.values():
        if addr == nodes[id]:
            continue
        channel = grpc.insecure_channel(addr)
        stub = pb2_grpc.RaftServiceStub(channel)
        response = None
        global term_number
        global state
        try:
            response = stub.AppendEntries(pb2.AppendEntriesMessage(term=term_number, id = int(id)))
        except:
            continue
        
        if response.term > term_number:
            term_number = response.term
            become_follower()
            return
    become_leader()

def send_request_vote():
    for addr in nodes.values():
        if addr == nodes[id]:
            continue
        channel = grpc.insecure_channel(addr)
        stub = pb2_grpc.RaftServiceStub(channel)
        response = None
        global term_number
        global state
        try:
            response = stub.RequestVote(pb2.RequestVoteMessage(term=term_number, id = int(id)))
        except:
            continue

        if response.term > term_number:
            term_number = response.term
            become_follower()
            return
        if response.vote == True and votes.get(term_number):
            votes[term_number] += 1
    print_to_console("Votes received")
    if votes.get(term_number) and votes[term_number] > len(nodes.keys()) / 2:
         become_leader()
    return 0

def reset_timer():
    global timer
    global timer_interval
    timer.cancel()
    timer = Timer(timer_interval, become_candidate)
    timer.start()

def become_leader():
    global state
    global leader_timer
    state = State.LEADER
    print_whoami()
    if leader_timer is None:
        leader_timer = Timer(0.05, send_heartbeat)
        leader_timer.start()
    else:
        leader_timer.cancel() 
        leader_timer = Timer(0.05, send_heartbeat)
        leader_timer.start()       
    
def become_candidate():
    global state
    global voted
    global votes
    global term_number
    global timer
    if timer.finished and state.FOLLOWER:        
        print_to_console("The leader is dead")
        state = State.CANDIDATE
        term_number += 1
        print_whoami()
        votes[term_number] = 1
        voted = True
        print_to_console("Voted for node " + id)
        send_request_vote()

def become_follower():
    global timer
    global state
    global voted
    voted = False
    state = State.FOLLOWER
    print_whoami()
    if timer is None:
        timer = Timer(timer_interval, become_candidate)
        timer.start()
    else:
        reset_timer()

if __name__ == "__main__":
    with open("config.conf") as conf:
        while line := conf.readline():
            data = line.split()
            nodes[data[0]] = data[1] + ":" + data[2]

    timer_interval = random.randint(300,600) / 1000
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RaftServiceServicer_to_server(RaftServiceHandler(), server)
    server.add_insecure_port(nodes[id])
    server.start()
    print_to_console("The server starts at " + nodes[id] )
    time.sleep(5)
    become_follower()

    while True:
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            print("Shutting down")
            sys.exit(0)
