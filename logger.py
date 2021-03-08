import os, errno
import sys
import json

class Logger(object):
    '''
    Base Logger object

    Initializes the log directory and creates log files given by name in arguments.
    Can be used to append future log values to each file.
    '''

    def __init__(self, log_dir, *args):
        self.log_dir = log_dir

        try:
            os.makedirs(log_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with open(os.path.join(self.log_dir, 'cmd.txt'), 'w') as f:
            f.write(" ".join(sys.argv))

        for arg in args:
            setattr(self, 'log_{}'.format(arg), lambda epoch,value,name=arg: self.log(name, epoch, value))
            self.init_logfile(arg)

    def log_config(self, config):
        with open(os.path.join(self.log_dir, 'config.json'), 'w') as f:
            json.dump(config, f)

    def init_logfile(self, name):
        fname = self.get_log_fname(name)

        with open(fname,  'w') as log_file:
            log_file.write("epoch,{}\n".format(name))

    def get_log_fname(self, name):
        return os.path.join(self.log_dir, '{}.log'.format(name))

    def log(self, name, epoch, value):
        fname = self.get_log_fname(name)

        with open(fname, 'a') as log_file:
            log_file.write("{},{}\n".format(epoch, value))

    def log_test_value(self, name, value):
        test_name = 'test_' + name
        self.init_logfile(test_name)
        self.log(test_name, 0, value)


