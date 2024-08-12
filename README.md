# This is a fork of CanvasSync
I have attempted to implement multi-threading functionality to this script to help with the first time file sync, as the original could easily take 20+ hours if users had many courses. The only other change made was a small bugfix in which courses were iterated through when displaying them in settings, it wasn't checking if a course was "access_restricted_by_date" before attempting to load its course_code and name, which threw an error. This was fixed with a simple filter of the bad courses.


Description
-----------
CanvasSync helps students automatically synchronize modules, assignments & files located on their institutions Canvas web server
to a mirrored folder on their local computer. It traverses the folder hierarchy in Canvas from the top course level down to individual
files and creates a similar folder structure on the local computer:

![](resources/overview.png)

First, CanvasSync creates a folder hierarchy on the local computer reflecting the 'Modules' section on the Canvas server.
Files are stored in folders such as ../SyncFolder/Course/Module/SubFolder/file.txt. Both regular files, links to external
web pages as well as Canvas 'Pages' (HTML pages) representing assignments etc. may be downloaded. In addition, CanvasSync
may download Canvas assignments along with all linked files that can be found in the description of the assignment. Both
files stored on Canvas as well as external files will be detected.
Lastly, all files that do not fall into the above categories are downloaded and stored in the 'Various Files' folder.

The user may specify various settings including:
- What type of items to be synchronized (files, HTML pages, external links)
- If assignments should be synchronized
- If CanvasSync should attempt to find external files described in the assignment description

Installation
-------------
The easiest way to install and run CanvasSync is by using PIP. However for such a small fork I felt no need to publish it there, so simply install CanvasSync (main)
with:
```
pip install CanvasSync
```
Or alternatively, download the source distribution from the https://github.com/perslev/CanvasSync/tree/master/dist on GitHub
(.tar.gz for UNIX and .zip for Windows) and run the following command on the distribution file:

```
pip install CanvasSync-<VERSION>.tar.gz
```

and follow it up by pulling the changes this fork made.


Lastly, you may use the supplied setup.py file to create your own source package or built package for your system.

If you choose not to work with PIP, CanvasSync has the following dependencies that must be installed:

Dependencies
---------------
- Requests  (http://docs.python-requests.org/en/master/)
- PyCrypto  (https://pypi.python.org/pypi/pycrypto)
- py-bcrypt (http://www.mindrot.org/projects/py-bcrypt/)
- six (https://pypi.python.org/pypi/six)

Usage examples
--------------
After installation CanvasSync is launched by executing the following command in the console:

```
canvas
```

When launched without commandline arguments, CanvasSync will start synchronizing with previously specified settings or
prompt the user to enter new settings if no previous settings could be found.

Command line arguments:
-i or --info will display the currently saved settings
-s or --setup will prompt the user to reinitialize settings
-h or --help will show the help screen
-S or --sync to synchronize
-p to specify settings password (potentially dangerous)
-t to specify thread count

Setup
----------
CanvasSync uses the Canvas LMS API (https://canvas.instructure.com/doc/api/) to pull resources on the Canvas server. In
order to authenticate with the server an authentication token must be generated on the Canvas web server. This is done by
going to the 'Account' section followed by 'Settings'. Near the bottom under the 'Approved integrations' section, a new authentication
token may be generated. A token is a substitution to the familiar username-password based authentication and allows
3rd party applications such as CanvasSync to authenticate with the Canvas server API and pull resources. Please note that
by supplying an authentication token to the CanvasSync software, you allow CanvasSync to communicate with the Canvas server on
your behalf, see Disclaimer below.

The process of generating a token is illustrated below:

![](resources/auth_token.png)

The authentication token is stored in an local file encrypted using a private password. Consequently, the user must
specify the password whenever CanvasSync is launched to synchronize at a later time. Passwords and/or auth tokens are
cannot and will not be shared with third parties.

Disclaimer
----------
Please note that by using CanvasSync the user allows the software to authenticate with the Canvas server on the users
behalf. CanvasSync stores the authentication key encrypted and locally and the key is never shared with 3rd parties.
The official version of CanvasSync will only pull resources from the server and never remove or modify resources on the
server. Modified/rogue versions of the software could however use the authentication token to remove or modify
resources that the user has access to on the server on the users behalf.

CanvasSync is still in its early version and is not guaranteed to be stable.

Use this software on your own risk :-)


Additional resources
--------------------
https://www.instructure.com
https://canvas.instructure.com/doc/api/index.html
