
import serial
import re
import logging

logger = logging.getLogger(__name__)


class BenqSerial(object):
    def __init__(self, device):
        self._ser = serial.serial_for_url(device, baudrate=115200, timeout=0.5)
        # self.power = False

    def __del__(self):
        self._ser.close()

    def _get_answer(self, command):
        # logger.debug('command is \'%s\'', command)
        self._ser.write('\r*%s=?#\r' % command)
        answer = self._ser.read(32)
        # logger.debug(
        #     'answer returned is \'%s\'',
        #     answer.encode('string_escape'),
        # )
        answer = re.findall(
            '^\>\*%s=\?\#\r\r\n\*(.*)\#\r\n' % command,
            answer
        )
        # logger.debug('real answer is \'%s\'', answer)
        if len(answer):
            return answer[0]
        else:
            logger.warn('Command %s returned nothing', command)
            return ''

    def _get_bool(self, command):
        return self._get_answer(command).count('ON') > 0

    @property
    def power(self):
        return self._get_bool('pow')

    @property
    def source(self):
        return self._get_answer('sour')

    @property
    def audio_mute(self):
        return self._get_bool('mute')

    def get_status(self):
        self.source = self._get_generic('sour')
        self.audo_volume = self._get_generic('vol')
        self.audio_micvolume = self._get_generic('micvol')

    def __repr__(self):
        return "%s" % self.__dict__


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    beamer = BenqSerial('/dev/ttyUSB0')

    print 'beamer is on? %s' % beamer.power
    print 'audio is muted? %s' % beamer.audio_mute
    print 'selected source? %s' % beamer.source

    # print beamer