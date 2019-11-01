import random


class Server:
    def __init__(self):
        """
        p: arrival_prob
        q: request_completion_prob
        """
        self.p = 1/40
        self.q = 1/30
        self.request_number = 0
        self.change_state = {
            'move_forward_prob': self.add_request,
            'go_back_prob': self.finish_request,
            'staying_prob': lambda x: x
        }
        self.occurrences_per_time = {}
        self.occurrences_per_state = {}

    def add_request(self):
        self.request_number += 1

    def finish_request(self):
        self.request_number -= 1

    def staying_prob(self):
        p = self.p
        q = self.q
        return p*q + (1-p)*(1-q)

    def move_forward_prob(self):
        return self.p*(1-self.q)

    def go_back_prob(self):
        return self.q*(1-self.p)

    def transition(self, timestamp):
        probs = [
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
        probs = sorted(probs, key=lambda x: x['name'])
        arrival = random.random()
        for prob in probs:
            if arrival <= prob['prob']:
                self.change_state[prob['name']]()
                self.occurrences_per_time.setdefault(timestamp, 0)
                self.occurrences_per_time[timestamp] += 1
                self.occurrences_per_state.setdefault(self.request_number, 0)
                self.occurrences_per_state[self.request_number] += 1
                return None
        return None

