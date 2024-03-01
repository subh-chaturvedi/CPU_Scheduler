
class Process:
    allProcess = [] #List of all process objects
    ATQueue = {} #Map of AT->Process in the format {time:[p1,p2,p3,...]}

    def __init__(self, pos=0,bt=0,at=0):
        self.pos = pos #Process Identifier
        self.bt = bt #Burst Time
        self.at = at #Arrival Time

        Process.allProcess.append(self) #Adding each process to the list

        #Adding process to the right AT Map
        if at in Process.ATQueue:
            Process.ATQueue[at].append(self)
        else:
            Process.ATQueue[at]=[self]

    #Returns a string call of the process as P1,P2,etc
    def __str__(self):
        return f"P{self.pos}"

#N processes asper user input
def ProcessListMaker(N):
    for i in range(N): 

        bt = int(input(f"Burst Time for P{i} "))
        at = int(input(f"Arrival Time for P{i} "))

        process = Process(i,bt,at)

#Firstcome FirstServe CPU Simulation
def FCFS_cpu():
    gantt="\nGantt:  (0)|" #Gantt Chart string form with initial 0 time

    time=0 #CPU Clock
    restTime=0 #A timer to count how long the CPU has remained idle, for Gantt generation

    terminated=set() #All terminated processes

    while len(terminated)<len(Process.allProcess):
        workDone=False #Resets work done switch

        for i in Process.allProcess:
            #   For every process in the processes list
            #   If the process has arrived and is not yet terminated
            #   It will be executed in order of acceptance into the CPU

            if i.at<=time and i not in terminated:
                workDone=True 

                #Adds the proper Gantt string asper rest time
                if restTime>0:
                    gantt+=f"  ({time})|"
                    restTime=0

                terminated.add(i)
                time+=i.bt
                gantt+=f" {i} ({time})|"

        #If no work was done, then forwards clock by 1s and also increases the idle counter
        if not workDone:
            time+=1
            restTime+=1
    
    return gantt+"\n"


if __name__ == "__main__":
    
    ProcessListMaker(4)
    print(FCFS_cpu())
