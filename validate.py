from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

schema = {
    'type': 'object',
    'properties': {
        'message': {'type': 'string'}
    }
}

class ValidateInputs(Inputs):
    """class for input validation.

    :param request: flask.Request object to validate.
    """

    json = [JsonSchema(schema=schema)]

    def validate(self):
        """Validate incoming request data. Returns True if all data is valid.
        Adds each of the validator's error messages to Inputs.errors if not valid.

        :returns: Boolean
        """
        res = Inputs.validate(self)
        for prop in schema['properties']:
            if not prop in self._request.get_json():
                res = False
                self.errors += ["Missing {} attribue!".format(prop)]
        return res