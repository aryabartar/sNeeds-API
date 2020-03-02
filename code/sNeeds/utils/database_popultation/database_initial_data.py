from sNeeds.apps.customAuth.models import *
from sNeeds.apps.account.models import *
from sNeeds.apps.consultants.models import *
from sNeeds.apps.store.models import *
from sNeeds.apps.carts.models import *
from sNeeds.apps.orders.models import *
from sNeeds.apps.comments.models import *
from sNeeds.apps.payments.models import *
from sNeeds.apps.userfiles.models import *
from sNeeds.apps.videochats.models import *
from sNeeds.apps.discounts.models import *
from sNeeds.apps.tickets.models import *
from sNeeds.apps.chats.models import *

User.objects.all().delete()
Country.objects.all().delete()
University.objects.all().delete()
FieldOfStudy.objects.all().delete()
ConsultantProfile.objects.all().delete()

user1 = User.objects.create_user(email="u1@g.com", password="user1234")
user1.is_admin = False
user1.set_user_type_student()

user2 = User.objects.create_user(email="u2@g.com", password="user1234")
user2.is_admin = False
user2.set_user_type_student()

# Countries -------
country_USA = Country.objects.create(
    name="آمریکا",
    slug="usa",
    picture=None
)
country_canada = Country.objects.create(
    name="کانادا",
    slug="canada",
    picture=None
)

country_UK = Country.objects.create(
    name="انگلستان",
    slug="uk",
    picture=None
)

# Universities -------
university_harvard = University.objects.create(
    name="هاروارد ",
    country=country_USA,
    description="دانشگاه هاروارد آمریکا",
    picture=None,
    slug="harvard"
)
university_mit = University.objects.create(
    name="ام آی تی ",
    country=country_USA,
    description="دانشگاه ام آی تی آمریکا",
    picture=None,
    slug="mit"
)
university_oxford = University.objects.create(
    name="آکسفورد ",
    country=country_UK,
    description="دانشگاه آکسفورد انگلستان",
    picture=None,
    slug="oxford"
)
university_cambridge = University.objects.create(
    name="کمبریج ",
    country=country_UK,
    description="دانشگاه کمبریج انگلستان",
    picture=None,
    slug="cambridge"
)
university_toronto = University.objects.create(
    name="تورنتو ",
    country=country_canada,
    description="دانشگاه تورنتو کانادا",
    picture=None,
    slug="toronto"
)

# Field of Studies -------
field_of_study_computer_engineering = FieldOfStudy.objects.create(
    name="مهندسی کامپیوتر",
    description="توضیحات رشته مهندسی کامپیوتر",
    picture=None,
    slug="computer-engineering"
)

field_of_study_computer_science = FieldOfStudy.objects.create(
    name="علوم کامپیوتر",
    description="توضیحات رشته علوم کامپیوتر",
    picture=None,
    slug="computer-science"
)

field_of_study_art = FieldOfStudy.objects.create(
    name="هنر",
    description="توضیحات رشته هنر",
    picture=None,
    slug="art"
)

# Consultants -------
user_ali_hejazi = User.objects.create_user(email="c1@g.com", password="user1234")
user_ali_hejazi.is_admin = False
user_ali_hejazi.set_user_type_consultant()
consultant_ali_hejazi = ConsultantProfile.objects.create(
    user=user_ali_hejazi,
    bio="علی فارغ التحصیل رشته های مهندسی کامپیوتر و برق ( به صورت دو رشته ای) هست و بدون آزمون ورودی و به صورت ارشد مستقیم مقطع کارشناسی ارشدش رو در دانشگاه شریف شروع کرد. یک سال بعد با گرفتن پذیرش از دانشگاه آلبرتا کانادا در رشته مهندسی برق از دانشگاه شریف انصراف داد و راهی کانادا شد.",
    profile_picture=None,
    aparat_link="https://www.aparat.com/v/vG4QC",
    resume=None,
    slug="ali-hejazi",
    active=True,
    time_slot_price=100000
)
consultant_ali_hejazi.universities.set([university_toronto, university_cambridge])
consultant_ali_hejazi.field_of_studies.set([field_of_study_computer_engineering])
consultant_ali_hejazi.countries.set([country_canada, country_USA])

user_narges_haghighati = User.objects.create_user(email="c2@g.com", password="user1234")
user_narges_haghighati.is_admin = False
user_narges_haghighati.set_user_type_consultant()
consultant_narges_haghighati = ConsultantProfile.objects.create(
    user=user_narges_haghighati,
    bio="نرگس حقیقتی، از دانشجویان مقطع کارشناسی ارشد رشته‌ی مهندسی کامپیوتر دانشگاه یورک (York) کاناداست. نرگس مقطع کارشناسی را در رشته‌ی الکترونیک دانشگاه اصفهان و کارشناسی ارشد را در رشته‌ی الکترونیک دیجیتال دانشگاه صنعتی امیرکبیر سپری کرد. نرگس در زمینه‌های مختلفی فعالیت از جمله سنسور‌های ذخیره و بازیابی داده فعالیت دارد و به‌تدریج پروژه‌ها و تحقیقاتش رو به سمت کامپیوتر سوق داد.",
    profile_picture=None,
    aparat_link="https://www.aparat.com/v/vG4QC",
    resume=None,
    slug="narges-haghighati",
    active=True,
    time_slot_price=80000
)
consultant_narges_haghighati.universities.set([university_oxford, university_mit, university_harvard])
consultant_narges_haghighati.field_of_studies.set([field_of_study_art])
consultant_narges_haghighati.countries.set([country_UK, country_USA])

# TimeSlotSales -------
time_slot_sale_ali_hejazi_no1 = TimeSlotSale.objects.create(
    consultant=consultant_ali_hejazi,
    start_time=timezone.now() + timezone.timedelta(days=1, hours=1),
    end_time=timezone.now() + timezone.timedelta(days=1, hours=2),
)
time_slot_sale_ali_hejazi_no2 = TimeSlotSale.objects.create(
    consultant=consultant_ali_hejazi,
    start_time=timezone.now() + timezone.timedelta(days=1, hours=3),
    end_time=timezone.now() + timezone.timedelta(days=1, hours=4),
)
time_slot_sale_ali_hejazi_no3 = TimeSlotSale.objects.create(
    consultant=consultant_ali_hejazi,
    start_time=timezone.now() + timezone.timedelta(days=1, hours=4),
    end_time=timezone.now() + timezone.timedelta(days=1, hours=5),
)
time_slot_sale_ali_hejazi_no4 = TimeSlotSale.objects.create(
    consultant=consultant_ali_hejazi,
    start_time=timezone.now() + timezone.timedelta(days=2, hours=0),
    end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
)
time_slot_sale_narges_haghighati_no1 = TimeSlotSale.objects.create(
    consultant=consultant_narges_haghighati,
    start_time=timezone.now() + timezone.timedelta(days=1, hours=0),
    end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
)
time_slot_sale_narges_haghighati_no2 = TimeSlotSale.objects.create(
    consultant=consultant_narges_haghighati,
    start_time=timezone.now() + timezone.timedelta(days=1, hours=1),
    end_time=timezone.now() + timezone.timedelta(days=1, hours=2),
)
time_slot_sale_narges_haghighati_no3 = TimeSlotSale.objects.create(
    consultant=consultant_narges_haghighati,
    start_time=timezone.now() + timezone.timedelta(days=2, hours=1),
    end_time=timezone.now() + timezone.timedelta(days=2, hours=2),
)

# Carts -------
cart_user1_no1 = Cart.objects.create(user=user1)
cart_user1_no1.products.set(
    [time_slot_sale_ali_hejazi_no3, time_slot_sale_ali_hejazi_no4, time_slot_sale_narges_haghighati_no1]
)
cart_user1_no2 = Cart.objects.create(user=user1)
cart_user1_no2.products.set(
    [time_slot_sale_ali_hejazi_no1, time_slot_sale_ali_hejazi_no2]
)
cart_user2_no1 = Cart.objects.create(user=user2)
cart_user2_no1.products.set(
    [time_slot_sale_narges_haghighati_no1, time_slot_sale_narges_haghighati_no2]
)

# Discount -------
ConsultantDiscount
