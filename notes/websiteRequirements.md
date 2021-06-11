# Website Requirements

## Needs (At least)

- Simulation setup is working, starting with players choosing a random Strategy out of the 7 (with probability 1/7 each)
- Step by Step generation with Imitation of the best Strategy of the 8 fields around each player and Migration with a (fixed) constant. A player Migrates when it gets more reward at a different location than at the current.
- A graph showing each strategy with their share over the population (in % or in absolute)
- See the simulation on the screen

## Would be Good

- Control the speed of the Simulation steps
- A slider for each Strategy to select the start share of the populaition for starting. (Probably this would be easier to implement by an absolute count instad of a share of the whole population. So after each Simulation is a slider from 0 to around 200 or so. If you change the slider and start the simulation again there should be exactly this number of players with this strategy all around the world)
- A slider for each of the T, R, P, S values to change the reward (not needed to be bounded e.g T could even be lower than R)
- Each Strategy should have its distinct color to see how they spread on the screen
- Export some gathered data from the Simulation to create the paper
- Have some good looking website so we could include pictures in the paper

## Nice to Have (If Time)

- Add an additional slider [0%, 10%] for random changes of strategies in the simulation (could have some interesting effects on the simulation)
- A start / pause button to start the simulation (it should be possible to make changes during the simulation if wanted)
- A slider to change the p value (for cooperation) of $RAND_p$ (even during the simulation)
- Can interact with the simulation (e.g give a specific player / pixel a strategy for the next round)
- More Graphics about migration and imitation
- For the given Values of T, R, P, S show a graphic (a histogram at best) of which strategy has which reward for playing against which other strategy (according to the Formulas)
- Perhaps include randomness with seeds so that you could go back in a simulation to look at important points / regenerate the same simulation again
