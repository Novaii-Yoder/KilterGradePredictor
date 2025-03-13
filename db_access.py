import sqlite3
import os
import csv

# Connect to the Kilter Board database
conn = sqlite3.connect('kilter.db')
cursor = conn.cursor()

#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#tables = cursor.fetchall()
#print("Tables in the database:", tables)

#table_name = 'climb_stats'#'products'#'holes'#'climb_stats'#'difficulty_grades'#'users'#'walls'#'placements' ##'climbs'

#cursor.execute(f"PRAGMA table_info({table_name});")
#columns = cursor.fetchall()

#print(f"Columns in {table_name}:")
#for col in columns:
#    print(col[1])  # Column name is in the second position

#cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 10')
#fetch = cursor.fetchall()

#print(fetch) 
#cursor.execute('SELECT * FROM climbs WHERE frames_count > 1 LIMIT 10')
#fetch = cursor.fetchall()

#print(fetch) 
#print(f"\n\n")









cursor.execute('SELECT uuid, name, setter_username, angle, layout_id, hsm, frames FROM climbs LIMIT 5')
#cursor.execute('SELECT id, layout_id, hole_id, set_id, default_placement_role_id FROM placements LIMIT 5')
#cursor.execute('SELECT difficulty, boulder_name, route_name, is_listed FROM difficulty_grades ') #WHERE boulder_name LIKE "%z%" LIMIT 5')
fetch = cursor.fetchall()

print(fetch) 
print(f"\n\n")

uuid, name, setter_username, angle, layout_id, hsm, frames = fetch[0]
cursor.execute(f'SELECT climb_uuid, angle, display_difficulty, benchmark_difficulty, ascensionist_count, difficulty_average, quality_average, fa_username, fa_at FROM climb_stats where climb_uuid == "{uuid}"')
fetch = cursor.fetchall()

print(fetch)
# Display the climbs
#for climb in climbs:
#    name, grade, setter, holds, hsm = climb
#    print(f"Name: {name}")
#    print(f"Grade: {grade}")
#    print(f"Setter: {setter}")
#    print(f"Holds: {holds}")
#    print(f"HSM: {hsm}\n")

def get_climb_data(cursor, climb_name = "what kind of triangle", ):
  cursor.execute(f'SELECT uuid, name, setter_username, angle, layout_id, hsm, frames FROM climbs WHERE name = "{climb_name}" AND layout_id = 1')
  fetch_climbs = cursor.fetchall()
  #print(f"Found {len(fetch_climbs)} climbs: {fetch_climbs}")
  if not fetch_climbs:
    print(f"ERROR: climb ({climb_name}) for KB1 not found")
    return []

  ret = []
  for cl in fetch_climbs:
    uuid, name, setter_username, angle, layout_id, hsm, frames = cl
    print(f"On Climb '{name}'\n")
    cursor.execute(f'SELECT * FROM climb_stats WHERE climb_uuid = "{uuid}"')
    fetch = cursor.fetchall()
    if not fetch:
      print(f"\tERROR: climb ({climb_name}) stats could not be found")
      return ret

    climb_uuid, angle, display_difficulty, benchmark_difficulty, ascensionist_count, difficulty_average, quality_average, fa_username, fa_at = fetch[0]

    cursor.execute(f'SELECT * FROM difficulty_grades WHERE difficulty = "{int(display_difficulty)}"')
    fetch = cursor.fetchall()
    if not fetch:
      print(f"\tERROR: climb ({climb_name}) difficulty ({display_difficulty}) equivalent cant be found")
      return ret

    difficulty, boulder_name, route_name, is_listed = fetch[0]

    frame = frames[1:].split("p")

    for i in range(len(frame)):
      f = frame[i]
      f = f.split("r")
      if f[1] == "12":
        f[1] = "Starting"
      if f[1] == "13":
        f[1] = "Hand"
      if f[1] == "14":
        f[1] = "Finish"
      if f[1] == "15":
        f[1] = "Feet"
      
      cursor.execute(f'SELECT * FROM placements WHERE id = {f[0]}')
      fetch = cursor.fetchall()
      if not fetch:
        printf("\tERROR: hold placements for climb ({climb_name}) can't be found")
        return ret

      _, layout_id, hole_id, set_id, default_placement_role_id = fetch[0]
      
      cursor.execute(f'SELECT * FROM holes WHERE id = {hole_id}')
      fetch = cursor.fetchall()
      if not fetch:
        printf("\tERROR: hole positions for climb ({climb_name}) can't be found")
        return ret
      _, product_id, hole_name, x, y, _, _ = fetch[0]
      f[0] = (x, y)

      frame[i] = f



    print(f"UUID:\t{uuid}\nName:\t{name}\nSetter:\t{setter_username}\nAngle:\t{angle}\nGrade: {boulder_name.split('V')[1]}\n")
    print(frame)
    ret.append((name, setter_username, angle, boulder_name.split("V")[1], frame))
  return ret

def get_all_climb_data(cursor, csv_file):
  with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Setter","Ascensionist Count", "Angle", "V Grade", "Holds"])

    cursor.execute(f'SELECT uuid, name, setter_username, angle, layout_id, hsm, frames FROM climbs WHERE layout_id = 1')
    fetch_climbs = cursor.fetchall()
    print(f"Found {len(fetch_climbs)}")
    if not fetch_climbs:
      print(f"\tERROR: climbs for KB1 not found")
      return

    for cl in fetch_climbs:
      uuid, name, setter_username, angle, layout_id, hsm, frames = cl
      print(f"On climb '{name}'")
      cursor.execute(f'SELECT * FROM climb_stats WHERE climb_uuid = "{uuid}"')
      fetch = cursor.fetchall()
      if not fetch:
        print(f"\tERROR: climb ({name}) stats could not be found")
        continue

      climb_uuid, angle, display_difficulty, benchmark_difficulty, ascensionist_count, difficulty_average, quality_average, fa_username, fa_at = fetch[0]

      if int(ascensionist_count) < 40:
        print(f"\tERROR: Climb is not well tested")
        continue

      cursor.execute(f'SELECT * FROM difficulty_grades WHERE difficulty = "{int(display_difficulty)}"')
      fetch = cursor.fetchall()
      if not fetch:
        print(f"\tERROR: climb ({name}) difficulty ({display_difficulty}) equivalent cant be found")
        continue

      difficulty, boulder_name, route_name, is_listed = fetch[0]

      frame = frames[1:].split("p")

      for i in range(len(frame)):
        f = frame[i]
        f = f.split("r")
        if f[1] == "12":
          f[1] = "Starting"
        if f[1] == "13":
          f[1] = "Hand"
        if f[1] == "14":
          f[1] = "Finish"
        if f[1] == "15":
          f[1] = "Feet"
        
        cursor.execute(f'SELECT * FROM placements WHERE id = {f[0]}')
        fetch = cursor.fetchall()
        if not fetch:
          printf("\tERROR: hold placements for climb ({name}) can't be found")
          continue 

        _, layout_id, hole_id, set_id, default_placement_role_id = fetch[0]
        
        cursor.execute(f'SELECT * FROM holes WHERE id = {hole_id}')
        fetch = cursor.fetchall()
        if not fetch:
          printf("\tERROR: hole positions for climb ({name}) can't be found")
          continue
        _, product_id, hole_name, x, y, _, _ = fetch[0]
        f[0] = (x, y)

        frame[i] = f
      
      writer.writerow([name, setter_username, ascensionist_count, angle, boulder_name.split("V")[1], frame])
      print(f"\tSuccess!")
      #print(f"UUID:\t{uuid}\nName:\t{name}\nSetter:\t{setter_username}\nAngle:\t{angle}\nGrade: {boulder_name.split('V')[1]}\n")
      #print(frame)
  return 



#cursor.execute(f'SELECT name FROM climbs LIMIT 100')
#fetch = cursor.fetchall()
#fetch = [["bump it"], []]
#ans = []
#for cl in fetch:
#print(f"\n\n\nStarting full search on one climb!\n")
#  if not cl:
#    continue
#  print(f"\nClimb: {cl[0]}\n\n", flush=True)
  
#  ans = get_climb_data(cursor, climb_name=cl[0])

#print(ans)

get_all_climb_data(cursor, "climbs_clean.csv")


# Close the connection
conn.close()
