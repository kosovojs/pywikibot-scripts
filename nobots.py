import mwparserfromhell

def deny_bots(text,jobname):
	text = mwparserfromhell.parse(text)
	for tl in text.filter_templates():
		if tl.name.matches(['nobots']):
			break
	else:
		return False
	for param in tl.params:
		jobs = [x.lower().strip() for x in param.value.split(",")]
		print(jobs)
		if param.name == 'job':
			for job in jobs:
				if job in (jobname, 'all'):
					return True
	if (tl.name.matches('nobots') and len(tl.params) == 0):
		return False
	return False
#
#newtext = """{{nobots|job=kategorijas+}}"""

#print(deny_bots(newtext,'kategorijas+'))