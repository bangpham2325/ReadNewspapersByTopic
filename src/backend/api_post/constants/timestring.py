from django.utils.translation import gettext, ngettext_lazy

TIME_STRINGS = {
    'year': ngettext_lazy('%d năm', '%d năm'),
    'month': ngettext_lazy('%d tháng', '%d tháng'),
    'week': ngettext_lazy('%d tuần', '%d tuần'),
    'day': ngettext_lazy('%d ngày', '%d ngày'),
    'hour': ngettext_lazy('%d giờ', '%d giờ'),
    'minute': ngettext_lazy('%d phút', '%d phút'),
}