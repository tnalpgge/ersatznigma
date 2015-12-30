#!/usr/bin/env python

import logging
import random
import subprocess
import sys
import time

# Patterned after http://priyom.org/number-stations/english/e07

logging.basicConfig(level=logging.ERROR)

class E07NonTraffic:
    def generate(self):
        return ( [ [ 5, 5, 3 ] ] * 3 + [ [ 0, 0, 0 ] ] ) * int(120 / 16)

class E07SingleMessage:

    def __init__(self, slope, intercept):
        self.unknown = int(random.random() * 1000)
        self.groupcount = int(random.random() * slope) + intercept

    def generate(self):
        return self.intro() + self.preamble() + self.message() + self.outro()

    def intro(self):
        return ( [ int2group(845) ] * 3 + [ [ '1' ] ] ) * int(120 / 14)

    def preamble(self):
        return [ int2group(self.unknown), int2group(self.groupcount) ] * 2

    def message(self):
        m = list()
        for i in range(self.groupcount):
            m.append(int2group(int(random.random() * 100000)))
        return m

    def outro(self):
            return [ [ '0' ] * 3 ] * 2


class Instruction:
    def render(self):
        pass

class Delay(Instruction):
    def __init__(self, duration):
        self.duration = duration

    def render(self):
        time.sleep(self.duration)
        return '\n'

class Syllables(Instruction):
    def __init__(self, thing):
        self.thing = thing

    def render(self):
        return ', '.join(self.thing) + '\n'

class InstructionFactory:
    def manufacture(self, things):
        output = []
        for thing in things:
            if isinstance(thing, list):
                output.append(Delay(1))
                output.append(Syllables(thing))
        return output[1:]


class Renderer:
    def __init__(self):
        self.voice = 'Daniel'

    def render(self, instruction):
        lips = subprocess.Popen(['say', '--voice', self.voice], stdin=subprocess.PIPE)
        syllables = instruction.render()
        language = bytes(syllables, 'utf-8')
        lips.communicate(language)

class ErsatzNigma:
    def __init__(self):
        self.format = E07SingleMessage(10, 10)
        self.fullmessage = None
        self.instructions = None

    def generate(self):
        self.fullmessage = self.format.generate()

    def speak(self):
        instructions = InstructionFactory().manufacture(self.fullmessage)
        renderer = Renderer()
        for i in instructions:
            logging.debug(i)
            renderer.render(i)
        renderer.shutdown()
 
def int2group(n):
    return [x for x in '{}'.format(n)]

def main():
    e = ErsatzNigma()
    e.generate()
    e.speak()

if __name__ == '__main__':
    sys.exit(main())
