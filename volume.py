from pycaw.pycaw import AudioUtilities

# 1. Get default audio output device (speakers/headphones)
device = AudioUtilities.GetSpeakers()

# 2. Access the volume controller directly
volume = device.EndpointVolume

# 3. Get current volume scalar (range 0.0 to 1.0)
current_vol = volume.GetMasterVolumeLevelScalar()
print(f"Current Volume: {int(current_vol * 100)}%")

# 4. Increase volume by 10% (0.10)
new_vol = min(1.0, current_vol + 0.10)  # Cap at 1.0 (100%)
volume.SetMasterVolumeLevelScalar(new_vol, None)

print(f"New Volume: {int(new_vol * 100)}%")