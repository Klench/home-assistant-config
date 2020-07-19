entity_id = data.get('entity_id')
group_volume = bool(data.get('group_volume'))
target_volume = float(data.get('volume_level'))
volume_increment = 0.015

if group_volume:
  entity_id_list = hass.states.get(entity_id).attributes['sonos_group']
else:
  entity_id_list = [entity_id]

entity_volume_synced = [False] * len(entity_id_list)

while entity_volume_synced.count(False):

  for speaker_entity_id in entity_id_list:
    current_volume = hass.states.get(speaker_entity_id).attributes['volume_level']

    volume_diff = target_volume - current_volume

    if abs(volume_diff) <= volume_increment:
      entity_volume_synced[entity_id_list.index(speaker_entity_id)] = True
      service_data = {"entity_id": speaker_entity_id, "volume_level": target_volume}
      hass.services.call("media_player", "volume_set", service_data)
      continue

    volume_diff_sign = volume_diff/abs(volume_diff)
    new_volume = current_volume + volume_increment * volume_diff_sign

    service_data = {"entity_id": speaker_entity_id, "volume_level": new_volume}
    hass.services.call("media_player", "volume_set", service_data)

    time.sleep(.1)