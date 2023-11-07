import sys, toolforge, re, pywikibot
import pymysql.cursors
from datetime import datetime, timedelta

conn = toolforge.connect('lvwiki_p')

def decode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def run_query(sql, params = []):
	try:
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		if len(params)>0:
			cursor.execute(sql, params)
		else:
			cursor.execute(sql)
		rows = cursor.fetchall()
	except KeyboardInterrupt:
		sys.exit()

	return rows

actor_id_with_edit_data = """SELECT
	r.rev_actor,
    COUNT(*) edit_count,
    min(r.rev_timestamp) first_edit,
    max(r.rev_timestamp) last_edit,
    COUNT(IF(rev_timestamp>DATE_FORMAT((DATE_SUB(NOW(),INTERVAL 1 YEAR)+0),'%Y%m%d%k%i%s'),'1',NULL)) AS last_year_edits
FROM revision_userindex r
GROUP BY r.rev_actor
having COUNT(*)>5000
"""
actor_id_with_edit_data = run_query(actor_id_with_edit_data)
actor_id_with_edit_data = {b.get('rev_actor', 0): b for b in actor_id_with_edit_data}
#print(actor_id_with_edit_data)

bot_ids = """SELECT actor_id
FROM `user` u
join user_groups ug on ug.ug_user=u.user_id
join actor a on a.actor_user=u.user_id
where ug_group='bot'
union all
SELECT actor_id
FROM `user` u
join user_former_groups ufg on ufg.ufg_user=u.user_id
join actor a on a.actor_user=u.user_id
where ufg_group='bot'
"""
bot_ids = run_query(bot_ids)
bot_ids = set([b.get('actor_id', 0) for b in bot_ids])

bot_usernames = """SELECT page_title
from categorylinks
join page on page.page_id=cl_from
where cl_to='Visi_Vikipēdijas_boti'
"""
bot_usernames = run_query(bot_usernames)
bot_usernames = set([b.get('page_title', 0) for b in bot_usernames])

interested_users = list(set(actor_id_with_edit_data) - bot_ids)

placeholders = ", ".join(["%s"] * len(interested_users))

users_by_articles = """SELECT r.rev_actor, count(*) cnt
FROM revision r
join page p on p.page_id=r.rev_page
WHERE p.page_namespace=0 and p.page_is_redirect=0
	and r.rev_parent_id=0 and r.rev_actor in ({})
    group by r.rev_actor
""".format(placeholders)

users_by_articles = run_query(users_by_articles, interested_users)
users_by_articles = {b.get('rev_actor', 0): b.get('cnt', 0) for b in users_by_articles}

actors = """SELECT actor_id, actor_name
from actor a
where a.actor_id in ({})""".format(placeholders)

actors = run_query(actors, interested_users)
actors = {b.get('actor_id', 0): b.get('actor_name', '') for b in actors}

to_save = []

for actor_id in interested_users:
	main_data = actor_id_with_edit_data.get(actor_id, {})
	articles = users_by_articles.get(actor_id, 0)
	user_name = actors.get(actor_id, '')

	if user_name in bot_usernames: continue

	to_save.append({
		'user_name': decode_if_necessary(user_name),
		'first_edit': decode_if_necessary(main_data.get('first_edit')),
		'last_edit': decode_if_necessary(main_data.get('last_edit')),
		'last_year_edits': main_data.get('last_year_edits', 0),
		'edit_count': main_data.get('edit_count', 0),
		'articles': articles,
	})

sorted_list = sorted(to_save, key=lambda x: x.get('edit_count'), reverse=True)

user_list = []

cnt = 1
for user in sorted_list:
	# 2008 05 21 16 14 23
	last_edit = datetime.strptime(user.get('last_edit'), '%Y%m%d%H%M%S')
	date_to_be_considered_active = datetime.now() - timedelta(days=365)

	is_active = last_edit > date_to_be_considered_active

	template = """|-{}
| {}.
| {{{{u|{}}}}}
| [https://xtools.wmcloud.org/ec/lv.wikipedia/{} {{{{formatnum:{}}}}}]
| {{{{formatnum:{}}}}}
| [https://xtools.wmcloud.org/pages/lv.wikipedia.org/{} {{{{formatnum:{}}}}}]
| {}
| {}""".format(
		'' if is_active else ' style="background-color: #EEEEEE"',
		cnt,
		user.get('user_name'),
		user.get('user_name').replace(' ', '_'),
		user.get('edit_count'),
		user.get('last_year_edits'),
		user.get('user_name').replace(' ', '_'),
		user.get('articles'),
		datetime.strptime(user.get('first_edit'), '%Y%m%d%H%M%S').strftime("%Y-%m-%d"),
		datetime.strptime(user.get('last_edit'), '%Y%m%d%H%M%S').strftime("%Y-%m-%d"),
	)
	user_list.append(template)

	cnt += 1

final_table = """Saraksts pēdējo reizi atjaunināts {}.

{{| class='wikitable sortable'
! Nr.
! Dalībnieks
! Labojumu skaits
! Labojumi pēdējās<br />365 dienās
! Rakstu skaits
! Pirmais labojums
! Pēdējais labojums
{}
|}}""".format(
	datetime.now().strftime("{{dat|%Y|%m|%d||bez}}"),
	'\n'.join(user_list)
)

def doreplace(text,pretext,header,footer):
	newtext = re.sub(header + '.*' + footer, header + '\n' + pretext + '\n' + footer, text, flags=re.DOTALL)

	return newtext
#
site = pywikibot.Site("lv", "wikipedia")
page = pywikibot.Page(site,'Vikipēdija:Dalībnieku uzskaitījums pēc labojumu skaita')
wikitext = page.get(get_redirect=True)

tableInserted = doreplace(wikitext,final_table,'<!-- TABLE_START -->','<!-- TABLE_END -->')

page.text = tableInserted
page.save(summary='Bots: atjaunināta tabula', botflag=True)
