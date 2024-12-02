import numpy as np
import random
import math

class Stage(): # Queueing System
    
    class Server(): # Server
        def __init__ (self,index,id,mu,ctype_mus = None):
            self.id = id
            self.index=index
            self.mu = mu
            self.ctype_mus = ctype_mus
            self.customer = None
            self.nextservice=math.inf
        def NextService(self,customer,clock):
            self.customer = customer
            self.customer.currentnode = self.index
            self.customer.startservice = clock
            if self.ctype_mus == None:
                self.nextservice = clock + random.expovariate(self.mu)
            else:
                self.nextservice = clock + random.expovariate(self.ctype_mus[self.customer.attributes[self.index]])
            return(self.nextservice)
    
    def __init__(self, index, mu, servers, priority = "FCFS", N = math.inf,  ctype_mus=None):
        self.index=index
        self.N =N
        self.n = 0
        self.mu = mu
        self.s = servers
        self.queue = []
        self.systemsizes=[]
        self.pi_n = []
        self.nextservice = math.inf
        self.serverlist = []
        self.priority = priority
        for server in range(self.s):
            self.serverlist.append(self.Server(self.index,server, mu,ctype_mus))
            
        
    def AddtoQ(self,customer,clock):
        self.queue.append(customer)
        customer.clockin = clock
        self.n +=1 
    #def RemovefromQ():
    
    def RemovefromQ(self, serviceinfo):
        customer = self.serverlist[serviceinfo[1].id].customer
        customer.clockout = serviceinfo[2]
        customer.AddWaitTime()
        customer.currentnode = None
    
    def Serve(self, serviceinfo):
        customer = self.serverlist[serviceinfo[1].id].customer
        self.RemovefromQ(serviceinfo) # pops Customer out of que
        self.ResetServer(serviceinfo)
        self.n -=1

        return(customer) # pops out customer for next queue
    def ResetServer(self,serviceinfo):
        self.serverlist[serviceinfo[1].id].customer=None
        self.serverlist[serviceinfo[1].id].nextservice=math.inf
    def Sort(self):
        if self.priority == "Classes":
            self.queue = sorted(self.queue, key=lambda customer: customer.ctype)
        else:
            pass
            
class Exit(Stage):
    def __init__(self, index):
        _mu = 0
        servers = 0
        super(Exit,self).__init__(self,index,_mu,servers)
        
class CustomerClass():
    
    
                
    def __init__(self,ctypelist,ctyperate,ctypedictionary):
        self.subclasslist = []
        self.waittime = None
        for ctype in ctypelist:
            self.subclasslist.append(self.Subclass(ctype,ctyperate[ctype]))
            
    class Subclass():
        def __init__ (self, ctype,ctyperate):
            clock = 0
            self.subwaittime = None
            self.ctype = ctype
            self.ctyperate = ctyperate
            self.nextarrival = self.NextArrival(self.ctype,clock)
        def NextArrival(self,ctype,clock):
            self.nextarrival = clock + random.expovariate(self.ctyperate)
            return(self.nextarrival)
        
class Customer(CustomerClass):    
    def __init__(self,ctype):
        from numpy.random import choice
        self.ctype = ctype
        self.ctype2 = choice([0,1],p=[.8,.2])
        self.attributes = [self.ctype,self.ctype2]
        self.clockin = None
        self.startservice = None
        self.clockout = None
        self.currentNode = None
        self.waittimelist = []
        
    def AddWaitTime(self):
        self.waittimelist.append([self.clockin,self.startservice,self.clockout])
        self.clockin = None
        self.startservice = None
        self.clockout = None
  
  
  
##################                         ##################
##################  General Model Actions  ##################
##################                         ##################  
    
def GenerateArrival(Classes,ctype,clock):
    Classes.subclasslist[ctype].NextArrival(ctype,clock)
    return()
def FindNextArrival(Classes):
    nextarrival = [None,math.inf]
    for subclass in Classes.subclasslist:
        if subclass.nextarrival < nextarrival[1]:
            nextarrival = [subclass.ctype, subclass.nextarrival]
    return(nextarrival)
def Independentarrival(rate):
    return(random.expovariate(rate))   
def GenerateServiceTimes(Queuelist,clock):
     ### Sorts node with premtive priority
    for Node in Queuelist:
        Node.Sort()
        if len(Node.queue) > 0: #If customers enter the Q # This line is redundant for performance
            for server in Node.serverlist:
                if len(Node.queue) > 0: #If customers enter the Q
                    if server.customer == None:
                        customer = Node.queue[0]
                        server.NextService(customer,clock) #Starts Next Service
                        Node.queue.remove(customer) # Removes Customer from queue, the patient is now being served.
            pass
    return()
def FindNextServiceTimes(Queuelist):
    nextservice = [None,None,math.inf]
    for Node in Queuelist:
        for Server in Node.serverlist:
            if Server.nextservice < nextservice[2]:
                nextservice = [Node,Server,Server.nextservice]
    return(nextservice)



##################                      ##################
##################   Model Evaluation   ##################
##################                      ##################
def CalcSystemStates(Queuelist):
    for Node in Queuelist:
        s=0
        for server in Node.serverlist:
            if server.customer != None:
                s+=1
        Node.systemsizes.append(len(Node.queue)+s)
    return()
def CalcSystemStats(Queuelist):
    for Node in Queuelist:
            for i in range(max(Node.systemsizes)):
                Node.pi_n.append(Node.systemsizes.count(i)/len(Node.systemsizes))
    return()
def CalcWaitTime(Queuelength,customersdone,ctypelist = None):
    import numpy as np
    Waittimes =[]
    ClassTimes = []
    for i in range(Queuelength):
        times = []
        qtimes = []
        ClassWaittimes = []
        ClassQWaittimes = []
        ClassTimes = []
        for ctype in ctypelist:
            ClassWaittimes.append([])
            ClassQWaittimes.append([])
            
        for customer in customersdone:
            time = customer.waittimelist[i][2]-customer.waittimelist[i][0]
            qtime = customer.waittimelist[i][1]-customer.waittimelist[i][0]
            ClassWaittimes[customer.ctype].append(time)
            ClassQWaittimes[customer.ctype].append(qtime)
            times.append(time)
            qtimes.append(qtime)
            
        for ctype in ctypelist:
            ClassTimes.append([np.mean(ClassWaittimes[ctype]),np.mean(ClassQWaittimes[ctype])])
        Waittimes.append([np.mean(qtimes), np.mean(times),ClassTimes])
        #NodeQueueTime.append(np.mean(qtimes))
    #Waittimes = [NodeWaitTime, NodeQueueTime]


    return(Waittimes)



def BusModel(ctyperate= [10,10,10],ctypemu1=[15,15,15],ctypemu2=[15,15,15],runtime=1000):
    #ctyperate customer arrivalrates for 3 classes for Q1
    #Ctypemu1 Customer Service rates for 3 classes for Q1
    #ctypemy2 Customer Service rates for 3 classes for Q2
    #Runtime Units of Time to run Model (Reccomend atleast 500, Min 100)
    
    clock = 0
    systemcheckinterval = 0.25
    systemcheck = (1/10)*runtime
    #######System Parameters#######
    N=0 #let N be the Total number in the sys
    Nlist = []

    #########Create Initial Arrivals##########
    #ctypelist = [0,1] # Customer Classes
    ctypelist =[0,1,2]
    ctypedictionary = ["Cripple","Elderly","Regular","Cripple"] #Customer Class Descriptions
    Classes = CustomerClass(ctypelist,ctyperate,ctypedictionary)

    ####################################
    #Define The list of Queues our Riders will be going through
    Queuelist = [] # Empty List of Queues,  follows form [M/M/2/FCFS/N, M/M/2/FCFS/N]
    Queuelist.append(Stage(0,15,2,priority="Classes", ctype_mus= ctypemu1))
    Queuelist.append(Stage(1,12,2,ctype_mus=ctypemu2))
    Queuelist.append(Exit(2))   #Finished Patients


    #Let N represent The Max number on a bus
    customersdone = []
    #Arrival into M/M/2/FCFS/N Bus Board Node
    #Transition from Bus Board Node to M/M/2/N Bus Exit Node
    #Exit from Bus Exit Node

    #while len(customersdone) <=  K:
    while clock <= runtime:
            nextservice = [None,None,math.inf]
            #nextarrival = [0,clock + random.expovariate(20)]
            
            GenerateServiceTimes(Queuelist,clock)
            nextservice = FindNextServiceTimes(Queuelist)
            nextarrival = FindNextArrival(Classes)
            if (systemcheck <= nextarrival[1]) and (systemcheck <= nextservice[2]):
                    CalcSystemStates(Queuelist)
                    systemcheck += systemcheckinterval
            if nextarrival[1] <= nextservice[2]:
                    clock = nextarrival[1]
                    customer = Customer(nextarrival[0])
                    #Queuelist[0].queue.append(customer) # Adds Customer to First Queue # This method is faster but less Dynamic
                    Queuelist[0].AddtoQ(customer,clock)
                    N+=1
                    GenerateArrival(Classes,customer.ctype,clock)
                    customer=None
                    nextarrival = [None, math.inf]
                    
            elif nextservice[2] <= nextarrival[1]:
                    clock = nextservice[2]
                    customer = Queuelist[nextservice[0].index].Serve(nextservice) #Serves Customer
                    
                    ###Insert Birth Death Between Queues ####
                    
                    #Queuelist[nextservice[0].index+1].queue.append(customer) # Bumps Customer to next Queue
                    Queuelist[nextservice[0].index+1].AddtoQ(customer,clock) # This method is faster but less Dynamic
                    if nextservice[0].index+1 == 2: # Final Stage
                            customer.clockout = nextservice[2]
                            customersdone.append(customer)
                            N -= 1
                            
                    customer = None
                    nextservice = [None,None,math.inf]
            Nlist.append(N)
    CalcSystemStats(Queuelist)
    NodeWaitTime = CalcWaitTime(2,customersdone,[0,1,2])
    
    def GeneralWaitTime(customersdone,Q):
        i = int(1/99) * len(customersdone)
        waittimes = []
        while i < len(customersdone):
            waittimes.append(customersdone[i].waittimelist[Q][2]-customersdone[i].waittimelist[Q][0])
            i+=1
        return(np.mean(waittimes))
    
    for n in range(10):
        Queuelist[0].pi_n.append(0)
        Queuelist[1].pi_n.append(0)
    
    Q1Info = [np.mean(Queuelist[0].systemsizes), GeneralWaitTime(customersdone,0),NodeWaitTime[0][2], Queuelist[0].pi_n[0:11]] #Average L, Average W, Wc, pi's
    Q2Info = [np.mean(Queuelist[1].systemsizes),GeneralWaitTime(customersdone,1),NodeWaitTime[1][2], Queuelist[1].pi_n[0:11]] #Average L
    
    
    return(Q1Info,Q2Info,customersdone)