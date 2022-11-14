import raft_pb2_grpc as pb2_grpc
import raft_pb2 as pb2
import grpc
import sys

server_channel = ""
channel = ""
stub = ""
if __name__ == "__main__":
    print("The client starts")
    while True:
        try:
            inp = input(">")
            splits = inp.split(" ")
            if splits[0] == "connect":
                server_channel = splits[1] + ":" + splits[2]
                channel = grpc.insecure_channel(server_channel)
                stub = pb2_grpc.RaftServiceStub(channel)
            elif splits[0] == "getleader":
                out = stub.GetLeader(pb2.GetLeaderMessage(message = "hi"))
                print(out)
            elif splits[0] == "suspend":
                id = int(splits[1])
                out = stub.Suspend(pb2.SuspendMessage(timeout=id))
                print(out)
            elif splits[0] == "quit":
                print("The client ends")
                break
            else:
                print("Unrecognised command\n")
        except KeyboardInterrupt:
            print("Shutting Down")
            sys.exit(0)
