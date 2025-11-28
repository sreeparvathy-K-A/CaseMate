from clientapp.models import advocate_case

def pending_cases_count(request):
    if  'advocateid' in request.session:
        advocate_id = request.session['advocateid']
        count = advocate_case.objects.filter(advocate=advocate_id, status="Pending").count()
        return {'pending_cases_count': count}
    return {'pending_cases_count': 0}
