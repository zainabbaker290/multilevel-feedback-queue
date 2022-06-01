#Author - Zainab Baker 
#Student number - 119340513

from operator import index
from sqlite3 import IntegrityError

class Queue():
    def __init__(self, quantum, priority):
        self._processes = [] #list of processes 
        self._quantum = quantum
        self._priority = priority 
    

class Process:
    def __init__(self,priority,quantum,state,id,io):
        self._priority = priority 
        self._quantum = quantum
        self._state = state 
        self._id = id 
        self._io = io
    
    def set_quantum(self,quantum):
        self._quantum = quantum

    def get_quantum(self):
        return self._quantum
    
    def set_state(self,state):
        self._state = state

    def get_state(self):
        return self._state
    
    def set_priority(self,priority):
        self._priority = priority

    def get_priority(self):
        return self._priority
    
    def set_io(self,io):
        self._io= io

    def get_io(self):
        return self._io
    
    quantum = property(set_quantum, get_quantum)
    state = property(set_state, get_state)
    priority = property(set_priority, get_priority) 
    io = property(set_io,get_io)   

class IO:
    def __init__(self, quantum, priority,state):
        self._quantum = quantum
        self._priority = priority
        self._state = state  
    
    def set_quantum(self,quantum):
        self._quantum = quantum

    def get_quantum(self):
        return self._quantum
    
    def set_state(self,state):
        self._state = state

    def get_state(self):
        return self._state
    
    def set_priority(self,priority):
        self._priority = priority

    def get_priority(self):
        return self._priority
    
    quantum = property(set_quantum, get_quantum)
    state = property(set_state, get_state)
    priority = property(set_priority, get_priority) 
        
class Schedular:
    def __init__(self,queue_list):
        self._queue_list = queue_list
        self._idle_state = False #keep track of idle 

    def scheduling(self): 
        #counter to keep track if queues are empty 
        empty_queue = 0 
        #running first queue, assumming queues put in order of priority 
        for queue in self._queue_list:
            queue_index = self._queue_list.index(queue) #getting index of queue 
            queue_orginal_time = queue._quantum #using to reset queues quantum 
            queue_time = queue._quantum
            #if the queue is empty 
            if len(queue._processes) == 0:
                print("queue ", empty_queue," is empty")
                empty_queue += 1
                #if all queues empty 
                if empty_queue == 8:
                    #change idle to true
                    self._idle_state = True
                    print("now in idle state")
                    empty_queue = 0 #reset counter variable
                    self._idle_state = False  #reset idle 
            #running the process, assuming process in order of priority 
            for p in queue._processes:
                #if process has i/o
                if p._io != None:
                    p._state = "blocked" #process blocked 
                    print("process has been blocked because of I/O")
                    print("now running IO")
                    p._io = None
                    p._state = "ready" #process now ready
                    #process put into higher priority queue 
                    before_queue = self._queue_list[queue_index - 1] 
                    if before_queue == None:
                        before_queue = self._queue_list[0]
                    print("process back in ready state and now higher in priority")
                #run the process 
                time_left = queue_time - p._quantum  
                #if the process is completed in time given 
                if time_left >= 0:
                    p._state = "terminated" #change state to terminated 
                    print("the process is now", p._state)
                    queue._processes.pop(0) #remove from queue 
                #if process not done in time finished 
                elif time_left < 0: 
                    p._quantum += 5 #increase quantum of process 
                    print("the processes quantum has been increased")
                    try:
                        next_queue = self._queue_list[queue_index + 1]
                        next_queue._processes.append(p) #added onto next queue 
                        print("the process has been moved to queue",next_queue._priority)
                        queue._processes.pop(0)
                        # if processes left over in previous queue, moving them to next queue 
                        if len(queue._processes) != 0:
                            for p in queue._processes:
                                next_queue._processes.append(p)
                                queue._processes.pop(0)
                    #if out of bounds in list  
                    except IndexError:
                        print("the process is in the last queue") #leave in last queue
            queue._quantum = queue_orginal_time #resetting queue time 
              

io_1 = IO(20,2, "ready")
    
    
process_a = Process(0,10,"ready", 1,None)
process_b= Process(1,20,"ready", 2, None)
process_c = Process(2,30,"ready", 3, io_1)
process_d = Process(3,5,"ready", 4, None )
process_e = Process(4,8,"ready", 4, None )
process_f = Process(5,12,"ready", 4, None )

queue_0 = Queue(10,0)
queue_1 = Queue(20,1)
queue_2 = Queue(40,2)
queue_3 = Queue(80,3)
queue_4 = Queue(160,4)
queue_5 = Queue(320,5)
queue_6 = Queue(640,6)
queue_7 = Queue(1280,7)


queue_0._processes.append(process_a)
queue_0._processes.append(process_b)
queue_0._processes.append(process_c)
queue_0._processes.append(process_d)
queue_0._processes.append(process_e)
queue_0._processes.append(process_f)

queue_list = [queue_0,queue_1, queue_2, queue_3, queue_4, queue_5, queue_6, queue_7]

print("INITIAL")
multilevel_feedback_queue = Schedular(queue_list)
multilevel_feedback_queue.scheduling()
print("round 2")
multilevel_feedback_queue.scheduling()
print("round 3")
multilevel_feedback_queue.scheduling()
print("getting to idle state")
multilevel_feedback_queue.scheduling()