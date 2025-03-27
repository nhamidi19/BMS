# utils.py
import xml.etree.ElementTree as ET
from django.http import HttpResponse

def convert_xml(table, objects=None):
    # ایجاد ریشه XML
    root = ET.Element(table._meta.model_name)

    # اگر اشیایی ارسال نشده یا لیست خالی است، تمام داده‌ها را بگیرید
    if objects is None or not objects.exists():
        objects = table.objects.all()

    for obj in objects:
        # ایجاد عنصر اصلی (row) برای هر شیء
        obj_element = ET.SubElement(root, "row")  # تغییر نام عنصر به "row"

        # دریافت فیلدهای مدل به صورت دینامیک
        for field in table._meta.fields:
            field_name = field.name
            field_value = getattr(obj, field_name, "")
            ET.SubElement(obj_element, field_name).text = str(field_value)
    
    # تبدیل داده‌های XML به رشته
    tree = ET.ElementTree(root)
    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="{table._meta.model_name}.xml"'
    tree.write(response, encoding='unicode')

    return response

