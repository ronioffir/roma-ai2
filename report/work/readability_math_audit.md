# Readability & math audit — human-readability-math-auditor

- Equations checked: 19
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
| `eq:formation` | ch2_problem.tex:34 | B, G, Q, R, S, epsilon, lambda | yes | — | ✔ |
| `eq:hyp` | ch2_problem.tex:82 | H, a, b, beta, u, v, y | yes | — | ✔ |
| `eq:vonkries` | ch3_literature.tex:37 | R, ell, epsilon | yes | — | ✔ |
| `eq:de00` | ch3_literature.tex:45 | C, H, L, R, S | yes | — | ✔ |
| `eq:smplx` | ch3_literature.tex:63 | J, M, P, W, beta, psi, theta | yes | — | ✔ |
| `eq:ddpm` | ch3_literature.tex:81 | I, N, alpha, q | yes | — | ✔ |
| `eq:ldmloss` | ch3_literature.tex:216 | L, epsilon, g, m, p, theta, z | yes | — | ✔ |
| `eq:ipadapter` | ch3_literature.tex:221 | K, Q, V, Z, lambda | yes | — | ✔ |
| `eq:cfg` | ch3_literature.tex:226 | epsilon, theta, varnothing, w, z | yes | — | ✔ |
| `eq:unit` | ch4_market.tex:141 | C, M, R, beta, f, g, lambda, p, r | yes | — | ✔ |
| `eq:pugh` | ch5_alternatives.tex:40 | S, w | yes | — | ✔ |
| `eq:map` | ch5_alternatives.tex:186 | A, I, M, gamma, lambda, mu | yes | — | ✔ |
| `eq:flash` | ch5_alternatives.tex:193 | I, Q, S, eta, kappa, lambda | yes | — | ✔ |
| `eq:ratio` | ch5_alternatives.tex:231 | C, H, L, r | yes | — | ✔ |
| `eq:fusion` | ch5_alternatives.tex:238 | C | yes | — | ✔ |
| `eq:score` | ch5_alternatives.tex:255 | eta, kappa, q, r | yes | — | ✔ |
| `eq:trend` | ch5_alternatives.tex:259 | alpha, v | yes | — | ✔ |
| `eq:sh` | ch6_workplan.tex:154 | A, L, Y, l, m | yes | — | ✔ |
| `eq:risk` | ch7_risks.tex:15 | I, P, R | yes | — | ✔ |

## 3. Hebrew inside math without \hebmath

None found. ✔

## 4. Punctuation spacing (Hebrew source)

None found. ✔

## 5. Raw LaTeX in the compiled PDF

None found. ✔
