import os
import requests

STATE = "last_signal.txt"


def ema(vals, n):
    k = 2 / (n + 1)
    out = [vals[0]]
    for x in vals[1:]:
        out.append(x * k + out[-1] * (1 - k))
    return out


def bb(closes, n=20, dev=2.0):
    w = closes[-n:]
    mid = sum(w) / n
    sd = (sum((x - mid) ** 2 for x in w) / n) ** 0.5
    return mid, mid + dev * sd, mid - dev * sd


def true_ranges(bars):
    return [max(c["h"] - c["l"], abs(c["h"] - p["c"]), abs(c["l"] - p["c"]))
            for p, c in zip(bars, bars[1:])]


def atr(bars, n=14):
    return sum(true_ranges(bars)[-n:]) / n


def adx(bars, n=14):
    tr = true_ranges(bars)
    pdm, mdm = [], []
