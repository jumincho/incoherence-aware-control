# Round5-A Dynamic Policy Selection Note

Run: `runs/round5a_tuning_splitA_r5_v2`  
Date: 2026-02-28 (UTC)

## Selection Inputs
- Compared methods on Split A:
  - `probe_only_fixedk`
  - `ours_controller_v2_nofallback`
  - `ours_controller_v2_nofallback_forcecontinue` (`force_continue_disagreement_threshold=0.25`)
  - `ours_controller_v2_nofallback_stopcap`
- Targets: `T={300,450,600,900,1200}`
- Repeats: `R=5`

## Key Observations
- `stopcap` degrades incoherence strongly at all mid/high targets and is rejected.
- `forcecontinue` tracks `nofallback` closely and is slightly worse at `T>=900` on incoherence.
- Both `nofallback` and `forcecontinue` improve over `probe_only_fixedk` at `T=450`, but not consistently at `T=600/900`.

## Fixed Choice for Round5-B
- Keep pre-registered dynamic variant: `ours_controller_v2_nofallback_forcecontinue`.
- Keep threshold fixed at `0.25` (no Split-B retuning).

