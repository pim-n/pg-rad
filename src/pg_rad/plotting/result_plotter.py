from importlib.resources import files
from typing import List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

from .landscape_plotter import LandscapeSlicePlotter
from pg_rad.simulator.outputs import SimulationOutput
from pg_rad.landscape.landscape import Landscape


class ResultPlotter:
    def __init__(self, landscape: Landscape, output: SimulationOutput):
        self.landscape = landscape
        self.count_rate_res = output.count_rate
        self.source_res = output.sources

    def plot(self, landscape_z: float = 0):
        self._plot_main(landscape_z)
        self._plot_detector()
        self._plot_metadata()

        plt.show()

    def save(self, path: str, landscape_z: float = 0) -> None:
        fig_1 = self._plot_main(landscape_z)
        fig_2 = self._plot_detector()
        fig_3 = self._plot_metadata()

        fig_1.savefig(path+"/main.jpg")
        fig_2.savefig(path+"/detector.jpg")
        fig_3.savefig(path+"/metadata.jpg")

    def _plot_main(self, landscape_z):
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle(self.landscape.name)
        fig.canvas.manager.set_window_title("Main results")

        gs = GridSpec(
            2, 2, figure=fig,
            height_ratios=[1, 2], width_ratios=[1, 1],
            hspace=0.3, wspace=0.3)

        ax_cps = fig.add_subplot(gs[0, 0])
        self._draw_cps(ax_cps)

        ax_counts = fig.add_subplot(gs[0, 1])
        self._draw_counts(ax_counts)

        ax_landscape = fig.add_subplot(gs[1, :])
        self._plot_landscape(ax_landscape, landscape_z)
        return fig

    def _plot_detector(self):
        det = self.landscape.detector

        fig = plt.figure(figsize=(10, 4))
        fig.canvas.manager.set_window_title("Detector")

        gs = GridSpec(1, 2, figure=fig, width_ratios=[0.5, 0.5])

        ax_table = fig.add_subplot(gs[0, 0])
        self._draw_detector_table(ax_table)

        if not det.is_isotropic:
            ax_polar = fig.add_subplot(gs[0, 1], projection='polar')

            energies = [
                source.primary_gamma for source in self.source_res
            ]

            self._draw_angular_efficiency_polar(ax_polar, det, energies[0])
        return fig

    def _plot_metadata(self):
        fig, axs = plt.subplots(2, 1, figsize=(10, 6))
        fig.canvas.manager.set_window_title("Simulation Metadata")

        self._draw_table(axs[0])
        self._draw_source_table(axs[1])
        return fig

    def _plot_landscape(self, ax, z):
        lp = LandscapeSlicePlotter()
        ax = lp.plot(landscape=self.landscape, z=z, ax=ax, show=False)
        return ax

    def _draw_cps(self, ax):
        x = self.count_rate_res.sub_points
        y = self.count_rate_res.cps
        ax.plot(x, y, color='b', label=f'max(CPS) = {y.max():.2f}')
        ax.legend(handlelength=0, handletextpad=0, fancybox=True)
        ax.set_title('Counts per second (CPS)')
        ax.set_xlabel('Arc length s [m]')
        ax.set_ylabel('CPS [s$^{-1}$]')

    def _draw_counts(self, ax):
        x = self.count_rate_res.distance[1:]
        y = self.count_rate_res.integrated_counts[1:]
        ax.plot(
            x, y, color='r', linestyle='--',
            alpha=0.2, label=f'max(counts) = {y.max():.2f}'
        )
        ax.legend(handlelength=0, handletextpad=0, fancybox=True)
        ax.scatter(x, y, color='r', marker='x')
        ax.set_title('Integrated counts')
        ax.set_xlabel('Arc length s [m]')
        ax.set_ylabel('N')

    def _draw_table(self, ax):
        ax.set_axis_off()
        ax.set_title('Simulation parameters')
        cols = ('Parameter', 'Value')
        data = [
            ["Air density (kg/m^3)", round(self.landscape.air_density, 3)],
            ["Total path length (m)", round(self.landscape.path.length, 3)],
            ["Readout points", len(self.count_rate_res.integrated_counts)],
            ["Mean background cps", round(self.count_rate_res.mean_bkg_cps, 3)]
        ]

        ax.table(
            cellText=data,
            colLabels=cols,
            loc='center'
        )

        return ax

    def _draw_detector_table(self, ax):
        det = self.landscape.detector

        if det.is_isotropic:
            det_type = "Isotropic"
        else:
            det_type = "Angular"

        source_energies = [
            source.primary_gamma for source in self.source_res
        ]

        # list field efficiencies for each primary gamma in the landscape
        effs = {e: det.get_efficiency(e) for e in source_energies}
        formatted_effs = ", ".join(
            f"{value:.5f} @ {key:.1f} keV"
            for key, value in effs.items()
        )
        ax.set_axis_off()
        ax.set_title('Detector')
        cols = ('Parameter', 'Value')
        data = [
            ["Detector", f"{det.name} ({det_type})"],
            ["Field efficiency", formatted_effs],
        ]

        ax.table(
            cellText=data,
            colLabels=cols,
            loc='center'
        )

        return ax

    def _draw_source_table(self, ax):
        ax.set_axis_off()
        ax.set_title('Point sources')

        cols = (
            'Name',
            'Isotope',
            'Activity (MBq)',
            'Position (m)',
            'Dist. to path (m)'
        )

        # this formats position to tuple
        data = [
            [
                s.name,
                s.isotope+f" ({s.primary_gamma} keV)",
                s.activity,
                "("+", ".join(f"{val:.2f}" for val in s.position)+")",
                round(s.dist_from_path, 2)
            ]
            for s in self.source_res
        ]
        ax.table(
            cellText=data,
            colLabels=cols,
            loc='center'
        )

        return ax

    def _draw_angular_efficiency_polar(self, ax, detector, energy_keV):
        # find the energies available for this detector.
        csv = files('pg_rad.data.angular_efficiencies').joinpath(
            detector.name + '.csv'
        )
        data = pd.read_csv(csv)
        energy_cols = [col for col in data.columns if col != "angle"]
        energies = np.array([float(col) for col in energy_cols])

        # take energy column that is within 1% tolerance of energy_keV
        rel_diff = np.abs(energies - energy_keV) / energies
        match_idx = np.where(rel_diff <= 0.01)[0]
        best_idx = match_idx[np.argmin(rel_diff[match_idx])]
        col = energy_cols[best_idx]

        theta_deg = data["angle"].to_numpy()
        eff = data[col].to_numpy()

        idx = np.argsort(theta_deg)
        theta_deg = theta_deg[idx]
        eff = eff[idx]

        theta_deg = np.append(theta_deg, theta_deg[0])
        eff = np.append(eff, eff[0])

        theta_rad = np.radians(theta_deg)

        ax.plot(theta_rad, eff)
        ax.set_title(f"Rel. angular efficiency @ {energy_keV:.1f} keV")
