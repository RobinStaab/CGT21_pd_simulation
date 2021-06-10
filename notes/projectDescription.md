# Imitation and Migration with repeated prisoners dilemma

Our group creates a similar simulation of the Imitation and Migration experiment as seen in the lecture.
We take this experiment a step further and look at the conversions from repeated(infinite) prisoners dilemma, instead of only one time meetings. In the real would, people meet each other multiple times and decide if they cooperate or defect, according to some long term strategy.
The goal is to let different strategies (like: Tit-for-Tat, Random, Always C, Always D, Tit-for-two-Tat, Joss, Grimm Trigger) battle for the superiority of the field. Just like in the lecture, to see if Tit-for-Tat would come out as the superior strategy when facing other competitors.
The simulation would be on a (interactive) website to play with the rewards, and punishments.

## Possible Ideas

### Ground Idea

- infinite repetitions
- Multiple strategies starting at random -> simulate like in lecture
- Errors ?
  [https://www.frontiersin.org/articles/10.3389/frobt.2018.00102/full]
  [https://www.pnas.org/content/109/26/10409]

### Optional prisoner's dilemma

[https://en.wikipedia.org/wiki/Optional_prisoner%27s_dilemma]

## Spieler

- Random
- Immer D
- Immer C
- Friedman (Grimm Trigger)
- TFT
- Joss
- TF2T

## Themen für Theoriepart

- Freudliche Strategie: Starten nie mit D wenn anderer nicht macht: bsp TFT, TF2T, Grimm Trigger, Immer C
- Evolutionär stabile Strategie (ESS):
  - Strategie I ist ESS, wenn für jede andere Strategie J:
  - $E(I,I) > E(J,I)$ oder
  - $E(I,I) = E(J,I) \land E(I,J) > E(J,J)$
- Frequenzabhängige Fitness: Der Erfolg einer Strategie ist abhängig von der Häufigkeit anderer Strategien
- Exploitable: Eine Strategie ist ausbeutbar oder nicht
- Nash-Equilibrium
- Subgame perfect equilibrium
- Dominant strategies
- Prisoners Dilemma (and where they can be applied)
- Schatten der Zukunft (Reward in Zukunft weniger wert -> konvergenz für unendliches Spiel)

### Bsp Gefangenendilemma (von Experimentelle Spieltheorie)

Diamanten im wert von 2Mio gestohlen.
Käufer kauft sie für 1Mio.
Sollten sie Kieselsteine hineinlegen anstatt Diamanten
Sellte Käufer Papier hineinlegen anstatt 1Mio

T = Gewinn von Diamanten bzw 1Mio ohne Gegenleistung
R = Gewinn durch Tausch
P = gegenseitiger Betrug
S = Verlust von Diamanten bzw 1Mio

T > R > P > S

|                     | Kooperation (C) | Defektion (D) |
| ------------------- | --------------- | ------------- |
| **Kooperation (C)** | R,R             | S,T           |
| **Defektion (D)**   | T,S             | P,P           |

1. D ist eine **dominante** Strategie
2. D ist eine **Maximin** Strategie
3. D ist eine **Nash-Gleichgewichtsstrategie**
   $s^+ = (s_1^+,s_2^+) = (D, D)$
4. $u(s^+) = (P,P)$ ist nicht **Pareto optimal** (Gleichgewicht ineffizient) Pareto-Optimum: $s_p = (C, C)$ mit $u(s_p) = (R,R)$

**Wiederholtes Spiel: Ist entstehung einer Ordnung möglich ohne exogene Eingriffe?**

Annahmen:

1. Eigennützige Individuel in einer "anarchischen Situation"
2. Standard-Spieltheorie

3. Basisspiel:
   $T > R > P > S$
   $ R > \frac{T+S}{2}$ (CDCDCDCD ausschliessen)

4. Unendlcih viele Iterationen (Nicht bekannt welche letzte Runde)
