from django.core.management.base import BaseCommand, CommandError
#import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time
from nhs.models import *

class Command(BaseCommand):
    help = 'polls NHS Conditions API for data'

    def handle(self, *args, **options):

        headers = {
            'subscription-key': '5c0342d6e3d94f95b3182077b37f2ec3',
        }
        
        page_count = 1 
        next_page = True

        while next_page:
            params = urllib.parse.urlencode({
                'page': str(page_count),
            })
            try:
                conn = http.client.HTTPSConnection('api.nhs.uk')
                conn.request("GET", "/conditions/?%s" % params, "{body}", headers)
                response = conn.getresponse()
                data = json.loads( response.read().decode())
                try:
                    for condition in data["significantLink"]:
                        print (json.dumps(condition["name"])[1:-1])
                        condition_obj, condition_created = NHSCondition.objects.get_or_create(
                            title = json.dumps(condition["name"])[1:-1],
                            description = json.dumps(condition["description"])[1:-1],
                            url = json.dumps(condition["url"])[1:-1]
                        )
                        for keyword in condition["mainEntityOfPage"]["keywords"]:
                            keyword_obj, keyword_created = NHSConditionKeyword.objects.get_or_create(
                                title = json.dumps(keyword)
                            )
                            keyword_obj.condition.add(condition_obj)
                            keyword_obj.save()
                except Exception as e:
                    print(e)
                    pass

                conn.close()
                time.sleep(7)
                page_count += 1
            except Exception as e:
                next_page = False
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
        