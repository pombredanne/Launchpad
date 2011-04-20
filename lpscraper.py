# I am only testing this in python 2.6 and 2.7. it will *NOT* work in python 3.x
# use 'python lpscraper.py -v' to get frequent status updates
import sys
if '-v' in sys.argv: v = True
else: v = False

from urllib import urlopen 

def do_page(pageurl):
    if v: print '- downloading page...'
    lp = urlopen(pageurl).read() # download the page's HTML
    #except: return # if there are any errors, just give up on this page
    if v: print '- done'
    
    # this splits the whole thing into a list of the project divs
    if v: print '- parsing it...'
    projects = '<div>'.join(lp.split("<div>")[1:]).split("""    </table>
        <table style="width: 100%;" class="lower-batch-nav">
      <tbody>
        <tr>
          <td style="white-space: nowrap" class="batch-navigation-index">""")[0] # it was kinda hard to find something unique to say where the end is, but this should do


    first = True # the first one is slightly different
    if v: print '- projects', len(projects.split("""    </div>
  </div>
</div>""")[0:-1])
    for proj in projects.split("""    </div>
  </div>
</div>""")[0:-1]: # this is always at the end of each project section
        lpp = proj.strip().split("\n")
        namesec = lpp[1]
        descsec = ' '.join(lpp[3:]).split("</div>")[0]
        authorsec = ' '.join(lpp[5:])
        
        if first: 
            namesec = lpp[0]
            descsec = ' '.join(lpp[2:]).split("</div>")[0]
            authorsec = lpp[4]
            
        
        url = 'https://launchpad.net' + namesec.split('<a href="')[1].split('"')[0]
        name = namesec.split(">")[1].split("<")[0]
        desc = descsec.split("<div>")[1]
        authorurl = 'https://launchpad.net' + authorsec.split('<a href="')[1].split('"')[0]
        author = authorsec.split(">")[1].split("<")[0]

        
        print name
        print url
        print desc
        print author
        print authorurl
        print '---'
        
        
        first = False
    if v: print '- done'
        

# unique bits we can use to split the html by to get the # of projects
start = """<p>There are
    <strong>"""
end = """</strong>
    projects registered in Launchpad."""

if v: print 'Getting first page to count the projects...'
try: lp = urlopen("http://launchpad.net/projects/+all?batch=1").read() # 
except: exit()
if v: print 'done'

if v: print 'parsing that page...'
total = float(lp.split(start)[1].split(end)[0] + '.0000000')

pages = total/300.0000000  # 300 results per page (its the limit)

if '.' in str(pages): # its not perfectly divisible by 300, there is an extra page with only a few results
    pages = int(pages) + 1
if v: print 'done,', pages, 'pages'
# now the interesting part, get EVERY SINGLE PAGE!!!
for pagenum in range(0, pages):
    if v: print 'starting page', pagenum + 1
    url = 'http://launchpad.net/projects/+all?start=%s&batch=300' % (pagenum * 300)
    print do_page(url)












