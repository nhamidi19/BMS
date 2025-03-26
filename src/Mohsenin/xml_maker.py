# utils.py
import xml.etree.ElementTree as ET
from django.http import HttpResponse

def convert_xml(table):
    # ایجاد ریشه XML
    root = ET.Element(table._meta.model_name)  # استفاده از نام مدل به عنوان ریشه

    # دریافت همه داده‌های مدل
    objects = table.objects.all()
    
    for obj in objects:
        # عنصر اصلی برای هر شیء
        obj_element = ET.SubElement(root, table._meta.model_name)

        # دریافت فیلدهای مدل به صورت دینامیک
        for field in table._meta.fields:
            field_name = field.name
            field_value = getattr(obj, field_name, "")
            ET.SubElement(obj_element, field_name).text = str(field_value)

    # تبدیل داده‌های XML به رشته
    tree = ET.ElementTree(root)
    response = HttpResponse(content_type='application/xml')  # تغییر نوع محتوا به application/xml
    response['Content-Disposition'] = f'attachment; filename="{table._meta.model_name}.xml"'  # تنظیم نام فایل خروجی
    tree.write(response, encoding='unicode')

    return response
