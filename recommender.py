"""Transparent rule-based recommender (mirrors recommend() in index.html).
NOT a trained ML model. Replace `score()` with a model once labelled data exists."""
CATALOG = {  # id: (tags, physical_effort 0-3, minutes)
 "yoga": (["yoga"], 2, 20), "prana": (["breathing"], 0, 10), "med": (["meditation"], 0, 10),
 "taichi": (["movement"], 2, 20), "pmr": (["relaxation"], 0, 15), "breath": (["breathing", "relaxation"], 0, 5),
 "mind": (["mindfulness", "meditation"], 0, 10), "yoga-breath": (["yoga", "breathing"], 2, 20),
 "walk-mind": (["walking", "mindfulness"], 2, 15), "stretch-med": (["stretching", "meditation"], 1, 15),
 "aerobic-relax": (["aerobic", "relaxation"], 3, 25), "yoga-pmr": (["yoga", "relaxation"], 2, 25)}
BANDS = [(25, ["walk-mind", "stretch-med"]), (50, ["yoga", "prana", "med"]),
         (75, ["breath", "yoga-pmr", "walk-mind", "mind"]), (100, ["breath", "pmr", "med"])]  # adjustable

def score(ex_id, profile, a, recent_ids):
    tags, phys, dur = CATALOG[ex_id]; s = 0; why = []
    band = next(ids for m, ids in BANDS if a["stressPercentage"] <= m)
    if ex_id in band: s += 5; why.append("fits stress range")
    if set(profile.get("preferences", [])) & set(tags): s += 2; why.append("matches preferences")
    if dur > a["availableTime"]: s -= 3; why.append("longer than available time")
    else: s += 1
    if a["mood"] in ("Anxious", "Sad", "Overwhelmed") and set(tags) & {"breathing", "meditation", "relaxation"}: s += 1
    low = a["sleepQuality"] <= 2 or a["mentalFatigue"] >= 4
    if low and phys <= 1: s += 1
    if low and phys >= 3: s -= 2
    if profile.get("limitations") and phys >= 2: s -= phys - 1; why.append("movement-heavy; limitations noted")
    if recent_ids.count(ex_id) >= 3: s -= 1
    return s, why

def recommend(profile, assessment, recent_ids=(), top=4):
    r = sorted(((score(i, profile, assessment, list(recent_ids)), i) for i in CATALOG), key=lambda x: -x[0][0])
    return [{"id": i, "score": s, "reasons": w} for (s, w), i in r[:top]]
