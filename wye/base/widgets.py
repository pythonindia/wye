import datetime

from django import forms
from django.utils.safestring import mark_safe


class CalendarWidget(forms.TextInput):
    """
    Calender widget: It will set bootstrap datepicker for
    the specified field.
    """

    def render(self, name, value, attrs=None):
        if value is not None and value != "":
            value = self.format_date(value)

        render_str = '''
            <script type="text/javascript">
            $(function() {
                $.noConflict(true);
                $("#id_%(name)s").datepicker({
                    format: 'dd/mm/yyyy'
                 });
            });
            </script>
        ''' % {'name': name}
        rendered_input = super(CalendarWidget, self).render(name, value, attrs)
        return mark_safe(rendered_input + render_str)

    def format_date(self, date):
        if type(date) == datetime.date:
            return date.strftime('%d/%m/%Y')
        return date

    class Media:
        css = {
            'all': ('css/libs/datepicker.css',)
        }
        js = ('js/libs/jquery-2.1.4.min.js', 'js/libs/bootstrap-datepicker.js',)
