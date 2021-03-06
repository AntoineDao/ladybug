# coding=utf-8

import unittest
import pytest

from ladybug.skymodel import dirint, disc, _get_dirint_coeffs


class SkyModelTestCase(unittest.TestCase):
    """Test for (ladybug/skymodel.py)"""

    def test_dirint(self):
        """Test the accuracy of the dirint model against pvlib results."""
        dirint_result = dirint(
            [1038.62, 254.53], [90 - 10.567, 90 - 72.469],
            [175, 175], [93193., 93193.])
        assert dirint_result[0] == pytest.approx(868.8332, rel=1e-2)
        assert dirint_result[1] == pytest.approx(699.65011, rel=1e-2)

    def test_dirint_tdew(self):
        """Test the accuracy of the dirint model against pvlib results."""
        dirint_result = dirint(
            [1038.62, 254.53], [90 - 10.567, 90 - 72.469],
            [175, 175], [93193., 93193.], temp_dew=[10, 10])

        assert dirint_result[0] == pytest.approx(882.1372, rel=1e-2)
        assert dirint_result[1] == pytest.approx(672.5589, rel=1e-2)

    def test_dirint_no_delta_kt(self):
        """Test the accuracy of the dirint model against pvlib results."""
        dirint_result = dirint(
            [1038.62, 254.53], [90 - 10.567, 90 - 72.469], [175, 175],
            [93193., 93193.], use_delta_kt_prime=False)
        assert dirint_result[0] == pytest.approx(861.857, rel=1e-1)
        assert dirint_result[1] == pytest.approx(670.341, rel=1e-3)

    def test_dirint_coeffs(self):
        """Test the dirint coefficients against pvlib results."""
        coeffs = _get_dirint_coeffs()
        assert coeffs[0][0][0][0] == 0.385230
        assert coeffs[0][1][2][1] == 0.229970
        assert coeffs[3][2][6][3] == 1.032260

    def test_disc(self):
        """Test the accuracy of the disc model against pvlib results."""
        disc_result = disc(1000, 80, 1)
        assert disc_result[0] == pytest.approx(611.40543, rel=1e-2)
        assert disc_result[1] == pytest.approx(0.716088, rel=1e-3)
        assert disc_result[2] == pytest.approx(1.014825, rel=1e-3)

        disc_result = disc(200, 20, 150)
        assert disc_result[0] == pytest.approx(203.0609, rel=1e-2)
        assert disc_result[1] == pytest.approx(0.43897, rel=1e-3)
        assert disc_result[2] == pytest.approx(2.89994, rel=1e-3)

    def test_disc_overirradiance(self):
        """Test overirradiance in the disc model."""
        disc_result = disc(3000, 90, 200)

        assert disc_result[0] == pytest.approx(872.544, rel=1e-2)
        assert disc_result[1] == pytest.approx(1.000, rel=1e-3)
        assert disc_result[2] == pytest.approx(0.999493933, rel=1e-3)


if __name__ == "__main__":
    unittest.main()
