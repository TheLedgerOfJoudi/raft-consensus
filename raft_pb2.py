# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\".\n\x12RequestVoteMessage\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\n\n\x02id\x18\x02 \x01(\x05\"1\n\x13RequestVoteResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0c\n\x04vote\x18\x02 \x01(\x08\"0\n\x14\x41ppendEntriesMessage\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\n\n\x02id\x18\x02 \x01(\x05\"2\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0b\n\x03\x61\x63k\x18\x02 \x01(\x08\"#\n\x10GetLeaderMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"0\n\x11GetLeaderResponse\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\"!\n\x0eSuspendMessage\x12\x0f\n\x07timeout\x18\x01 \x01(\r\"\x11\n\x0fSuspendResponse2\xe9\x01\n\x0bRaftService\x12\x38\n\x0bRequestVote\x12\x13.RequestVoteMessage\x1a\x14.RequestVoteResponse\x12>\n\rAppendEntries\x12\x15.AppendEntriesMessage\x1a\x16.AppendEntriesResponse\x12\x32\n\tGetLeader\x12\x11.GetLeaderMessage\x1a\x12.GetLeaderResponse\x12,\n\x07Suspend\x12\x0f.SuspendMessage\x1a\x10.SuspendResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTVOTEMESSAGE._serialized_start=14
  _REQUESTVOTEMESSAGE._serialized_end=60
  _REQUESTVOTERESPONSE._serialized_start=62
  _REQUESTVOTERESPONSE._serialized_end=111
  _APPENDENTRIESMESSAGE._serialized_start=113
  _APPENDENTRIESMESSAGE._serialized_end=161
  _APPENDENTRIESRESPONSE._serialized_start=163
  _APPENDENTRIESRESPONSE._serialized_end=213
  _GETLEADERMESSAGE._serialized_start=215
  _GETLEADERMESSAGE._serialized_end=250
  _GETLEADERRESPONSE._serialized_start=252
  _GETLEADERRESPONSE._serialized_end=300
  _SUSPENDMESSAGE._serialized_start=302
  _SUSPENDMESSAGE._serialized_end=335
  _SUSPENDRESPONSE._serialized_start=337
  _SUSPENDRESPONSE._serialized_end=354
  _RAFTSERVICE._serialized_start=357
  _RAFTSERVICE._serialized_end=590
# @@protoc_insertion_point(module_scope)
