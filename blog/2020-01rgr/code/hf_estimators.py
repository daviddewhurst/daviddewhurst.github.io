import numpy as np


def kaplan_meier_sf(marks, events=None, surviving=None):
    marks = np.array(marks)
    if events is None:
        events = np.ones(marks.shape[0])
    else:
        events = np.array(events)
    if surviving is None:
        surviving = marks.shape[0] - np.linspace(0, marks.shape[0] - 1, marks.shape[0])
    arr = 1. - events / surviving
    return np.cumprod(arr)


def kaplan_meier_cumhf(marks, events=None, surviving=None):
    sf = kaplan_meier_sf(marks, events=events, surviving=surviving)
    return -1. * np.log(sf)


def kaplan_meier_hf(marks, events=None, surviving=None, returndim='same'):
    cumhf = kaplan_meier_cumhf(marks, events=events, surviving=surviving)
    # interpolate
    if returndim == 'same':
        dim = marks.shape[0] + 1
        x_interp = np.linspace(marks.min(), marks.max(), dim)
        cumhf_interp = np.interp(
            x_interp,
            marks,
            cumhf
                )
    else:
        raise NotImplementedError('Currently only returndim == same is implemented')
    dx = np.diff(x_interp)
    d_cumhf = np.diff(cumhf_interp)
    return x_interp[1:], d_cumhf / dx


def nelson_aalen_cumhf(marks, events=None, surviving=None):
    marks = np.array(marks)
    if events is None:
        events = np.ones(marks.shape[0])
    else:
        events = np.array(events)
    if surviving is None:
        surviving = marks.shape[0] - np.linspace(0, marks.shape[0] - 1, marks.shape[0])
    arr = events / surviving
    return np.cumsum(arr)


def nelson_aalen_hf(marks, events=None, surviving=None, returndim='same'):
    cumhf = nelson_aalen_cumhf(marks, events=events, surviving=surviving)
    # interpolate
    if returndim == 'same':
        dim = marks.shape[0] + 1
        x_interp = np.linspace(marks.min(), marks.max(), dim)
        cumhf_interp = np.interp(
            x_interp,
            marks,
            cumhf
                )
    else:
        raise NotImplementedError('Currently only returndim == same is implemented')
    dx = np.diff(x_interp)
    d_cumhf = np.diff(cumhf_interp)
    return x_interp[1:], d_cumhf / dx

