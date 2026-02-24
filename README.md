### quickfix

assesment

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch HEAD
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
# quickfix

A2 - Multi-Site & Configuration :

1. Actually the site config file is used to store the db name, db password,api key,api key password like that and each site contains the separate site config file.
 
* if some secrets is shared in common_site config file it has been accessed for all sites it may creates vulnerability and may access other sites data's and may also access the api and it's secret keys and common_site_config contains general data's like background workers,gunicorn,socket.io,etc...

2. if we hit the command bench start it will goes to procfile in that file contains the web,socket.io,watch,schedule,redis cache and queue 

* the web will initialize the http port to start
* worker is used to finish a job given by redis_queue or any background jobs in developer mode it contains only one worker 
* scheduler is used to trigger the cron jobs and it queued to redis_queue at correct time to accomplish the job 
* socket.io is used to communicate the realtime without db hit first the client intimate to upgrade the socket io it goes to realtime.js and it navigate to index.js file to make the socket.io it is used realtime monitoring

if the worker is failed while do the job it will creates the log in logs/worker.error.log in this file if it is finished logs/worker.log like finished with this seconds like that all the maintained in logs but it does not affect any other jobs.