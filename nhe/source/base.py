# nhlib: A New Hazard Library
# Copyright (C) 2012 GEM Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Module :mod:`nhe.source.base` defines a base class for seismic sources.
"""
import abc

from nhe import const


class SeismicSource(object):
    """
    Seismic Source is an object representing geometry and activity rate
    of a structure generating seismicity.

    :param source_id:
        Some (numeric or literal) source identifier. Supposed to be unique
        within the source model.
    :param name:
        String, a human-readable name of the source.
    :param tectonic_region_type:
        Source's tectonic regime. See :class:`const.TRT`.
    :param mfd:
        Magnitude-Frequency distribution for the source. See :mod:`nhe.mfd`.
    :param rupture_mesh_spacing:
        The desired distance between two adjacent points in source's
        ruptures' mesh, in km. Mainly this parameter allows to balance
        the trade-off between time needed to compute the :meth:`distance
        <nhe.geo.surface.base.BaseSurface.get_min_distance>` between
        the rupture surface and a site and the precision of that computation.
    :raises ValueError:
        If ``tectonic_region_type`` is wrong/unknown.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, source_id, name, tectonic_region_type,
                 mfd, rupture_mesh_spacing):
        if not const.TRT.is_valid(tectonic_region_type):
            raise ValueError('unknown tectonic region type %r' %
                              tectonic_region_type)
        if not rupture_mesh_spacing > 0:
            raise ValueError('rupture mesh spacing must be positive')
        self.source_id = source_id
        self.name = name
        self.tectonic_region_type = tectonic_region_type
        self.mfd = mfd
        self.rupture_mesh_spacing = rupture_mesh_spacing

    @abc.abstractmethod
    def iter_ruptures(self, temporal_occurrence_model):
        """
        Get a generator object that yields probabilistic ruptures the source
        consists of.

        :param temporal_occurrence_model:
            Temporal occurrence model (supposedly
            :class:`nhe.tom.PoissonTOM`). It is passed intact
            to the probabilistic rupture constructor.
        :returns:
            Generator of instances
            of :class:`~nhe.source.rupture.ProbabilisticRupture`.
        """
