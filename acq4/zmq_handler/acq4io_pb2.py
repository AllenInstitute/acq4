# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: acq4io.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import aibsmw_messages_pb2 as aibsmw__messages__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='acq4io.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x0c\x61\x63q4io.proto\x1a\x15\x61ibsmw_messages.proto\"A\n\rconfig_loaded\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\x12\x0f\n\x07version\x18\x02 \x02(\t\"D\n\rcapture_image\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\x12\x12\n\nimage_type\x18\x02 \x02(\t\"\xce\x01\n\x0eimage_captured\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\x12\x12\n\nimage_type\x18\x02 \x02(\t\x12\x12\n\nimage_path\x18\x03 \x02(\t\x12\x12\n\nx_stage_um\x18\x04 \x02(\x02\x12\x12\n\ny_stage_um\x18\x05 \x02(\x02\x12\x12\n\nz_stage_um\x18\x06 \x02(\x02\x12\x11\n\ttimestamp\x18\x07 \x02(\t\x12\x11\n\tx_size_um\x18\x08 \x02(\x02\x12\x11\n\ty_size_um\x18\t \x02(\x02\".\n\x0bget_z_depth\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\">\n\x07z_depth\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\x12\x12\n\nz_stage_um\x18\x02 \x02(\x02\"F\n\x12set_link_btn_state\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\x12\x0f\n\x07\x63hecked\x18\x02 \x02(\x08\"C\n\x0fset_surface_btn\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header\x12\x0f\n\x07\x65nabled\x18\x02 \x02(\x08\"4\n\x11\x63lear_tile_images\x12\x1f\n\x06header\x18\x01 \x02(\x0b\x32\x0f.message_header'
  ,
  dependencies=[aibsmw__messages__pb2.DESCRIPTOR,])




_CONFIG_LOADED = _descriptor.Descriptor(
  name='config_loaded',
  full_name='config_loaded',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='config_loaded.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='config_loaded.version', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=104,
)


_CAPTURE_IMAGE = _descriptor.Descriptor(
  name='capture_image',
  full_name='capture_image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='capture_image.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_type', full_name='capture_image.image_type', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=174,
)


_IMAGE_CAPTURED = _descriptor.Descriptor(
  name='image_captured',
  full_name='image_captured',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='image_captured.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_type', full_name='image_captured.image_type', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_path', full_name='image_captured.image_path', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x_stage_um', full_name='image_captured.x_stage_um', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y_stage_um', full_name='image_captured.y_stage_um', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z_stage_um', full_name='image_captured.z_stage_um', index=5,
      number=6, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='image_captured.timestamp', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='x_size_um', full_name='image_captured.x_size_um', index=7,
      number=8, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y_size_um', full_name='image_captured.y_size_um', index=8,
      number=9, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=383,
)


_GET_Z_DEPTH = _descriptor.Descriptor(
  name='get_z_depth',
  full_name='get_z_depth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='get_z_depth.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=385,
  serialized_end=431,
)


_Z_DEPTH = _descriptor.Descriptor(
  name='z_depth',
  full_name='z_depth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='z_depth.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z_stage_um', full_name='z_depth.z_stage_um', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=433,
  serialized_end=495,
)


_SET_LINK_BTN_STATE = _descriptor.Descriptor(
  name='set_link_btn_state',
  full_name='set_link_btn_state',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='set_link_btn_state.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='checked', full_name='set_link_btn_state.checked', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=497,
  serialized_end=567,
)


_SET_SURFACE_BTN = _descriptor.Descriptor(
  name='set_surface_btn',
  full_name='set_surface_btn',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='set_surface_btn.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='set_surface_btn.enabled', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=569,
  serialized_end=636,
)


_CLEAR_TILE_IMAGES = _descriptor.Descriptor(
  name='clear_tile_images',
  full_name='clear_tile_images',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='clear_tile_images.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=638,
  serialized_end=690,
)

_CONFIG_LOADED.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_CAPTURE_IMAGE.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_IMAGE_CAPTURED.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_GET_Z_DEPTH.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_Z_DEPTH.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_SET_LINK_BTN_STATE.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_SET_SURFACE_BTN.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
_CLEAR_TILE_IMAGES.fields_by_name['header'].message_type = aibsmw__messages__pb2._MESSAGE_HEADER
DESCRIPTOR.message_types_by_name['config_loaded'] = _CONFIG_LOADED
DESCRIPTOR.message_types_by_name['capture_image'] = _CAPTURE_IMAGE
DESCRIPTOR.message_types_by_name['image_captured'] = _IMAGE_CAPTURED
DESCRIPTOR.message_types_by_name['get_z_depth'] = _GET_Z_DEPTH
DESCRIPTOR.message_types_by_name['z_depth'] = _Z_DEPTH
DESCRIPTOR.message_types_by_name['set_link_btn_state'] = _SET_LINK_BTN_STATE
DESCRIPTOR.message_types_by_name['set_surface_btn'] = _SET_SURFACE_BTN
DESCRIPTOR.message_types_by_name['clear_tile_images'] = _CLEAR_TILE_IMAGES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

config_loaded = _reflection.GeneratedProtocolMessageType('config_loaded', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG_LOADED,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:config_loaded)
  })
_sym_db.RegisterMessage(config_loaded)

capture_image = _reflection.GeneratedProtocolMessageType('capture_image', (_message.Message,), {
  'DESCRIPTOR' : _CAPTURE_IMAGE,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:capture_image)
  })
_sym_db.RegisterMessage(capture_image)

image_captured = _reflection.GeneratedProtocolMessageType('image_captured', (_message.Message,), {
  'DESCRIPTOR' : _IMAGE_CAPTURED,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:image_captured)
  })
_sym_db.RegisterMessage(image_captured)

get_z_depth = _reflection.GeneratedProtocolMessageType('get_z_depth', (_message.Message,), {
  'DESCRIPTOR' : _GET_Z_DEPTH,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:get_z_depth)
  })
_sym_db.RegisterMessage(get_z_depth)

z_depth = _reflection.GeneratedProtocolMessageType('z_depth', (_message.Message,), {
  'DESCRIPTOR' : _Z_DEPTH,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:z_depth)
  })
_sym_db.RegisterMessage(z_depth)

set_link_btn_state = _reflection.GeneratedProtocolMessageType('set_link_btn_state', (_message.Message,), {
  'DESCRIPTOR' : _SET_LINK_BTN_STATE,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:set_link_btn_state)
  })
_sym_db.RegisterMessage(set_link_btn_state)

set_surface_btn = _reflection.GeneratedProtocolMessageType('set_surface_btn', (_message.Message,), {
  'DESCRIPTOR' : _SET_SURFACE_BTN,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:set_surface_btn)
  })
_sym_db.RegisterMessage(set_surface_btn)

clear_tile_images = _reflection.GeneratedProtocolMessageType('clear_tile_images', (_message.Message,), {
  'DESCRIPTOR' : _CLEAR_TILE_IMAGES,
  '__module__' : 'acq4io_pb2'
  # @@protoc_insertion_point(class_scope:clear_tile_images)
  })
_sym_db.RegisterMessage(clear_tile_images)


# @@protoc_insertion_point(module_scope)
