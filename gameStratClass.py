import pandas as pd
class Strategy():

    def __init__(self,decisionCode,allocationCode,data="appDf.pkl"):
        self.df = pd.read_pickle(data).to_dict('records')
        self.decideFunction = "def decide(Team_A,Team_B):"+decisionCode.replace('\n','\n    ')
        self.allocateFunction = "def allocate():"+allocationCode.replace('\n','\n    ')
        self.results={}

    # def runIt(self,x):
    #     exec(self.defineF,globals())
    #     return f(x)

    def simulate(self):
        # win or loss on the pick
        actual = []
        expected = []
        correct = []
        nets = []
        rollingNets = []
        
        totalNet = 0

        exec(self.decideFunction,globals())
        exec(self.allocateFunction,globals())
        for idx in range(0,len(self.df),2):
            Team_A = self.df[idx]
            Team_B = self.df[idx+1]
            # print(Team_A['ROI'],Team_B['ROI'])

            outcome = [int(self.df[idx]['Win']),int(self.df[idx+1]['Win'])]
            actual.append(self.df[idx]['Win'])

            decision = decide(Team_A,Team_B)
            if decision[0] > decision[1]:
                expected.append(True)
            else:
                expected.append(False)

            correct.append(int(expected[-1]==actual[-1]))

            allocation = allocate()

            net = -allocation            
            winnings = outcome[0]*decision[0]*allocation*self.df[idx]['ROI'] + outcome[1]*decision[1]*allocation*self.df[idx+1]['ROI']
  
            net += winnings
            nets.append(net)
            
            totalNet += net
            rollingNets.append(totalNet)


        self.results = {
        "acutal":actual,
        "expected":expected,
        "correct":correct,
        "nets":nets,
        "rollingNets":rollingNets,
        "totalNet":totalNet
        }

        return self.results

        

d = """
if Team_A['ROI'] < Team_B['ROI']:
    return [0,1]
else:
    return [1,0]
"""
a = """
return 10
"""
my_strat = Strategy(d,a)
sim = my_strat.simulate()
print(sim)
print(max(sim['rollingNets']))
print(sum(sim['correct'])/len(sim['correct']))

