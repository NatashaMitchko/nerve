"""Helper function to construct SendGrid API requests when users send feedback
or reporta problem."""

import sendgrid
import os
import sendgrid.helpers.mail


def generate_feedback_request(name, email, type, user_feedback):
    """constructs request for general feedback"""
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = sendgrid.helpers.mail.Email(email, "Nerve Feedback")
    subject = type
    to_email = sendgrid.helpers.mail.Email("natasha.mitchko@gmail.com", "Natasha")

    html_string = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <!--<![endif]-->

  <!--[if (gte mso 9)|(IE)]><style type="text/css">
  table {border-collapse: collapse;}
  table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
  img {-ms-interpolation-mode: bicubic;}
  </style>
  <![endif]-->
  <style type="text/css">
  body {
    color: #626262;
  }
  body a {
    color: #0088cd;
    text-decoration: none;
  }
  p { margin: 0; padding: 0; }
  table[class="wrapper"] {
    width:100% !important;
    table-layout: fixed;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  img[class="max-width"] {
    max-width: 100% !important;
  }
  @media screen and (max-width:480px) {
    .preheader .rightColumnContent,
    .footer .rightColumnContent {
        text-align: left !important;
    }
    .preheader .rightColumnContent div,
    .preheader .rightColumnContent span,
    .footer .rightColumnContent div,
    .footer .rightColumnContent span {
      text-align: left !important;
    }
    .preheader .rightColumnContent,
    .preheader .leftColumnContent {
      font-size: 80% !important;
      padding: 5px 0;
    }
    table[class="wrapper-mobile"] {
      width: 100% !important;
      table-layout: fixed;
    }
    img[class="max-width"] {
      height: auto !important;
    }
    a[class="bulletproof-button"] {
      display: block !important;
      width: auto !important;
      font-size: 80%;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    // 2 columns
    #templateColumns{
        width:100% !important;
    }

    .templateColumnContainer{
        display:block !important;
        width:100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
  }
  </style>
  <style>
  body, p, div { font-family: helvetica,arial,sans-serif; }
</style>
  <style>
  body, p, div { font-size: 15px; }
</style>
</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 15px; font-family: helvetica,arial,sans-serif; color: #626262; background-color: #F4F4F4; color: #626262;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23F4F4F4%22%2C%22bodyfontname%22%3A%22helvetica%2Carial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23626262%22%2C%22bodylinkcolor%22%3A%22%230088cd%22%2C%22bodyfontsize%22%3A15%7D'>
  <center class="wrapper">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#F4F4F4">
      <tr><td valign="top" bgcolor="#F4F4F4" width="100%">
      <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
          <![endif]-->
            <table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23F4F4F4%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td>
                    <!--[if (gte mso 9)|(IE)]>
                      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <![endif]-->
                              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
                                <tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #626262; text-align: left;" bgcolor="#F4F4F4" width="100%" align="left">
                                  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
  <tr><td role="module-content"><p>This is the preheader text.</p></td></tr>
</table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%2234%2C23%2C34%2C23%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 34px 23px 34px 23px;" bgcolor="#ffffff"><h1 style="text-align: center;"><font color="#2d2d2d">Feedback from Nerve</font></h1>  <div style="text-align: center;">""" + "Hello, World" + """</div> </td>
</tr>
</table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A3%2C%22containerbackground%22%3A%22%2332a9d6%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 3px 0px;" bgcolor="#32a9d6"></td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A34%2C%22containerbackground%22%3A%22%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 34px 0px;" bgcolor=""></td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A3%2C%22containerbackground%22%3A%22%2332A9D6%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 3px 0px;" bgcolor="#32A9D6"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A%222%22%2C%22padding%22%3A%2248%2C34%2C17%2C34%22%2C%22containerbackground%22%3A%22%2332a9d6%22%7D'>
  <tr><td style="padding: 48px 34px 17px 34px;" bgcolor="#32a9d6">
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        
        <td align="center" valign="top" width="50%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="">  <div style="font-size: 10px; line-height: 150%; margin: 0px;">&nbsp;</div><div style="font-size: 10px; line-height: 150%; margin: 0px;">&nbsp;</div><div style="font-size: 10px; line-height: 150%; margin: 0px;"><a href="[unsubscribe]"><span style="color:#FFFFFF;">Unsubscribe</span></a><span style="color:#FFFFFF;"> | </span><a href="[Unsubscribe_Preferences]"><span style="color:#FFFFFF;">Update Preferences</span></a></div>  </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>
        <td align="center" valign="top" width="50%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="rightColumnContent" role="column-two" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor=""><div style="font-size: 10px; line-height: 150%; margin: 0px; text-align: right;"><font color="#ffffff">Nerve</font></div> </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>
        
      </tr>
    </table>
  </td></tr>
</table>

                                </tr></td>
                              </table>
                            <!--[if (gte mso 9)|(IE)]>
                          </td>
                        </td>
                      </table>
                    <![endif]-->
                    </td>
                  </tr>
                </table></td>
              </tr>
            </table>
          <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
      </table>
      <![endif]-->
      </tr></td>
      </table>
    </div>
  </center>
</body>
</html>"""

    content = sendgrid.helpers.mail.Content("text/html", "<html><body>" + html_string + "</body></html>")
    mail = sendgrid.helpers.mail.Mail(from_email, subject, to_email, content)

    # Send e-mail and get status message
    data = mail.get()
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)

# if __name__=="__main__":
#     # Do a test email
#     # generate_feedback_request("Bob", "bob@gmail.com", "Send-Feedback", "You're great!")
