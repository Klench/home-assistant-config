entity_id = data.get('entity_id')
target_volume = float(data.get('volume_level'))
set_group_volume = bool(data.get('set_group_volume'))
volume_increment = 0.003

if set_group_volume:
  entity_id_list = hass.states.get(entity_id).attributes['sonos_group']
else:
  entity_id_list = [entity_id]

entity_current_volume_list = []
entity_volume_is_set_list = []

for entity_id in entity_id_list:
  entity_current_volume_list.append(hass.states.get(entity_id).attributes['volume_level'])
  entity_volume_is_set_list.append(False)

while not all(entity_volume_is_set_list):

  for i in range(len(entity_id_list)):

    volume_diff = target_volume - entity_current_volume_list[i]

    if abs(volume_diff) <= volume_increment:
      entity_volume_is_set_list[i] = True
      service_data = {"entity_id": entity_id_list[i], "volume_level": target_volume}
      hass.services.call("media_player", "volume_set", service_data)
      continue

    volume_diff_sign = volume_diff/abs(volume_diff)
    new_volume = entity_current_volume_list[i] + volume_increment * volume_diff_sign

    service_data = {"entity_id": entity_id_list[i], "volume_level": new_volume}
    hass.services.call("media_player", "volume_set", service_data)

    entity_current_volume_list[i] = new_volume

  time.sleep(.01)