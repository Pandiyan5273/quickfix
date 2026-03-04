from quickfix.quickfix.doctype.job_card.job_card import JobCard
import frappe
class CustomJobCard(JobCard):
    def validate(self):
        super().validate()  
        self._check_urgent_unassigned()

    def _check_urgent_unassigned(self):
        if self.priority == "Urgent" and not self.assigned_technician:
            settings = frappe.get_single("Quickfix Settings")
            frappe.enqueue("quickfix.utils.send_urgent_alert",
            job_card=self.name, manager=settings.manager_email)

"""custom override for job card validation
* python use the MRO to determine the order in which methods are inherited and executed when multiple classes are invloved.
the custom jobcard extends the jobcard the pyhton will look for methods in customjob card and then move to jobcard and other parent class.

* when calling super().validate() ensures the parent validation
is executes before our custom logic ,
if we skip the super(),it may leads to break the important validations like status,other some validations...in the parent job card.
"""

"""
when to choose override_doctype_class over doc_events

in frappe there os two common ways to customize the behavior of a doctype: override_doctype_class and doc_events.
1.docevents is generally safer and it additinally added the events to existing events like validate,before_save..
2.override doctype class replaces the entire doctype class with custom class .

-use doc events for simple event-based customizations 
-use override doctype class only in deep modificaation of the doctype class behaviour is required.

"""