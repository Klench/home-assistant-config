entity_id = data.get('entity_id')
initial_volume_level = hass.states.get(entity_id).attributes['volume_level']
volume_reference = data.get("volume_level")
volume_diff = volume_reference - initial_volume_level
volume_diff_sign = volume_diff/abs(volume_diff)

# logger.warning("Entity id: " + entity_id)
# logger.warning("Initial volume level: " + str(initial_volume_level))
# logger.warning("Volume reference: " + str(volume_reference))
# logger.warning("Volume difference: " + str(volume_diff))
# logger.warning("Volume difference sign: " + str(volume_diff_sign))

volume_increment = 0.01 * volume_diff_sign
volume_level = initial_volume_level

while ((volume_level + volume_increment < volume_reference) and (volume_diff_sign > 0)) or ((volume_level + volume_increment > volume_reference) and (volume_diff_sign < 0)):
    volume_level = volume_level + volume_increment
    service_data = {"entity_id": entity_id, "volume_level": volume_level}
    hass.services.call("media_player", "volume_set", service_data)
    time.sleep(.1)

service_data_reference = {"entity_id": entity_id, "volume_level": volume_reference}
hass.services.call("media_player", "volume_set", service_data_reference)