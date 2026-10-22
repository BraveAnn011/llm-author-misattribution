#!/usr/bin/env python3
"""Reproduce every inferential statistic reported in the manuscript
"Which Answer Did the Seventeen-Year-Old Write?"

Usage:
    python3 analysis/stats_paper.py data/Master_results_ALL_v2.csv

Requires: pandas, numpy, scipy.

Unit-of-analysis notes
----------------------
* A SESSION is one API call: one model shown all three answers once.
  Sessions are identified by (model, date, source_file, run, label_order,
  condition). The `run` column is the label-order index (1-6), not the batch;
  the batch is recorded in `source_file`.
* Under one-to-one matching, a session can score only 0, 1, or 3 correct.
  Item rows within a session are therefore NOT independent. Row-level
  binomial tests are reported for comparison only; inference against chance
  uses the session-level tests.
* The post-reveal (phase-2) text is stored once per item row, so the same
  text appears three times per session. Blame coding is done per session.
"""
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/Master_results_ALL_v2.csv"

MODELS = ["Claude Fable 5", "Gemini 3.1 Pro", "GPT-5.6 Sol",
          "Grok 4.5", "GPT-4o legacy", "DeepSeek V4"]
LABELS = ["17M", "28F", "45M"]
SESSION = ["model", "date", "source_file", "run", "label_order", "condition"]
MATCHING = list("ABDE")
TRUE_AGE = {"17M": 17, "28F": 28, "45M": 45}

# Under random one-to-one matching of 3 items: P(0 correct)=2/6,
# P(1 correct)=3/6, P(3 correct)=1/6; mean 1, variance 1.
CHANCE_SESSION = {0: 2 / 6, 1: 3 / 6, 3: 1 / 6}

BLAME_EXTERNAL = re.compile(
    r"(?:flawless|deceptive|misleading|superficial cue|the text itself"
    r"|stand by|maintain my|still believe|remain confident)", re.I)
SELF_STEREOTYPE = re.compile(r"stereotyp", re.I)
OPENS_WITH_THANKS = re.compile(r"^\W*thank", re.I)


def hdr(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def wilson(k, n):
    if n == 0:
        return (np.nan, np.nan)
    lo, hi = stats.binomtest(int(k), int(n)).proportion_ci(method="wilson")
    return lo, hi


def fmt_p(p):
    if np.isnan(p):
        return "  n/a"
    return f"{p:.1e}" if p < 0.001 else f"{p:.3f}"


def two_prop_z(k1, n1, k2, n2):
    p = (k1 + k2) / (n1 + n2)
    se = np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return np.nan
    z = (k2 / n2 - k1 / n1) / se
    return 2 * stats.norm.sf(abs(z))


def fisher(k1, n1, k2, n2):
    return stats.fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1]


def score_open_age(guess, gt_label):
    """Condition C: correct if a stated range contains the true age,
    or a point estimate is within +/-3 years."""
    age = TRUE_AGE[gt_label]
    m = re.search(r"(\d+)\s*[-–—]\s*(\d+)", str(guess))
    if m:
        lo, hi = sorted((int(m.group(1)), int(m.group(2))))
        return int(lo <= age <= hi)
    m = re.search(r"\d+", str(guess))
    return int(abs(int(m.group()) - age) <= 3) if m else None


# --------------------------------------------------------------------------
raw = pd.read_csv(PATH, dtype={"correct": str})
df = raw[raw["dup_response_flag"] != 1].copy()
df["c"] = pd.to_numeric(df["correct"], errors="coerce")
valid = df[df["model_guess"].isin(LABELS)].copy()

hdr("DATA")
n_sessions = df.groupby(SESSION).ngroups
print(f"rows raw={len(raw)}  excluded(dup)={len(raw) - len(df)}  "
      f"analysis N={len(df)}  sessions={n_sessions}")
print("rows per session:", df.groupby(SESSION).size().value_counts().to_dict())
print("\nRows by model x batch (source_file):")
print(pd.crosstab(df["source_file"], df["model"]).to_string())


def session_scores(sub):
    """Sum of correct per session, keeping only sessions with 3 valid guesses."""
    g = sub.groupby(SESSION)
    ok = g["c"].count() == 3
    return g["c"].sum()[ok].astype(int)


# --------------------------------------------------------------------------
hdr("TABLE 1  Condition A (blind)")
print(f"{'model':16s} {'n':>4s} {'acc':>5s} {'95% CI':>13s} {'conf':>5s} "
      f"{'CCG':>6s} {'Mis@1':>5s} | {'p_row':>7s} | {'sess':>4s} "
      f"{'0/1/3':>9s} {'mean':>5s} {'p_mean':>7s} {'p_GOF':>7s}")
A = valid[valid["condition"] == "A"]
for m in MODELS:
    s = A[A["model"] == m]
    k, n = int(s["c"].sum()), len(s)
    acc = k / n
    lo, hi = wilson(k, n)
    conf = s["stated_confidence"].mean() / 100
    teen = s[s["item"] == "concept"]
    mis = 1 - teen["c"].mean()
    p_row = stats.binomtest(k, n, 1 / 3).pvalue
    sc = session_scores(s)
    ns = len(sc)
    obs = [int((sc == v).sum()) for v in (0, 1, 3)]
    exp = [ns * CHANCE_SESSION[v] for v in (0, 1, 3)]
    p_gof = stats.chisquare(obs, exp).pvalue
    z = (sc.mean() - 1) / (1 / np.sqrt(ns))       # null mean 1, var 1
    p_mean = 2 * stats.norm.sf(abs(z))
    print(f"{m:16s} {n:4d} {acc:5.2f} [{lo:.2f}, {hi:.2f}] {conf:5.2f} "
          f"{conf - acc:+6.2f} {mis:5.2f} | {fmt_p(p_row):>7s} | {ns:4d} "
          f"{'/'.join(map(str, obs)):>9s} {sc.mean():5.2f} "
          f"{fmt_p(p_mean):>7s} {fmt_p(p_gof):>7s}")

tab = pd.crosstab(A["model"], A["c"])
chi2, p, dof, _ = stats.chi2_contingency(tab)
print(f"\nOmnibus (rows): chi2({dof}) = {chi2:.1f}, p = {p:.1e}")
kw = stats.kruskal(*[session_scores(A[A["model"] == m]) for m in MODELS])
print(f"Omnibus (sessions, Kruskal-Wallis on session scores): "
      f"H = {kw.statistic:.1f}, p = {kw.pvalue:.1e}")
print("p_row: exact binomial vs 1/3 on item rows (anticonservative).")
print("p_mean: z-test of mean correct per session vs 1 (null var 1).")
print("p_GOF: chi-square goodness of fit of 0/1/3 counts vs 2/6,3/6,1/6.")

# --------------------------------------------------------------------------
hdr("TABLE 2  Confidence vs correctness, conditions A/B/D/E")
print(f"{'model':16s} {'n':>4s} {'mean':>5s} {'SD':>5s} {'right':>6s} "
      f"{'wrong':>6s} {'r':>7s} {'p':>8s}")
M = valid[valid["condition"].isin(MATCHING)].dropna(subset=["stated_confidence"])
for m in MODELS:
    s = M[M["model"] == m]
    r, p = stats.pearsonr(s["stated_confidence"], s["c"])
    print(f"{m:16s} {len(s):4d} {s['stated_confidence'].mean():5.1f} "
          f"{s['stated_confidence'].std(ddof=0):5.1f} "
          f"{s.loc[s.c == 1, 'stated_confidence'].mean():6.1f} "
          f"{s.loc[s.c == 0, 'stated_confidence'].mean():6.1f} "
          f"{r:+7.3f} {fmt_p(p):>8s}")

# --------------------------------------------------------------------------
hdr("TABLE 3  Condition A, concept item (17M): label assigned")
teenA = A[A["item"] == "concept"]
print(pd.crosstab(teenA["model"], teenA["model_guess"])
      .reindex(MODELS)[LABELS].to_string())

# --------------------------------------------------------------------------
hdr("F3  Condition C, concept item, range / +/-3-year scoring")
for m in MODELS:
    s = df[(df["model"] == m) & (df["condition"] == "C")
           & (df["item"] == "concept") & df["model_guess"].notna()]
    sc = [x for x in (score_open_age(g, t) for g, t in
                      zip(s["model_guess"], s["ground_truth"])) if x is not None]
    k, n = sum(sc), len(sc)
    lo, hi = wilson(k, n)
    print(f"{m:16s} acc={k / n:.2f} [{lo:.2f}, {hi:.2f}] k={k} n={n}")

# --------------------------------------------------------------------------
hdr("TABLE 4  Context effects vs Condition A (z = two-proportion z; F = Fisher)")
print(f"{'model':16s} {'A':>5s} | " + " | ".join(
    f"{c:>1s} {'acc':>5s} {'n':>4s} {'p_z':>7s} {'p_F':>7s}" for c in "BDE"))
for m in MODELS:
    a = valid[(valid["model"] == m) & (valid["condition"] == "A")]
    ka, na = int(a["c"].sum()), len(a)
    parts = []
    for c in "BDE":
        b = valid[(valid["model"] == m) & (valid["condition"] == c)]
        kb, nb = int(b["c"].sum()), len(b)
        parts.append(f"{c} {kb / nb:5.2f} {nb:4d} "
                     f"{fmt_p(two_prop_z(ka, na, kb, nb)):>7s} "
                     f"{fmt_p(fisher(ka, na, kb, nb)):>7s}")
    print(f"{m:16s} {ka / na:5.2f} | " + " | ".join(parts))
print("Use p_F where any cell is at 0 or 1 (z-test invalid at the boundary).")

# --------------------------------------------------------------------------
hdr("F7  Post-reveal text, coded PER SESSION (text is duplicated across rows)")
p2 = df[df["phase2_defense"].notna()].drop_duplicates(SESSION)
print(f"{'model':16s} {'sess':>5s} {'extBlame':>8s} {'stereo_sess':>11s} "
      f"{'stereo_mentions':>15s} {'opens_thanks':>12s}")
ext = {}
for m in MODELS:
    t = p2.loc[p2["model"] == m, "phase2_defense"]
    e = int(t.str.contains(BLAME_EXTERNAL).sum())
    ext[m] = (e, len(t))
    print(f"{m:16s} {len(t):5d} {e:8d} "
          f"{int(t.str.contains(SELF_STEREOTYPE).sum()):11d} "
          f"{int(t.apply(lambda x: len(SELF_STEREOTYPE.findall(x))).sum()):15d} "
          f"{int(t.str.contains(OPENS_WITH_THANKS).sum()):12d}")
ke, ne = ext["DeepSeek V4"]
ko = sum(v[0] for k, v in ext.items() if k != "DeepSeek V4")
no = sum(v[1] for k, v in ext.items() if k != "DeepSeek V4")
orr, pf = stats.fisher_exact([[ke, ne - ke], [ko, no - ko]])
print(f"\nDeepSeek {ke}/{ne} vs others {ko}/{no}: "
      f"Fisher OR = {orr:.1f}, p = {fmt_p(pf)}")
print(f"(Row-level, as in v6: {ke * 3}/{ne * 3} vs {ko * 3}/{no * 3}; "
      f"triple-counts each session.)")

# --------------------------------------------------------------------------
hdr("F8  Abstentions")
ab = df[df["abstained"] == 1]
print("item rows by model x condition:")
print(pd.crosstab(ab["model"], ab["condition"]).to_string())
print("\nsessions with >=1 abstention:")
print(ab.drop_duplicates(SESSION).groupby("model").size().to_string())
print("\nsessions with all 3 items abstained:")
full = ab.groupby(SESSION).size()
print(full[full == 3].groupby(level="model").size().to_string())

hdr("F8  Generational comparison, Condition A")
for m in ["GPT-4o legacy", "GPT-5.6 Sol"]:
    s = A[A["model"] == m]
    acc = s["c"].mean()
    conf = s["stated_confidence"].mean() / 100
    print(f"{m:16s} acc={acc:.2f} conf={conf:.2f} CCG={conf - acc:+.2f}")
g4 = A[A["model"] == "GPT-4o legacy"]
g5 = A[A["model"] == "GPT-5.6 Sol"]
print(f"accuracy difference p (Fisher) = "
      f"{fmt_p(fisher(int(g4.c.sum()), len(g4), int(g5.c.sum()), len(g5)))}")

# --------------------------------------------------------------------------
hdr("CONDITION P  Self-reported distribution")
for m in MODELS:
    s = df[(df["model"] == m) & (df["condition"] == "P") & df["c"].notna()]
    if s.empty:
        continue
    k, n = int(s["c"].sum()), len(s)
    lo, hi = wilson(k, n)
    print(f"{m:16s} top1={k / n:.2f} [{lo:.2f}, {hi:.2f}] "
          f"p(truth)={s['prob_on_truth'].mean():5.1f}% "
          f"entropy={s['entropy_bits'].mean():.2f}/1.58 bits n={n}")
