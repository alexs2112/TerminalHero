from world.feature import *
from dialog.dialog_loader import *

# pylint: disable=invalid-name
_feature_factory = None
def get_feature_factory():
    global _feature_factory
    if not _feature_factory:
        _feature_factory = FeatureFactory()
    return _feature_factory

class FeatureFactory():
    def test_dialog(self):
        f = DialogFeature("Testing")
        f.set_dialog_function(test_dialog)
        return f
