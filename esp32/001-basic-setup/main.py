from time import sleep

print("ESP32_READY")
for count in range(1, 6):
    print("count =", count)
    sleep(1)
print("DONE")
