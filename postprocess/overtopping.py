import numpy as np
import scipy.signal
from numpy.typing import ArrayLike, NDArray


def compute(
    data: ArrayLike,
    min_depth: float,
    sta_depth: float,
    direction: tuple[float, float] = (1, 0),
    # method: str = "point",
) -> NDArray:

    data = np.array(data)

    if data.ndim != 2:
        raise ValueError("Expected two-dimensional array.")

    # Normalizing
    nx, ny = direction
    d = np.sqrt(nx**2 + ny**2)
    nx /= d
    ny /= d

    t = data[:, 0]
    eta = data[:, 1]
    u = data[:, 2]
    v = data[:, 3]

    # Velocity in direction
    s = u * nx + v * ny

    # Height of water column above station
    wl = eta - sta_depth
    # Removing error points, e.g., eta =0 if dry
    wl[wl < min_depth] = min_depth

    # Computing flux
    flux = wl * s
    return np.vstack([t, flux]).T


def compute_stats(
    flux_data: ArrayLike,
    min_depth: float,
    sta_depth: float,
    direction: tuple[float, float] = (1, 0),
    peaks_opts: dict = {},
    r_percent: float = 0.02,
) -> tuple[dict, NDArray, NDArray, dict]:

    flux_data = compute(flux_data, min_depth, sta_depth, direction)

    # Compute peaks from data
    peaks_idxs, properties = scipy.signal.find_peaks(flux_data[:, 1], **peaks_opts)
    peaks = flux_data[peaks_idxs, 1]

    # Total number of overtopping events
    n_events = len(peaks)

    # Getting start index of r2 %
    sorted_peaks = np.sort(peaks)
    i = round((1 - r_percent) * n_events)

    stats = dict(
        n_events=n_events,
        min=peaks.min(),
        median=np.median(peaks),
        mean=peaks.mean(),
        max=peaks.max(),
        r2=sorted_peaks[i],
    )

    peak_data = flux_data[peaks_idxs, :]
    return stats, flux_data, peak_data, properties
