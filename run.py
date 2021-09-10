from matplotlib import pyplot as plt
from scipy.stats import norm
import numpy as np

upgrade_costs = {
    1: 10,
    2: 50,
    3: 125,
    4: 250,
    5: 500
}

class UserInfo:

    def __init__(self, name):

        self.name = name
        self.score = 0
        self.gems_found = []
        self.gambling_won = 0
        self.gambling_lost = 0
        self.spent_on_upgrades = 0

    def __eq__(self, other):
        return other.name == self.name

    def __ne__(self, other):
        return not (other.name == self.name)

users = []

with open('log.txt', 'r') as file:
    for line in file:

        mod = line[line.find(': ')+2:] #get the entry without the timestamp

        if mod.startswith('**'): 
            segs = mod.split('**')
            user = UserInfo(segs[1])

            if user not in users:
                users.append(user)
            else:
                user = users[users.index(user)]

            content = segs[2].strip()

            if content.startswith('found: '):
                content = content[len('found: '):]
                segs = content.split(' ')
                gem = ' '.join(segs[:-4])
                rarity = segs[-3]
                score = int(segs[-1][1:])

                user.score += score
                user.gems_found.append(gem)
            elif content.startswith(': won '):
                content = content[len(': won '):]
                score = int(content)
                user.gambling_won += score

            elif content.startswith(': lost '):
                content = content[len(': lost '):]
                score = int(content)
                user.gambling_lost += score
    
        else:
            segs = mod.split(':')
            if len(segs) >= 2 and segs[1].startswith(' UPGRADED'):
                
                user = UserInfo(segs[0])

                if user not in users:
                    users.append(user)
                else:
                    user = users[users.index(user)]

                lvl = int(segs[1].split(' ')[-1])

                cost = upgrade_costs[lvl]

                user.spent_on_upgrades += cost
          
fig, ax = plt.subplots(2)

#total upgrade cost: 1870
users_score = sorted(users, key=lambda u: u.score, reverse=True)
for user in users_score[:10]:
    print(f"{user.name} has total score {user.score}")
    print(f"     spent {user.spent_on_upgrades} on upgrades")
    print(f"     won: {user.gambling_won}      lost: {user.gambling_lost}\n")

ax[0].plot( [user.score for user in users_score] )
ax[0].set(xlabel="Rank", ylabel="Score")

users_gambling_total = sorted(users, key=lambda u: u.gambling_won + u.gambling_lost, reverse=True)
for user in users_gambling_total[:10]:
    print(user.name)
    print(f"    won: {user.gambling_won}      lost: {user.gambling_lost}\n")

x_data = [user.gambling_won for user in users_gambling_total[9:]]
y_data = [user.gambling_lost for user in users_gambling_total[9:]]

ax[1].scatter(x_data, y_data)
ax[1].set(xlabel="Won", ylabel="Lost")
plt.subplots_adjust(hspace=0.8)   
plt.show()