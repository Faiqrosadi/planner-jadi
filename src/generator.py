import jinja2 as j2
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from argparse import ArgumentParser, BooleanOptionalAction
'''
  %d = 01 hari
  %-d = 1
  %W = 01 minggu
  %-W = 1
  %m = 01 bulan
  %-m = 1 bulan
  %A = monday
  %Y = 2024
  %B = january
'''

def generate_html(planner_html, out_file):
  with open(out_file, 'w') as fp:
    fp.write(planner_html)

## dipanggil setiap function 
def mini_calendar_dates(month, year):
    first_day = date(year, month, 1)
    current_day = first_day - timedelta(days=first_day.weekday())

    date_list = []

    while True:
        if current_day.month == month:
            date_list.append((
                current_day.strftime('%d'),  # Use '%d' for two-digit day
                current_day.strftime('%m-%d'), 
                True,  # cur_month is always True for the current month
                current_day.strftime('W%U'),  # Week number with leading zero (from Sunday)
                current_day.strftime('%Y-W%U'), 
                first_day.strftime('%B').upper(), 
                first_day.strftime('%Y-%m'),
                first_day.strftime('%b').upper(),
                first_day.strftime('%B').lower(),
                first_day.strftime('%m'),
            ))
        
        if (current_day.month != month and current_day.weekday() == 6) or ((current_day + timedelta(days=1)).month != month and current_day.weekday() == 6):
            break
        
        current_day += timedelta(days=1)
    
    return date_list

## menyiapkan template-template yang dibangun
def build_planner(pages, j2_env: j2.Environment):
  return j2_env.get_template('full_planner.html.j2').render(pages=pages)


#bulanan -> 12 page
def build_monthly_pages(start: date, end: date, j2_env: j2.Environment):
  def build_monthly_page(cur_month, j2_template: j2.Template):
    return j2_template.render(month=cur_month, mini_cal=mini_calendar_dates(cur_month.month, cur_month.year)) 
  sidebar_bulan_list = []
  for i in range(12):
    sidebar_bulan_list.append(mini_calendar_dates(i + 1, start.year))

  cur_month = start + relativedelta(months=+0)
  month_templates = {}
  month_overview_template = j2_env.get_template('month_overview.html.j2')
  month_reflection_template = j2_env.get_template('month_reflection.html.j2')
  month_vision_template = j2_env.get_template('month_vision.html.j2')
  month_finance_template = j2_env.get_template('month_finance.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')

  while cur_month <= end:
    content = build_monthly_page(cur_month, month_overview_template)
    month_templates[cur_month.strftime('%Y-%m')+'-month-overview'] = frame_template.render(
      content=content,
      date=cur_month,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )

    content = build_monthly_page(cur_month, month_reflection_template)
    month_templates[cur_month.strftime('%Y-%m')+'-month-reflection'] = frame_template.render(
      content=content,
      date=cur_month,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )

    content =month_vision_template.render(month=cur_month, sidebar_bulan_list=sidebar_bulan_list, mini_cal=mini_calendar_dates(cur_month.month, cur_month.year))
    month_templates[cur_month.strftime('%Y-%m')+'-month-vision'] = frame_template.render(
      content=content,
      date=cur_month,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )

    content = build_monthly_page(cur_month, month_finance_template)
    month_templates[cur_month.strftime('%Y-%m')+'-month-finance'] = frame_template.render(
      content=content,
      date=cur_month,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )

    cur_month += relativedelta(months=+1)

  return month_templates


def build_annual_pages(start_year, end_year, j2_env: j2.Environment):
  def build_annual_page(year, j2_template: j2.Template):
    mini_cal_list = []
    for i in range(12):
      mini_cal_list.append(mini_calendar_dates(i + 1, year))
    return j2_template.render(year=year, mini_cal_list=mini_cal_list)

  sidebar_bulan_list = []
  for i in range(12):
    sidebar_bulan_list.append(mini_calendar_dates(i + 1, start_year.year))

  annual_template = j2_env.get_template('index.html.j2')
  calendar_template = j2_env.get_template('yearly-calendar.html.j2')
  vision_template = j2_env.get_template('yearly-vision.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  annual_templates = {}

  for year in range(start_year.year, end_year.year + 1):
    content = build_annual_page(year, annual_template)
    annual_templates['index-page'] = frame_template.render(
      content=content,
      index_page=True,
      sidebar_bulan_list=sidebar_bulan_list
    )
    content = build_annual_page(year, calendar_template)
    annual_templates['yearly-calendar'] = frame_template.render(
      content=content,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )
    content = build_annual_page(year, vision_template)
    annual_templates['yearly-vision'] = frame_template.render(
      content=content,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )
  return annual_templates

#OTHER PAGES
def build_other_pages(start:date, j2_env: j2.Environment):
  def build_other_page(j2_template: j2.Template):
    return j2_template.render()

  sidebar_bulan_list = []
  for i in range(12):
    sidebar_bulan_list.append(mini_calendar_dates(i + 1, start.year))

  def build_frame(name:str, template:j2.Template):
    content = build_other_page(template)
    annual_templates[name] = frame_template.render(
      content=content,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )

  annual_templates = {}
  skincare_template = j2_env.get_template('other_skincare.html.j2')
  cleaning_template = j2_env.get_template('other_cleaning.html.j2')
  project_template = j2_env.get_template('other_project.html.j2')
  password_template = j2_env.get_template('other_password.html.j2')
  habit_template = j2_env.get_template('other_habit.html.j2')
  account_template = j2_env.get_template('other_account.html.j2')
  album1_template = j2_env.get_template('other_album1.html.j2')
  album2_template = j2_env.get_template('other_album2.html.j2')
  album3_template = j2_env.get_template('other_album3.html.j2')
  tl1_template = j2_env.get_template('other_tl1.html.j2')
  tl2_template = j2_env.get_template('other_tl2.html.j2')
  tl3_template = j2_env.get_template('other_tl3.html.j2')
  tl4_template = j2_env.get_template('other_tl4.html.j2')
  tl5_template = j2_env.get_template('other_tl5.html.j2')
  tl6_template = j2_env.get_template('other_tl6.html.j2')
  tl7_template = j2_env.get_template('other_tl7.html.j2')
  tl8_template = j2_env.get_template('other_tl8.html.j2')
  tl9_template = j2_env.get_template('other_tl9.html.j2')
  frame_template = j2_env.get_template('frame.html.j2')
  
 
  build_frame('skincare_page', skincare_template)
  build_frame('cleaning_page', cleaning_template)
  for i in range(10):
    content = project_template.render(id='pp'+str(i+1))
    annual_templates['pp'+str(i)] = frame_template.render(
      content=content,
      index_page=False,
      sidebar_bulan_list=sidebar_bulan_list
    )
  build_frame('password_page', password_template)
  build_frame('habit_page', habit_template)
  build_frame('account-page', account_template)
  build_frame('album1-page', album1_template)
  build_frame('album2-page', album2_template)
  build_frame('album3-page', album3_template)
  build_frame('tl8-page', tl8_template)
  build_frame('tl1-page', tl1_template)
  build_frame('tl2-page', tl2_template)
  build_frame('tl3-page', tl3_template)
  build_frame('tl4-page', tl4_template)
  build_frame('tl5-page', tl5_template)
  build_frame('tl6-page', tl6_template)
  build_frame('tl7-page', tl7_template)
  build_frame('tl9-page', tl9_template)
  return annual_templates

if __name__ == "__main__":
  parser = ArgumentParser(prog='Python Planner Generator',
                          description='GoodNotes 5 Optimized PDF Planner')

  parser.add_argument('start', help='Start date in YYYY-MM-DD format')
  parser.add_argument('end', help='End date in YYYY-MM-DD format')
  parser.add_argument('--start-time', default=7, help='Start hour for daily agenda (24 hour time)')
  parser.add_argument('--end-time', default=19, help='End hour for daily agenda (24 hour time)')
  parser.add_argument('--file-suffix', default='', help='Suffix to add to output file names')
  parser.add_argument('--dark-mode', action=BooleanOptionalAction, default=False)

  args = parser.parse_args()


  env = j2.Environment(
    loader=j2.FileSystemLoader('./src/templates')
  )

  start_date = date.fromisoformat(args.start)
  end_date = date.fromisoformat(args.end)

  start_time = datetime(2022, 12, 26, args.start_time, 0, 0)
  end_time = datetime(2022, 12, 26, args.end_time, 0, 0)

  pages = []

  pages.extend(build_annual_pages(start_date, end_date, env).values())
  pages.extend(build_monthly_pages(start_date, end_date, env).values())
  pages.extend(build_other_pages(start_date, env).values())

  planner = build_planner(pages, env)

  generate_html(planner, f'./dest/index{args.file_suffix}.html')