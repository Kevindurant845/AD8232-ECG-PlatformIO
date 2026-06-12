import serial

ser = serial.Serial('COM9', 115200)

print("Listening for ECG data...")

json_started = False
json_data = ""

while True:
    line = ser.readline().decode(errors='ignore').strip()
    print(line)

    if '{"ecg":[' in line:
        json_started = True

    if json_started:
        json_data += line

    if "Done!" in line:
        break

# remove "Done!"
json_data = json_data.replace("Done!", "")

with open("ecg_data.json", "w") as f:
    f.write(json_data)

print("Saved clean JSON to ecg_data.json")