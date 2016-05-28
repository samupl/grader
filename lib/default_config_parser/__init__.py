from configparser import ConfigParser, NoOptionError, NoSectionError


class NotSet(KeyError):
    pass


class DefaultConfigParser(ConfigParser):
    def _dispatch(self, default, method, args, kwargs):
        """
        Dispatch all getters back to the base class, but allow them to use the default value when file doesn't have one.

        :param default: The default value to be used when a value is not present in the config file
        :param method: The base class method to be called
        :param args: Positional arguments that will be passed to the base class method
        :param kwargs: Keyword arguments that will be passed to the base class method
        """
        try:
            return method(self, *args, **kwargs)
        except (NoOptionError, NoSectionError):
            if default is not NotSet:
                return default
            raise

    def get(self, section, option, raw=False, vars=None, default=NotSet):
        return self._dispatch(default, ConfigParser.get, [section, option], {'raw': raw, 'vars': vars})

    def getboolean(self, section, option, default=NotSet):
        return self._dispatch(default, ConfigParser.getboolean, [section, option], {})

    def getint(self, section, option, default=NotSet):
        return self._dispatch(default, ConfigParser.getint, [section, option], {})

    def getfloat(self, section, option, default=NotSet):
        return self._dispatch(default, ConfigParser.getfloat, [section, option], {})
