# submit.py
import cgi

form = cgi.FieldStorage()

print "Content-Type: text/html"
print
print "<html><body>"
print "<h1>Gracias por enviar su mensaje, %s!</h1>" % form["name"].value
print "</body></html>"
