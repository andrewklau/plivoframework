# -*- coding: utf-8 -*-
import traceback
from telephonie.core.inboundsocket import InboundEventSocket
from telephonie.utils.logger import StdoutLogger

if __name__ == '__main__':
    log = StdoutLogger()

    log.info('#'*60)
    log.info("Connect with bad host")
    try:
        inbound_event_listener = InboundEventSocket('falsehost', 8021, 'ClueCon')
        inbound_event_listener.connect()
    except:
        [ log.info(line) for line in traceback.format_exc().splitlines() ]
    log.info('#'*60 + '\n')

    log.info('#'*60)
    log.info("Connect with bad port")
    try:
        inbound_event_listener = InboundEventSocket('127.0.0.1', 9999999, 'ClueCon')
        inbound_event_listener.connect()
    except:
        [ log.info(line) for line in traceback.format_exc().splitlines() ]
    log.info('#'*60 + '\n')

    log.info('#'*60)
    log.info("Connect with bad password")
    try:
        inbound_event_listener = InboundEventSocket('127.0.0.1', 8021, 'falsepassword')
        inbound_event_listener.connect()
    except:
        [ log.info(line) for line in traceback.format_exc().splitlines() ]
    log.info('#'*60 + '\n')

    log.info('exit')
        

