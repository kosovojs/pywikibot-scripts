import pywikibot
import re

eusite = pywikibot.Site("es", "wikisource")
ensite = pywikibot.Site('en', "wikipedia")

json = {
	"headers": ["page_title"], "meta": {"rev_id": 282356, "query_id": 28277, "run_id": 275715}, "rows": [["P1542"], ["P1788"], ["F1531"], ["P1427"], ["N1695"], ["P1492"], ["N1937"], ["N1977"], ["P1932"], ["N1465"], ["F1514"], ["N1431"], ["F1482"], ["N1410"], ["N1443"], ["N1428"], ["F1495"], ["F1492"], ["F1516"], ["F1504"], ["N1697"], ["N1638"], ["N1598"], ["P2015"], ["F2017"], ["F2003"], ["N1405"], ["F1464"], ["N1605"], ["P1992"], ["P2016"], ["P1944"], ["P1938"], ["P1608"], ["P1603"], ["F2015"], ["F1567"], ["N1986"], ["N1978"], ["N1971"], ["N1957"], ["N1955"], ["N1948"], ["N1909"], ["N1726"], ["N1703"], ["N1674"], ["N1648"], ["N1568"], ["N1566"], ["N1523"], ["F1270"], ["N1553"], ["F2016"], ["F2013"], ["P1568"], ["P2014"], ["P1960"], ["P1765"], ["F2012"], ["P1784"], ["P1582"], ["P1994"], ["P1985"], ["P1984"], ["P1673"], ["P1681"], ["P1679"], ["P1671"], ["P1660"], ["P1659"], ["P1665"], ["P1656"], ["P1662"], ["P1600"], ["P1642"], ["P1668"], ["P1680"], ["P1678"], ["P1672"], ["P1663"], ["P1677"], ["P1661"], ["P1649"], ["P1708"], ["P1658"], ["P1691"], ["P1684"], ["P1725"], ["P1945"], ["P1643"], ["P1683"], ["P1674"], ["P1717"], ["P1664"], ["P1629"], ["F1988"], ["P1622"], ["N1974"], ["N1962"], ["F2014"], ["P1750"], ["P2012"], ["P1610"], ["P1587"], ["P1611"], ["P1621"], ["P1612"], ["P1624"], ["P1638"], ["P1666"], ["P1619"], ["P1627"], ["P1667"], ["P1714"], ["P1986"], ["P1592"], ["P1983"], ["P1292"], ["N1739"], ["N1611"], ["N1609"], ["N1577"], ["N1540"], ["N1518"], ["N1511"], ["N1767"], ["N1758"], ["N1752"], ["N1747"], ["N1705"], ["N1687"], ["N1661"], ["N1657"], ["F1557"], ["F1838"], ["F1979"], ["F1826"], ["N1984"], ["P1941"], ["F252"], ["N178"], ["N1671"], ["N1526"], ["N1670"], ["N1718"], ["N1672"], ["N1635"], ["F1835"], ["N1200"], ["N1631"], ["P1981"], ["P1713"], ["P53"], ["P1999"], ["P1997"], ["P1990"], ["P1623"], ["F195"], ["N95"], ["N1588"], ["F45"], ["N1658"], ["F1534"], ["F55"], ["N1711"], ["P1975"], ["P1965"], ["P1565"], ["P1474"], ["P1506"], ["P1817"], ["N1688"], ["F1554"], ["P2006"], ["P1803"], ["N1485"], ["P1805"], ["P1831"], ["P2010"], ["P1792"], ["P1993"], ["P2011"], ["P1811"], ["P2002"], ["P1728"], ["P1820"], ["P1763"], ["P1761"], ["P1756"], ["P1748"], ["P1752"], ["P1729"], ["P2007"], ["P1697"], ["F180"], ["P1632"], ["N1556"], ["P1769"], ["N1689"], ["P1982"], ["P1976"], ["P1974"], ["P1988"], ["P1979"], ["P1978"], ["P1973"], ["P1534"], ["P1774"], ["P1796"], ["P1818"], ["N1578"], ["P1964"], ["P1970"], ["P1966"], ["P1968"], ["P1969"], ["P1971"], ["F1825"], ["P1826"], ["N1404"], ["N1517"], ["N1585"], ["N1644"], ["F1812"], ["F1840"], ["P1730"], ["N1181"], ["F1226"], ["N1784"], ["N1692"], ["P1785"], ["N1597"], ["F1586"], ["N1492"], ["N1513"], ["P1791"], ["F1575"], ["N1514"], ["P1555"], ["P1636"], ["P1800"], ["F1561"], ["P1829"], ["F1559"], ["P1804"], ["P1799"], ["N1613"], ["F1742"], ["F1657"], ["P1594"], ["P1575"], ["N1529"], ["P1685"], ["F1807"], ["F1550"], ["N1730"], ["P1802"], ["P1585"], ["P1827"], ["P1830"], ["P8_a._C."], ["P1847"], ["P1810"], ["P1739"], ["F933"], ["N902"], ["P41"], ["P58"], ["P40"], ["P42"], ["P102"], ["N55"], ["F120"], ["P1825"], ["P5"], ["F1674"], ["N1608"], ["P1824"], ["P1616"], ["P1472"], ["N1960"], ["P66"], ["F870"], ["P1726"], ["P1595"], ["P1934"], ["N810"], ["P1641"], ["N1599"], ["P1620"], ["P1719"], ["P1604"], ["P1579"], ["N1724"], ["F1816"], ["P1946"], ["P1956"], ["N1552"], ["P1942"], ["P1940"], ["N1436"], ["F1991"], ["F1993"], ["N1660"], ["N1940"], ["F1980"], ["F181"], ["F1954"], ["N1639"], ["N1642"], ["N1736"], ["F1803"], ["F1806"], ["F1274"], ["N1225"], ["N1480"], ["P1851"], ["P1705"], ["N1636"], ["P1782"], ["F1810"], ["N1621"], ["N1779"], ["N1782"], ["P1928"], ["N1510"], ["F1472"], ["N1402"], ["F1592"], ["F1565"], ["P1842"], ["F1844"], ["F101"], ["N1699"], ["F1860"], ["P1862"], ["F1588"], ["F1470"], ["F1596"], ["N1548"], ["N1567"], ["F1503"], ["P1417"], ["N1432"], ["P1931"], ["P1949"], ["N1612"], ["F1874"], ["N1678"], ["F1571"], ["N1524"], ["N1727"], ["F430"], ["N354"], ["F1583"], ["F1868"], ["N1528"], ["P1927"], ["N1543"], ["P1839"], ["P1330"], ["F1346"], ["N1270"], ["N1532"], ["F1488"], ["F1532"], ["N1565"], ["N1664"], ["N1610"], ["P1775"], ["F1829"], ["N1675"], ["N1751"], ["F1802"], ["N1719"], ["N1686"], ["N1662"], ["F1983"], ["P1922"], ["P1939"], ["P1937"], ["P1840"], ["P1822"], ["N1715"], ["F1316"], ["F66"], ["N35"], ["N1683"], ["N1716"], ["N1895"], ["N20"], ["P1856"], ["F1558"], ["N1645"], ["N1646"], ["N1950"], ["F1992"], ["N1738"], ["N1615"], ["N1558"], ["F1813"], ["F1999"], ["N1652"], ["P1628"], ["F1843"], ["N1761"], ["N1953"], ["F1827"], ["N1560"], ["N1581"], ["F1506"], ["N1451"], ["P1670"], ["F95"], ["F1533"], ["P1866"], ["F1595"], ["N1544"], ["F1547"], ["F1374"], ["N1304"], ["F1975"], ["F1933"], ["P1823"], ["F17"], ["P1653"], ["P1637"], ["P1645"], ["N1452"], ["F1375"], ["N1313"], ["F1819"], ["N1748"], ["F1907"], ["F1530"], ["N1486"], ["F1994"], ["P1631"], ["P1625"], ["P1853"], ["N1070"], ["N1491"], ["P1870"], ["F1141"], ["F1556"], ["F1855"], ["N1746"], ["N1749"], ["N590"], ["F651"], ["N1494"], ["N1847"], ["P1648"], ["F1551"], ["N1522"], ["F104"], ["N40"], ["F1856"], ["N1714"], ["F1908"], ["F1930"], ["N1550"], ["N1579"], ["N1857"], ["F1832"], ["F1509"], ["F1902"], ["F1894"], ["F1946"], ["F1925"], ["N1755"], ["F1808"], ["N1590"], ["N1859"], ["N1866"], ["N1498"], ["P1850"], ["P1646"], ["N1951"], ["P1844"], ["F1854"], ["P1852"], ["N1846"], ["P1602"], ["P1874"], ["N1787"], ["F1549"], ["P1618"], ["N1589"], ["N1221"], ["P1821"], ["F1284"], ["N1282"], ["F1348"], ["F1869"], ["N1574"], ["N1586"], ["P1857"], ["N1384"], ["P1657"], ["P1841"], ["F1434"], ["F1824"], ["F1871"], ["P1869"], ["P1858"], ["F1823"], ["N1766"], ["F1185"], ["N1110"], ["N1706"], ["N1722"], ["F1834"], ["P1675"], ["N1618"], ["P1634"], ["P1630"], ["N1603"], ["N1781"], ["F1847"], ["N1774"], ["F1845"], ["N1734"], ["F1853"], ["F1846"], ["N1701"], ["F1861"], ["F1833"], ["N1707"], ["N1765"], ["N1770"], ["N1771"], ["F1820"], ["F1809"], ["N1764"], ["N1789"], ["N1725"], ["N1786"], ["F1859"], ["P1502"], ["P1868"], ["P1617"], ["N1584"], ["N1682"], ["N1729"], ["P1873"], ["P1583"], ["F1877"], ["F159_a._C."], ["N190_a._C."], ["P1875"], ["P1878"], ["P1881"], ["P1884"], ["P1887"], ["P1896"], ["P1897"], ["N1468"], ["N1474"], ["P1889"], ["P1836"], ["P1834"], ["P1871"], ["F65"], ["P1635"], ["P1892"], ["F1918"], ["N1769"], ["P1633"], ["F1578"], ["N1530"], ["F1580"], ["N1520"], ["N1490"], ["N1783"], ["F1841"], ["F1264"], ["N1197"], ["N1845"], ["N1542"], ["P1615"], ["F1566"], ["N1484"], ["N1785"], ["N1858"], ["F1899"], ["N1600"], ["N1741"], ["F1915"], ["F1911"], ["F1594"], ["F1982"], ["F1828"], ["N1760"], ["N1676"], ["N1776"], ["F1852"], ["N1788"], ["F1839"], ["F1350"], ["N1753"], ["N1283"], ["N1750"], ["F1407"], ["N1332"], ["N1562"], ["F1591"], ["N1527"], ["F1924"], ["P1647"], ["F1529"], ["F1458"], ["N1411"], ["F1817"], ["N1754"], ["F1814"], ["N1740"], ["F1821"], ["N1768"], ["N1469"], ["F1913"], ["N1412"], ["F1490"], ["F1479"], ["F1939"], ["F1842"], ["N1628"], ["F1920"], ["N1851"], ["F1857"], ["N1772"], ["F1541"], ["N1473"], ["F1917"], ["N1848"], ["N1759"], ["F1887"], ["N1580"], ["F1889"], ["N1515"], ["F1582"], ["F1850"], ["N1778"], ["N1745"], ["N1694"], ["N1470"], ["F1553"], ["N1497"], ["F1928"]]
}

mapper = {
	'N':'births',
	'F':'deaths',
	'P':'works'
}

parselist = json['rows']

for article in parselist:
	try:
		#article = article.title()
		article = article[0]
		
		matchobj = re.match('^([NFP])(\d{1,4})$',article)
		
		if not matchobj: continue
		
		if matchobj.group(1) not in mapper: continue
		
		entitle = 'Category:{} {}'.format(matchobj.group(2),mapper[matchobj.group(1)])
		print(entitle)
		
		page = pywikibot.Page(eusite,'Categoría:'+article)
		
		enpage = pywikibot.Page(ensite,entitle)
		
		if enpage.exists():
			if enpage.isRedirectPage():
				enpage = enpage.getRedirectTarget()
					
			if not enpage.isDisambig():
				
				item = enpage.data_item()
				item.get()
				#pywikibot.output(item.sitelinks.keys())
		
				if 'eswikisource' not in item.sitelinks.keys():
					item.setSitelink(page, summary=u'Added sitelink to [[w:s:es:%s]]' % page.title())
						#page.touch()
	except:
		continue