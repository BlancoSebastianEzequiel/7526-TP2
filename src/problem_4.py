import simpy
from random import randint
from numpy.random import exponential

class baseApi:
    def  __init__(self, env):
       self.env= env

    def makeRequest(self):
        yield self.env.timeout(exponential(scale=(0.8)))

class dualBaseApi:
    def  __init__(self, env):
       self.env= env

    def makeRequest(self):
        if randint(0, 100) < 60 :
            yield self.env.timeout(exponential(scale=(0.7)))
        else:
            yield self.env.timeout(exponential(scale=(1)))

class webService: 
    def __init__(self, env, dataBase, baseApi, times_til_process, times_til_request):
        self.env = env
        self.web_service_process = env.process(self.start(dataBase, baseApi, times_til_process, times_til_request))

    def start(self, dataBase , baseApi, times_til_process, times_til_request):
        # Llega la consulta al webService
        yield self.env.process(self.request())
        time_start = self.env.now
        

        with dataBase.request() as req:
            yield req
            # Esta liberado el recurso de la api a la base de datos y lo uso
            times_til_request.append(self.env.now - time_start)

            # Hago la request a la base
            request_base = self.env.process(baseApi.makeRequest())
            yield request_base
            times_til_process.append(self.env.now - time_start)

    def request(self):
        yield self.env.timeout(exponential(scale=(4)))



def dataBaseOption(option, env):
    if dataBaseOption == 1:
        return baseApi(env)
    else:
        return dualBaseApi(env)


def runSimulation(option, consultas=1):
    env = simpy.Environment()
    dataBase = simpy.Resource(env, capacity=1)
    dataBaseApi = dataBaseOption(option, env)
    times_til_process = []
    times_til_request = []
    for i in range(0, consultas):
        webService(env, dataBase, dataBaseApi, times_til_process, times_til_request)
        
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
