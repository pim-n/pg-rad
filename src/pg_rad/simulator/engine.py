from typing import List

from pg_rad.landscape.landscape import Landscape
from pg_rad.simulator.outputs import (
    CountRateOutput,
    SimulationOutput,
    SourceOutput
)
from pg_rad.detector.detectors import IsotropicDetector, AngularDetector
from pg_rad.physics.fluence import calculate_counts_along_path
from pg_rad.utils.projection import minimal_distance_to_path
from pg_rad.inputparser.specs import RuntimeSpec, SimulationOptionsSpec


class SimulationEngine:
    """Takes a fully built landscape and produces results."""
    def __init__(
        self,
        landscape: Landscape,
        detector: IsotropicDetector | AngularDetector,
        runtime_spec: RuntimeSpec,
        sim_spec: SimulationOptionsSpec,
    ):

        self.landscape = landscape
        self.detector = detector
        self.runtime_spec = runtime_spec
        self.sim_spec = sim_spec

    def simulate(self) -> SimulationOutput:
        """Compute everything and return structured output."""

        count_rate_results = self._calculate_count_rate_along_path()
        source_results = self._calculate_point_source_distance_to_path()

        return SimulationOutput(
            name=self.landscape.name,
            count_rate=count_rate_results,
            sources=source_results
        )

    def _calculate_count_rate_along_path(self) -> CountRateOutput:
        arc_length, phi = calculate_counts_along_path(
            self.landscape,
            self.detector,
            acquisition_time=self.runtime_spec.acquisition_time
        )
        return CountRateOutput(arc_length, phi)

    def _calculate_point_source_distance_to_path(self) -> List[SourceOutput]:

        path = self.landscape.path
        source_output = []
        for s in self.landscape.point_sources:
            dist_to_path = minimal_distance_to_path(
                path.x_list,
                path.y_list,
                path.z,
                s.pos)

            source_output.append(
                SourceOutput(
                    s.name,
                    s.isotope.name,
                    s.activity,
                    s.pos,
                    dist_to_path)
            )

        return source_output
