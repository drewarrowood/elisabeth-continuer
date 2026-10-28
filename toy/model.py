"""Toy Kripke model for 'Two Elisabeths' (paper §3.4). Not a proof: a small model check.

Worlds: w0 now; w1a pilot passes and d deleted; w1b pilot passes and d kept; w2 pilot fails.
Individuals are tracked as rigid ids; identity is id-equality (so NI/ND hold by construction).
K (continuer) is defined by test evidence and checked for non-transitivity.
"""
from itertools import product

WORLDS = {
    "w0":  {"exists": {"o", "e", "d"},             "pass": set()},
    "w1a": {"exists": {"o", "e", "c", "m1", "m2"}, "pass": {"c"}},
    "w1b": {"exists": {"o", "e", "d", "c", "m1", "m2"}, "pass": {"c"}},
    "w2":  {"exists": {"o", "e", "d", "c"},        "pass": set()},
}
# Continuer evidence (graded 0..1), the same in every world where both exist.
K = {("o","e"):.9, ("o","d"):.9, ("d","c"):.8, ("c","m1"):.8, ("m1","m2"):.8, ("c","m2"):.4}
THRESH = .7

def k(x, y):
    return x == y or K.get((x, y), 0) >= THRESH

def ident(x, y):          # rigid identity
    return x == y

def closest_continuer_is(x, y, w):   # Nozick, read naively
    ex = WORLDS[w]["exists"]
    if y not in ex or not k(x, y): return False
    rivals = [z for z in ex if z not in (x, y) and K.get((x, z), 0) >= K.get((x, y), 0)]
    return not rivals and (x not in ex or x == y)

ids = {"o", "e", "d", "c", "m1", "m2"}
# (NI)/(ND): identity facts constant across worlds
assert all(ident(a, b) == ident(a, b) for a, b in product(ids, ids))
# Fission: o continues to both e and d, but e != d, so continuing is not identity
assert k("o","e") and k("o","d") and not ident("e","d")
# K not transitive across edits
assert k("c","m1") and k("m1","m2") and not k("c","m2")
# Closest-continuer 'identity' of d with c flips with deletion alone -> violates NI in spirit
cc = {w: closest_continuer_is("d", "c", w) for w in ("w1a", "w1b")}
assert cc["w1a"] and not cc["w1b"], cc
print("NI/ND hold; fission blocks identity; K non-transitive (c->m1->m2);")
print("closest-continuer: d is c in w1a (d deleted) but not in w1b (d kept):", cc)
