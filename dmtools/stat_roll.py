# Generic python imports
import os
import sys
import random
import numpy
import math
import matplotlib.pyplot as plt

# Setup imports using relative paths
this_file = os.path.abspath(__file__)
this_folder = os.path.dirname(this_file)
sys.path.append(this_folder)


def main():
    print("Running test")
    expected_avg = 30.355
    expected_stdev = 9.7065

    PB = []
    statslist = []
    N = 100000
    for i in range(N):
        stats = CharacterStats()
        stats.generate_stats()
        PB.append(stats.point_buy)
        statslist.append(stats)

    avg = numpy.mean(PB)
    stdev = numpy.std(PB)

    print("\r\n===================== Raw data =====================")
    print("Test Result: Avg = {0}, StdDev = {1}, min = {2}, max = {3} (for N = {4})".format(avg, stdev, min(PB), max(PB), N))
    print("Expected: Avg = {0}, StdDev = {1}".format(expected_avg, expected_stdev))
    print("====================================================\r\n\r\n")

    # Now try raising all rolls to 27 min, and forcing a re-roll if >1 std dev from the center
    pb_used = []
    pb_after_reroll = []
    reroll_count = 0
    min_allowed = 27
    max_cutoff = 40 # one std dev away from avg
    outliers = 0

    i = 0
    best_stats = []
    worst_stats = []
    for pb in PB:
        min_assumed_best_stat = 0
        if(pb < min_allowed):
            pb_used.append(min_allowed)
            min_assumed_best_stat = 15
        elif(pb <= max_cutoff):
            pb_used.append(pb)
        else:
            if pb > max_cutoff:
                reroll_count += 1
                new_stats = CharacterStats()
                new_stats.generate_stats()
                statslist[i] = new_stats
                new_value = new_stats.point_buy
                if(new_stats.point_buy < min_allowed):
                    min_assumed_best_stat = 15
                    new_value = min_allowed

            if(new_value > max_cutoff):
                outliers += 1
            pb_used.append(new_value)
            pb_after_reroll.append(new_value)

        best_stats.append(max(min_assumed_best_stat, statslist[i].max))
        worst_stats.append(statslist[i].min)
        i += 1

    avg = numpy.mean(pb_used)
    stdev = numpy.std(pb_used)
    avg_reroll = numpy.mean(pb_after_reroll)
    stdev_reroll = numpy.std(pb_after_reroll)
    print("===================== For the Players =====================")
    print("Test Result: Avg = {0}, StdDev = {1}, min = {2}, max = {3}, reroll = {4}% (for N = {5})".format(print_friendly(avg,3), print_friendly(stdev,2), min(pb_used), max(pb_used), reroll_count*100/N, len(pb_used)))
    print("Subcategory after re-roll: Avg = {0}, StdDev = {1}, min = {2}, max = {3}, (for N = {4})".format(print_friendly(avg_reroll,3), print_friendly(stdev_reroll,2), min(pb_after_reroll), max(pb_after_reroll), len(pb_after_reroll)))
    print("Percent above max cutoff: {0}%".format(outliers*100/N))
    print("----")
    print("Percentages of max stat values:")
    for val in range(min(best_stats),max(best_stats)+1):
        print("{0}: {1}%".format(val, print_friendly(best_stats.count(val)*100/N,2)))
    print("----")
    print("Percentages of min stat values:")
    for val in range(min(worst_stats),max(worst_stats)+1):
        print("{0}: {1}%".format(val, print_friendly(worst_stats.count(val)*100/N,2)))
    print("Used min allowed value = {0}, and max cutoff = {1}".format(min_allowed, max_cutoff))
    print("====================================================\r\n")

    plt.figure()
    histogram_integer_data(worst_stats, 'red')
    plt.ylabel("Probability")
    plt.xlabel("Stat value")
    title_str = "Worst Stats for 4d6 drop 1"
    #title_str += "\nProbability of {0} = {1}%, ".format(min_allowed, print_friendly(proportions[0]*100,4))
    #title_str += "Avg = {0}, StdDev = {1}".format(print_friendly(avg,4), print_friendly(stdev,4))
    plt.title(title_str)

    plt.figure()
    histogram_integer_data(best_stats, 'green')
    plt.ylabel("Probability")
    plt.xlabel("Stat value")
    title_str = "Best Stats for 4d6 drop 1"
    #title_str += "\nProbability of {0} = {1}%, ".format(min_allowed, print_friendly(proportions[0]*100,4))
    #title_str += "Avg = {0}, StdDev = {1}".format(print_friendly(avg,4), print_friendly(stdev,4))
    plt.title(title_str)

    plt.figure()
    histogram_integer_data(PB, 'yellow')
    proportions, bins = histogram_integer_data(pb_used, 'red')
    #proportions, bins = histogram_integer_data(pb_after_reroll, 'blue')
    plt.ylabel("Probability")
    plt.xlabel("Point buy")
    title_str = "Roll for stats (4d6 drop 1) in point buy values"
    title_str += "\nProbability of {0} = {1}%, ".format(min_allowed, print_friendly(proportions[0]*100,4))
    title_str += "Avg = {0}, StdDev = {1}".format(print_friendly(avg,4), print_friendly(stdev,4))
    plt.title(title_str)

    plt.show()

def print_friendly(value, sigfigs):
    if value == 0:
        return str(value)

    digits_before_decimal = math.floor(math.log10(abs(value))) + 1
    return round(value, sigfigs - digits_before_decimal)

def histogram_integer_data(data, color):
    bin_set = [x+0.5 for x in range(min(data)-1, max(data)+1)]
    axes = plt.gca()
    x1,x2,y1,y2 = plt.axis()
    if(y2 == 1.0):
        y2 = 0
    proportions, bins, patches = plt.hist(data, bin_set, normed=1, edgecolor='black', facecolor=color, alpha=0.5)
    except_for_max = [x for x in proportions]
    except_for_max.remove(max(except_for_max))
    ymax = max(except_for_max) * 1.2
    if(ymax > y2):
        axes.set_ylim(0,ymax)

    return proportions, bins

def get_pb_sum():
    return sum(calculate_pointbuy(roll_one_stats_set()))

'''
For each element in stats, calculates the point-buy value equivalent
'''
def calculate_pointbuy(stats):
    # This uses standard point buy
    # For dealing with <8, it uses "-1" for each value under
    # For dealing with >15, it adds "2" for each increased value, but adds "3" for an 18
    pointbuy = []
    for stat in stats:
        if(stat <= 0):
            raise(ValueError("calculate_pointbuy: Stat was {0} but it must be >0!".format(stat)))
        elif(stat <= 7):
            pointbuy.append(stat-8)
        elif(stat <= 13):
            pointbuy.append(stat-8)
        elif(stat <= 17):
            pointbuy.append(stat-8 + stat-13)
        elif(stat <= 18):
            pointbuy.append(stat-8 + stat-13 + stat-17)
        else:
            raise(ValueError("calculate_pointbuy: Stat was {0} but it must be <=18!".format(stat)))
    return pointbuy

def test_pointbuy():
    stats = [x for x in range(1,19)]
    pb = calculate_pointbuy(stats)
    for i in range(len(pb)):
        print(stats[i], ":", pb[i])

def roll_one_stats_set():
    stats = []
    for i in range(6):
        stats.append(roll_n_d_sided_choose_m(4,6,3))
    return stats

'''
Rolls n d-sided dice, and chooses the top m results
'''
def roll_n_d_sided_choose_m(n, d, m):
    if(m > n):
        raise(ValueError("Invalid inputs: Cannot choose the m={0} largest dice out of n={1} dice! {0} must be <= {1}!".format(m,n)))

    Dice = []
    for i in range(n):
        Dice.append(random.randint(1,6))

    Dice = sorted(Dice)
    Chosen = Dice[-m:]
    return sum(Chosen)

class CharacterStats():
    def __init__(self):
        base_stats = []
        min = 0
        max = 0
        avg = 0
        point_buy = 0

    def generate_stats(self):
        self.base_stats = roll_one_stats_set()
        self.min = min(self.base_stats)
        self.max = max(self.base_stats)
        self.avg = numpy.mean(self.base_stats)
        self.point_buy = sum(calculate_pointbuy(self.base_stats))
        return self.base_stats


if __name__ == '__main__':
    main()

    '''if(len(sys.argv) > 1):
        test_name = sys.argv[1]
    else:
        test_name = "Unnamed_test"
    if(len(sys.argv) > 2):
        channels = [sys.argv[2]]
    else:
        channels = [1,2] # Modify this if you want data captured for >1 channel
        #channels = [1,2]
    main(test_name, channels)'''
