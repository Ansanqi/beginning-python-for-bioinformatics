#!/usr/bin/env python

import fasta
import sys
from collections import defaultdict

def choose(n, k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def get_quorums(seqs, mlen):
    """
    add seq id_no to a set
    use explicit counter to create seq_no
    """
    quorum = defaultdict(int)
    for seq in seqs:
        for n in range(len(seq) - mlen):
            quorum[seq[n:n + mlen]] += 1
    return quorum

input_seqs = fasta.read_seqs(open(sys.argv[1]).readlines())
input_seqs2 = fasta.read_seqs(open(sys.argv[2]).readlines())

foreground = get_quorums(input_seqs, 10)
background = get_quorums(input_seqs2, 10)

N = len(input_seqs) + len(input_seqs2)

res_motifs = []
for i in foreground:
    term1 = choose(len(background[i]), len(foreground[i]))
    term2 = choose((N - len(background[i])), len(input_seqs)-1)
    term3 = choose(N, len(input_seqs))
    p = (float(term1) * float(term2)) / term3
    if 0 < p <= 0.0001:
        res_motifs.append(i + '\t' + str(foreground[i]) + '\t' + str(background[i]) + '\t' + str(p))

res_motifs.sort()
for i in res_motifs:
    print i
