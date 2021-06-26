# Colculations for each infinite round of the players

|                     | Kooperation (C) | Defektion (D) |
| ------------------- | --------------- | ------------- |
| **Kooperation (C)** | R,R             | S,T           |
| **Defektion (D)**   | T,S             | P,P           |

With assumption: $T > R > P > S$
Shadow of the future: $0 <\omega < 1$

The reward is therefore: $u(s_0,s_1) = \sum_{i=0}^\infty \omega^i \cdot r(s_{0_i}, s_{1_i}) = u_0 + \omega u_1 + \omega^2 u_2 + \omega^3 u_3 + ... $ (where $u_i = r(s_{0_i}, s_{1_i})$)
By the geometric series we have: $1+\omega + \omega^2 + \omega ^3 + ... = \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}$

### Observation 1

If we have the reward $u(s_0,s_1)$ for two strategies $s_0$ and $s_1$, we can easily calculate the reward of the game: $u(s_1, s_0)$ by swapping all S's and T's in the formula. This holds beacuse when in a round $s_0$ gets the reward of $S$, we know that $s_0$ must have played C and $s_1$ must have played D. Therefore we know, that $s_1$ would get the reward of $T$ when he plays against $s_0$ in that exact round. The same reasoning works when $s_0$ gets the reward of $T$. Therefore by swapping $S$ and $T$ in the formula we get the reward of the other player in this game.

### Observation 2

If two friendly strategies meet, they will always get the same payout of $u(FRIENDLY_1, FRIENDLY_2) =  \frac{1}{1-\omega} \cdot  R$. This is the case because a friendly strategy never starts to defect if the other strategy doesn't defect. Therefore if two friendly strategies play against each other, nobody will ever play D. This results in the reward of: $u(FRIENDLY_1, FRIENDLY_2) = R + \omega R+ \omega^2R+...= R \cdot  \sum_{i=0}^{\infin} \omega^i=  \frac{1}{1-\omega} \cdot  R$ for both players.

## RANDOM with parameter p (for cooperation)

##### vs. RANDOM with param $p_2$

$u(RAND_{p_1}, RAND_{p_2}) = p_1 \cdot  p_2 \cdot  R + p_1 \cdot  (1-p_2)\cdot S + (1-p_1)\cdot p_2 \cdot  T + (1-p_1)(1-p_2)\cdot P + \omega \cdot  u(RAND_{p_1}, RAND_{p_2}) = \frac{p_1 \cdot  p_2 \cdot  R + p_1 \cdot  (1-p_2)\cdot S + (1-p_1)\cdot p_2 \cdot  T + (1-p_1)(1-p_2)\cdot P}{1-\omega}$

##### vs. AD

$u(RAND_{p}, AD) = p \cdot  S +  (1-p)\cdot P + \omega \cdot  u(RAND_{p},AD) = \frac{p \cdot  S +  (1-p)\cdot P}{1-\omega}$

##### vs. AC

$u(RAND_{p}, AC) = p \cdot  R +  (1-p)\cdot T + \omega \cdot  u(RAND_{p},AC) = \frac{p \cdot  R +  (1-p)\cdot T}{1-\omega}$

##### vs. GT

$u(RAND_{p}, GT) = p \cdot  (R + \omega \cdot  u(RAND_{p}, GT)) +  (1-p)\cdot (T + \omega \cdot  u(RAND_{p},AD)) = p \cdot  \omega \cdot  u(RAND_{p}, GT) + p \cdot  R + (1-p) \cdot  (T + \omega \cdot  \frac{p \cdot  S +  (1-p)\cdot P}{1-\omega})$

$u(RAND_{p}, GT) = \frac {p \cdot  R + (1-p) \cdot  (T + \omega \cdot  \frac{p \cdot  S +  (1-p)\cdot P}{1-\omega})}{1-p\cdot \omega}$

##### vs. TFT

Results from: $u(TFT, RAND_p)$ by swapping $S$ and $T$

$u(RAND_p, TFT) = \frac{p^2\cdot \omega\cdot (T+S-R-P)+p\cdot (2\omega P + R(\omega-1)-2\omega T+T - \omega S)-\omega P+T(\omega-1)}{\omega-1}$

##### vs. TFTD

Results from: $u(TFTD, RAND_p)$ by swapping $S$ and $T$
Note: $u(TFTD, RAND_p)$ is part of the calculation of $u(TFT, RAND_p)$
$u(RAND_p, TFTD) = \frac {\omega p^3 + \omega p^2(R - S - T - 1) + \omega  p T + p(S+1-p)}{1-\omega}$

##### vs. TF2T

$u_1 := u(RAND_p, TF2T) = p(R + \omega \cdot  u(RAND_p, TF2T))+(1-p)(T + \omega \cdot  u(RAND_p, TF2T_1))$
$u_2 := u(RAND_p, TF2T_1) = p(R + \omega \cdot  u(RAND_p, TF2T))+(1-p)(T + \omega \cdot  u(RAND_p, TF2T_2))$
$u_3 := u(RAND_p, TF2T_2) = p(S + \omega \cdot  u(RAND_p, TF2T))+(1-p)(P + \omega \cdot  u(RAND_p, TF2T_2))$

$u_3 = \frac{pS+ωp\cdot u_1+p-p^2}{1-ω+ωp}$
$\implies u_2 = p(R + \omega \cdot  u_1)+(1-p)(T + \omega \cdot  \frac{pS+ωp\cdot u_1+p-p^2}{1-ω+ωp}) = p\left(R+ωu_1\right)+\left(1-p\right)\left(T+\frac{ω\left(pS+ωpu_1+p-p^2\right)}{1-ω+ωp}\right)$
$\implies u_1 = p(R + \omega \cdot  u_1)+(1-p)(T + \omega \cdot  (p\left(R+ωu_1\right)+\left(1-p\right)\left(T+\frac{ω\left(pS+ωpu_1+p-p^2\right)}{1-ω+ωp}\right))) = \frac{-ω^2p^4+3ω^2p^3+ω^2p^3T-ω^2p^3R+ω^2p^3S-3ω^2p^2-3ω^2p^2T+2ω^2p^2R-2ω^2p^2S+ω^2p+3ω^2pT-pT+pR-ω^2pR+ω^2pS+T-ω^2T}{-ω+1} = \frac{-ω^2p^4+ω^2p^3\cdot (3+T-R+S) + ω^2p^2\cdot (-3-3T+2R-2S)+ω^2p(1+3T)+p(-T+R)+ω^2p\cdot (-R+S)+T-ω^2T}{1-ω}$

## AD

##### vs. RANDOM with param p

Results from: $u(RAND_p, AD)$ by swapping $S$ and $T$

$u(AD, RAND_{p}) = p \cdot  T +  (1-p)\cdot P + \omega \cdot  u(AD, RAND_{p}) = \frac{p \cdot  T +  (1-p)\cdot P}{1-\omega}$

##### vs. AD

$u(AD, AD) = P + \omega P+ \omega^2P+... = \frac{1}{1-\omega} \cdot  P$

##### vs. AC

$u(AD, AC) = T + \omega T+ \omega^2T+... = \frac{1}{1-\omega} \cdot  T$

##### vs. GT

$u(AD, GT) = T + \omega \cdot  u(AD, AD) = T + \frac \omega {1-\omega} P$

##### vs. TFT

Same behaviour as GT
$u(AD, TFT) = T + \omega \cdot  u(AD, AD) = T + \frac \omega {1-\omega} P$

##### vs. TFTD

$u(AD, TFTD) = P + \omega \cdot  u(AD, AD) = \frac 1 {1-\omega} P$

##### vs. TF2T

$u(AD, TF2T) = T + \omega \cdot  T + \omega ^ 2 \cdot  u(AD, AD) = T + \omega T + \frac {\omega^2} {1-\omega} P$

## AC

##### vs. RANDOM with param p

Results from: $u(RAND_p, AC)$ by swapping $S$ and $T$

$u(AC, RAND_{p}) = p \cdot  R +  (1-p)\cdot S + \omega \cdot  u(AC, RAND_{p}) = \frac{p \cdot  R +  (1-p)\cdot S}{1-\omega}$

##### vs. AD

$u(AC, AD) = S + \omega S+ \omega^2S+... = \frac{1}{1-\omega} \cdot  S$

##### vs. AC

$u(AC, AC) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. GT

$u(AC, GT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. TFT

$u(AC, TFT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. TFTD

$u(AC, TFTD) = S + \frac \omega {1-\omega} \cdot  R$

##### vs. TF2T

$u(AC, TF2T) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

## GT

##### vs. RANDOM with param p

Results from: $u(RAND_p, GT)$ by swapping $S$ and $T$

$u(GT, RAND_{p}) = \frac {p \cdot  R + (1-p) \cdot  (S + \omega \cdot  \frac{p \cdot  T +  (1-p)\cdot P}{1-\omega})}{1-p\cdot \omega}$

##### vs. AD

$u(GT, AD) = S + \omega \cdot  u(AD, AD) = S + \frac \omega {1-\omega} P$

##### vs. AC

$u(GT, AC) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. GT

$u(GT, GT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. TFT

$u(GT, TFT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. TFTD

$u(GT, TFTD) = S + \omega \cdot  T + \frac {\omega^2} {1-\omega} \cdot  P$

##### vs. TF2T

$u(GT, TF2T) = R + \omega R + \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

## TFT

##### vs. RANDOM with param p

$u_1 := u(TFT, RAND_p) = p \cdot  (R + \omega \cdot  u(TFT, RAND_p)) + (1-p)\cdot (S + \omega \cdot  u(TFTD, RAND_p))$ with:
$u_2 := u(TFTD, RAND_p) = p \cdot  (T + \omega \cdot  u(TFT, RAND_p)) + (1-p)\cdot (P + \omega \cdot  u(TFTD, RAND_p))$

$u_2 = p \cdot  (T + \omega \cdot  u_1) + (1-p)\cdot (P + \omega \cdot  u_2)$
$\Leftrightarrow u_2 = p \cdot  (T + \omega \cdot  u_1) + (1-p) \cdot  P + (1-p)\cdot  \omega \cdot  u_2$
$\Leftrightarrow u_2 - (1-p)\cdot  \omega \cdot  u_2 = p \cdot  (T + \omega \cdot  u_1) +  (1-p) \cdot  P$
$\Leftrightarrow u_2(1-(1-p)\cdot  \omega) = p _ (T + \omega _ u\cdot 1) + (1-p) \cdot  P$
$\Leftrightarrow u_2 = \frac{p \cdot  (T + \omega \cdot  u_1) + (1-p) \cdot  P}{1-(1-p)\cdot  \omega} = \frac{p \cdot  (T + \omega \cdot  u_1) + (1-p) \cdot  P}{1-(1-p)\cdot  \omega}$

$u_1 = p \cdot  (R + \omega \cdot  u_1) + (1-p)\cdot (S + \omega \cdot  u_2)$
$\Leftrightarrow u_1 = p \cdot  \omega \cdot  u_1 + p\cdot R + (1-p)\cdot (S + \omega \cdot  u_2)$
$\Leftrightarrow u_1(1-p\cdot \omega) = p\cdot R + (1-p)\cdot (S + \omega \cdot  u_2)$
$\Leftrightarrow u_1 =\frac{ p\cdot R + (1-p)\cdot (S + \omega \cdot  u_2)}{1-p\cdot \omega}$

$u_2 = \frac{p \cdot  (T + \omega \cdot  \frac{ p\cdot R + (1-p)\cdot (S + \omega \cdot  u_2)}{1-p\cdot \omega}) + (1-p) \cdot  P}{1-(1-p)\cdot  \omega}$
$u(TFTD, RAND_p) = \frac {\omega p^3 + \omega p^2(R - T - S - 1) + \omega  p S + p(T+1-p)}{1-\omega}$

$u_1 = \frac{ p\cdot R + (1-p)\cdot (S + \omega \cdot  \frac{p \cdot  (T + \omega \cdot  u_1) + (1-p) \cdot  P}{1-(1-p)\cdot  \omega})}{1-p\cdot \omega}$
$u(TFT, RAND_p) = \frac {\omega p^3 + \omega p^2(R - T - S - 2) + \omega  p (1+T-R+2S)+p(R-S) + S - \omega S}{1-\omega}$

##### vs. AD

$u(TFT, AD) = S + \omega P+ \omega^2P+... = S + \omega P \cdot  \sum_{i=0}^{\infin} \omega^i = S + \frac{\omega}{1-\omega}P$

##### vs. AC

$u(TFT, AC) = R + \omega R+ \omega^2R+... = R \cdot  \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. GT

$u(TFT, GT) = R + \omega R+ \omega^2R+... = R \cdot  \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. TFT

$u(TFT, TFT) = R + \omega R+ \omega^2R+... = R \cdot  \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. TFTD

$u(TFT, TFTD) = S + \omega  T + \omega^2  S + \omega^3  T +... = \sum_{i=0}^{\infin}\omega^{2i}S + \omega\sum_{i=0}^{\infin}\omega^{2i}T$
$u(TFT, TFTD) = \frac 1 {1-\omega^2}S + \frac \omega {1-\omega^2}T$

##### vs. TF2T

$u(TFT, TF2T) = R + \omega R+ \omega^2R+... = R \cdot  \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

## TFTD

##### vs. RANDOM with param p

Results from: $u(RAND_p, TFTD)$ by swapping $S$ and $T$
Note: see $u(TFT, RAND_p)$ for the calculation
$u(TFTD, RAND_p) = \frac {\omega p^3 + \omega p^2(R - T - S - 1) + \omega  p S + p(T+1-p)}{1-\omega}$

##### vs. AD

$u(TFTD, AD) = u(AD, AD) = \frac 1 {1-\omega} \cdot  P$

##### vs. AC

$u(TFTD, AC) = T + \omega \cdot  u(AC, AC) = T + \frac {\omega}{1-\omega} \cdot  R$

##### vs. GT

$u(TFTD, GT) = T + \omega \cdot  S + \omega^2 \cdot  u(AD, AD) = T + \omega S+ \frac {\omega^2}{1-\omega} \cdot  R$

##### vs. TFT

see TFT:
$u(TFTD, TFT) = \frac 1 {1-\omega^2}T + \frac \omega {1-\omega^2}S$

##### vs. TFTD

$u(TFTD, TFTD) = u(AD, AD) = \frac{1}{1-\omega} \cdot  P$

##### vs. TF2T

$u(TFTD, TF2T) = T + \omega \cdot  u(AC, AC) = T + \frac \omega {1-\omega} \cdot  R$

## TF2T

##### vs. RANDOM with param p

Results from: $u(RAND_p, TF2T)$ by swapping $S$ and $T$

$u(TF2T, RAND_p)=\frac{-ω^2p^4+3ω^2p^3+ω^2p^3S-ω^2p^3R+ω^2p^3T-3ω^2p^2-3ω^2p^2S+2ω^2p^2R-2ω^2p^2T+ω^2p+3ω^2pS-pS+pR-ω^2pR+ω^2pT+S-ω^2S}{-ω+1}
=\frac{-ω^2p^4+ω^2p^3\cdot (3+S-R+T) + ω^2p^2\cdot (-3-3S+2R-2T)+ω^2p(1+3S)+p(-S+R)+ω^2p\cdot (-R+T)+S-ω^2S}{1-ω}$

##### vs. AD

$u(TF2T, AD) = S + \omega \cdot  S + \omega ^ 2 \cdot  u(AD, AD) = S + \omega S + \frac {\omega^2} {1-\omega} P$

##### vs. AC

$u(TF2T, AC) = S + \omega \cdot  S + \omega ^ 2 \cdot  u(AD, AD) = S + \omega S + \frac {\omega^2} {1-\omega} P$

##### vs. GT

$u(TF2T, GT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. TFT

$u(TF2T, TFT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$

##### vs. TFTD

$u(TF2T, TFTD) = S + \frac \omega {1-\omega} \cdot  R$

##### vs. TF2T

$u(TF2T, TF2T) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} \cdot  R$
