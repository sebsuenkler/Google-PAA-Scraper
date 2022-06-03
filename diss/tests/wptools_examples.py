import wptools
page = wptools.page('Cat')
page.get_wikidata()
wikidata = page.data['wikidata']
print(wikidata)
 
