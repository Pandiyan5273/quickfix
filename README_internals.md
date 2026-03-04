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

D1 and D2:
frappe.get_all bypasses all the permission and it fetching all the details so it is unsafe .

the permission query conditions is used to apply automatic row-level filtering to list queries so it has applied for get_list and get_list gives respect for permissions so it applies the permission_query condition and get_all does not applyies any permission_query_conditions.

E1 : Complete Job Card Lifecycle

while we calling the save in on_update it recursivly calling the save function and while calling this it may arise recursion error 

E2: autoname & Renaming

if we put merge=True it has delete already data and replce the new data it has been overridden and , if merge=false it handles proper renaming it does not loss any data while renaming and it also safer to rename the field and it safe for production side also and it update where ever the fields links.

E3-part -B

when to choose override_doctype_class over doc_events

in frappe there os two common ways to customize the behavior of a doctype: override_doctype_class and doc_events.
1.docevents is generally safer and it additinally added the events to existing events like validate,before_save..
2.override doctype class replaces the entire doctype class with custom class .

-use doc events for simple event-based customizations 
-use override doctype class only in deep modificaation of the doctype class behaviour is required.

the doc event is more safer .


F1-doc_events:
task-b:

i'll added two validate one is for priority in jobcard.py in the method validate() and i added in hooks.py inside that doc_events -> "Job Card" :path name 

it first executes the contoller method and next goes to doc_events in hooks file.


F3-asset ,jinja & website hooks:

Asset- 

app_incluse.js- this loads javascript files globally where we want to use that specifically and it also used as interface such as administrator, the main example when adding functionality to frappe desk ui such as dashboard widgets or any client scripts

web_include.js- it includes only js on website or portal pages and they are accessed by public web interface.

ex- portals,customer-features.

doctype_js- this runs only when a specific doctype form opens for an example job_card.js file activated when the doc opens.

doctype_list_js- it is used to load list view of the doc and it is an access the form control outer side.

doctype_tree_js- this is view like hierarchical doctype ex-in erp the chart of account.
it is used when doctype represents hierarchical data and is displayed using tree structure.

cache busting- when we change the js files ,the browser caches old details, so the new changes won't appear immediately after refreshing the browser it will clear and loads properly.

bench build- it compile the js and css files and it generate the new hashed file name because the code will changed so it genrated the hash .

jinja hooks- 

printformat- the frappe pass the doc automatically to print the details present in the document 

2.web pages- in web pages there is no automatic doc object is passed the data muat be passed explicitly from python controllers it contaisn custom format to print.

