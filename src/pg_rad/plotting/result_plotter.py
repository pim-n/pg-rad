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
        fig = plt.figure(figsize=(12, 10), constrained_layout=True)
        fig.suptitle(self.landscape.name)
        gs = GridSpec(
            4,
            2,
            width_ratios=[0.5, 0.5],
            height_ratios=[0.7, 0.1, 0.1, 0.1],
            hspace=0.2)

        ax1 = fig.add_subplot(gs[0, 0])
        self._draw_count_rate(ax1)

        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_landscape(ax2, landscape_z)

        ax3 = fig.add_subplot(gs[1, :])
        self._draw_table(ax3)

        ax4 = fig.add_subplot(gs[2, :])
        self._draw_detector_table(ax4)

        ax5 = fig.add_subplot(gs[3, :])
        self._draw_source_table(ax5)

        plt.show()

    def _plot_landscape(self, ax, z):
        lp = LandscapeSlicePlotter()
        ax = lp.plot(landscape=self.landscape, z=z, ax=ax, show=False)
        return ax

    def _draw_count_rate(self, ax):
        x = self.count_rate_res.arc_length
        y = self.count_rate_res.count_rate
        ax.plot(x, y, label='Count rate', color='r')
        ax.set_title('Count rate')
        ax.set_xlabel('Arc length s [m]')
        ax.set_ylabel('Counts')
        ax.legend()

    def _draw_table(self, ax):
        ax.set_axis_off()
        ax.set_title('Simulation parameters')
        cols = ('Parameter', 'Value')
        data = [
            ["Air density (kg/m^3)", round(self.landscape.air_density, 3)],
            ["Total path length (m)", round(self.landscape.path.length, 3)],
        ]

        ax.table(
            cellText=data,
            colLabels=cols,
            loc='center'
        )

        return ax

    def _draw_detector_table(self, ax):
        det = self.landscape.detector
        print(det)
        ax.set_axis_off()
        ax.set_title('Detector')
        cols = ('Parameter', 'Value')
        data = [
            ["Name", det.name],
            ["Type", det.efficiency],
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
                s.isotope,
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
