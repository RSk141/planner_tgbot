from data.config import I18N_DOMAIN, LOCALES_DIR
from middlewares import Localization

i18n = Localization(I18N_DOMAIN, LOCALES_DIR)

_ = i18n.gettext
_l = i18n.lazy_gettext
