# Copyright (c) 2026, admin and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model import docstatus


def execute(filters: dict | None = None):
	columns = get_columns(filters)
	data = get_data(filters)
	chart=get_chart(data)
	summary=get_summary(data)

	return columns, data, chart, summary


def get_columns(filters):
	cols=[{
		"fieldname": "technician",
		"label": _("Technician"),
		"width": 200,
		"fieldtype": "Link",
		"options": "Technician",
	},
	{
		"fieldname":"total_jobs",
		"label": _("Total Jobs"),
		"width": 150,
		"fieldtype": "Int",
	},
	{
		"fieldname":"completed",
		"label": _("Completed"),
		"width": 150,
		"fieldtype": "Int",
	},
	{
		"fieldname":"avg_turnaround",
		"label": _("Avg Turnaround Time Days"),
		"width": 150,
		"fieldtype": "Float",
	},
	{
		"fieldname":"revenue",
		"label": _("Revenue"),
		"width": 150,
		"fieldtype": "Currency",
	},
	{
		"fieldname":"completion_rate",
		"label": _("Completion Rate %"),
		"width": 150,
		"fieldtype": "Percent",
	}
	]
	for dt in frappe.get_all("Device Type",fields=["name"]):
		cols.append({
			"fieldname": dt.name,
			"label": _(dt.name),
			"width": 150,
			"fieldtype": "Int",
		})
	return cols


def get_data(filters):

    conditions = {}

    if filters.get("technician"):
        conditions["assigned_technician"] = filters["technician"]

    jobs = frappe.get_list("Job Card",filters=conditions,fields=["assigned_technician", "device_type","status","creation","delivery_date", "final_amount",])
    result = {}
    device_types = [d.name for d in frappe.get_all("Device Type", fields=["name"])]
    for j in jobs:
        tech = j.assigned_technician
        if not tech:
            continue
        if tech not in result:
            result[tech] = {
                "technician": tech,
                "total_jobs": 0,
                "completed": 0,
                "avg_turnaround": 0,
                "revenue": 0,
            }
            for dt in device_types:
                result[tech][dt.lower().replace(" ", "_")] = 0
        result[tech]["total_jobs"] += 1

        # device type count
        if j.device_type:
            field = j.device_type.lower().replace(" ", "_")
            result[tech][field] += 1

        # completed jobs
        if j.status == "Delivered" and docstatus != 2:
            result[tech]["completed"] += 1
            result[tech]["revenue"] += j.final_amount or 0
            if j.delivery_date and j.creation:
                days = (j.delivery_date - j.creation.date()).days
                result[tech]["avg_turnaround"] += days

    # calculate averages and completion rate
    for tech in result:
        row = result[tech]
        if row["completed"] > 0:
            row["avg_turnaround"] = row["avg_turnaround"] / row["completed"]
        if row["total_jobs"] > 0:
            row["completion_rate"] = (row["completed"] / row["total_jobs"]) * 100
        else:
            row["completion_rate"] = 0
    return list(result.values())


def get_chart(data):
    labels = []
    total = []
    completed = []

    for d in data:
        labels.append(d["technician"])
        total.append(d["total_jobs"])
        completed.append(d["completed"])
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Total Jobs", "values": total},
                {"name": "Completed", "values": completed},
            ],
        },
        "type": "bar",
    }


def get_summary(data):
    total_jobs = sum(d["total_jobs"] for d in data)
    total_revenue = sum(d["revenue"] for d in data)
    best_performer = None
    if data:
        best_performer = max(data, key=lambda x: x["completed"])

    return [
        {"label": "Total Jobs", "value": total_jobs, "indicator": "Blue"},
        {"label": "Total Revenue", "value": total_revenue, "indicator": "Green"},
        {
            "label": "Best Technician",
            "value": best_performer["technician"] if best_performer else "",
            "indicator": "Purple",
        },
    ]