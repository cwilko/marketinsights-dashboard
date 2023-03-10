from marketinsights.utils.cacheUtils import cache


class DashboardComponent():

    def __init__(self, app, bcm, mds, id, theme):
        self.mds = mds
        self.bcm = bcm
        self.app = app
        self.id = id
        self.theme = theme

    @cache()
    def getData(self, market, source=None):
        print("Retrieving data from Price Store")
        if source is None:
            return self.mds.get(market, debug=False)
        else:
            return self.mds.aggregate(market, [source], debug=False)

    def __getstate__(self):
        return "DashboardComponent"

    def __setstate__(self, state):
        return "DashboardComponent"
