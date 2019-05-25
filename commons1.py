#!/usr/bin/python
# -*- coding: utf-8  -*-
#$ -l h_rt=0:40:00
#$ -l s_rt=0:35:00
#$ -l virtual_free=100M
#$ -j y
#$ -o $HOME/commons_deletion.out


'''

list images that will be deleted from Commons and are used in local wiki

'''

import sys, os
import pywikibot
import MySQLdb
from time import strftime

# "constants"

# wikipedia category namespace
WP_CATEGORY_NS = 14
# output debug messages
DEBUG = False

def connectWikiDatabase(lang):
    '''
    Connect to the wiki database
    '''
    if (lang):
        conn = MySQLdb.connect(host="commonswiki.analytics.db.svc.eqiad.wmflabs", db="commonswiki_p", read_default_file="~/replica.my.cnf")
        cursor = conn.cursor()
        return (conn, cursor)

def getSubCats(cursor, sourceCat):
    outSubCats = []
    sourceCat = sourceCat.replace(u' ', u'_')
    query = """SELECT page_title
        FROM commonswiki_p.categorylinks
        LEFT JOIN commonswiki_p.page ON page_id = cl_from
        WHERE cl_to = %s
        AND page_namespace = %s"""
    cursor.execute(query, (sourceCat, WP_CATEGORY_NS))
    if DEBUG:
        print cursor._executed        
    while True:
        try:
            (subCat,) = cursor.fetchone()
            outSubCats.append( subCat )
        except TypeError:
            break  
    
    return outSubCats    
  
def getImages(cursor, imgCat):
    outImages = []
    query = """SELECT DISTINCT lvwiki_p.imagelinks.il_to
        FROM lvwiki_p.imagelinks, commonswiki_p.image, commonswiki_p.categorylinks, commonswiki_p.page
        WHERE lvwiki_p.imagelinks.il_to = commonswiki_p.image.img_name
        AND commonswiki_p.image.img_name = commonswiki_p.page.page_title
        AND commonswiki_p.categorylinks.cl_from = commonswiki_p.page.page_id
        AND commonswiki_p.categorylinks.cl_to = %s
        AND NOT EXISTS(
            SELECT  1
            FROM lvwiki_p.image
            WHERE lvwiki_p.image.img_name = lvwiki_p.imagelinks.il_to
        )
        ORDER BY lvwiki_p.imagelinks.il_to"""
    cursor.execute(query, (imgCat, ))
    if DEBUG:
        print cursor._executed        
    while True:
        try:
            (imgName,) = cursor.fetchone()
            imgName = unicode(imgName, "utf-8")
            outImages.append( imgName )
        except TypeError:
            break 
    return outImages

   
def main():
    targetWiki = 'lv'
    outText = u''
    wikiSite = pywikibot.getSite(u'lv', u'wikipedia')
    galPageName = u'User:Edgars2007/Commons delete'  
    
    (conn, cursor) = connectWikiDatabase(targetWiki)
    imgCats = getSubCats(cursor, 'Deletion_requests')
    imgCats.extend( getSubCats(cursor, 'Media_without_a_source') )
    imgCats.extend( getSubCats(cursor, 'Media_without_a_license') )
    imgCats.extend( getSubCats(cursor, 'Media_missing_permission') )
    imgCats.extend( getSubCats(cursor, 'Media_uploaded_without_a_license') )
    imgCats.append('Other_speedy_deletions')
    imgCats.append('Copyright_violations')
    imgCats.append('Items_with_disputed_copyright_information')
    imgCats.append('Pending_fair_use_deletes')
    imgCats.extend( getSubCats(cursor, 'Pending_fair_use_deletes') )
    imgCats.append('Possibly_out_of_scope')

    
    totalImageCount = 0
    for imgCat in imgCats:
        delImages = getImages(cursor, imgCat)
        if ( len(delImages) ):
            totalImageCount += len(delImages)
            outText += u'== [[commons:Category:' + imgCat + u"]] ==\n"
            outText += u"<gallery>\n"
            for delImage in delImages:
                outText += delImage + u"| \n"
            outText += u"</gallery>\n"
            outText += u"\n"
    
    galleryPage = pywikibot.Page(wikiSite, galPageName)

    localtime = strftime("%Y-%m-%d %H:%M:%S")
    addTxt = u"Updated: " + localtime + u" \n\n"
    outText = addTxt + outText
    #print outText
    commentText = u'%d images' % totalImageCount
    
    #galleryPage.put(outText, comment = commentText, botflag=False, minor=False)    

    galleryPage.text = outText
    galleryPage.save(summary=commentText, botflag=False, minor=False)
    
        
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()