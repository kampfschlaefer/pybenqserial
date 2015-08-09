#
# Copyright 2015 Arnold Krille
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import serial
import re
import logging
import argparse

logger = logging.getLogger(__name__)


class BenqSerial(object):
    def __init__(self, device):
        self._ser = serial.serial_for_url(device, baudrate=115200, timeout=0.5)

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

    @property
    def audio_volume(self):
        return self._get_answer('vol')

    @property
    def audio_micvolume(self):
        return self._get_answer('micvol')

    @property
    def lamp_hours(self):
        return self._get_answer('ltim')


def run(argv):

    parser = argparse.ArgumentParser(description="control BenQ beamers via serial interface")
    parser.add_argument('--device', '-d', type=str, default='/dev/ttyUSB0', help='serial device to open')

    args = parser.parse_args(argv[1:])

    logging.basicConfig(level=logging.DEBUG)

    beamer = BenqSerial(args.device)

    print('beamer is on? %s' % beamer.power)
    print('audio is muted? %s' % beamer.audio_mute)
    print('audio volume? speaker: %s microphone: %s' % (
        beamer.audio_volume, beamer.audio_micvolume
    ))
    print('selected source? %s' % beamer.source)
    print('lamp hours? %s' % beamer.lamp_hours)


if __name__ == '__main__':
    import sys
    run(sys.argv)
