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

##### vs. TFTD

see TFT + SWAP:
$u(TFTD, RAND_p) = \frac {\omega p^3 + \omega p^2(R - S - T - 1) + \omega  p T + p(S+1-p)}{1-\omega}$

##### vs. TF2T

$u_1 := u(RAND_p, TF2T) = p(R + \omega * u(RAND_p, TF2T))+(1-p)(T + \omega * u(RAND_p, TF2T_1))$
$u_2 := u(RAND_p, TF2T_1) = p(R + \omega * u(RAND_p, TF2T))+(1-p)(T + \omega * u(RAND_p, TF2T_2))$
$u_3 := u(RAND_p, TF2T_2) = p(S + \omega * u(RAND_p, TF2T))+(1-p)(P + \omega * u(RAND_p, TF2T_2))$

$u_3 = \frac{pS+ωp*u_1+p-p^2}{1-ω+ωp}$
$\implies u_2 = p(R + \omega * u_1)+(1-p)(T + \omega * \frac{pS+ωp*u_1+p-p^2}{1-ω+ωp}) = p\left(R+ωu_1\right)+\left(1-p\right)\left(T+\frac{ω\left(pS+ωpu_1+p-p^2\right)}{1-ω+ωp}\right)$
$\implies u_1 = p(R + \omega * u_1)+(1-p)(T + \omega * (p\left(R+ωu_1\right)+\left(1-p\right)\left(T+\frac{ω\left(pS+ωpu_1+p-p^2\right)}{1-ω+ωp}\right))) = \frac{-ω^2p^4+3ω^2p^3+ω^2p^3T-ω^2p^3R+ω^2p^3S-3ω^2p^2-3ω^2p^2T+2ω^2p^2R-2ω^2p^2S+ω^2p+3ω^2pT-pT+pR-ω^2pR+ω^2pS+T-ω^2T}{-ω+1}$

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

##### vs. TFTD

$u(AD, TFTD) = P + \omega * u(AD, AD) = \frac 1 {1-\omega} P$

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

##### vs. TFTD

$u(AC, TFTD) = S + \frac \omega {1-\omega} * R$

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

##### vs. TFTD

$u(GT, TFTD) = S + \omega * T + \frac {\omega^2} {1-\omega} * P$

##### vs. TF2T

$u(GT, AC) = R + \omega R + \omega^2R+... = \frac{1}{1-\omega} * R$

## TFT

##### vs. RANDOM with param p

$u_1 := u(TFT, RAND_p) = p * (R + \omega * u(TFT, RAND_p)) + (1-p)*(S + \omega * u(TFTD, RAND_p))$ with:
$u_2 := u(TFTD, RAND_p) = p * (T + \omega * u(TFT, RAND_p)) + (1-p)*(P + \omega * u(TFTD, RAND_p))$

$u_2 = p * (T + \omega * u_1) + (1-p)*(P + \omega * u_2)$
$\Leftrightarrow u_2 = p * (T + \omega * u_1) + (1-p) * P + (1-p)* \omega * u_2$
$\Leftrightarrow u_2 - (1-p)* \omega * u_2 = p * (T + \omega * u_1) +  (1-p) * P$
$\Leftrightarrow u_2(1-(1-p)* \omega) = p _ (T + \omega _ u*1) + (1-p) * P$
$\Leftrightarrow u_2 = \frac{p * (T + \omega * u_1) + (1-p) * P}{1-(1-p)* \omega} = \frac{p * (T + \omega * u_1) + (1-p) * P}{1-(1-p)* \omega}$

$u_1 = p * (R + \omega * u_1) + (1-p)*(S + \omega * u_2)$
$\Leftrightarrow u_1 = p * \omega * u_1 + p*R + (1-p)*(S + \omega * u_2)$
$\Leftrightarrow u_1(1-p*\omega) = p*R + (1-p)*(S + \omega * u_2)$
$\Leftrightarrow u_1 =\frac{ p*R + (1-p)*(S + \omega * u_2)}{1-p*\omega}$

$u_2 = \frac{p * (T + \omega * \frac{ p*R + (1-p)*(S + \omega * u_2)}{1-p*\omega}) + (1-p) * P}{1-(1-p)* \omega}$
$u(TFTD, RAND_p) = \frac {\omega p^3 + \omega p^2(R - T - S - 1) + \omega  p S + p(T+1-p)}{1-\omega}$

$u_1 = \frac{ p*R + (1-p)*(S + \omega * \frac{p * (T + \omega * u_1) + (1-p) * P}{1-(1-p)* \omega})}{1-p*\omega}$
$u(TFT, RAND_p) = \frac {\omega p^3 + \omega p^2(R - T - S - 2) + \omega  p (1+T-R+2S)+p(R-S) + S - \omega S}{1-\omega}$

##### vs. AD

$u(TFT, AD) = S + \omega P+ \omega^2P+... = S + \omega P * \sum_{i=0}^{\infin} \omega^i = S + \frac{\omega}{1-\omega}P$

##### vs. AC

Since both strategies are nice, nobody starts with defection. Therefore when two nice strategies face off, the reward will always be:
$u(TFT, AC) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. GT

$u(TFT, GT) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. TFT

$u(TFT, TFT) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

##### vs. TFTD

$u(TFT, TFTD) = S + \omega  T + \omega^2  S + \omega^3  T +... = \sum_{i=0}^{\infin}\omega^{2i}S + \omega\sum_{i=0}^{\infin}\omega^{2i}T$
$u(TFT, TFTD) = \frac 1 {1-\omega^2}S + \frac \omega {1-\omega^2}T$

##### vs. TF2T

$u(TFT, TF2T) = R + \omega R+ \omega^2R+... = R * \sum_{i=0}^{\infin} \omega^i = \frac 1{1-\omega}R$

## TFTD

##### vs. RANDOM with param p

See $u(TFT, RAND_p)$
$u(TFTD, RAND_p) = \frac {\omega p^3 + \omega p^2(R - T - S - 1) + \omega  p S + p(T+1-p)}{1-\omega}$

##### vs. AD

$u(TFTD, AD) = u(AD, AD) = \frac 1 {1-\omega} * P$

##### vs. AC

$u(TFTD, AC) = T + \omega * u(AC, AC) = T + \frac {\omega}{1-\omega} * R$

##### vs. GT

$u(TFTD, GT) = T + \omega * S + \omega^2 * u(AD, AD) = T + \omega S+ \frac {\omega^2}{1-\omega} * R$

##### vs. TFT

see TFT:
$u(TFTD, TFT) = \frac 1 {1-\omega^2}T + \frac \omega {1-\omega^2}S$

##### vs. TFTD

$u(TFTD, TFTD) = u(AD, AD) = \frac{1}{1-\omega} * P$

##### vs. TF2T

$u(TFTD, TF2T) = T + \omega * u(AC, AC) = T + \frac \omega {1-\omega} * R$

## TF2T

##### vs. RANDOM with param p

$u(TF2T, RAND_p)=\frac{-ω^2p^4+3ω^2p^3+ω^2p^3S-ω^2p^3R+ω^2p^3T-3ω^2p^2-3ω^2p^2S+2ω^2p^2R-2ω^2p^2T+ω^2p+3ω^2pS-pS+pR-ω^2pR+ω^2pT+S-ω^2S}{-ω+1}$

##### vs. AD

$u(TF2T, AD) = S + \omega * S + \omega ^ 2 * u(AD, AD) = S + \omega S + \frac {\omega^2} {1-\omega} P$

##### vs. AC

$u(TF2T, AC) = S + \omega * S + \omega ^ 2 * u(AD, AD) = S + \omega S + \frac {\omega^2} {1-\omega} P$

##### vs. GT

$u(TF2T, GT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. TFT

$u(TF2T, TFT) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$

##### vs. TFTD

$u(TF2T, TFTD) = S + \frac \omega {1-\omega} * R$

##### vs. TF2T

$u(TF2T, TF2T) = R + \omega R+ \omega^2R+... = \frac{1}{1-\omega} * R$
