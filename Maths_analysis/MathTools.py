__author__ = 'ValadeAurelien'

def avg(ls):
    """
    Float: return the average of the values of a given list.
    """
    return sum(ls)/len(ls)


def moving_avg(ls, nb_values):
    """
    Float: returns the average the last values.
    """
    return sum(ls[-1:-nb_values])/nb_values


def instant_speed(dates, values):
    """
    List: returns the instantaneous speed values of each point of the given list.
    """
    return (values[-1]-values[-2])/(dates[-1]-dates[-2])


def ge_instant_speed(dates, values):
    """
    Generator: generates floats. These are the instantaneous speed values of each point of the given list.
    """
    for i in xrange(len(values)-1):
        yield (values[i+1]-values[i])/(dates[i+1]-dates[i])
    raise StopIteration


def ls_instant_accel(dates, values):
    """
    List: returns the instantaneous acceleration values of each point of the given list.
    """
    return [item for item in ge_instant_accel(dates, values)]


def ge_instant_accel(dates, values):
    """
    Generator: generates floats. These are the instantaneous acceleration values of each point of the given list.
    """
    ospeed = (values[1]-values[0])/(dates[1]-dates[0])
    for i in xrange(len(values)-2):
        ispeed = (values[i+2]-values[i+1])/(dates[i+2]-dates[i+1])
        yield 2*(ispeed-ospeed)/(dates[i+2]-dates[i])
        ospeed = ispeed
    raise StopIteration


def instant_accel(dates, values):
    """
    Float: returns the second order derived (=acceleration) number of the value tail.
    """
    ispeed = instant_speed(dates, values)
    values.pop(-1)
    dates.pop(-1)
    ospeed = instant_speed(dates, values)
    return (ispeed-ospeed)/(dates[-1]-dates[-2])


def ls_smooth_mov_avg(dates, values, nb_points):
    """
    Tuple of two lists: new dates, new values, both made on moving average.
    Please enter an non pair integer for nb_points.
    """
    aux = [item for item in ge_smooth_mov_avg(dates, values, nb_points)]
    return [item[0] for item in aux], [item[1] for item in aux]


def ge_smooth_mov_avg(dates, values, nb_points):
    """
    Generator: generates tuples of two lists (dates;values) made on moving average.
    Please enter an non pair integer for nb_points.
    """
    correc = int(nb_points)
    for mid in xrange(len(values)-correc):
        moy_val = 0
        moy_date = 0
        for nval in xrange(mid-correc, mid+correc+1):
            moy_val += values[nval]
            moy_date += dates[nval]
        yield moy_date/nb_points, moy_val/nb_points
    raise StopIteration


def stairs(values, step_size):
    """
    List: returns a list made of steps (like stairs).
    Each step is the average of the precised number of values.
    The tails is treated anyway, the head is not.
    """
    new = []
    values.reverse()
    while len(values) >= step_size:
        step_ori = [values.pop() for i in xrange(step_size)]
        step_val = avg(step_ori)
        new += [step_val for i in xrange(step_size)]
    new += values
    new.reverse()
    return new

def ge_diff(X, Y):
    """
    Generator: generates a list of absolute difference between items taken out of two lists.
    """
    for i in xrange(len(X)):
        yield abs(X[i]-Y[i])
    raise StopIteration

def best_stairs(values, max_step_size, min_step_size):
    """
    List: returns a stairs list.
    It has been optimized in order to minimize the maximal difference between the real values and the step ones.
    It means that the returned is the one for which max( abs(a-b) for (a,b) in (Values * stairs(Values) ) is minimal.
    """
    best = None, 1000
    for i in xrange(min_step_size, max_step_size+1):
        istairs = stairs(values, i)
        diff = max(ge_diff(values, istairs))
        if diff < best[1]:
            best = istairs, diff
    return best

def last_upon(dates, values, to_exceed):
    """
    Tuple: returns the last couple (date, value) of the last point of the given list whom value exceeded or is equal to the given one.
    None is returned if no point fits.
    """
    for i in xrange(len(values)):
        if values[i] >= to_exceed:
            return dates[i], values[i]


def last_under(dates, values, to_exceed):
    """
    Tuple: returns the last couple (date, value) of the last point of the given list whom value is lower than or equal to the given one.
    None is returned if no point fits.
    """
    for i in xrange(len(values)):
        if values[i] <= to_exceed:
            return dates[i], values[i]

