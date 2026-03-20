# --- Physics defaults ---
DEFAULT_AIR_DENSITY = 1.243  # kg/m^3, Skåne

# --- Simulation defaults ---
DEFAULT_SEED = None
DEFAULT_ACQUISITION_TIME = 1.0

# --- Source defaults ---
DEFAULT_PATH_HEIGHT = 0.0
DEFAULT_SOURCE_HEIGHT = 0.0

# --- Segmented road defaults ---
DEFAULT_MIN_TURN_ANGLE = 30.
DEFAULT_MAX_TURN_ANGLE = 90.

DEFAULT_FRICTION_COEFF = 0.7      # dry asphalt
DEFAULT_GRAVITATIONAL_ACC = 9.81  # m/s^2
DEFAULT_ALPHA = 100.

# --- Detector efficiencies ---
DETECTOR_EFFICIENCIES = {
    "dummy": 1.0,
    "NaIR": 0.0216,
    "NaIF": 0.0254
}

# A, B, C parameters for different detector types
# for formula FWHM(E) = sqrt(A + B*E + C*E^2)
FWHM_PARAMS = {
    "NaI": (-70.55, 2.678, 0.000602),
    "HPGe": (1.778, 0.001843, 0.000001)
}
