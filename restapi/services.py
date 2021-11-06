import requests
from .models import *
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .serializer import *

def check_black_lists(uin):
    black_list = BlackList.objects.filter(uin=uin)
    if len(black_list) > 0:
        return f"Заемщик в черном списке"
    

def check_amount_age(amount, borrower_uin, programm):
    age = get_different_year(borrower_uin)
    if amount < programm.min_credit or amount > programm.max_credit:
        return f"Заявка не подходит по сумме"
    elif age < programm.min_age or age > programm.max_age:
        return f"Заемщик не подходит по возрасту"


def check_uin(uin):
    res = requests.get(f"https://stat.gov.kz/api/juridical/counter/api/?bin={uin}&lang=ru")
    if res.status_code == 200:
        data = res.json()
        if data["success"]:
            return f"иин является ИП"


def get_different_year(borrower_uin):
    year_, month_, day_ = (borrower_uin[:2],int(borrower_uin[2:4]), int(borrower_uin[4:6]))
    temp_year = int(year_)
    if temp_year > 21:
        year_ = str(temp_year )
        year_ = int("19"+year_)
    if temp_year < 21:
        year_ = str(temp_year )
        year_ = int("20"+year_)
    
    start = datetime(year=year_, month=month_, day=day_)
    end = datetime.today()
    age = relativedelta(end, start)
    return age.years


def create_application_service(uin, programm_name, amount):
    app = dict()
    def create_app_dict(reason,status,amount_,borrower_id,programm_id):
        app["rejection_reason"] = reason
        app["status"] = status
        app["amount"] = amount_
        app["borrower"] = borrower_id
        app["programm"] = programm_id
    
    borrower = Borrower.objects.get(uin=uin)
    programm = Programm.objects.get(name=programm_name)

    if result := check_amount_age(amount, borrower.uin, programm):
        create_app_dict(result, "отказ", amount, borrower.id, programm.id)
    elif result := check_black_lists(uin):
        create_app_dict(result, "отказ",amount, borrower.id, programm.id)
    elif result := check_uin(uin):
        create_app_dict(result, "отказ", amount, borrower.id, programm.id)
    else:
        create_app_dict(None, "одобрено", amount, borrower.id, programm.id)
    
    serializer = ApplicationSerializer(data=app)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, 201
    else:
        return {"error": "serializer is not valid"}, 500
    

def get_applications_service():
    applications = Application.objects.all()
    serializer = ApplicationSerializer(applications,many=True)  
    return serializer.data