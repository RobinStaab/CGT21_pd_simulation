### Extension: Infinitely repeated Prisoners Dilemma with migration and imitation

In the real world, you can never be sure if you see a person exactly five times or not. There can always be a unexpected meeting somewhere at some time in the future. So dealing with a finite repetition is an simplification of the real world. This also holds for the strategies in the Prisoners Dilemma as seen in this paper. If one knows that there are exactly five rounds to be played, defecting at the fifth round is a dominant strategy. The strategies discussed in this paper are not aware of how many rounds they are playing. But more sophisticated strategies could exploit that fact and therefore have a clear advantage against the others. Another disadvantage of only finitely many repetitions is, that a strategy could start to build up trust at the beginning and therefore have a bad reward at the start, but after investing in that trust be successfull in the end of the game. Such strategies could just be ranked as bad, since they never reach a state where their investment made profit because the finite game is already finished.

##### Why Infinitely repeated Prisoners Dilemma?

The finite prisoners dilemma is clearly an abstraction of the real interactions in the world, but why should an infinitely repeated game solve the problem? People clearly don't interact infinitely often in the real world. It's because the shadow of the future in these games. After each round of playing the Prisoners Dilemma, there is a chance $0 < \omega < 1$ to go on playing another round of the dilemma. This $\omega$ corresponds to the probability that two people which made business in the real world meet each other at some time in the future to make business again. It's therefore possible to play infinitely many times against the same opponent. Clearly this is also an abstraction, since this $\omega$ would be specific to each person and also depends on how good the last interaction turned out. Here we assume that $\omega$ is fixed and the same for every strategy and does not depend on the previous outcome.

##### Calculation of success

We calculate the success of the strategy as the expected reward against another strategy. Let $u:S\times S\rightarrow\reals$ be the reward function which maps a pair of strategies $(s_1, s_2)\in S^2$ to a real number corresponding to the expected reward of $s_1$ against the strategy $s_2$. Clearly $u$ depends on the values of $T$, $R$, $P$, and $S$. In this special case we assume that: $T > R > P > S$ and $2 \cdot R > T + S$ to have some reasonable results. Because simulating infinitely many repetitions for battle in the simulation is impossible, we calculated the expected reward of each strategy against each other strategy in advance (See [apendix A]()). We only focus on the seven players: $RANDOM$, $AD$, $AC$, $GT$, $TFT$, $TF2T$ for this section.

##### Experiment set-up

We choose 50 players of each strategy in our simulation on a $20\times 20$ grid. Each strategy is placed at a random location on the grid to start. We use the payoff matrix:

|               | Cooperate | Defect |
| ------------- | --------- | ------ |
| **Cooperate** | 20,20     | 5,20   |
| **Defect**    | 20,5      | 10,10  |

with the parameters:

- Window play size: 1
- Migration range: 3
- Imitation probability: 0.2
- Migration probability 0.1
- Random Seed: 12345

##### Results

TODO

##### Interpretation

TODO

##### Discussion

TODO
