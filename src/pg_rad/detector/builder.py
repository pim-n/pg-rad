from pg_rad.inputparser.specs import DetectorSpec

from .detectors import IsotropicDetector, AngularDetector


class DetectorBuilder:
    def __init__(
        self,
        detector_spec: DetectorSpec,
    ):
        self.detector_spec = detector_spec

    def build(self) -> IsotropicDetector | AngularDetector:
        if self.detector_spec.is_isotropic:
            return IsotropicDetector(
                self.detector_spec.name,
                self.detector_spec.efficiency
            )
        else:
            raise NotImplementedError("Angular detector not supported yet.")
