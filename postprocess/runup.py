import numpy as np
import scipy.signal
from numpy.typing import ArrayLike, NDArray
from typing_extensions import dataclass_transform


def compute(
    t: ArrayLike, x: ArrayLike, h: ArrayLike, runup_data: ArrayLike, sta_idxs: ArrayLike
) -> tuple[NDArray, NDArray, NDArray]:

    x, h, runup_data, sta_idxs = [np.array(s) for s in [x, h, runup_data, sta_idxs]]

    # Getting indices of zero-crossings
    wl = runup_data[:, :] - h
    zeros = np.diff(np.sign(wl), axis=1)
    zeros_idx = [np.where(x)[0] for x in zeros]
    # Converting local transect indices to station indices
    raw_zeros_sta_idx = [sta_idxs[x] for x in zeros_idx]

    # Saving jagged arrays into 2D array with -1 denoting no value
    n_zeros = np.max([x.size for x in zeros_idx])
    nt = len(zeros_idx)
    zero_sta_idx = np.full([nt, n_zeros], -1).astype(int)
    for i, s in enumerate(raw_zeros_sta_idx):
        zero_sta_idx[i, : len(s)] = s

    min_idxs = np.array([i[0] for i in zeros_idx])
    #    max_idxs = np.array([i[-1] for i in zeros_idx])

    runup_x = x[min_idxs]
    runup_h = h[min_idxs]
    #print("unique min_idxs:", np.unique(min_idxs)[:20])
    #print("min_idxs first 20:", min_idxs[:20])
    #print("first few zeros_idx lens:", [len(i) for i in zeros_idx[:10]])
    # Adjusting to reference frame of first wet/dry location (initial shoreline)
    runup_x -= runup_x[0]

    runup_x = np.vstack([t, runup_x]).T
    runup_h = np.vstack([t, runup_h]).T

    return runup_x, runup_h, zero_sta_idx


def _compute_stats(data: NDArray, peaks_opts: dict, r_percent: float):
    peaks_idxs, properties = scipy.signal.find_peaks(data[:, 1], **peaks_opts)
    peaks = data[peaks_idxs, 1]

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

    peak_data = data[peaks_idxs, :]
    return stats, peak_data, properties


def compute_stats(
    t: ArrayLike,
    x: ArrayLike,
    h: ArrayLike,
    runup_data: ArrayLike,
    sta_idxs: ArrayLike,
    peaks_opts: dict = {},
    r_percent: float = 0.02,
) -> tuple[dict, dict, NDArray, NDArray, NDArray, NDArray, dict, dict, NDArray]:

    runup_x, runup_h, zero_sta_idx = compute(t, x, h, runup_data, sta_idxs)

    stats_x, peak_x, properties_x = _compute_stats(runup_x, peaks_opts, r_percent)
    stats_h, peak_h, properties_h = _compute_stats(runup_h, peaks_opts, r_percent)

    return (
        stats_x,
        stats_h,
        runup_x,
        runup_h,
        peak_x,
        peak_h,
        properties_x,
        properties_h,
        zero_sta_idx,
    )
