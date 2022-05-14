from starlette_context.plugins.base import Plugin, PluginUUIDBase


class RequestIdPlugin(PluginUUIDBase):
    def __init__(
        self,
        key: str = "X-Request-Id",
        force_new_uuid: bool = False,
        version: int = 4,
        validate: bool = True,
    ):
        self.key = key
        super(RequestIdPlugin, self).__init__(force_new_uuid, version, validate)


class RequestIpPlugin(Plugin):
    def __init__(self, key: str = "X-Request-Ip"):
        self.key = key
