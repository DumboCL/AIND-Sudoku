# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked Twins means those two numbers are locked in those two boxes, so other boxes in the same unit can apply a conclusion that they should not include these two numbers.
Step 1: Find all the remained boxes contain two possible digits.
     2: iterate each box, in its belonging unit (at least 3, 4 if concerning diagonal), if there is total two equals to that two possible digits, then these two boxes are naked twins.
     3: For the rest box in the certain unit, replace those two digits with '' if they contain either digit.
     4: Achieve the purpose: reduce the possible digits
     
# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Add diagonal boxes into initial unitlist to join the constraint. Treat it as normal unit, let computer do the rest.

## Issues Solved

###First Solution takes 5806.075s to pass the 3 tests. Awful!
Solution: Add diagonal units into original unitlist, join the solving strategy at first place

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.