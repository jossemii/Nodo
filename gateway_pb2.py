# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gateway.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ipss_pb2 as ipss__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gateway.proto',
  package='gateway',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rgateway.proto\x12\x07gateway\x1a\nipss.proto\"\x07\n\x05\x45mpty\"\x1d\n\x0cTokenMessage\x12\r\n\x05token\x18\x01 \x01(\t\"\x1b\n\x0b\x43ostMessage\x12\x0c\n\x04\x63ost\x18\x01 \x01(\x05\";\n\x08Instance\x12 \n\x08instance\x18\x01 \x01(\x0b\x32\x0e.ipss.Instance\x12\r\n\x05token\x18\x02 \x01(\t\"\x82\x01\n\x10ServiceTransport\x12\x0e\n\x04hash\x18\x01 \x01(\tH\x00\x12 \n\x07service\x18\x02 \x01(\x0b\x32\r.ipss.ServiceH\x00\x12(\n\x06\x63onfig\x18\x03 \x01(\x0b\x32\x13.ipss.ConfigurationH\x01\x88\x01\x01\x42\x07\n\x05oneOfB\t\n\x07_config\"\x17\n\x05\x43hunk\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\x32\xf7\x02\n\x07Gateway\x12@\n\x0cStartService\x12\x19.gateway.ServiceTransport\x1a\x11.gateway.Instance\"\x00(\x01\x12\x36\n\x0bStopService\x12\x15.gateway.TokenMessage\x1a\x0e.gateway.Empty\"\x00\x12*\n\x06Hynode\x12\x0e.ipss.Instance\x1a\x0e.ipss.Instance\"\x00\x12@\n\rGetServiceTar\x12\x19.gateway.ServiceTransport\x1a\x0e.gateway.Chunk\"\x00(\x01\x30\x01\x12=\n\rGetServiceDef\x12\x19.gateway.ServiceTransport\x1a\r.ipss.Service\"\x00(\x01\x12\x45\n\x0eGetServiceCost\x12\x19.gateway.ServiceTransport\x1a\x14.gateway.CostMessage\"\x00(\x01\x62\x06proto3'
  ,
  dependencies=[ipss__pb2.DESCRIPTOR,])




_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='gateway.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=45,
)


_TOKENMESSAGE = _descriptor.Descriptor(
  name='TokenMessage',
  full_name='gateway.TokenMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='gateway.TokenMessage.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=47,
  serialized_end=76,
)


_COSTMESSAGE = _descriptor.Descriptor(
  name='CostMessage',
  full_name='gateway.CostMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cost', full_name='gateway.CostMessage.cost', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=78,
  serialized_end=105,
)


_INSTANCE = _descriptor.Descriptor(
  name='Instance',
  full_name='gateway.Instance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='gateway.Instance.instance', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='token', full_name='gateway.Instance.token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=166,
)


_SERVICETRANSPORT = _descriptor.Descriptor(
  name='ServiceTransport',
  full_name='gateway.ServiceTransport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hash', full_name='gateway.ServiceTransport.hash', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service', full_name='gateway.ServiceTransport.service', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='config', full_name='gateway.ServiceTransport.config', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='oneOf', full_name='gateway.ServiceTransport.oneOf',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_config', full_name='gateway.ServiceTransport._config',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=169,
  serialized_end=299,
)


_CHUNK = _descriptor.Descriptor(
  name='Chunk',
  full_name='gateway.Chunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='buffer', full_name='gateway.Chunk.buffer', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=324,
)

_INSTANCE.fields_by_name['instance'].message_type = ipss__pb2._INSTANCE
_SERVICETRANSPORT.fields_by_name['service'].message_type = ipss__pb2._SERVICE
_SERVICETRANSPORT.fields_by_name['config'].message_type = ipss__pb2._CONFIGURATION
_SERVICETRANSPORT.oneofs_by_name['oneOf'].fields.append(
  _SERVICETRANSPORT.fields_by_name['hash'])
_SERVICETRANSPORT.fields_by_name['hash'].containing_oneof = _SERVICETRANSPORT.oneofs_by_name['oneOf']
_SERVICETRANSPORT.oneofs_by_name['oneOf'].fields.append(
  _SERVICETRANSPORT.fields_by_name['service'])
_SERVICETRANSPORT.fields_by_name['service'].containing_oneof = _SERVICETRANSPORT.oneofs_by_name['oneOf']
_SERVICETRANSPORT.oneofs_by_name['_config'].fields.append(
  _SERVICETRANSPORT.fields_by_name['config'])
_SERVICETRANSPORT.fields_by_name['config'].containing_oneof = _SERVICETRANSPORT.oneofs_by_name['_config']
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['TokenMessage'] = _TOKENMESSAGE
DESCRIPTOR.message_types_by_name['CostMessage'] = _COSTMESSAGE
DESCRIPTOR.message_types_by_name['Instance'] = _INSTANCE
DESCRIPTOR.message_types_by_name['ServiceTransport'] = _SERVICETRANSPORT
DESCRIPTOR.message_types_by_name['Chunk'] = _CHUNK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway.Empty)
  })
_sym_db.RegisterMessage(Empty)

TokenMessage = _reflection.GeneratedProtocolMessageType('TokenMessage', (_message.Message,), {
  'DESCRIPTOR' : _TOKENMESSAGE,
  '__module__' : 'gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway.TokenMessage)
  })
_sym_db.RegisterMessage(TokenMessage)

CostMessage = _reflection.GeneratedProtocolMessageType('CostMessage', (_message.Message,), {
  'DESCRIPTOR' : _COSTMESSAGE,
  '__module__' : 'gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway.CostMessage)
  })
_sym_db.RegisterMessage(CostMessage)

Instance = _reflection.GeneratedProtocolMessageType('Instance', (_message.Message,), {
  'DESCRIPTOR' : _INSTANCE,
  '__module__' : 'gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway.Instance)
  })
_sym_db.RegisterMessage(Instance)

ServiceTransport = _reflection.GeneratedProtocolMessageType('ServiceTransport', (_message.Message,), {
  'DESCRIPTOR' : _SERVICETRANSPORT,
  '__module__' : 'gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway.ServiceTransport)
  })
_sym_db.RegisterMessage(ServiceTransport)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), {
  'DESCRIPTOR' : _CHUNK,
  '__module__' : 'gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway.Chunk)
  })
_sym_db.RegisterMessage(Chunk)



_GATEWAY = _descriptor.ServiceDescriptor(
  name='Gateway',
  full_name='gateway.Gateway',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=327,
  serialized_end=702,
  methods=[
  _descriptor.MethodDescriptor(
    name='StartService',
    full_name='gateway.Gateway.StartService',
    index=0,
    containing_service=None,
    input_type=_SERVICETRANSPORT,
    output_type=_INSTANCE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='StopService',
    full_name='gateway.Gateway.StopService',
    index=1,
    containing_service=None,
    input_type=_TOKENMESSAGE,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Hynode',
    full_name='gateway.Gateway.Hynode',
    index=2,
    containing_service=None,
    input_type=ipss__pb2._INSTANCE,
    output_type=ipss__pb2._INSTANCE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetServiceTar',
    full_name='gateway.Gateway.GetServiceTar',
    index=3,
    containing_service=None,
    input_type=_SERVICETRANSPORT,
    output_type=_CHUNK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetServiceDef',
    full_name='gateway.Gateway.GetServiceDef',
    index=4,
    containing_service=None,
    input_type=_SERVICETRANSPORT,
    output_type=ipss__pb2._SERVICE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetServiceCost',
    full_name='gateway.Gateway.GetServiceCost',
    index=5,
    containing_service=None,
    input_type=_SERVICETRANSPORT,
    output_type=_COSTMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GATEWAY)

DESCRIPTOR.services_by_name['Gateway'] = _GATEWAY

# @@protoc_insertion_point(module_scope)
