# [Blessdle](https://ufcdle.netlify.app/)
A UFC spinoff to the popular game Wordle built with Flask, SQLite, and React. Named after the BMF Max "Blessed" Holloway.

[Contact](https://forms.gle/PtpfrbGeQzEm6CWz9) 

## About

New fighter and bonus stats are released daily at midnight (EST).
Users have 8 tries to guess the daily UFC fighter. 
* Green indicates an exact match.
* Yellow indicates a close match where:
  * Wins, losses, age, or height are off by at most 3 (years, inches, etc.).
  * Weight class is adjacent to the solution (ex: LW < WW < MW)
  * Bonus Stat is off by at most 5

*Possible Bonus Stats: KO/TKO win %, submission win %, strike accuracy %, strike defense %, takedown defense %.*
