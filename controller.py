import requests
import json
from datetime import date, datetime, timedelta
PASSPORT_BRANCHES_URL = "https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branchGroups;servicePublicId=d1b043c75655a6756852ba9892255243c08688a071e3b58b64c892524f58d098"
PASSPORT_SCHEDULE_URL = "https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branches/{}/dates;servicePublicId=d1b043c75655a6756852ba9892255243c08688a071e3b58b64c892524f58d098;customSlotLength=10"
PASSPORT_DATE_SLOTS = "https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branches/{}/dates/{}/times;servicePublicId=d1b043c75655a6756852ba9892255243c08688a071e3b58b64c892524f58d098;customSlotLength=10"

class PolitiAPI:

  def __init__(self):
    self.refresh_session()
  
  def refresh_session(self):
    self.s = requests.Session()
    self.s.get("https://pass-og-id.politiet.no/timebestilling/index.html")
    self.last_refresh = datetime.now()

  def _get(self, url):
    diff = datetime.now() - self.last_refresh
    if (diff.total_seconds() / 60) > 240:
      self.refresh_session()
    return self.s.get(url)

  def get_branches(self):
    return self._get(PASSPORT_BRANCHES_URL).json()
  
  def get_schedules(self, branch_id):
    return self._get(PASSPORT_SCHEDULE_URL.format(branch_id)).json()
  
  def get_schedule_date_list(self, branch_id):
    date_list = self.get_schedules(branch_id)
    return DateFormatter.format_date_from_json_array(date_list)
    
  def get_available_time_for_date(self, branch_id, date):
    return self._get(PASSPORT_DATE_SLOTS.format(branch_id, date)).json()
    

class DateFormatter:

  @staticmethod
  def format_date_from_json_array(json_array):
    start = date.fromisoformat(json_array[0].get("date"))
    end = date.fromisoformat(json_array[-1].get("date"))
    date_range = [
      (end - timedelta(days=i)).isoformat()
      for i in range((end - start).days)
    ]
    return list(reversed(date_range))

if __name__ == '__main__':
  s = PolitiAPI()
  #print(s.getBranches())
  #print(s.getSchedule("d7b7dfe29e507f78dff90f35d540095f4d4eea1a78be9b1299b375e7ca30f227"))
  #schedules = print(s.getScheduleDateList("d7b7dfe29e507f78dff90f35d540095f4d4eea1a78be9b1299b375e7ca30f227")[0])
  print(s.get_available_time_for_date("58fd1fc0f9c3169e1d365575511cfb339c50b5db5cb26113bc95592fc9636a68", "2022-07-07"))