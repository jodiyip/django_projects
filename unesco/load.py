import csv

from home.models import Site, Category, Iso, Region, States

fh = open('whc-sites-2018-small.csv')
rows = csv.reader(fh)
next(rows, None)
Site.objects.all().delete()
Category.objects.all().delete()
Iso.objects.all().delete()
Region.objects.all().delete()
States.objects.all().delete()

for row in rows:
    try:
        c = Category.objects.get(name=row[7])
    except:
        print("Inserting category",row[7])
        c = Category(name=row[7])
        c.save()

    try:
        i = Iso.objects.get(name=row[10])
    except:
        print("Inserting iso",row[10])
        i = Iso(name=row[10])
        i.save()

    try:
        r = Region.objects.get(name=row[9])
    except:
        print("Inserting region",row[9])
        r = Region(name=row[9])
        r.save()

    try:
        s = States.objects.get(name=row[8])
    except:
        print("Inserting states",row[8])
        s = States(name=row[8])
        s.save()

    try:
        year = int(row[3])
    except:
        year = None

    try:
        longitude = float(row[4])
    except:
        longitude = None

    try:
        latitude = float(row[5])
    except:
        latitude = None

    try:
        area = float(row[6])
    except:
        area = None

    site = Site(category=c, iso=i, region=r, states=s, year=year, longitude=longitude, latitude=latitude, area_hectare=area)
    site.save()