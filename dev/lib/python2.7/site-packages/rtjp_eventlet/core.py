import logging
try:
    import json
except ImportError:
    import simplejson as json
logger = logging.getLogger('rtjp.core')

class RTJPParseException(Exception):
    def __init__(self, msg="", id=None):
        Exception.__init__(self, msg)
        self.id = id

def deserialize_frame(line):
    id = None
    try:
        frame = json.loads(line)
    except:
        logger.debug("Error parsing frame: %s", repr(line), exc_info=True)
        raise RTJPParseException("Invalid json", id)        
    if not isinstance(frame, list):
        logger.debug("Invalid frame (not a list): " + repr(frame))
        raise RTJPParseException("Invalid frame (not a list)", id)
    if len(frame) > 0 and isinstance(frame[0], int):
        id = frame[0]
    if not len(frame) == 3:
        logger.debug("Invalid frame length for: " + repr(frame))
        raise RTJPParseException("Invalid frame length", id)
    if (isinstance(frame[1], unicode)):
        frame[1] = str(frame[1])
    if not isinstance(frame[0], int):
        logger.debug("Invalid frame id: " + repr(frame[0]))
        raise RTJPParseException("Invalid frame id (must be int)", id)
    
    if not isinstance(frame[1], str) or len(frame[1]) == 0:
        logger.debug("Invalid frame name: " + repr(frame[1]))
        raise RTJPParseException("Invalid frame name (must be string)", id)
    if not isinstance(frame[2], dict):
        logger.debug("Invalid frame kwargs: " + repr(frame[2]))
        raise RTJPParseException("Invalid frame keyword arguments (must be dictionary)", id)
    return frame

DELIMITER = '\r\n'    
def serialize_frame(frame_id, name, args):
    buffer = json.dumps([frame_id, name, args]) + DELIMITER
    return buffer
