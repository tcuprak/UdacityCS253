# Udacity 253  Unit 2 Homework 1

# Implement a web form that converts text to ROT13

# Theresa Cuprak
# Aug 24, 2012

import webapp2
import cgi

#----------------------------------------- view layer code

form="""
<html>
  <head>
    <title>Udacity Unit 2 Homework 1 --  Rot13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

#----------------------------------------- controller layer code

# main request handler and entrance into app  
class MainPage(webapp2.RequestHandler):
    
    def write_form(self, text=""):
        self.response.out.write(form % {"text": text})
    
    def get(self):
        self.write_form()
        

    def post(self):
        user_text = self.request.get('text')
        converted = pos13String(user_text)
        converted = escape_html(converted)
        self.write_form(converted)

# this line provides mapping between URLs and request handler code
# don't know what the debug flag is for
# NOTE: when I first submitted this to Udacity, it would not pass the 
#       grading test because I only had '/' as the path.  Worked fine
#       after I updated it to have a new path
app = webapp2.WSGIApplication([('/rot13', MainPage)],debug=True)

#----------------------------------------- application layer code

# cgi package provides code to correctly escape HTML Symbols    
def escape_html(s):
      return cgi.escape(s, quote=True)

# convert a single char to its POS13 equivalent      
def pos13SingleChar(char1):

    upperAlpha ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerAlpha = upperAlpha.lower()

    isLower=False
    initPos= upperAlpha.find(char1)
    if (initPos < 0):
      isLower=True
      initPos=lowerAlpha.find(char1)
    if initPos < 0:
      return char1  

    finalPos = (initPos + 13) % 26
    if isLower: 
      return lowerAlpha[finalPos] 
    else:
      return upperAlpha[finalPos] 

# convert an entire string to its POS13 equivalent  
# not very efficient, but saved me from looking up 
# additional Python syntax     
def pos13String(str1):
  newStr = ""
  for ch in str1:
    newStr= newStr + pos13SingleChar(ch)
  return newStr  



