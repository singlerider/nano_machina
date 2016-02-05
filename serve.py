#!/usr/bin/env python2.7

from src.bot import Bot
from src.config.config import config

bot = Bot(config).run()
