import simpy
from random import randint
from numpy.random import exponential

class baseApi:
    def  __init__(self, env, dataBase):
       self.env= env
       self.dataBase = dataBase

    def makeRequest(self, times_til_request, time_start):
        with self.dataBase.request() as req:
            yield req
            times_til_request.append(self.env.now - time_start)
            # Esta liberado el recurso de la api a la base de datos y lo uso

            yield self.env.timeout(exponential(scale=(0.8)))

class dualBaseApi:
    def  __init__(self, env, dataBase1, dataBase2):
       self.env= env
       self.dataBase1 = dataBase1
       self.dataBase2 = dataBase2

    def makeRequest(self, times_til_request, time_start):
        if self.pickFirst():
            with self.dataBase1.request() as req:
                yield req
                times_til_request.append(self.env.now - time_start)

                # Esta liberado el recurso de la api a la base de datos y lo uso

                yield self.env.timeout(exponential(scale=(0.7)))
        else:
            with self.dataBase2.request() as req:
                yield req
                times_til_request.append(self.env.now - time_start)
                # Esta liberado el recurso de la api a la base de datos y lo uso

                yield self.env.timeout(exponential(scale=(1)))
    
    def pickFirst(self):
        if (self.dataBase1.count == 0 and self.dataBase2.count == 0 or 
         self.dataBase1.count == 1 and self.dataBase2.count == 1):
            return randint(0, 100) < 60
        else:
            return self.dataBase1.count == 0

class webService: 
    def __init__(self, env, baseApi, times_til_process, times_til_request):
        self.env = env
        self.web_service_process = env.process(self.start(baseApi, times_til_process, times_til_request))

    def start(self, baseApi, times_til_process, times_til_request):
        # Llega la consulta al webService
        yield self.env.process(self.request())
        time_start = self.env.now

        # Hago la request a la base
        request_base = self.env.process(baseApi.makeRequest(times_til_request, time_start))
        yield request_base
        times_til_process.append(self.env.now - time_start)

    def request(self):
        yield self.env.timeout(exponential(scale=(4)))



def dataBaseOption(option, env):
    if option == 1:
        dataBase = simpy.Resource(env, capacity=1)
        return baseApi(env, dataBase)
    else:
        dataBase1 = simpy.Resource(env, capacity=1)
        dataBase2 = simpy.Resource(env, capacity=1)
        return dualBaseApi(env, dataBase1, dataBase2)


def runSimulation(option, consultas=1):
    env = simpy.Environment()
    dataBaseApi = dataBaseOption(option, env)
    times_til_process = []
    times_til_request = []
    for i in range(0, consultas):
        webService(env, dataBaseApi, times_til_process, times_til_request)
        
    env.run()

    print(f"Tiempo hasta poder hacer la consulta promedio en la base {option}: {sum(times_til_request) / len(times_til_request)}")

    no_wait = [i for x in times_til_request if x == 0]
    print(f"Aquellos que no esperaron en la base {option}: {len(no_wait)}")

    return sum(times_til_process) / len(times_til_process)

consultas = 100000
# Opcion con 1 base
result_simu_1 = runSimulation(1, consultas)
# Opcion con 2 bases
result_simu_2 = runSimulation(2, consultas)

print(f"Tiempo promedio de procesamiento con la base 1: {result_simu_1}")
print(f"Tiempo promedio de procesamiento con la base 2: {result_simu_2}")

if ((result_simu_1 / 2) > result_simu_2):
    print(f"Recomiendo usar la opcion que utiliza 2 bases distribuidas")
else:
    print(f"Recomiendo usar la opcion que utiliza 1 base de datos central")
