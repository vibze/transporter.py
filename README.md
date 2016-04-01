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
    helpers/     <- Put your helpers and utility functions here
    jobs/        <- This is where you jobs should sit
    logs/        <- By default logs are gonna be stored here
    config.py    <- Project configuration file
```

Take a look at configuration file and you are ready to start coding.

## Datastores
Datastore is a class that extends one of the framework's built in datasource helper classes like MySQL, PostgreSQL, CSV, etc.
Each type of datastore has it's own configuration properties.

## Jobs
Job is a module. It should either have a run function or a class with the same name as module, but camelized. The class must
implement a `run` method.

Jobs can be run using transporter cli with params that will be passed to executable function as keyword arguments.
```
transporter run jobs.sample_job period=20150501
```

## Logger
When a job is run using transporter cli you can send messages to internal logger and log will be stored in `logs` directory
in project folder under the jobs name.

Example;
```python
# file is load_data.py
from transporter import log

def run():
    log.info('Running load_data log without any parameters')
```

```
tranporter run jobs.load_data
```
Log will be stored in `logs/load_data_<timestamp>.log` file.

## Plugins
Transporter has plugins for various data sources or connections:
- CSV
- Oracle
- MySQL
- SSH

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
