If you workout at a Starting Strength Gym and use their app app.ssgyms.com/logbook to track your workouts, you can use this code and script to convert it into a comma separated values (CSV) file that you can open with Excel, Google Books, and other data analysis tools.

The first step for this is to manually visit the page on Google Chrome and File --> Save As and in the dialog box choose "Complete Webpage" and remember where you saved the html file.

Usage is to run run_logbook_parser.py with the path to the html file and desired output file.

example:
```python ./run_logbook_parser.py --logbook_html_path "/foo/bar/Starting Strength Gyms.html" --logbook_csv_output_path /foo/bar/starting_strength_logbook.csv```

You can of course, also import the functions in parsing_utils.py and use them as you wish.
