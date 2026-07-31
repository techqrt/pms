from datetime import date, timedelta

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.response import Response

from pms_apps.common.common import Common
from pms_apps.common.dataclasses.get_all import GetAll
from pms_apps.common.utils import Utils

from pms_apps.checkin_checkout.models.check_in import CheckIn
from pms_apps.checkin_checkout.models.check_out import CheckOut
from pms_apps.checkin_checkout.models.check_out_inspection_item import CheckOutInspectionItem
from pms_apps.checkin_checkout.models.check_out_utility_reading import CheckOutUtilityReading
from pms_apps.checkin_checkout.models.check_out_key import CheckOutKey
from pms_apps.checkin_checkout.models.check_out_payment import CheckOutPayment


def _percentage(part: int, total: int) -> float:
    return round((part / total) * 100, 2) if total else 0.0


def _last_n_months(n: int) -> list:
    today = date.today()
    year, month = today.year, today.month
    months = []
    for _ in range(n):
        months.append((year, month))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return list(reversed(months))


def _month_over_month_change(queryset, date_field: str = "created_at") -> float:
    today = date.today()
    this_month = queryset.filter(**{f"{date_field}__year": today.year, f"{date_field}__month": today.month}).count()
    prev_month_date = today.replace(day=1) - timedelta(days=1)
    last_month = queryset.filter(
        **{f"{date_field}__year": prev_month_date.year, f"{date_field}__month": prev_month_date.month}
    ).count()
    if last_month == 0:
        return 100.0 if this_month else 0.0
    return round(((this_month - last_month) / last_month) * 100, 2)


class MainDashboardView:
    def __init__(self):
        self.data_summary = "Dashboard summary fetched successfully"
        self.data_pending_settlements = "Pending settlements fetched successfully"

    @Common().exception_handler
    def summary_extract(self, params: GetAll):
        with transaction.atomic():
            total_check_ins = CheckIn.objects.filter(is_active=True).count()
            pending_check_ins = CheckIn.objects.filter(is_active=True, check_in_status="Pending").count()
            total_check_outs = CheckOut.objects.filter(is_active=True).count()
            pending_check_outs = CheckOut.objects.filter(is_active=True, check_out_status="Pending").count()
            pending_settlements_amount = CheckOut.objects.filter(
                is_active=True, settlement_status="Pending"
            ).aggregate(total=Sum("total_amount"))["total"] or 0

            checked_in = CheckIn.objects.filter(is_active=True, check_in_status="Active").count()
            checked_out = CheckOut.objects.filter(is_active=True, check_out_status="Completed").count()
            status_total = checked_in + checked_out + pending_check_ins + pending_check_outs

            status_overview = {
                "checkedIn": {"count": checked_in, "percentage": _percentage(checked_in, status_total)},
                "checkedOut": {"count": checked_out, "percentage": _percentage(checked_out, status_total)},
                "pendingCheckIn": {"count": pending_check_ins, "percentage": _percentage(pending_check_ins, status_total)},
                "pendingCheckOut": {"count": pending_check_outs, "percentage": _percentage(pending_check_outs, status_total)},
            }

            months = _last_n_months(6)
            check_in_month_counts = {
                (row["check_in_date__year"], row["check_in_date__month"]): row["count"]
                for row in CheckIn.objects.filter(is_active=True, check_in_date__isnull=False)
                .values("check_in_date__year", "check_in_date__month")
                .annotate(count=Count("check_in_id"))
            }
            check_out_month_counts = {
                (row["check_out_date__year"], row["check_out_date__month"]): row["count"]
                for row in CheckOut.objects.filter(is_active=True, check_out_date__isnull=False)
                .values("check_out_date__year", "check_out_date__month")
                .annotate(count=Count("check_out_id"))
            }
            monthly_overview = [
                {
                    "month": date(year, month, 1).strftime("%b"),
                    "year": year,
                    "checkedIn": check_in_month_counts.get((year, month), 0),
                    "checkedOut": check_out_month_counts.get((year, month), 0),
                }
                for year, month in months
            ]

            data = {
                "totalCheckIns": total_check_ins,
                "pendingCheckIns": pending_check_ins,
                "totalCheckOuts": total_check_outs,
                "pendingCheckOuts": pending_check_outs,
                "pendingSettlements": pending_settlements_amount,
                "statusOverview": status_overview,
                "monthlyOverview": monthly_overview,
            }

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_summary, data=data)
        )

    @Common().exception_handler
    def pending_settlements_extract(self, params: GetAll):
        with transaction.atomic():
            from pms_apps.lead.models.lead import Lead
            from pms_apps.property.models.property_details import PropertyDetail

            query = CheckOut.objects.filter(
                is_active=True, settlement_status="Pending"
            ).order_by("-created_at")
            rows = list(query.values("check_out_id", "tenant_id", "property_id", "total_amount"))

            tenant_ids = {r["tenant_id"] for r in rows if r.get("tenant_id")}
            property_ids = {r["property_id"] for r in rows if r.get("property_id")}

            tenant_map = {
                t["lead_id"]: f"{t.get('first_name') or ''} {t.get('last_name') or ''}".strip() or None
                for t in Lead.objects.filter(lead_id__in=tenant_ids).values("lead_id", "first_name", "last_name")
            }
            detail_map = {
                d["property_id"]: d
                for d in PropertyDetail.objects.filter(property_id__in=property_ids).values(
                    "property_id", "building_name", "property_code"
                )
            }

            data_rows = []
            for row in rows:
                detail = detail_map.get(row["property_id"]) or {}
                data_rows.append({
                    "checkOutId": row["check_out_id"],
                    "tenantId": row["tenant_id"],
                    "tenantName": tenant_map.get(row["tenant_id"]),
                    "propertyId": row["property_id"],
                    "propertyName": detail.get("building_name") or detail.get("property_code"),
                    "amount": row["total_amount"],
                })

            pages = Paginator(data_rows, per_page=params.limit)
            if pages.num_pages and pages.num_pages < params.page_num:
                raise ValueError("Page limit exceed!")
            page_data = list(pages.page(params.page_num)) if pages.num_pages else []

            data = Utils.add_page_parameter(
                final_data=page_data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_pending_settlements, data=data)
        )


class CheckInDashboardView:
    def __init__(self):
        self.data_summary = "Check-In dashboard summary fetched successfully"
        self.data_upcoming = "Upcoming check-ins fetched successfully"

    @Common().exception_handler
    def summary_extract(self, params: GetAll):
        with transaction.atomic():
            base = CheckIn.objects.filter(is_active=True)
            total = base.count()

            status_counts = dict(
                base.values("check_in_status").annotate(count=Count("check_in_id"))
                .values_list("check_in_status", "count")
            )
            completed = status_counts.get("Completed", 0)
            in_progress = status_counts.get("In Progress", 0)
            pending = status_counts.get("Pending", 0)
            cancelled = status_counts.get("Cancelled", 0)

            completed_change_percentage = _month_over_month_change(
                base.filter(check_in_status="Completed"), date_field="created_at"
            )

            status_overview = {
                "completed": {"count": completed, "percentage": _percentage(completed, total)},
                "inProgress": {"count": in_progress, "percentage": _percentage(in_progress, total)},
                "pending": {"count": pending, "percentage": _percentage(pending, total)},
                "cancelled": {"count": cancelled, "percentage": _percentage(cancelled, total)},
            }

            from pms_apps.property.models.property import Property
            property_type_overview = {choice: 0 for choice, _ in Property.RENTAL_TYPE_CHOICES}
            for row in base.values("property__rental_type").annotate(count=Count("check_in_id")):
                rental_type = row["property__rental_type"] or "Unknown"
                property_type_overview[rental_type] = row["count"]

            # Best-effort mapping of the check-in workflow funnel onto existing fields;
            # there is no dedicated stage field, so each step approximates a milestone.
            workflow = {
                "visitScheduled": total,
                "inspectionCompleted": base.filter(inspection_date__isnull=False).count(),
                "agreementInProgress": base.filter(agreement_status__in=["Prepared", "Signed"]).count(),
                "companySigned": base.filter(manager_signed_on__isnull=False).count(),
                "agreementCompleted": base.filter(agreement_status="Executed").count(),
            }

            data = {
                "totalCheckIns": total,
                "completed": completed,
                "completedChangePercentage": completed_change_percentage,
                "inProgress": in_progress,
                "pending": pending,
                "cancelled": cancelled,
                "statusOverview": status_overview,
                "propertyTypeOverview": property_type_overview,
                "workflow": workflow,
            }

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_summary, data=data)
        )

    @Common().exception_handler
    def upcoming_extract(self, params: GetAll):
        with transaction.atomic():
            from pms_apps.lead.models.lead import Lead
            from pms_apps.property.models.property_details import PropertyDetail

            today = date.today()
            query = CheckIn.objects.filter(
                is_active=True, check_in_date__gte=today
            ).order_by("check_in_date")
            rows = list(query.values(
                "check_in_id", "check_in_date", "tenant_id", "property_id",
                "assigned_employee_id", "assigned_employee__name",
            ))

            tenant_ids = {r["tenant_id"] for r in rows if r.get("tenant_id")}
            property_ids = {r["property_id"] for r in rows if r.get("property_id")}

            tenant_map = {
                t["lead_id"]: f"{t.get('first_name') or ''} {t.get('last_name') or ''}".strip() or None
                for t in Lead.objects.filter(lead_id__in=tenant_ids).values("lead_id", "first_name", "last_name")
            }
            detail_map = {
                d["property_id"]: d
                for d in PropertyDetail.objects.filter(property_id__in=property_ids).values(
                    "property_id", "building_name", "property_code"
                )
            }

            data_rows = []
            for row in rows:
                detail = detail_map.get(row["property_id"]) or {}
                data_rows.append({
                    "checkInId": row["check_in_id"],
                    "checkInDate": row["check_in_date"],
                    "tenantId": row["tenant_id"],
                    "tenantName": tenant_map.get(row["tenant_id"]),
                    "propertyId": row["property_id"],
                    "propertyName": detail.get("building_name") or detail.get("property_code"),
                    "assignedEmployeeId": row["assigned_employee_id"],
                    "assignedEmployeeName": row["assigned_employee__name"],
                })

            pages = Paginator(data_rows, per_page=params.limit)
            if pages.num_pages and pages.num_pages < params.page_num:
                raise ValueError("Page limit exceed!")
            page_data = list(pages.page(params.page_num)) if pages.num_pages else []

            data = Utils.add_page_parameter(
                final_data=page_data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_upcoming, data=data)
        )


class CheckOutDashboardView:
    def __init__(self):
        self.data_summary = "Check-Out dashboard summary fetched successfully"
        self.data_upcoming = "Upcoming check-outs fetched successfully"
        self.data_widgets = "Check-Out dashboard widgets fetched successfully"

    @Common().exception_handler
    def summary_extract(self, params: GetAll):
        with transaction.atomic():
            today = date.today()
            base = CheckOut.objects.filter(is_active=True)
            total = base.count()

            status_counts = dict(
                base.values("check_out_status").annotate(count=Count("check_out_id"))
                .values_list("check_out_status", "count")
            )
            pending = status_counts.get("Pending", 0)
            completed = status_counts.get("Completed", 0)
            in_progress = (
                status_counts.get("Inspection Pending", 0)
                + status_counts.get("Approved", 0)
                + status_counts.get("Active", 0)
            )
            pending_settlements = base.filter(settlement_status="Pending").count()
            overdue = base.filter(
                check_out_date__lt=today
            ).exclude(check_out_status__in=["Completed", "Cancelled"]).count()

            status_total = completed + in_progress + pending + overdue
            status_overview = {
                "completed": {"count": completed, "percentage": _percentage(completed, status_total)},
                "inProgress": {"count": in_progress, "percentage": _percentage(in_progress, status_total)},
                "pending": {"count": pending, "percentage": _percentage(pending, status_total)},
                "overdue": {"count": overdue, "percentage": _percentage(overdue, status_total)},
            }

            # Best-effort mapping of the check-out progress funnel onto existing fields;
            # there is no dedicated stage field, so each step approximates a milestone.
            request_raised = total
            inspection = base.filter(check_out_status="Inspection Pending").count()
            repair_damage = base.filter(repair_required="Yes").exclude(
                check_out_status__in=["Completed", "Cancelled"]
            ).count()
            utility_reading = base.filter(
                check_out_id__in=CheckOutUtilityReading.objects.filter(is_active=True).values("check_out_id")
            ).exclude(check_out_status__in=["Completed", "Cancelled"]).count()
            settlement = base.filter(settlement_status__in=["Pending", "Partially Settled"]).count()

            progress = {
                "requestRaised": request_raised,
                "inspection": inspection,
                "repairAndDamage": repair_damage,
                "utilityReading": utility_reading,
                "settlement": settlement,
                "completed": completed,
                "overallProgressPercentage": _percentage(completed, total),
            }

            data = {
                "totalCheckOuts": total,
                "pendingCheckOuts": pending,
                "completedCheckOuts": completed,
                "pendingSettlements": pending_settlements,
                "overdueCheckOuts": overdue,
                "statusOverview": status_overview,
                "progress": progress,
            }

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_summary, data=data)
        )

    @Common().exception_handler
    def upcoming_extract(self, params: GetAll):
        with transaction.atomic():
            from pms_apps.lead.models.lead import Lead
            from pms_apps.property.models.property_details import PropertyDetail

            today = date.today()
            query = CheckOut.objects.filter(
                is_active=True, check_out_date__gte=today
            ).order_by("check_out_date")
            rows = list(query.values(
                "check_out_id", "check_out_date", "tenant_id", "property_id",
                "assigned_employee_id", "assigned_employee__name",
            ))

            tenant_ids = {r["tenant_id"] for r in rows if r.get("tenant_id")}
            property_ids = {r["property_id"] for r in rows if r.get("property_id")}

            tenant_map = {
                t["lead_id"]: f"{t.get('first_name') or ''} {t.get('last_name') or ''}".strip() or None
                for t in Lead.objects.filter(lead_id__in=tenant_ids).values("lead_id", "first_name", "last_name")
            }
            detail_map = {
                d["property_id"]: d
                for d in PropertyDetail.objects.filter(property_id__in=property_ids).values(
                    "property_id", "building_name", "property_code"
                )
            }

            data_rows = []
            for row in rows:
                detail = detail_map.get(row["property_id"]) or {}
                days_left = (row["check_out_date"] - today).days
                data_rows.append({
                    "checkOutId": row["check_out_id"],
                    "checkOutDate": row["check_out_date"],
                    "daysLeft": days_left,
                    "tenantId": row["tenant_id"],
                    "tenantName": tenant_map.get(row["tenant_id"]),
                    "propertyId": row["property_id"],
                    "propertyName": detail.get("building_name") or detail.get("property_code"),
                    "assignedEmployeeId": row["assigned_employee_id"],
                    "assignedEmployeeName": row["assigned_employee__name"],
                })

            pages = Paginator(data_rows, per_page=params.limit)
            if pages.num_pages and pages.num_pages < params.page_num:
                raise ValueError("Page limit exceed!")
            page_data = list(pages.page(params.page_num)) if pages.num_pages else []

            data = Utils.add_page_parameter(
                final_data=page_data,
                page_num=params.page_num,
                total_page=pages.num_pages,
                present_url=params.present_url,
                next_page_required=True if pages.num_pages != params.page_num else False,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_upcoming, data=data)
        )

    @Common().exception_handler
    def widgets_extract(self, params: GetAll):
        with transaction.atomic():
            today = date.today()
            active_check_out_ids = CheckOut.objects.filter(is_active=True).values("check_out_id")

            payments = CheckOutPayment.objects.filter(is_active=True, check_out_id__in=active_check_out_ids)
            total_pending_amount = payments.filter(status="Pending").aggregate(total=Sum("amount"))["total"] or 0
            collected_this_month = payments.filter(
                status="Paid", payment_date__year=today.year, payment_date__month=today.month
            ).aggregate(total=Sum("amount"))["total"] or 0

            damage_categories = list(
                CheckOutInspectionItem.objects.filter(
                    is_active=True, inspection_status="Issue", check_out_id__in=active_check_out_ids
                ).values("category").annotate(count=Count("check_out_inspection_item_id")).order_by("-count")
            )
            top_damage_categories = [
                {"category": row["category"], "count": row["count"]} for row in damage_categories
            ]

            utility_readings = CheckOutUtilityReading.objects.filter(
                is_active=True, check_out_id__in=active_check_out_ids
            )
            total_utility = utility_readings.count()
            paid_readings = utility_readings.filter(charges__isnull=False).count()
            pending_readings = utility_readings.filter(charges__isnull=True).count()
            other_pending = utility_readings.filter(status="Issues").count()

            keys = CheckOutKey.objects.filter(is_active=True, check_out_id__in=active_check_out_ids)
            total_keys_issued = keys.count()
            keys_returned = keys.filter(status="Returned").count()
            keys_pending = keys.filter(status="Pending").count()

            data = {
                "financialOverview": {
                    "totalPendingAmount": total_pending_amount,
                    "collectedThisMonth": collected_this_month,
                },
                "topDamageCategories": top_damage_categories,
                "utilityOverview": {
                    "totalUtility": total_utility,
                    "pendingReadings": pending_readings,
                    "paidReadings": paid_readings,
                    "otherPending": other_pending,
                },
                "keyReturnStatus": {
                    "totalKeysIssued": total_keys_issued,
                    "keysReturned": keys_returned,
                    "keysPending": keys_pending,
                },
            }

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_widgets, data=data)
        )
