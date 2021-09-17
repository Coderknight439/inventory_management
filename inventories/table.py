import django_tables2 as tables


class InventoryTable(tables.Table):
    id = tables.Column(visible=False)
    name = tables.Column(verbose_name="Name")
    code = tables.Column(verbose_name="Code")
    balance = tables.Column(verbose_name="Balance")

    actions = tables.TemplateColumn(template_name='inventory/table_actions.html', orderable=False)

    class Meta:
        attrs = {"class": "table table-vcenter card-table"}
