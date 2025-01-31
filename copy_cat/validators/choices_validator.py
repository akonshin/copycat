from copy_cat.models.error import Error
from copy_cat.utils import find_dictionary
from copy_cat.validators.abstract_validator import AbstractValidator


class ChoicesValidator(AbstractValidator):
    def validate(self, design_object, test_data_object):
        self.validate_choices(design_object, test_data_object)

    def validate_choices(self, design_object, test_data_object):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        if restriction_obj.get('displayName') == 'StringSet':
            qualifiers = [i.strip() for i in design_object.get("qualifiers", '').split(',')]
            if test_data_object.value not in qualifiers and not restriction_obj.get("dropExtraRecords"):
                # TODO: Fix error message to be similar to web xd
                error_message = f"Qualifier {test_data_object.value} is not valid. " \
                                f"Possible choices -> {qualifiers}"
                self.errors_container.append(Error(fieldName=test_data_object.name,
                                                   designPath=design_object['location'],
                                                   xpath=test_data_object.location,
                                                   errorMessage=error_message))
