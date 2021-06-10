# Colculations for each infinite round of the players

T > R > P > S

|                     | Kooperation (C) | Defektion (D) |
| ------------------- | --------------- | ------------- |
| **Kooperation (C)** | R,R             | S,T           |
| **Defektion (D)**   | T,S             | P,P           |

Shadow of the future: $0 <\omega < 1$
reward is therefore: $u = u_0 + \omega u_1 + \omega^2 u_2 + \omega^3 u_3 + ...$

By the geometric series we have: $1+\omega + \omega^2 + \omega ^3 + ... = \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}$

## RANDOM

##### vs. RANDOM with param p

$u(RAND_{p_1}, RAND_{p_2}) = p_1 * p_2 * R + p_1 * (1-p_2)*S + (1-p_1)*p_2 * T + (1-p_1)(1-p_2)*P + \omega * u(RAND_{p_1}, RAND_{p_2}) = \frac{p_1 * p_2 * R + p_1 * (1-p_2)*S + (1-p_1)*p_2 * T + (1-p_1)(1-p_2)*P}{1-\omega}$

##### vs. AD

$u(RAND_{p}, AD) = p * S +  (1-p)*P + \omega * u(RAND_{p},AD) = \frac{p * S +  (1-p)*P}{1-\omega}$

##### vs. AC

$u(RAND_{p}, AC) = p * R +  (1-p)*T + \omega * u(RAND_{p},AC) = \frac{p * R +  (1-p)*T}{1-\omega}$

##### vs. GT

$u(RAND_{p}, GT) = p * (R + \omega * u(RAND_{p}, GT)) +  (1-p)*(T + \omega * u(RAND_{p},AD)) = p * \omega * u(RAND_{p}, GT) + p * R + (1-p) * (T + \omega * \frac{p * S +  (1-p)*P}{1-\omega})$

$u(RAND_{p}, GT) = \frac {p * R + (1-p) * (T + \omega * \frac{p * S +  (1-p)*P}{1-\omega})}{1-p*\omega}$

##### vs. TFT

same as $u(TFT, RAND_p)$ but with: S and T swaped

$u(TFT, RAND_p) = \frac{p^2*\omega*(T+S-R-P)+p*(2\omega P + R(\omega-1)-2\omega T+T - \omega S)-\omega P+T(\omega-1)}{\omega-1}$

##### vs. JOSS with param p for defection

TODO

##### vs. TF2T

TODO

## AD

##### vs. RANDOM with param p

Same as $u(RAND_p, AD)$ but with S -> T

$u(AD, RAND_{p}) = p * T +  (1-p)*P + \omega * u(RAND_{p},AD) = \frac{p * T +  (1-p)*P}{1-\omega}$

##### vs. AD

$u(AD, AD) = P + \omega P+ \omega^2P+... = \frac{1}{1-\omega} * P$

##### vs. AC

$u(AD, AC) = T + \omega T+ \omega^2T+... = \frac{1}{1-\omega} * T$

##### vs. GT

$u(AD, GT) = T + \omega * u(AD, AD) = T + \frac \omega {1-\omega} P$

##### vs. TFT

same as GT:
$u(AD, TFT) = T + \omega * u(AD, AD) = T + \frac \omega {1-\omega} P$

##### vs. JOSS with param p for defection

$u(AD, JOSS_p) = p*T + (1-p)*P + \omega * u(AD, AD) = p*T + (1-p)*P + \frac \omega {1-\omega} P$

##### vs. TF2T

$u(AD, TF2T) = T + \omega * T + \omega ^ 2 * u(AD, AD) = T + \omega T + \frac {\omega^2} {1-\omega} P$

## AC

##### vs. RANDOM with param p

Same as $u(RAND_p, AC)$ but with T -> S

$u(AC, RAND_{p}) = p * R +  (1-p)*S + \omega * u(AC, RAND_{p}) = \frac{p * R +  (1-p)*S}{1-\omega}$

##### vs. AD

$u(AC, AD) = S + \omega S+ \omega^2S+... = \frac{1}{1-\omega} * S$

##### vs. AC

$u(AC, AC) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. GT

$u(AC, GT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. TFT

$u(AC, TFT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. JOSS with param p for defection

$u(AC, JOSS_p) = (1-p) R + p * S + \omega u(AC, JOSS_p) = \frac {(1-p) R + p * S}{1-\omega}$

##### vs. TF2T

$u(AC, TF2T) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

## GT

##### vs. RANDOM with param p

wie $u(RAND_{p}, GT)$ aber mit T -> S, S -> T
$u(GT, RAND_{p}) = p * (R + \omega * u(GT, RAND_{p})) +  (1-p)*(S + \omega * u(AD, RAND_{p})) = p * \omega * u(GT, RAND_{p}) + p * R + (1-p) * (S + \omega * \frac{p * T +  (1-p)*P}{1-\omega})$

$u(GT, RAND_{p}) = \frac {p * R + (1-p) * (S + \omega * \frac{p * T +  (1-p)*P}{1-\omega})}{1-p*\omega}$

##### vs. AD

$u(GT, AD) = S + \omega * u(AD, AD) = S + \frac \omega {1-\omega} P$

##### vs. AC

$u(GT, AC) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. GT

$u(GT, GT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. TFT

$u(GT, AC) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. JOSS with param p for defection

$u(GT, JOSS_p) = (1-p)(R + \omega * u(GT, JOSS_p)) + p * (S + \omega * u(AD, JOSS_p))$
$u(GT, JOSS_p) = \frac {(1-p)*R + p * (S + \omega * (p*T + (1-p)*P + \frac \omega {1-\omega} P))}{1-(1-p)*\omega}$

##### vs. TF2T

$u(GT, AC) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

## TFT

##### vs. RANDOM with param p

Lets denote: $TFT_D$ as the strategy of TFT, but it starts with defection instead of cooperation

$u_1 := u(TFT, RAND_p) = p * (R + \omega * u(TFT, RAND_p)) + (1-p)*(S + \omega * u(TFT_D, RAND_p))$ with:
$u_2 := u(TFT_D, RAND_p) = p * (T + \omega * u(TFT, RAND_p)) + (1-p)*(P + \omega * u(TFT_D, RAND_p))$

$u_2 = p * (T + \omega * u_1) + (1-p)*(P + \omega * u_2)$
$\Leftrightarrow u_2 = p * (T + \omega * u_1) + (1-p) * P + (1-p)* \omega * u_2$
$\Leftrightarrow u_2 - (1-p)* \omega * u_2 = p * (T + \omega * u_1) +  (1-p) * P$
$\Leftrightarrow u_2(1-(1-p)* \omega) = p _ (T + \omega _ u*1) + (1-p) * P$
$\Leftrightarrow u_2 = \frac{p * (T + \omega * u_1) + (1-p) * P}{1-(1-p)* \omega} = \frac{p * (T + \omega * u_1) + (1-p) * P}{1-(1-p)* \omega}$

$u_1 = p * (R + \omega * u_1) + (1-p)*(S + \omega * u_2)$
$\Leftrightarrow u_1 = p * \omega * u_1 + p*T + (1-p)*(S + \omega * u_2)$
$\Leftrightarrow u_1(1-p*\omega) = p*T + (1-p)*(S + \omega * u_2)$
$\Leftrightarrow u_1 =\frac{ p*T + (1-p)*(S + \omega * u_2)}{1-p*\omega}$

$u(TFT, RAND_p) = \frac{ p*T + (1-p)*(S + \omega *\frac{p * (T + \omega * u(TFT, RAND_p) ) + (1-p) * P}{1-(1-p)* \omega})}{1-p*\omega} = \frac{p^2*\omega*(T+S-R-P)+p*(2\omega P + R(\omega-1)-2\omega S+S - \omega T)-\omega P+S(\omega-1)}{\omega-1}$

##### vs. AD

$u(TFT, AD) = S + \omega P+ \omega^2P+... = S + \omega P * \sum_{i=0}^{\infin} \omega^i = S + \frac{\omega}{1-\omega}P$

##### vs. AC

Since both strategies are nice, nobody starts with defection. Therefore when two nice strategies face off, the reward will always be:
$u(TFT, AC) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. GT

$u(TFT, GT) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. TFT

$u(TFT, TFT) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. JOSS with param p for defection

Lets denote: $JOSS_p^D$ as the strategy of $JOSS_p$, but it starts with defection instead of cooperation

$u(TFT, JOSS_p) = (1-p)(R+\omega*u(TFT, JOSS_p)) + p(S + \omega*u(TFT_D, JOSS_p))$
$u(TFT_D, JOSS_p) = (1-p)(T + \omega*u(TFT, JOSS_p^D)) + p(P + \omega*u(TFT_D, JOSS_p^D))$
$u(TFT, JOSS_p^D) = S + \omega * u(TFT_D, JOSS_p)$
$u(TFT_D, JOSS_p^D) = P + \omega * u(TFT_D, JOSS_p^D) = P + \omega P+ \omega^2P+... = \frac 1{1-\omega}*P$

$u(TFT_D, JOSS_p) = (1-p)(T + \omega*u(TFT, JOSS_p^D)) + \frac p {1-\omega} * P$

$u_1 = (1-p)(R+\omega*u_1) + p(S + \omega*u_2)$
$u_2 = (1-p)(T + \omega*u_3) + \frac p {1-\omega} * P$
$u_3 = S + \omega * u_2$

$u(TFT_D, JOSS_p) = \frac{(\omega-1)(\omega S + T) - p (P+(\omega - 1)(\omega S + T))}{(\omega-1)((p-1)\omega^2 + 1)}$
$u(TFT, JOSS_p) = \frac {(1-p)*R + p(S + \omega*\frac{(\omega-1)(\omega S + T) - p (P+(\omega - 1)(\omega S + T))}{(\omega-1)((p-1)\omega^2 + 1)})}{1-(1-p)*\omega}$

##### vs. TF2T

$u(TFT, TF2T) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

## Joss

##### vs. RANDOM with param p

TODO

##### vs. AD

See AD
$u(JOSS_p, AD) = p*S + (1-p)*P + \omega * u(AD, AD) = p*S + (1-p)*P + \frac \omega {1-\omega} P$

##### vs. AC

See AC
$u(JOSS_p, AC) = (1-p) R + p * T + \omega u(JOSS_p, AC) = \frac {(1-p) R + p * T}{1-\omega}$

##### vs. GT

$u(JOSS_p, GT) = \frac {(1-p)*R + p * (T + \omega * (p*S + (1-p)*P + \frac \omega {1-\omega} P))}{1-(1-p)*\omega}$

##### vs. TFT

see TFT:
$u(JOSS_p, TFT) = \frac {(1-p)*R + p(T + \omega*\frac{(\omega-1)(\omega T + S) - p (P+(\omega - 1)(\omega T + S))}{(\omega-1)((p-1)\omega^2 + 1)})}{1-(1-p)*\omega}$

##### vs. JOSS with param p for defection

TODO

##### vs. TF2T

TODO

## TF2T

##### vs. RANDOM with param p

TODO

##### vs. AD

$u(TF2T, AD) = S + \omega * S + \omega ^ 2 * u(AD, AD) = S + \omega S + \frac {\omega^2} {1-\omega} P$

##### vs. AC

TODO

##### vs. GT

TODO

##### vs. TFT

TODO

##### vs. JOSS with param p for defection

TODO

##### vs. TF2T

TODO
