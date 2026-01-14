# Smart Home & Lighting Standards Knowledge Base

## 1. Protocols & Compatibility
### Zigbee
- **Description**: Low-power, mesh network protocol.
- **Requires Hub**: YES (e.g., Philips Hue Bridge, Amazon Echo w/ Zigbee, Samsung SmartThings).
- **Range**: ~10-20 meters indoor.
- **Pros**: Reliable, doesn't clog Wi-Fi network.
- **Cons**: Needs a bridge hardware.

### Wi-Fi
- **Description**: Connects directly to router.
- **Requires Hub**: NO.
- **Pros**: Cheap, no extra hardware.
- **Cons**: High power consumption, can congest network if >20 devices.

### Matter
- **Description**: Universal interoperability standard.
- **Requires Hub**: Yes, a "Matter Controller" (Apple HomePod, Nest Hub, etc.).
- **Key Feature**: Local control, works with Siri/Alexa/Google simultaneously.

## 2. Product Specifics: Philips Hue
- **Protocol**: Zigbee Light Link (ZLL).
- **Bluetooth Models**: Work without Bridge (phone only, limited range).
- **With Bridge**: Required for Apple HomeKit, out-of-home control, and sensors.
- **Dimming Rules**: NEVER use standard wall dimmers (will flicker/buzz). Must use Hue Dimmer Switch or App.

## 3. Lighting Norms (ISO/EN 12464-1)
- **Home Office**: Target 500 Lux on desk surface.
- **Living Room**: Target 150-300 Lux (ambient).
- **CRI (Color Rendering)**: >80 recommended.
- **Color Temp**: 2700K (Warm/Relax), 4000K (Cool/Work), 6500K (Daylight).