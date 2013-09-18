import sys, os
import inspect

import abc

def initCommands():
    cwd=os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)
    for m in Command.knownCommands.keys():
        Command.knownCommands[m]=__import__("Command_%s" % m)

class Command():
    __metaclass__ = abc.ABCMeta

    knownCommands = {"START": None}

    answer = ""
    OK="OK"
    KO="KO"

    """command"""
    def __init__(self, name):
        self.name = name
        initCommands()
        assert(len(Command.knownCommands) > 0)
    
    @staticmethod
    def unserialize(serialized):
        initCommands()

        ident, command, answer = serialized.split(',')
        assert(ident == "CMD")

        className = "Command_%s" % command
        print Command.knownCommands
        assert(command in Command.knownCommands.keys())

        print dir(Command.knownCommands[command])
        if command in Command.knownCommands:
            m = Command.knownCommands[command]
            c = getattr(m, className)
            cmd = c(command)
            cmd.answer = answer
            return cmd

    def serialize(self):
        return "CMD,%s,%s" % (self.name, self.answer)

    """ server side """
    @abc.abstractmethod
    def onInit(self):
        pass

    @abc.abstractmethod
    def onAnswer(self, answer):
        pass

    """ client side """
    @abc.abstractmethod
    def Execute(self):
        return self.answer

    def __str__(self):
        return self.name

