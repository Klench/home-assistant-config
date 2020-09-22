entity_id = data.get('entity_id')
target_volume = float(data.get('volume_level'))
set_group_volume = bool(data.get('set_group_volume'))
volume_increment = 0.025

if set_group_volume:
  speaker_entity_id_list = hass.states.get(entity_id).attributes['sonos_group']
else:
  speaker_entity_id_list = [entity_id]

speaker_entity_dict = {speaker_entity_id: False for speaker_entity_id in speaker_entity_id_list}

while False in speaker_entity_dict.values():

  for speaker_entity_id in speaker_entity_id_list:
    current_volume = hass.states.get(speaker_entity_id).attributes['volume_level']

    volume_diff = target_volume - current_volume

    if abs(volume_diff) <= volume_increment:
      speaker_entity_dict[speaker_entity_id] = True
      service_data = {"entity_id": speaker_entity_id, "volume_level": target_volume}
      hass.services.call("media_player", "volume_set", service_data)
      continue

    volume_diff_sign = volume_diff/abs(volume_diff)
    new_volume = current_volume + volume_increment * volume_diff_sign

    service_data = {"entity_id": speaker_entity_id, "volume_level": new_volume}
    hass.services.call("media_player", "volume_set", service_data)

  time.sleep(.05)
