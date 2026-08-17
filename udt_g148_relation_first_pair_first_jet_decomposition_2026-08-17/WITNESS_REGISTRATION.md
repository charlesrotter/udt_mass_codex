# G148 exact witness registration

Date: 2026-08-17

This file freezes the production liveness witness before executing the G148 outcome script. Values
are small distinct rationals chosen mechanically to avoid equal-entry symmetry. They are numerical
controls, not physical coefficients or a candidate history.

With formal parameter `lambda`, every block is affine:

```text
M(lambda)=M0+lambda dM.
```

The base point is the already regular G147 witness:

```text
B0=[[2,1/2],[0,3]]
Q0=[[1,1/3],[0,2]]
S0=[[1/5,-1/7],[1/4,1/6]]
Y0=[[1,0],[0,1]]
Z0=[[1/10,-1/8],[-1/12,1/9]]
```

The independently nonzero first jets are:

```text
dB=[[1/11,1/13],[-1/17,1/19]]
dQ=[[1/23,-1/29],[1/31,1/37]]
dS=[[-1/41,1/43],[1/47,-1/53]]
dY=[[1/59,1/61],[-1/67,1/71]]
dZ=[[-1/73,1/79],[1/83,1/89]]
```

The scripts must evaluate each jet alone and all five together. The registered liveness gate is
only that each block changes at least one exact first-jet output among `dot h`, `dot phi_pair`, and
`dot P_H`; it does not demand that every block change every output.
