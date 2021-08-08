from pathlib import Path

from bot.middlewares import Localization

I18N_DOMAIN = 'planner_tgbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / r'C:\Users\Boryslavq\PycharmProjects\planner_tgbot\bot\locales'
i18n = Localization(I18N_DOMAIN, LOCALES_DIR)

_ = i18n.gettext
_l = i18n.lazy_gettext