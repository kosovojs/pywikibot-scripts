#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from datetime import date, datetime, timedelta
import pywikibot
import json
from collections import Counter
import operator

botflag = False

site = pywikibot.Site("lv", "wikipedia")

pagetosave = pywikibot.Page(site,'User:Edgars2007/Example123')
#pagetosave = pagetosave.get()

curtime = datetime.now().strftime("%y-%m-%d-%H-%M")

pagetosave.text = curtime
pagetosave.save(summary='cron tests')
