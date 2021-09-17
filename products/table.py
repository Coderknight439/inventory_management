import django_tables2 as tables


class ProductTable(tables.Table):
    id = tables.Column(visible=False)
    name = tables.Column(verbose_name="Name")
    code = tables.Column(verbose_name="Code")
    purchase_price = tables.Column(verbose_name="Purchase Price")
    sale_price = tables.Column(verbose_name="Sale Price")
    stock = tables.Column(verbose_name="Stock")

    actions = tables.TemplateColumn(template_name='product/table_actions.html', orderable=False)

    class Meta:
        attrs = {"class": "table table-vcenter card-table"}
