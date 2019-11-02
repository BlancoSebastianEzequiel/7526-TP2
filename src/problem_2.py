import random
import numpy as np
import matplotlib.pyplot as plt


class Server:
    def __init__(self, total_time=1000000, time_between_arrivals=10):
        """
        total_time: total time in milli-seconds
        time_between_arrivals: time for arrival or processing completion
        in milli-seconds
        p: arrival_prob
        q: request_completion_prob
        """
        self.total_time = total_time
        self.time_between_arrivals = time_between_arrivals
        self.p = 1/40
        self.q = 1/30
        self.request_number = 0
        self.change_state = {
            'move_forward_prob': self.add_request,
            'go_back_prob': self.finish_request,
            'staying_prob': lambda: None
        }
        self.occurrences_per_time = {}
        self.occurrences_per_state = {}
        self.probs = [
            {
               'prob': self.move_forward_prob(),
               'name': 'move_forward_prob'
            },
            {
                'prob': self.go_back_prob(),
                'name': 'go_back_prob',
            },
            {
                'prob': self.staying_prob(),
                'name': 'staying_prob'
            }
        ]
        self.probs = sorted(self.probs, key=lambda x: x['prob'])
        for idx in range(len(self.probs)-1):
            self.probs[idx+1]['prob'] += self.probs[idx]['prob']

        self.no_processing_request_number = 0

    def add_request(self):
        self.request_number += 1

    def finish_request(self):
        if self.request_number == 0:
            return
        self.request_number -= 1

    def staying_prob(self):
        p = self.p
        q = self.q
        return p*q + (1-p)*(1-q)

    def move_forward_prob(self):
        return self.p*(1-self.q)

    def go_back_prob(self):
        return self.q*(1-self.p)

    def graph_occurrences_per_state(self):
        x = list(self.occurrences_per_state.keys())
        y = list(self.occurrences_per_state.values())
        y_pos = np.arange(len(x))
        x_ticks = (str(t) for t in x)
        plt.bar(y_pos, y, color='C1', align='center', alpha=0.5, log=True)
        plt.xticks(y_pos, x_ticks)
        plt.title('occurrences_per_state')
        plt.show()

    def graph_occurrences_per_time(self):
        x = list(self.occurrences_per_time.keys())
        y = list(self.occurrences_per_time.values())
        plt.plot(x, y, color='C2', label='occurrences_per_time')
        plt.legend(loc='upper right')
        plt.show()

    def percentage_no_processing_request(self):
        return self.no_processing_request_number * \
               self.time_between_arrivals/self.total_time*100

    def transition(self, timestamp):
        arrival = random.uniform(0.00000, 1.00000)
        for idx, prob in enumerate(self.probs):
            if arrival <= prob['prob']:
                if prob['name'] == 'staying_prob':
                    self.no_processing_request_number += 1
                self.change_state[prob['name']]()
                self.occurrences_per_time.setdefault(timestamp, 0)
                self.occurrences_per_time[timestamp] += self.request_number
                self.occurrences_per_state.setdefault(self.request_number, 0)
                self.occurrences_per_state[self.request_number] += 1
                return True
        return None


server = Server()
print(f"probs: {server.probs}")
for i in range(100000):
    server.transition((i + 1) * 10)
server.graph_occurrences_per_time()
server.graph_occurrences_per_state()
print(f"percentage_no_processing_request: "
      f"{server.percentage_no_processing_request()}")
