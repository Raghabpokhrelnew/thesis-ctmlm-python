import numpy as np

from thesis_ctmlm.thermodynamics import (
    saturation_specific_humidity,
    cloud_fraction_from_decoupling,
    clip_cloud_fraction,
)


def test_saturation_specific_humidity_positive():
    q = saturation_specific_humidity(289.0)
    assert q > 0


def test_saturation_specific_humidity_increases_with_temperature():
    q1 = saturation_specific_humidity(285.0)
    q2 = saturation_specific_humidity(295.0)
    assert q2 > q1


def test_cloud_fraction_bounds():
    vals = cloud_fraction_from_decoupling(np.array([0.0, 0.5, 1.0]))
    assert np.all(vals >= 0.0)
    assert np.all(vals <= 1.0)


def test_clip_cloud_fraction():
    vals = clip_cloud_fraction(np.array([-0.2, 0.5, 1.4]))
    assert np.allclose(vals, np.array([0.0, 0.5, 1.0]))
