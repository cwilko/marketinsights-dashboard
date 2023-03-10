import marketinsights.dashboard.components as components


class Dashboard:

    def __init__(self, app, background_callback_manager, mds, theme):
        self.content = []
        self.app = app
        self.bcm = background_callback_manager
        self.mds = mds
        self.theme = theme

    def getContent(self):
        return [component.getContent() for component in self.content]

    def addComponent(self, id, componentClass, opts):
        self.content.append(self.createComponent(id, componentClass, opts))

    def createComponent(self, id, componentClass, opts={}):
        componentInstance = getattr(components, componentClass)
        component = componentInstance(self.app, self.bcm, self.mds, id, self.theme, **opts)
        return component
