# Players of the Simulation

$T > R > P > S$
| | Cooperation (C) | Defection (D) |
| ------------------- | --------------- | ------------- |
| **Cooperation (C)** | R,R | S,T |
| **Defection (D)** | T,S | P,P |

Let S be the set of all different strategies.
We use a evaluation function $u: S \times S \rightarrow \mathbb{R}$ for the reward of the first strategy in the infinitly repeated prisoners dilemma.

## Random

This strategy chooses at random between cooperation with a probability of $p$ or defection with a probability of $1-p$

This strategy is used as a groundstrategy to test other strategies.

## Always defect (AD)

As the name suggests, this strategy always chooses defection.

##### Advantages

- Best strategy against "Always cooperate", "Random"

##### Disadvantages

- u(AD, AD) is far from optimal since it always results in P every round.

## Always cooperate (AC)

This strategy always chooses cooperation, no matter how the opponent is playing.

##### Advantages

- u(AC, AC) is pareto optimal, a nash-equilibrium, and a subgame perfect equilibrium
- nice strategy

##### Disadvantages

- It can easily be exploited by "Always D"

## Grimm Trigger (GT)

Grimm Trigger does always cooperate until the opponent had defected once. Once the opponent chosed defection, Grimm Trigger chooses defection for the rest of the game.

##### Advantages

- nice strategy
- nonexploitability

##### Disadvantages

- non-forgiving
- If the opponent chooses defection by accident once in the game, Grimm Trigger will never forgive him anymore

## Tit-for-Tat (TFT)

Tit for Tat always plays what the other player has played previously. It always starts with cooperation(C) in the first round.

##### Advantages

- nice strategy
- nonexploitability
- forgiving
- no compley rules

##### Disadvantages

- If two TFT players play against each other, but one of them chooses defection(D) by accident ("wrong button"). This leads to interchanged cooperation and defection for the rest of the game. Therefor Tit-for-two-Tat was proposed to prevent such behaviour.
- TFT is not the best awnser to RANDOM
- u(TFT, TFT) is a Nash-Equilibrium but no Subgame perfect equilibrium. For a situation (D,C): u(TF2T,TFT) scores more points than u(TFT, TFT). (Only if $R > \frac{T+S}{2}$)

## Suspicious Tit-for-Tat (DTFT)

Suspicious Tit-for-Tat is exactly like Tit-for-Tat but it starts with defaction rather than cooperation on the first turn.

##### Advantages

- Cannot be exploited at the first turn

##### Disadvantages

- Most other strategies start to also defect, if you start with defection
- Leads to interchanged cooperation and defection against Tit-for-Tat from the beginning on (which is not optimal in most cases)

## Tit-for-two-Tat (TF2T)

Tit for two Tat is similar to Tit-for-Tat but is more forgiving. TF2T only defects of the opponent chose defection for two consecutive rounds.

##### Advantages

- Solution to the "wrong button" problem of Tit for Tat
- More forgiving than TFT

##### Disadvantages

- TF2T needs more time to realize, that it is exploited than TFT
- It can be exploited by interchanged cooperation and defection
