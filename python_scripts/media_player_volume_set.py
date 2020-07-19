list_of_speaker_ids = list() # Dunno how you get these values
dict_of_speaker_bools = dict((speaker_id, False) for speaker_id in list_of_speaker_ids)

target_volume = float(data.get('volume_level'))
volume_increment = 0.015

while not all(dict_of_speaker_bools.values()):

  for speaker_id in list_of_speaker_ids:
    current_volume = hass.states.get(speaker_id).attributes['volume_level']

    volume_diff = target_volume - current_volume

    if abs(volume_diff) <= volume_increment:
      dict_of_speaker_bools[speaker_id] = True
      service_data = {"entity_id": speaker_id, "volume_level": target_volume}
      hass.services.call("media_player", "volume_set", service_data)
      continue

    volume_diff_sign = volume_diff/abs(volume_diff)
    volume_delta = volume_increment * volume_diff_sign
    new_volume = current_volume + volume_delta

    service_data = {"entity_id": speaker_id, "volume_level": new_volume}
    hass.services.call("media_player", "volume_set", service_data)

    time.sleep(.1)

