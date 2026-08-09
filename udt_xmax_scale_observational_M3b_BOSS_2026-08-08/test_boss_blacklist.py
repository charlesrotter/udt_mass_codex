#!/usr/bin/env python3
"""F-IMPORT-LCDM machine-test for the BOSS adapter (prereg af9fa75d, freeze
f9c5b436). Confirms the loader is PHYSICALLY UNABLE to return fiducial-cosmology
/ n(z) / comoving columns or to open a reconstruction (_rec) file. Physics-blind:
tests PROVENANCE only, never merit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
M2 = os.path.join(os.path.dirname(HERE),
                  "udt_xmax_scale_observational_M2_build_2026-08-07")
sys.path.insert(0, M2)
sys.path.insert(0, HERE)
import boss_loader as bl  # noqa: E402


def _expect_block(cols, label):
    try:
        bl._load_boss_columns("galaxy_DR12v5_LOWZ_North.fits.gz", cols)
    except bl.BossBlacklistViolation:
        return True
    raise AssertionError(f"BLACKLIST BREACH: {label} was not blocked -> {cols}")


def test_fkp_blocked():
    assert _expect_block(["RA", "WEIGHT_FKP"], "WEIGHT_FKP (fiducial)")


def test_nz_nbar_blocked():
    assert _expect_block(["RA", "NZ"], "NZ (n(z))")
    assert _expect_block(["RA", "NBAR"], "NBAR (n(z))")


def test_comoving_distance_blocked():
    assert _expect_block(["RA", "COMOVING"], "COMOVING")
    assert _expect_block(["RA", "DISTANCE"], "DISTANCE")
    assert _expect_block(["DC"], "DC (comoving)")


def test_comp_blocked():
    # COMP is a fiducial completeness product not on the whitelist.
    assert _expect_block(["RA", "COMP"], "COMP")


def test_non_whitelist_blocked():
    assert _expect_block(["RA", "PSFFLUX"], "arbitrary non-whitelist column")


def test_rec_path_blocked():
    try:
        bl._load_boss_columns("galaxy_DR12v5_CMASS_North_rec.fits", ["RA"])
    except bl.BossBlacklistViolation:
        return
    raise AssertionError("BREACH: a _rec reconstruction path was not blocked")


def test_whitelist_allows_only_expected():
    # sanity: the allowed set is exactly RA/DEC/Z + completeness weights
    assert set(bl.BOSS_ALLOWED) == {
        "RA", "DEC", "Z", "WEIGHT_SYSTOT", "WEIGHT_CP", "WEIGHT_NOZ"}


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"\nALL {len(tests)} BLACKLIST TESTS PASSED (F-IMPORT-LCDM wired)")
