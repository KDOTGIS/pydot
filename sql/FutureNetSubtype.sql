UPDATE SHARED.FUTURE_NETWORK f
set SUBTYPE = 2
WHERE f.PREFIX = 'U' and
f.ADMO in ('S', 'D') and
f.DIV_UND = 'D';

UPDATE SHARED.FUTURE_NETWORK f
set SUBTYPE = 5
WHERE f.PREFIX = 'U' and
f.ADMO in ('S', 'D') and
f.DIV_UND = 'U';

UPDATE SHARED.FUTURE_NETWORK f
set SUBTYPE = 6
WHERE f.PREFIX = 'K' and
f.ADMO in ('S', 'D') and
f.DIV_UND = 'U';


select distinct div_und, prefix, ADMO, subtype from SHARED.Future_NETWORK F


1 = interstate divided state
2= US route divided state
3 = K Route divided state
4= (doesn’t equal anything)
5= US Route undivided state
6= K Route undivided state
7= Turnpike 
