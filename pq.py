import heapq

class Process:
    allProcess = [] #List of all process objects
    ATQueue = {} #Map of AT->Process in the format {time:[p1,p2,p3,...]}

    def __init__(self, pos=0,bt=0,at=0,priority=1):
        self.pos = pos #Process Identifier
        self.bt = bt #Burst Time
        self.at = at #Arrival Time
        self.priority = priority #Priority
        self.TaT = None
        self.wt = None
        Process.allProcess.append(self) #Adding each process to the list

        #Adding process to the right AT Map
        if at in Process.ATQueue:
            Process.ATQueue[at].append(self)
        else:
            Process.ATQueue[at]=[self]

    #Returns a string call of the process as P1,P2,etc
    def __str__(self):
        return f"P{self.pos}"
    
    # Comparison methods for process class on the basis of Priority
    def __lt__(self, other):
        return self.priority < other.priority
    def __eq__(self, other):
        return self.priority == other.priority
    def __gt__(self, other):
        return self.priority > other.priority
    
    # Hash method to make the class hashable 
    # This is because the class is used as keys in dictionaries and sets
    def __hash__(self):
        return hash(self.pos)

#N processes asper user input
def ProcessListMaker(N):
    for i in range(N): 

        at = int(input(f"Arrival Time for P{i+1} "))
        bt = int(input(f"Burst Time for P{i+1} "))
        p = int(input(f"Priority for P{i+1} "))

        process = Process(i+1,bt,at,p) #1 indexed process

#Priority Queue CPU Simulation
def PQ_cpu():
    gantt="\nGantt:  (0)|" #Gantt Chart string form with initial 0 time

    aTAT=0 # avg Turn-Around-Time
    aWT=0 # avg Waiting Time

    time=0 #CPU Clock
    restTime=0 #A timer to count how long the CPU has remained idle, for Gantt generation

    terminated=set() #All terminated processes

    # Ready Queue as a Heap
    readyQ = []
    heapq.heapify(readyQ)


    while len(terminated)<len(Process.allProcess):
        workDone=False #Resets work done switch

        for i in Process.allProcess:
            #   For every process in the processes list
            #   If the process has arrived and is not yet terminated
            #   It will be added to the ready queue heap (sorted from min priority)
            if i.at<=time and i not in terminated and i not in readyQ:
                heapq.heappush(readyQ,i)
        
        #   If ready queue has elements, the job with lowest priority will be executed
        #   Only one job will be executed
        #   Then the processes which should have arrived by the end of its BT will be added to ready queue
        if readyQ:
            curr = heapq.heappop(readyQ) #Executes the shortest job

            workDone=True 

            #Adds the proper Gantt string asper rest time
            if restTime>0:
                gantt+=f"  ({time})|"
                restTime=0

            terminated.add(curr) #Adds current process to terminated set
            time+=curr.bt

            #Calculate TAT and WT for each process
            curr.TaT=time-curr.at
            aTAT+=curr.TaT
            curr.wt= curr.TaT-curr.bt
            aWT+=curr.wt

            gantt+=f" {curr} ({time})|"

        #If no work was done, then forwards clock by 1s and also increases the idle counter
        if not workDone:
            time+=1
            restTime+=1

    #Averaging the TAT & WT
    aTAT = aTAT / len(terminated)
    aWT = aWT / len(terminated)


    print(gantt)
    print("ATAT: "+str(aTAT),"\n", "AWT: "+str(aWT))


if __name__ == "__main__":
    
    ProcessListMaker(6)
    PQ_cpu()
