import csv

zipcodes = []
zip_to_rate_area = {}
area_rates = {}

# read in zipcodes to process
with open('slcsp.csv') as csvfile:
  reader = csv.reader(csvfile)
  # skip the headers
  next(reader, None)
  for row in reader:
    zipcodes.append(row[0])

# read in zipcode/rate area mapping
with open('zips.csv') as csvfile:
  reader = csv.reader(csvfile)
  # skip the headers
  next(reader, None)
  for row in reader:
    zip = row[0]
    state = row[1]
    rate_area = row[4]
    # only store relevant zip codes
    if zip in zipcodes:
      # if zip is in more than one rate area, leave blank
      if zip in zip_to_rate_area and zip_to_rate_area[zip] != (state, rate_area):
        zip_to_rate_area[zip] = 0
      else:
        zip_to_rate_area[zip] = (state, rate_area)

# read in plans
with open('plans.csv') as csvfile:
  reader = csv.reader(csvfile)
  # skip the headers
  next(reader, None)
  for row in reader:
    state = row[1]
    metal_level = row[2]
    rate = row[3]
    rate_area = row[4]
    # only keep silver
    if metal_level == 'Silver':
      if (state, rate_area) in area_rates:
        area_rates[(state, rate_area)].append(float(rate))
      else:
        area_rates[(state, rate_area)] = [float(rate)]


# process and show data to fill in slcsp.csv
print('zipcode', 'rate')
for zip in zipcodes:
  if zip in zip_to_rate_area and zip_to_rate_area[zip] != 0:
    rate_area_tuple = zip_to_rate_area[zip]
    if rate_area_tuple in area_rates:
      # get second lowest rate in the rate area
      area_rate_list = area_rates[rate_area_tuple]
      area_rate_list.sort()
      if len(area_rate_list) > 1:
        # list is sorted lowest to highest, so second lowest is second element
        print(f'{zip}, {area_rate_list[1]:.2f}')
        continue
  
  print(f'{zip},')
