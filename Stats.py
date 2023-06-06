import csv
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from scipy.stats.distributions import chi2
from scipy.stats import norm
from random import sample
from scipy.interpolate import interp1d
import math
from scipy.special import rel_entr

csv_file_name_2015 = 'Lottery_Powerball_Winning_Numbers__Beginning_2015.csv'
csv_file_name_2010 = 'Lottery_Powerball_Winning_Numbers__Beginning_2010.csv'


def Simulate_Probabilities(r,n,trials,val):
    distribution = [0]*r
    probability_distribution = []
    list = []
    #setting observed counts
    for trial in range(trials):
        list = sample(createList(r), n)
        list.sort()
        distribution[list[val] - 1] += 1        
    
    for i in distribution:
        probability_distribution.append(i/trials)
    return probability_distribution

def Create_Observed_Distribution(r,matrix):
    distribution = []

    for i in range(r):    
        distribution.append(Occurences(matrix,i+1))      

    return distribution

def Frequency(matrix,num):
    s = 0
    matrix = np.ravel(matrix)
    for i in matrix:
        if i == num:
            s += 1

    return s/len(matrix)

def Occurences(matrix,num):
    s = 0
    matrix = np.ravel(matrix)
    for i in matrix:
        if i == num:
            s += 1

    return s

def Total_1PropZTest(r,matrix):
    p_values = [0]*r
    n = np.ravel(matrix).shape[0]
    
    for i in range(len(p_values)):
        P = Frequency(matrix,i+1)
        P0 = 1/r
        a = (P-P0)
        b = P0*(1-P0)/n
        z = a/math.sqrt(b)
        p_values[i] = norm.cdf(z)

    return p_values


def Generate_Histogram(a,title,c):
    # Creating histogram

    fig, ax = plt.subplots(figsize =(10, 7))
    N, bins, patches = ax.hist(a, bins = createList(c),range=[0,c],align='left')
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    
    ax.yaxis.set_tick_params(pad = 10)
    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.6)
    
    # Setting color
    fracs = ((N**(1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())
    
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    plt.locator_params(axis='x', nbins=c)
    plt.xlabel("Value")
    plt.ylabel("Number of Draws")
    plt.title(title)
    # Show plot
    plt.show()

def Generate_Histogram_With_Curve(a,title,c,expected):
    # Creating histogram
    expected_counts = []
    fig, ax = plt.subplots(figsize =(10, 7))
    N, bins, patches = ax.hist(a, bins = createList(c),range=[0,c],align='left')
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    for prob in expected:
        expected_counts.append(prob*885)
    
    ax.yaxis.set_tick_params(pad = 10)
    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.6)
    
    # Setting color
    fracs = ((N**(1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())
    
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    mn, mx = plt.xlim()
    plt.xlim(mn, mx)
    x = np.linspace(mn, mx, 69)
    plt.plot(x, expected_counts, color='C0', label='Expected Values')
    plt.locator_params(axis='x', nbins=c)
    plt.xlabel("Value")
    plt.legend()
    plt.ylabel("Number of Draws")
    plt.title(title)
    # Show plot
    plt.show()

def createList(n):
    lst = []
    for i in range(n):
        lst.append(i + 1)
    return(lst)
#returns Chi squared statistic
def Chi_Squared_GOF_Test(power_ball_data, catagories):
    observed_counts = []
    expected_counts = []
    count = 0
    #setting observed counts
    for catagory in range(catagories):
        for draw in power_ball_data:
            if(draw == (catagory+1)):
                count += 1
        observed_counts.append(count)
        count = 0
    #setting expected counts
    for index in range(catagories):
        expected_counts.append((1/catagories)*len(power_ball_data))

    chi_squared = 0
    for i in range(catagories): 
        chi_squared += (((observed_counts[i]-expected_counts[i])**2)/expected_counts[i])

    p_val = chi2.sf(chi_squared, catagories-1)

    return p_val

def Count_Rows(file):
    rowcount = 0
    for row in open(file):
        rowcount+= 1
    return rowcount

def String_to_Arr(str):
    arr = str.split()
    return_arr = np.empty([len(arr)], dtype=int)
    for i in range(len(arr)):
        return_arr[i] = int(arr[i])
    return return_arr

number_draw= np.zeros([5,Count_Rows(csv_file_name_2015)-1], dtype=int)
power_ball = np.zeros([Count_Rows(csv_file_name_2015)-1], dtype=int)


f = open('Lottery_Powerball_Winning_Numbers__Beginning_2015.csv', 'r')
reader = csv.reader(f)
i = 0
for row in reader:
    if(i > 0):
        for k in range(5):
            number_draw[k][i-1] = String_to_Arr(row[1])[k]
    i+=1
print("sample size 2010: " + str(i))

f = open('Lottery_Powerball_Winning_Numbers__Beginning_2015.csv', 'r')
reader = csv.reader(f)
i = 0
for row in reader:
    if(i > 0):
        power_ball[i-1] = String_to_Arr(row[1])[5]
    i+=1

np.random.choice(a=12, size=12, replace=False)

print("sample size 2015: " + str(i))
#Powerball Tests

pvals = Total_1PropZTest(69,number_draw)


print(Chi_Squared_GOF_Test(power_ball,26))
Generate_Histogram(power_ball,'Powerball Draw Distribution since 09/16/2015',27)


#Draw Tests
probs1 = Simulate_Probabilities(69,5,885000,0)

print(sum(rel_entr([i/885 for i in Create_Observed_Distribution(69,number_draw[0])], probs1)))
# print(Chi_Squared_GOF_Test_With_Simulation(number_draw[0],69,probs1))
Generate_Histogram_With_Curve(number_draw[0],'Lowest Digit Draw Distribution since 09/16/2015',70,probs1)

probs2 = Simulate_Probabilities(69,5,885000,1)

print(sum(rel_entr([i/885 for i in Create_Observed_Distribution(69,number_draw[1])], probs2)))
# print(Chi_Squared_GOF_Test_With_Simulation(number_draw[1],69,probs2))
Generate_Histogram_With_Curve(number_draw[1],'Second Lowest Digit Draw Distribution since 09/16/2015',70,probs2)

probs3 = Simulate_Probabilities(69,5,885000,2)

print(sum(rel_entr([i/885 for i in Create_Observed_Distribution(69,number_draw[2])], probs3)))
# print(Chi_Squared_GOF_Test_With_Simulation(number_draw[2],69,probs3))
Generate_Histogram_With_Curve(number_draw[2],'Middle Digit Draw Distribution since 09/16/2015',70,probs3)

probs4 = Simulate_Probabilities(69,5,885000,3)

print(sum(rel_entr([i/885 for i in Create_Observed_Distribution(69,number_draw[3])], probs4)))
# print(Chi_Squared_GOF_Test_With_Simulation(number_draw[3],69,probs4))
Generate_Histogram_With_Curve(number_draw[3],'Second Highest Digit Draw Distribution since 09/16/2015',70,probs4)

probs5 = Simulate_Probabilities(69,5,885000,4)

print(sum(rel_entr([i/885 for i in Create_Observed_Distribution(69,number_draw[4])], probs5)))
# print(Chi_Squared_GOF_Test_With_Simulation(number_draw[4],69,probs5))
Generate_Histogram_With_Curve(number_draw[4],'Highest Digit Draw Distribution since 09/16/2015',70,probs5)
