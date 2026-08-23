from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

# Get current volume (0.0 to 1.0)
current_vol = volume.GetMasterVolumeLevelScalar()

# Decrease by 10% (0.10), capped at 0.0 (0%)
new_vol = max(0.0, current_vol - 0.10)
volume.SetMasterVolumeLevelScalar(new_vol, None)

print(f"Volume decreased from {int(current_vol * 100)}% to {int(new_vol * 100)}%")