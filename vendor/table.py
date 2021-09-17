import django_tables2 as tables


class VendorTable(tables.Table):
    id = tables.Column(visible=False)
    name = tables.Column(verbose_name="Name")
    address_line_1 = tables.Column(verbose_name="Address-1")
    address_line_2 = tables.Column(verbose_name="Address-2")
    contact_number = tables.Column(verbose_name="Contact")
    email = tables.Column(verbose_name="Email")
    contact_person = tables.Column(verbose_name="Contact Person")

    actions = tables.TemplateColumn(template_name='vendor/table_actions.html', orderable=False)

    class Meta:
        attrs = {"class": "table table-vcenter card-table"}
