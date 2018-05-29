## Details

 *Dotfiles, Shell Scripts and SQL statements that useful to Greenplum and PostgreSQL DBA on day to day activity.
Few dotfiles I have copied from below repositories and have modified for Greenplum Database Users.*

###### https://github.com/swaroopch/dotvim :thumbsup:
###### https://github.com/mbrochh/mbrochh-dotfiles :thumbsup:

## Features:
*:one: All required environment exports*

*:two: Aliases to make work easier*

*:three: Python autocomplete for vim*

*:four: Python Script to get notified through email with waiters and blockers information if queries are in waiting state more that 10 minutes (Using gmail,outlook etc)*

*:five: Shell script to get notified through email with waiters and blockers information if queries are in waiting state more that 10 minutes (Using Unix Mail Utility)*

*:six: Shell script to archive the GPDB log files in `pg_log/YEAR/MONTH` directory*

*:seven: Greenplum Utility like logging using gplog.py from [gpdb source code.](https://github.com/greenplum-db/gpdb)*

*:eight: And More...* :blush:

## Installation:

`mkdir $HOME/git`
 
`cd $HOME/git`

`git clone https://github.com/pgyogesh/greenplum.git`

`cd greenplum`
 
`chmod +x install.sh`

`./install.sh`

*And Relax..* :relaxed:

*Don't forget to* `source ~/.bash_profile` *after installation.*

<script src="https://asciinema.org/a/119139.js" id="asciicast-119139" async></script>


