import threading
import json
import time
import random
import queue
from abc import ABC, abstractmethod

threadLock = threading.Lock()
chr_list = queue.Queue()

class myThread(threading.Thread):

  # new Thread
  def __init__(self, threadID, name, speed):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.speed = speed

  def run(self):
    while True:
      time.sleep(40 / self.speed)
      # Get lock to synchronize threads
      threadLock.acquire()

      # enemy action
      if (int(self.threadID) == 3):
          ls = chr_list.get()


          # Battle finish?
          if (ls == 0) or (ls == 1):
            chr_list.put(ls)
            threadLock.release()
            return 

          i = 0
          while i< len(ls) - 1:
            if ls[i].curHP > 0:
              break
            i += 1

          if i == len(ls) - 1:
            chr_list.put(0)
            threadLock.release()
            return


          # do damage
          damage = ls[3].ATK - ls[i].DEF * (1 + ls[i].per_action)
          if damage < 0:
            damage = 0

          print(" %s attacked %s, make %s damage \n" % (ls[3].Name, ls[i].Career, damage))
          ls[i].curHP -= damage

          for s in ls:
            print(s)

          chr_list.put(ls)
          print("\n")

      # hero action
      else:
          ls = chr_list.get()

          # battle finish?
          if (ls == 0) or (ls == 1):
            chr_list.put(ls)
            threadLock.release()
            return


          i = int(self.threadID)

          if ls[i].curHP <= 0:
            chr_list.put(ls)
            threadLock.release()
            return


          for s in ls:
            print(s)
          
          # take action
          print("\n You are %s" % (ls[i].Career))
          action = int(input("Choose your action (1) Attack (2) Defence:") or "-1")

          ls[i].per_action = 0
          if action == 2:
            ls[i].per_action = 1
            print(" %s  choose to defend \n" % (ls[i].Career))
          
          # do damage
          if action == 1:
            damage = ls[i].ATK - ls[3].DEF
            if damage < 0:
              damage = 0
          
            print(" %s attacked %s, make %s damage \n" % (ls[i].Career, ls[3].Name, damage))
            ls[3].curHP -= damage

          for s in ls:
            print(s)
          
          print("\n")
          if ls[3].curHP <= 0:
            print("Enemy die \n")
            chr_list.put(1)
            threadLock.release()
            return 

          chr_list.put(ls)
          


      # Free lock to release next thread
      threadLock.release()
  


class game():
    def __init__(self):
        self.chr1 = None
        self.chr2 = None
        self.chr3 = None

    def menu(self):
        while True:
            choice = int(
                input(
                    "Choose action: (1) New game (2) Load game (3) Exiting \n")
            )

            if choice == 1:
                self.create_new()
                return 1
            elif choice == 2:
                self.load()
                return 1
            elif choice == 3:
                return 0
            else:
                print("\n please enter a correct input")

    # create new hero
    def create_new(self):
        with open('Hero.json', 'r') as f:
            hero_list = json.load(f)

        while True:
            num = random.sample(hero_list.keys(), 1)[0]
            self.chr1 = hero(hero_list[num])

            num = random.sample(hero_list.keys(), 1)[0]
            self.chr2 = hero(hero_list[num])

            num = random.sample(hero_list.keys(), 1)[0]
            self.chr3 = hero(hero_list[num])

            print(self.chr1)
            print(self.chr2)
            print(self.chr3, "\n")

            while True:
                ans = input("Do you want to reload (Y/N):")
                if (ans == 'Y'):
                    break
                elif (ans == 'N'):
                    return

    #load historical record
    def load(self):
        with open('Record.json', 'r') as f:
            hero_list = json.load(f)

        self.chr1 = hero(hero_list['1'])
        self.chr2 = hero(hero_list['2'])
        self.chr3 = hero(hero_list['3'])
        return

    def battle(self):
        print("\n\n Game Start ----->\n")

        # load enemy data
        while True:
            with open('Enemy.json', 'r') as f:
                enemy_list = json.load(f)

            num = random.sample(enemy_list.keys(), 1)[0]
            enemy1 = enemy(enemy_list[num])
            enemy1.levelup(max(
                self.chr1.LV,
                self.chr2.LV,
                self.chr3.LV,
            ))
            print("Find a enemy \n", enemy1, "\n")
            print("Battle begin ----->\n")

            if (not self.runtime(enemy1)):
                break


            # level up and save record
            self.chr1.levelup1()
            self.chr2.levelup1()
            self.chr3.levelup1()

            self.save()

        print(" Game Over ---->\n")

    def save(self):
        choice = input("\n Do you want to save it (Y/N)?:")

        if choice == "Y":
            data = dict()
            data['1'] = self.chr1.json()
            data['2'] = self.chr2.json()
            data['3'] = self.chr3.json()
            with open('Record.json', 'w') as outfile:
                json.dump(data, outfile)

    # battle stage
    def runtime(self, enemy1):

        threads = []
        while  not chr_list.empty():
          chr_list.get()

        chr_list.put([self.chr1, self.chr2, self.chr3, enemy1])
        # Create new threads
        thread1 = myThread(0, "char-1", self.chr1.SPD)
        thread2 = myThread(1, "char-2", self.chr2.SPD)
        thread3 = myThread(2, "char-3", self.chr3.SPD)
        thread4 = myThread(3, "enemy-1", enemy1.SPD)

        # Add threads to thread list
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)

        # Start new Threads
        for t in threads:
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # game lose/ win?
        if chr_list.get() == 0:
            return 0
        else:
            return 1

# Abstract class
class Charaters(ABC):
    @abstractmethod
    # Name, HP, ATK, DEF, SPD
    def __init__(self, obj):
        pass

    @abstractmethod
    def levelup(self, Target_LV):
        pass

    @abstractmethod
    def __str__(self):
        pass

# hero class
class hero(Charaters):
    def __init__(self, obj):
        self.per_action = 0
        self.Career = obj['Career']
        self.LV = obj['LV']
        self.HP = obj['HP']
        self.curHP = obj['HP']
        self.ATK = obj['ATK']
        self.DEF = obj['DEF']
        self.SPD = obj['SPD']
        self.grow = obj['grow']

    def levelup(self, Target_LV):
        self.HP += (Target_LV - self.LV) * self.grow[0]
        self.curHP = self.HP
        self.ATK += (Target_LV - self.LV) * self.grow[1]
        self.DEF += (Target_LV - self.LV) * self.grow[2]
        self.SPD += (Target_LV - self.LV) * self.grow[3]
        self.LV = Target_LV

    # levelup 1 level
    def levelup1(self):
        self.HP += self.grow[0]
        self.curHP = self.HP
        self.ATK += self.grow[1]
        self.DEF += self.grow[2]
        self.SPD += self.grow[3]
        self.LV += 1

    # output the record as json format
    def json(self):
      return { "Career":self.Career, "LV":self.LV, "HP":self.HP, "ATK":self.ATK, "DEF":self.DEF, "SPD":self.SPD, "grow":self.grow}

    def __str__(self):
        return (
            "Career: %s, LV: %s, HP: %s, ATK: %s, DEF: %s, SPD: %s" %
            (self.Career, self.LV, self.curHP, self.ATK, self.DEF, self.SPD))

#enemy class
class enemy(Charaters):
    def __init__(self, obj):
        self.Name = obj['Name']
        self.LV = obj['LV']
        self.HP = obj['HP']
        self.curHP = obj['HP']
        self.ATK = obj['ATK']
        self.DEF = obj['DEF']
        self.SPD = obj['SPD']
        self.grow = obj['grow']

    def levelup(self, Target_LV):
        self.HP += (Target_LV - self.LV) * self.grow[0]
        self.curHP = self.HP
        self.ATK += (Target_LV - self.LV) * self.grow[1]
        self.DEF += (Target_LV - self.LV) * self.grow[2]
        self.SPD += (Target_LV - self.LV) * self.grow[3]
        self.LV = Target_LV

    def __str__(self):
        return ("Name: %s, LV: %s, HP: %s, ATK: %s, DEF: %s, SPD: %s" %
                (self.Name, self.LV, self.curHP, self.ATK, self.DEF, self.SPD))


#Main

if __name__ == "__main__":

    print("Welcome to boring RPG \n")
    new_game = game()

    while (new_game.menu()):
        new_game.battle()

    print("Thank you for your play")
