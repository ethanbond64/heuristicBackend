import pandas as pd


class Strategy():

    def __init__(self, decisionCode, allocationCode, data="appDf.pkl"):
        self.df = pd.read_pickle(data).to_dict('records')
        self.decideFunction = "def decide(Team_A,Team_B):" + \
            decisionCode.replace('\n', '\n    ')
        self.allocateFunction = "def allocate():"+allocationCode.replace('\n', '\n    ')
        self.results = {}

    def simulate(self):
        # win or loss on the pick
        actual = []
        expected = []
        correct = []
        nets = []
        rollingNets = []

        totalNet = 0

        exec(self.decideFunction, globals())
        exec(self.allocateFunction, globals())
        for idx in range(0, len(self.df), 2):
            Team_A = self.df[idx]
            Team_B = self.df[idx+1]
            # print(Team_A['ROI'],Team_B['ROI'])

            outcome = [int(self.df[idx]['Win']), int(self.df[idx+1]['Win'])]
            actual.append(self.df[idx]['Win'])

            decision = decide(Team_A, Team_B)
            if decision[0] > decision[1]:
                expected.append(True)
            else:
                expected.append(False)

            correct.append(int(expected[-1] == actual[-1]))

            allocation = allocate()

            net = -allocation
            winnings = outcome[0]*decision[0]*allocation*self.df[idx]['ROI'] + \
                outcome[1]*decision[1]*allocation*self.df[idx+1]['ROI']

            net += winnings
            nets.append(net)

            totalNet += net
            rollingNets.append(totalNet)

        self.results = {

            # True means the first team listed won, False means second team listed
            "acutal": actual,
            "expected": expected,

            # 1 if actual[i]==expected[i] 0 otherwise
            "correct": correct,

            # net win/loss on each individual game
            "nets": nets,

            # net worth of the user after each additional game
            "rollingNets": rollingNets,

            # final net worth of the user after all of the games
            "totalNet": totalNet
        }

        return self.results


# decision function defined by user, must be string of working python
# return the % to bet on each team [team_a,team_b], so [0,1] picks team b, [0.5,0.5] picks both
d = """
if Team_A['ROI'] < Team_B['ROI']:
    return [0,1]
else:
    return [1,0]
"""

# allocation function, for now its spending $10 on each game
a = """
return 10
"""
my_strat = Strategy(d, a)
sim = my_strat.simulate()
print(sim)
print(max(sim['rollingNets']))
print(sum(sim['correct'])/len(sim['correct']))
