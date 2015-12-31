#!/usr/bin/env python3

import argparse
import logging
import subprocess
import sys
import time

import ersatznigma.formats

#logging.basicConfig(level=logging.DEBUG)

class Instruction:
    def render(self):
        return '\n'

class Delay(Instruction):
    def __init__(self, duration):
        self.duration = duration

    def render(self):
        time.sleep(self.duration)
        return super().render()

class Syllables(Instruction):
    def __init__(self, thing):
        self.thing = thing

    def render(self):
        logging.debug(self.thing)
        n = ', '.join(self.thing)
        x = super().render()
        logging.debug(n)
        logging.debug(x)
        return n + x

class InstructionFactory:
    def manufacture(self, things):
        output = []
        for thing in things:
            if isinstance(thing, list):
                output.append(Delay(1))
                output.append(Syllables(thing))
        return output[1:]

class Renderer:
    def __init__(self, voice, show):
        self.voice = voice
        self.show = show

    def render(self, instruction):
        cmd = ['say']
        if self.show:
            cmd.append('--interactive')
        if self.voice is not None:
            cmd.append('--voice')
            cmd.append(self.voice)
        lips = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        syllables = instruction.render()
        logging.debug(syllables)
        language = bytes(syllables, 'utf-8')
        lips.communicate(language)

class ErsatzNigma:
    def __init__(self, args):
        self.voice = args.voice
        self.show = args.show
        self.msgformat = ersatznigma.formats.E07aNonTraffic()
        self.fullmessage = None
        self.instructions = None

    def generate(self):
        self.fullmessage = self.msgformat.generate()

    def speak(self):
        instructions = InstructionFactory().manufacture(self.fullmessage)
        renderer = Renderer(self.voice, self.show)
        for i in instructions:
            logging.debug(i)
            renderer.render(i)
 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--show', action='store_true', help='Show number groups as they are being spoken')
    parser.add_argument('-v', '--voice', help='Alternate voice for speaking the numbers')
    args = parser.parse_args()
    e = ErsatzNigma(args)
    e.generate()
    e.speak()

if __name__ == '__main__':
    sys.exit(main())
