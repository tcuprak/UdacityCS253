# Udacity 253  Unit 2 Homework 2

# Implement a web form that validates username, password and email

# Theresa Cuprak
# Aug 24, 2012

import webapp2
import cgi
import re

#----------------------------------------- view layer code


signup_form='''
<html>
  <head>
    <title>Udacity 253 Unit2 Homework 2 -- Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: blue}
    </style>
  </head>

  <body>
    <h2>Udacity 253 Unit2 Homework 2 -- Sign Up</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(username_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td class="error">
            %(password_error)s
          </td>
            
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(verify)s">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>
</html>
'''

#----------------------------------------- controller layer code

# main request handler and entrance into app  
class SignupHandler(webapp2.RequestHandler):

    def write_form(self, username="", password="", verify="", email="", username_error="", password_error="", verify_error="", email_error=""):
        self.response.out.write(signup_form % {"username" : username,
                                                "password" : password,
                                                "verify" : verify,
                                                "email" : email,
                                                "username_error" : username_error,
                                                "password_error" : password_error,
                                                "verify_error" : verify_error,
                                                "email_error" : email_error})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        escaped_username = escape_html(user_username)
        escaped_password = escape_html(user_password)
        escaped_verify = escape_html(user_verify)
        escaped_email = escape_html(user_email)

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        # Assume we are error free, then go through each validator
        error = False
        if not valid_username(user_username):
            username_error = "That's not a valid username."
            error = True

        if not valid_password(user_password):
            password_error = "That wasn't a valid password."
            escaped_password =""
            escaped_verify =""
            error = True

        if not (user_password == user_verify):
            verify_error = "Your passwords didn't match."
            escaped_password =""
            escaped_verify =""
            error = True

        if not valid_email(user_email):
            email_error = "That's not a valid email."
            error = True

        if error:
            self.write_form(escaped_username, escaped_password, escaped_verify, escaped_email, username_error, password_error, verify_error, email_error)
        else:
            self.redirect("/welcome?username=%s" % user_username)

class WelcomeHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("Welcome, %s!" % self.request.get("username"))


# this line provides mapping between URLs and request handler code
# don't know what the debug flag is for
app = webapp2.WSGIApplication([('/signup', SignupHandler), ('/welcome', WelcomeHandler)],debug=True)

#----------------------------------------- application/service layer code

# cgi package provides code to correctly escape HTML Symbols    
def escape_html(s):
      return cgi.escape(s, quote=True)

# regular expressions provided in Udacity lesson     
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

# validation code
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return (email=="") or EMAIL_RE.match(email)