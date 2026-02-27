A2 - Multi-Site & Configuration :

1. Actually the site config file is used to store the db name, db password,api key,api key password like that and each site contains the separate site config file.
 
* if some secrets is shared in common_site config file it has been accessed for all sites it may creates vulnerability and may access other sites data's and may also access the api and it's secret keys and common_site_config contains general data's like background workers,gunicorn,socket.io,etc...

2. if we hit the command bench start it will goes to procfile in that file contains the web,socket.io,watch,schedule,redis cache and queue 

* the web will initialize the http port to start
* worker is used to finish a job given by redis_queue or any background jobs in developer mode it contains only one worker 
* scheduler is used to trigger the cron jobs and it queued to redis_queue at correct time to accomplish the job 
* socket.io is used to communicate the realtime without db hit first the client intimate to upgrade the socket io it goes to realtime.js and it navigate to index.js file to make the socket.io it is used realtime monitoring

if the worker is failed while do the job it will creates the log in logs/worker.error.log in this file if it is finished logs/worker.log like finished with this seconds like that all the maintained in logs but it does not affect any other jobs.


C1- Child Table Internals :

1. 4column - idx, parent,parenttype,parentfield
2. tabPart Usage Entry
3. if we delete the idx 2 in child table it automatically change the idx value like how many item contains in the child table if the item contains 2 it will create idx 1 and idx 2.

C3-Renaming task :

1.the technician name has renamed in technician doctype it will also reflect in jobcard doc also because assigned technician field has linked field so it changed, this an actual standard frappe behaviour .
2.track changes do whatever changes made in the doc it will show below in the doc and it was enable the check button track changes button in doc.
3.the unique does not allow the duplicate values in column in the table ig the the column index has unique it does not allow the duplicate values in a table .
the validate function in frappe act as before saving the form it checks all the given functions inside the validate function , Inside that it checks the example "if frappe.db.exists("Customer",{'email':"pandiyan@gmail.com"}) " if runs inside the validate function .if any error or does not exists it does not allow to save the form.