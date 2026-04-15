from dataclasses import asdict
from datetime import datetime as dt
import json
import os
import logging
import re

from numpy import array, full_like, ndarray
from pandas import DataFrame

from pg_rad.simulator.outputs import SimulationOutput


logger = logging.getLogger(__name__)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        return super().default(obj)


def generate_folder_name(sim: SimulationOutput) -> str:
    formatted_sim_name = re.sub(r"\s+", '_',  sim.name.lower())
    folder_name = (
        formatted_sim_name +
        '_result_' +
        dt.today().strftime('%Y%m%d_%H%M')
    )
    return folder_name


def save_results(sim: SimulationOutput, folder_name: str) -> None:
    """Parse all simulation output and save to a folder."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        logger.warning("Folder already exists. Overwrite?")
        ans = input("[type 'n' to cancel overwrite] ")
        if ans.lower() == 'n':
            return

    df = generate_df(sim)
    csv_name = generate_csv_name(sim)
    df.to_csv(f"{folder_name}/{csv_name}.csv", index=False)
    with open(f"{folder_name}/parameters.json", 'w') as f:
        json.dump(generate_sim_param_dict(sim), f, cls=NumpyEncoder)
    logger.info(f"Simulation output saved to {folder_name}!")


def generate_sim_param_dict(sim: SimulationOutput) -> dict:
    """Parse simulation parameters and hyperparameters to dictionary."""
    d = asdict(sim)
    d.pop('count_rate')
    return d


def generate_df(sim: SimulationOutput) -> DataFrame:
    """Parse simulation output to CSV format and the name of CSV."""

    br_array = full_like(
        sim.count_rate.integrated_counts,
        sim.count_rate.mean_bkg_cps
    )

    result_df = DataFrame(
        {
            "East": sim.count_rate.x,
            "North": sim.count_rate.y,
            "ROI_P": sim.count_rate.integrated_counts,
            "ROI_BR": br_array,
            "Dist": sim.count_rate.distance
        }
    )

    return result_df


def generate_csv_name(sim: SimulationOutput) -> str:
    """Generate CSV name according to Alex' specification"""
    num_src = len(sim.sources)
    src_ids = [str(i+1) for i in range(num_src)]
    bkg_cps = round(sim.count_rate.mean_bkg_cps)
    source_param_strings = [
        [
            str(round(s.activity))+"MBq",
            str(round(s.dist_from_path))+"m",
            str(round(s.position[0]))+'_'+str(round(s.position[1]))
        ]
        for s in sim.sources
    ]

    if num_src == 1:
        src_str = "_".join(source_param_strings[0])
    else:
        src_str_array = array(
            [list(item) for item in zip(*source_param_strings)]
        )

        src_str = "_".join(src_str_array.flat)

    src_ids_str = "_".join(src_ids)
    csv_name = f"{src_ids_str}_src_{bkg_cps}_cps_bkg_{src_str}"
    return csv_name
