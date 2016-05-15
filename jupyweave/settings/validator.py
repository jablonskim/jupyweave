from jupyweave.exceptions.settings_errors import InvalidConfigurationError


class Validator:
    """Settings validators"""

    @staticmethod
    def check_keys(settings_data, allowed_keys, setting_name):
        """Checks if only allowed keys are in dictionary"""
        keys = settings_data.keys()

        for k in keys:
            if k not in allowed_keys:
                msg = str.format("Invalid setting '{0}' in '{1}'. \nAllowed settings:", k, setting_name)

                for ak in allowed_keys:
                    msg += "\n\t'" + ak + "'"

                raise InvalidConfigurationError(msg)
