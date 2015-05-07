# Transporter

Yes! It's an ETL python framework!
You can kick off a new ETL project like this
```python
transporter new loader 
```
This will create a loader directory with the following structure:
```
loader/
    datastores/  <- You configure your datastores here
    helpers/  <- Put your helpers and utility functions here
    jobs/  <- This is where you jobs should sit
    logs/  <- By default logs are gonna be stored here
    config.py  <- Project configuration file
```

Take a look at configuration file and you are ready to start coding.

## Datastores
Datastore is a class that extends one of the framework's built in datasource helper classes like MySQL, PostgreSQL, CSV, etc.
Each type of datastore has it's own configuration properties.

## Running jobs
```
transporter run jobs.sample_job period=20150501
```
Run command runs a given job with parameters.

## Scheduling jobs
```
transporter schedule add jobs.sample_job

Please enter first run date and time for this job using '2015-05-03.14:26' format
> 2015-03-04.23:00
How often do you want to run it? Enter one of: monthly / weekly / daily / hourly
> weekly
Job 'jobs.sample_job' has been scheduled to run weekly starting from 04.03.2015 at 23:00
```

## Show current schedule
```
transporter schedule

1) jobs.sample_job | weekly | last 04.03.2015 at 23:00 | next 11.03.2015 at 23:00
```

## Remove job from schedule
```
transporter schedule remove 1
Please confirm that you want to remove jobs.sample_job from a weekly schedule [y/n]
> y
Job 'jobs.sample_job' has been removed from weekly schedule. Last run was 04.03.2015 23:00.
```

## Monitoring
```
transporter monitor start
Transporter monitor operational! You can access it at 0.0.0.0:8200.
```

## Job
Job is basically a module with a run function. Transporter framework provides a number of decorators
that you can use to buff that execute function. Decorators can be applied to any function that can also
be some subjob function like cleaning up the target table or do any necessary preparations. These will be logged
like separate jobs, but transporters cli and scheduler will always look for a run command.

@transporter.catch_errors
This will catch any errors that are raised in the process of executing a job so that execution of your
badge job won't stop if one of them decides to bail out.

@transporter.monitor
This will log execution start, end and exec result in a monitor database so you can see it on the monitor web interface.

## Plugins
Transporter has plugins for various data sources:
- CSV
- XML
- XLS/XLSX
- Oracle
- MySQL
- PostgreSQL
- MS SQL

Every plugin has an `extract` method that returns a `Cargo` instance. Cargo is a list extending class that provides some
additional functionality.

```python
oltp = OLTPSystem()
cargo = oltp.extract('SELECT * FROM users')
```

Every plugin has an `load` method that takes a `Cargo` instance as its parameter.

```
bi = BIDatabase()
bi.table('users').load(cargo)

fs = CSVFileStorage()
fs.file('users.csv').load(cargo)
```

## YQMD
Transporter comes with YQMD library and that is a recommended way to handle your date work.
```
for month in Month.sequence('01.01.2014', '01.12.2014'):
    jobs.sample_job.run(month)
```
