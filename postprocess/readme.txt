Need ref3 and ref3 wave reflection metrics output to input_summary *.csv and *.parquet file for data processing
Need Kt transmission metric output to input_summary *.csv and *.parquet file for data processing
These can be separate files or combined.

Added runup/overtopping, with some grace if flat trials are accidentally 
included or there is no runup or overtopping found. If you get all nans that's
an issue, and you can debug by removing the try/except to see what's triggering
the error specifically.'
