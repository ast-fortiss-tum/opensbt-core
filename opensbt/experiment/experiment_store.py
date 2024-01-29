from opensbt.experiment.experiment import *
import logging as log

class Singleton(object):
        def __new__(cls, *args, **kwds):
            it = cls.__dict__.get("__it__")
            if it is not None:
                return it
            cls.__it__ = it = object.__new__(cls)
            it.init(*args, **kwds)
            return it

        def init(self, *args, **kwds):
            pass

class DefaultExperiments(Singleton):
    def init(self):
        self.store = {}

    def register(self, exp: Experiment):
        if not exp.name in self.store:
            self.store[exp.name] = exp
            return 0
        else:
            log.info("Experiment with the given name is already registered.")
            return 1

    def load(self, experiment_name: str) -> Experiment:
        if experiment_name in self.store:
            return self.store[experiment_name]
        else:
            log.info("Experiment with the given name does not exist.")
            return 1

    def get_store(self):
        return self.store

experiments_store = DefaultExperiments()