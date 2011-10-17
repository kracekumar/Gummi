from __future__ import absolute_import
import sys
import eventlet
#from eventlet import api, coros, event
import logging
from . import core
from . import errors
#from .. import core
#logging.basicConfig()


class RTJPServer(object):
    logger = logging.getLogger("rtjp_eventlet.RTJPServer")
    def __init__(self, sock=None):
        self._accept_queue = eventlet.queue.Queue()
        self._sock = sock
        if self._sock:
            eventlet.spawn(self._run)
        
    def listen(self, port=None, interface="", sock=None):
        if not (sock or port):
            raise Exception("listen requires either a listening sock or port")
        if sock:
            self._sock = sock
        else:
            self._sock = eventlet.listen((interface, port))
        ev = eventlet.event.Event()
        ev.send(None)
        eventlet.spawn(self._run)
        return ev
        
    def _run(self):
        while True:
            sock, addr = self._sock.accept()
            self.logger.debug('accepted connection sock: %s, addr: %s', sock, addr)
            self._accept_queue.put(RTJPConnection(sock=sock, addr=addr))
            
    def accept(self):
        ev = eventlet.event.Event()
        if self._accept_queue.qsize():
            ev.send(self._accept_queue.get())
        else:
            eventlet.spawn(self._accept, ev)
        return ev
        
    def _accept(self, ev):
        conn = self._accept_queue.get()
        if isinstance(conn, Exception):
            ev.send_exception(e)
        else:
            ev.send(conn)

class RTJPConnection(object):
    logger = logging.getLogger('rtjp_eventlet.RTJPConnection')
    def __init__(self, delimiter='\r\n', sock=None, addr=None):
        self.frame_id = 0
        self._frame_queue = eventlet.queue.Queue()
        self.delimiter = delimiter
        self._sock = None
        self._addr = addr
        self._loop = None
        self._send_lock = eventlet.semaphore.Semaphore()
        if sock:
            self._make_connection(sock)
        
    def connect(self, host, port):
        self._connected = False
        e = eventlet.event.Event()
        eventlet.spawn(self._connect, host, port, e)
        return e
        
    def close(self):
        if self._connected:
            self._loop.kill()
            self._sock.close()
            self._sock = None
            self._connected = False
        
    def _connect(self, host, port, ev):
        try:
            sock = eventlet.connect((host, port))
            self._addr = (host, port)
            self._make_connection(sock)
        except Exception, e:
            ev.send_exception(e)
        else:
            ev.send(None)
        
    def _make_connection(self, sock):
        self._sock = sock
        self._connected = True
        self._loop = eventlet.spawn(self._read_forever)
        
    def _read_forever(self):
        buffer = ""
        try:
            while True:
                try:
                    data = self._sock.recv(1024)
                    self.logger.debug('RECV %s: %s', self, repr(data))
                except Exception, e:
                    self.logger.exception('%s Error while reading from self._sock')
                    break
                if not data:
                    self.logger.debug('no data, breaking...')
                    break;
                buffer += data
                while self.delimiter in buffer:
                    raw_frame, buffer = buffer.split(self.delimiter, 1)
                    try:
                        frame = core.deserialize_frame(raw_frame)
                    except core.RTJPParseException, e:
                        self.send_error(e.id, str(e))
                        continue
                    self.logger.debug('RECV: %s, %s, %s' % tuple(frame))
                    self._frame_queue.put(frame)
            self.logger.debug('put Connection Lost in the queue')
            self._connected = False
            self._sock = None
            self._frame_queue.put(errors.ConnectionLost("Connection Lost"))
        except:
            logger.exception('%s Unknown exception while reading from sock', self)
            self._loop = None
            pass

    def recv_frame(self):
        ev = eventlet.event.Event()
        if self._frame_queue.qsize():
            ev.send(self._frame_queue.get())
        else:
            eventlet.spawn(self._recv_frame, ev)
        return ev
        
    def _recv_frame(self, ev):
        frame = self._frame_queue.get()
        if isinstance(frame, Exception):
            ev.send_exception(frame)
        else:
            ev.send(frame)

    def send_frame(self, name, args={}):
        if not self._sock:
            raise Exception("Not Connected")
        self.frame_id += 1
        self.logger.debug('SEND: %s, %s, %s' % (self.frame_id, name, args))
        buffer = core.serialize_frame(self.frame_id, name, args)
        e = eventlet.event.Event()
        eventlet.spawn(self._send_frame, self.frame_id, buffer, e)
        return e
        
    def _send_frame(self, id, buffer, ev):
        if not self._connected:
            ev.send_exception(Exception("Not Connected"))
        try:
            self._send_lock.acquire()
            self._sock.sendall(buffer)
            self.logger.debug('SENT %s: %s', self, repr(buffer))
        except Exception, e:
            self.logger.exception('%s Error sending payload %s', self, repr(buffer))
            ev.send_exception(*sys.exc_info())
        else:
            ev.send(id)
        finally:
            self._send_lock.release()
            
            
    def send_error(self, reference_id, msg):
        self.send_frame('ERROR', { 'id': reference_id, 'msg': str(msg) })
