# Wifi-Statistics
This is just for show-and-tell.  Likely not something useful for anyone other than me.  I automated filling out tedious Excel sheets with 100k+ lines of Mikrotik Wireless Gateway Logs. Excel would chug and parse/calculate every line of text, send it to other sheets and do tallys of Public/Staff usage of our wireless networks.  It would take about 20 minutes per day of logs, 365 times a year.

I got extremely tired of manually copying these logs, and having my laptop chug along... and doing this 365x20mins. Also, many of these logs were blasting past Excel's theoretical row-limit.  This means that often, some of these daily tallies were probably wrong.  

So I wrote this python script to parse these logs and only put in "good" data that I wanted and discard all the other junk lines.  The fun part is with the Linux script. I take advantage of threading and can parse several sheets at once making this process even faster.

*Excel sheet not included.
