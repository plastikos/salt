# -*- coding: utf-8 -*-

# Import python libs
from __future__ import absolute_import

# Import 3rd-party libs
from salttesting.helpers import requires_salt_modules, requires_system_grains

# Import salt libs
import integration
import salt.utils


def _find_new_locale(current_locale):
    for locale in ['en_US.UTF-8', 'de_DE.UTF-8', 'fr_FR.UTF-8']:
        if locale != current_locale:
            return locale


@pytest.mark.skipif(salt.utils.is_windows(), 'minion is windows')
@requires_salt_modules('locale')
class LocaleModuleTest(integration.ModuleCase):
    @requires_system_grains
    def test_get_locale(self, grains):
        locale = self.run_function('locale.get_locale')
        self.assertNotEqual(None, locale)

    @pytest.mark.destructive_test
    @requires_system_grains
    def test_gen_locale(self, grains):
        locale = self.run_function('locale.get_locale')
        new_locale = _find_new_locale(locale)
        ret = self.run_function('locale.gen_locale', [new_locale])
        self.assertEqual(True, ret)

    @pytest.mark.destructive_test
    @requires_system_grains
    def test_set_locale(self, grains):
        original_locale = self.run_function('locale.get_locale')
        locale_to_set = _find_new_locale(original_locale)
        self.run_function('locale.gen_locale', [locale_to_set])
        ret = self.run_function('locale.set_locale', [locale_to_set])
        new_locale = self.run_function('locale.get_locale')
        self.assertEqual(True, ret)
        self.assertEqual(locale_to_set, new_locale)
        self.run_function('locale.set_locale', [original_locale])
