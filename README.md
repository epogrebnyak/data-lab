Macroeconomic data sandbox

[lab.py](lab.py) can now:
- read data from local csv file 
- create pandas dataframes using Indicator class
- plot time series and saving them to Excel file

Now working:
- add df directly to Indicator class 
- groups of variables
- separate names for groups of variables

Ideas:
- Indicator() to replace KEP() class


# Database configuration for Rosstat KEP Data

- Use Factory and Dependency Injection as database wrappers
- MVC?
- SQLite

Main job:
- parse a CSV using config files 
- get this new data from CSV (possibly a generator)
- update a database using this new data 
- create pandas dataframes from a database 

```
db # database connection
s = CSV_Reader(csv_filename, config_filnames).get_stream()
DatabaseUpdater(db, s).update() 
dfa = DataframeConstructor(db, "annual").get_df()
```

