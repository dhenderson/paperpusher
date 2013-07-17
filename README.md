Paper Pusher
==============
Paper Pusher is a python library that automates common Excel reporting tasks. Paper Pusher can generate new transformed variable columns based on a JSON reporting schema, and report simple summaries and whether arbitrary thresholds were or were not met for given variable values.

Dependencies
--------------------------
Python 3+
xlrd
pandas

License
-------------------
MIT. Do what you want.

Usage scenarios
-------------------------
I work in the socail sector where there are a *lot* of reporting requirements (funders, government entities, etc.). I developed Paper Pusher to ease automation of common reporting tasks.

Paper Pusher is most effective in situations where an entity recieves or updates a spreadsheet with the same column headers and needs to report some outcomes from that spreadsheet regularly. While I intend this system to be used in the social sector, Paper Pusher could just as easily be used in any scenario where one needs to perform the same simple report on similarliy structured data with some frequencey.

Paper Pusher is *not* useful for advanced reporting, such as econometric modeling. However, Paper Pusher can be used to cleanup Excel data and transform variables for import into statistical packages like R.

Author
------------
David Henderson
fullcontactphilanthropy.com