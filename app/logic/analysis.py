# Analysis class
class Analyze(object):
    def __init__(self):
        pass

    # Time calculator
    @staticmethod
    def timefinder(times):
        # Calculate
        tscore = times.mean(axis=1) * (times.max(axis=1) / times.min(axis=1))
        return tscore

    # Compare Histories
    def comp_hists(self, usr1, usr2):
        # Inner join to get only restaurants both have been to
        matched = usr1.merge(usr2, on='type')

        # Calculate mean time visited and like percentage
        matched['meantime'] = matched[['time_x', 'time_y']].mean(axis=1)
        matched['meanlike'] = matched[['like_x', 'like_y']].mean(axis=1)
        matched['recenyscr'] = self.timefinder(matched[['time_x', 'time_y']])
        matched['reccoscr'] = matched.recenyscr * matched.meanlike

        # Sort by time then likes
        matched.sort('reccoscr')

        return matched
