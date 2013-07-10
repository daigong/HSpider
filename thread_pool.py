# -*- coding: utf-8 -*-

import threading
import Queue

__DEBUG_FALG__ = False


class ThreadPool(threading.Thread):

    def __init__(self, thread_max_count, task_queue=Queue.Queue()):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName('Thread-Pool')
        self.task_queue = task_queue
        self.thread_max_count = thread_max_count
        self.thread_list = []
        for i in range(0, self.thread_max_count):
            thread_worker = ThreadWorker('Thread-Worker-%s' % str(i),
                    self.task_queue)
            self.thread_list.append(thread_worker)

    def run(self):
        for thread_worker in self.thread_list:
            thread_worker.start()
        self.__wait_threaders_done__()

    def wait_done(self):
        self.join()

    def __wait_threaders_done__(self):
        for thread_worker in self.thread_list:
            if thread_worker.isAlive():
                thread_worker.join()

    def add_task(self, task_job, *args):
        self.task_queue.put((task_job, list(args)))

    def current_task_count(self):
        return self.task_queue.qsize()


class ThreadWorker(threading.Thread):

    def __init__(self, name, task_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName(name)
        self.task_queue = task_queue

    def run(self):
        while True:
            (job, args) = self.task_queue.get()
            try:
                job(*args)
                if __DEBUG_FALG__:
                    print '%s done job ! ' % self.getName()
            except Exception, e:
                print '%s has Exception %s' % (self.getName(), e)
            finally:
                self.task_queue.task_done()


