import django_tables2 as tables


class PurchaseOrderTable(tables.Table):
    id = tables.Column(visible=False)
    order_number = tables.Column(verbose_name="Order Number")
    status = tables.TemplateColumn(template_name='purchase_order/status.html', orderable=False,
                          verbose_name='Status')
    entry_date = tables.Column(verbose_name="Entry Date")
    vendor_id = tables.Column(verbose_name="Vendor")
    inventory_id = tables.Column(verbose_name="Inventory")
    amount = tables.Column(verbose_name="Amount")
    purpose = tables.Column(verbose_name="Description")

    actions = tables.TemplateColumn(template_name='purchase_order/table_actions.html', orderable=False)

    class Meta:
        attrs = {"class": "table table-vcenter card-table"}
