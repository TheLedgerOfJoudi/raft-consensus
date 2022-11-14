import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2
import grpc
from concurrent import futures
import random
import sys

term_number = 0
timer = 0
nodes = {}
id = sys.argv[1]


class RaftServiceHandler(pb2_grpc.RaftServiceServicer):
    def RequestVote(self, request, context):
        msg = request.message
        reply = {"term": 0, "vote": True}
        return pb2.RequestVoteResponse(**reply)

    def AppendEntries(self, request, context):
        msg = request.message
        reply = {"term": 0, "ack": True}
        return pb2.AppendEntriesResponse(**reply)

    def GetLeader(self, request, context):
        msg = request.message
        addr = "0.0.0.0"
        i = 1
        reply = {"id": i, "address": addr}
        return pb2.GetLeaderResponse(**reply)

    def Suspend(self, request, context):
        msg = request.timeout
        reply = {}
        return pb2.SuspendResponse(**reply)


if __name__ == "__main__":
    with open("config.conf") as conf:
        while line := conf.readline():
            data = line.split()
            nodes[data[0]] = data[1] + ":" + data[2]

    timer = random.randint(150,300)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RaftServiceServicer_to_server(RaftServiceHandler(), server)
    server.add_insecure_port(nodes[id])
    server.start()
    while True:
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            print("Shutting down")
            sys.exit(0)
