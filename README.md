The project is a framework that applies outlier algorithms on integer datasets. 
The current work was constructed to check data extracted from contiki OS cooja experiments. More specifically, nodes communicating in RPL exchange ICMP data regualarly. If there is an intruder in the network, those new incoming data will be outliers to the ordinary data series. 

PARAMETERS:
The project contains an .ini file that needs to be configured (look into folder config_files for the *.ini. Change the path for the data file accordingly (full_file_path=...).

# Dixon Q-Test 
Dixon's Q-test can easilly point out the outlier. Since it is light and easy to implement (it needs only a division), it is ideal to be running in the IoT part (Hybrid placement).
Read more [here.](https://www.statisticshowto.com/dixons-q-test/)
## Arguments:
### 1. INPUT
data = An ordered or unordered list of data points (int or float).
left = Q-test of minimum value in the ordered list if True.
right = Q-test of maximum value in the ordered list if True.
q_dict = A dictionary of Q-values for a given confidence level, where the dict. keys are sample sizes N, and the associated values are the corresponding critical Q values. E.g., {3: 0.97, 4: 0.829, 5: 0.71, 6: 0.625, ...} (Tables are provided, look [here](https://chem.libretexts.org/Bookshelves/Ancillary_Materials/Reference/Reference_Tables/Analytic_References/Appendix_06%3A_Critical_Values_for_Dixon%E2%80%99s_Q-Test) for details). 

### 2. Search window (Memory)
Also you can set the search "window". Dixon-Q test can have a memory (how many passed values to consider. The smallest is three (3) and can become bigger. Feel free to experiment with values until 15.
[DIXON_Q_TEST_SUBSET_VARIABLES]
static_n = 3
static_n_maximum = 11
### 3. DATA FORMAT
Input is a csv file, with four columns: NODE: string TIME: integer DATA TYPE: string VALUES: integer. The program will try to identify the delimiter, if you face problems, place a ";" as a delimeter. DON'T FORGET the first row-titles:
NODE;TIME;DATA TYPE;VALUES
The important thing is the NODE and the VALUES columns.
4. Output is a csv file, with seven columns: outlier_no: integer : number of outliers subset_size: integer: the size of the list that contains the numbers that the outlier was found subset: string: the list of numbers NODE: reflects to input file DATA TYPE: reflects to input file index_first_element: integer: within the in memory grouped, subset's starting position index_last_element: integer: within the in memory grouped, subset's finishing position

## Pseudocode Details
/* Denominator = (x[n]-x[1] */
/* Lower Outlier: Q = (x[2]-x[1])/(x[n]-x[1]) */					
/* Higher Outlier: Q = (x[n]-x[n-1])/(x[n]-x[1]) */

# Chebyshev's Inequality
Chebyshev's Inequality is more complicated (and usually more accureate) than the above Dixon-Q. That is why it is run in the controller of an IoT network, since it needs to calculate among others the mean and the std.deviation of the samples. For the purposes of this project, we use the same input (integer data samples), trying to find the outliers with sample size of 7+1 (the data sample has already seven samples all considered normal, and the incoming value is tested as an outlier). For more information, look [here](https://ieeexplore.ieee.org/document/1559688).
### Sensitivity parameters
p1 was set to 0.10 and p2 was set to 0.01. Feel free to change them at will. Again, read [here](https://ieeexplore.ieee.org/document/1559688) for details.


### date: 14-8-2020
### author: Kyriakos Vougioukas
### email: vougioukaskyriakos@live.com
### github username: boygioykaskyriakos

