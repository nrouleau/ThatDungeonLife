# Python imports
import os
import sys
import numpy
import random
import matplotlib.pyplot as plt

# Generates random races and genders based on an configured population distribution.
# Useful for generating NPCs in-game or in-prep

# Features:
# Convert everything to database style (probably JSON)
# Add name generation based on the race/gender
# Support non standard genders
# So many more things
def main():
    tasaldahn_races = RaceDistribution()
    tasaldahn_races.set_percentage("dwarf", 10)
    tasaldahn_races.set_percentage("elf", 5)
    tasaldahn_races.set_percentage("halfling", 16)
    tasaldahn_races.set_percentage("gnome", 3)
    tasaldahn_races.set_percentage("dragonborn", 2.4)
    tasaldahn_races.set_percentage("halfelf", 9)
    tasaldahn_races.set_percentage("halforc", 1.3)
    tasaldahn_races.set_percentage("tiefling", 2.2)
    tasaldahn_races.set_percentage("goliath", 0.5)
    tasaldahn_races.set_percentage("human", tasaldahn_races.get_other() - 0.1)
    #print(tasaldahn_races.get_other())

    print(tasaldahn_races.get_random_race() + " " + get_random_gender())
    print(tasaldahn_races.get_random_race() + " " + get_random_gender())
    print(tasaldahn_races.get_random_race() + " " + get_random_gender())
    print(tasaldahn_races.get_random_race() + " " + get_random_gender())
    print(tasaldahn_races.get_random_race() + " " + get_random_gender())
    #tasaldahn_races.generate_pie_plot()
    #tasaldahn_races.self_test()


def get_random_gender():
    coinflip = random.randint(0,1)
    if(coinflip == 0):
        return "male"
    else:
        return "female"

class RaceDetails:
    def __init__(self):
        self.pdf = 0
        self.cdf = 0
        self.test_count = 0

class RaceDistribution:
    def __init__(self):
        self.race_dict = {}
        self.race_dict['human'] = RaceDetails()
        self.race_dict['dwarf'] = RaceDetails()
        self.race_dict['elf'] = RaceDetails()
        self.race_dict['halfling'] = RaceDetails()
        self.race_dict['gnome'] = RaceDetails()
        self.race_dict['dragonborn'] = RaceDetails()
        self.race_dict['halfelf'] = RaceDetails()
        self.race_dict['halforc'] = RaceDetails()
        self.race_dict['tiefling'] = RaceDetails()
        self.race_dict['goliath'] = RaceDetails()

        self.race_keys_ordered_list = list(self.race_dict.keys())
        self.race_dict['other'] = RaceDetails()
        self.race_keys_ordered_list.append('other')

    def generate_pie_plot(self):
        pdfs = []
        for race_name in self.race_keys_ordered_list:
            pdfs.append(self.race_dict[race_name].pdf)

        plt.pie(pdfs, labels=self.race_keys_ordered_list, shadow=True)
        plt.show()

    def get_other(self):
        return round(self.race_dict['other'].pdf, 4)

    def get_random_race(self):
        # Check some things
        if(self.get_other() < 0):
            raise ValueError("The sum total of race percents is " + str(100 - get_other()) + "! Cannot get a random race...")
        if(self.race_keys_ordered_list[-1] != "other"):
            print(self.race_keys_ordered_list)
            raise ValueError("Critical Code error! 'other' race must be listed last!")

        # get the value
        select = random.uniform(0,100)
        for key in self.race_keys_ordered_list:
            if (self.race_dict[key].cdf >= select):
                return key

        raise ValueError("get_random_race: Never got a race! Should be impossible...")

    def set_percentage(self, race, percent):
        if(percent > 100 or percent < 0):
            raise ValueError("Set Percentage: The percent must be between 0 and 100, but was " + str(percent))
        if race in self.race_dict:
            self.race_dict[race].pdf = percent
            self.recalculate_cumulative_dict()
        else:
            raise ValueError("The Race '" + str(race) + "' does not exist in the race_dict dictionary")

    def recalculate_cumulative_dict(self):
        sum = 0
        for key in self.race_keys_ordered_list:
            if(key == "other"):
                self.race_dict[key].cdf = 100
                self.race_dict[key].pdf = 100 - sum
            else:
                sum += self.race_dict[key].pdf
                self.race_dict[key].cdf = sum

    def self_test(self):
        N = 100000
        other_count = 0
        for i in range(0,N):
            race = self.get_random_race()
            self.race_dict[race].test_count += 1

        for race in self.race_dict.keys():
            result = round(100 * (self.race_dict[race].test_count / N), 2)
            expected = round((self.race_dict[race].pdf), 2)
            print ("Race '{0}': True = {1}%, Test = {2}%. Difference: {3}%".format(race, expected, result, round(result - expected, 4)))

        #result = other_count / N
        #expected = self.race_dict[race].pdf
        #print ("Race '{0}': True = {1}%, Test = {2}%. Difference: {3}%".format(expected, result, result - expected))

if __name__ == '__main__':
    main()