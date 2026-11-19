# Readability & math audit — human-readability-math-auditor

- Equations checked: 16
- **Verdict: PASS**

## 1. Breathing room (class settings)

| setting | value | rule | ok |
|---|---|---|---|
| \onehalfspacing | True | required | ✔ |
| \parskip | 6 pt | ≥ 6 pt | ✔ |
| \arraystretch | 1.35 | ≥ 1.25 | ✔ |
| box padding (left, top) | ('9', '6') pt | ≥ 8, ≥ 6 | ✔ |

## 2. Equation integrity

| label | file:line | symbols | Hebrew "כאשר" right below | not defined nearby | ok |
|---|---|---|---|---|---|
| `eq:hyp` | ch2_problem.tex:77 | H, a, b | yes | — | ✔ |
| `eq:vonkries` | ch3_literature.tex:37 | R, ell, epsilon | yes | — | ✔ |
| `eq:de00` | ch3_literature.tex:45 | C, H, L, R, S | yes | — | ✔ |
| `eq:smplx` | ch3_literature.tex:63 | J, M, P, W, beta, psi, theta | yes | — | ✔ |
| `eq:ddpm` | ch3_literature.tex:81 | I, N, alpha, q | yes | — | ✔ |
| `eq:ldmloss` | ch3_literature.tex:215 | L, epsilon, g, m, p, theta, z | yes | — | ✔ |
| `eq:ipadapter` | ch3_literature.tex:220 | K, Q, V, Z, lambda | yes | — | ✔ |
| `eq:cfg` | ch3_literature.tex:225 | epsilon, theta, varnothing, w, z | yes | — | ✔ |
| `eq:unit` | ch4_market.tex:141 | C, p, q, r | yes | — | ✔ |
| `eq:pugh` | ch5_alternatives.tex:40 | S, w | yes | — | ✔ |
| `eq:map` | ch5_alternatives.tex:186 | A, I, M, gamma, lambda, mu | yes | — | ✔ |
| `eq:ratio` | ch5_alternatives.tex:217 | C, H, L, r | yes | — | ✔ |
| `eq:fusion` | ch5_alternatives.tex:224 | C | yes | — | ✔ |
| `eq:score` | ch5_alternatives.tex:241 | eta, kappa, q, r | yes | — | ✔ |
| `eq:trend` | ch5_alternatives.tex:245 | alpha, v | yes | — | ✔ |
| `eq:risk` | ch7_risks.tex:15 | I, P, R | yes | — | ✔ |

## 3. Hebrew inside math without \hebmath

None found. ✔

## 4. Punctuation spacing (Hebrew source)

None found. ✔

## 5. Raw LaTeX in the compiled PDF

None found. ✔
