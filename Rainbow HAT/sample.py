// import the RainbowHat driver
import com.google.android.things.contrib.driver.rainbowhat.RainbowHat;
// Light up the Red LED.
Gpio led = RainbowHat.openLedRed();
led.setValue(true);
// Close the device when done.
led.close();
// Display a string on the segment display.
AlphanumericDisplay segment = RainbowHat.openDisplay();
segment.setBrightness(Ht16k33.HT16K33_BRIGHTNESS_MAX);
segment.display("ABCD");
segment.setEnabled(true);
// Close the device when done.
segment.close();
// Play a note on the buzzer.
Speaker buzzer = RainbowHat.openPiezo();
buzzer.play(440);
// Stop the buzzer.
buzzer.stop();
// Close the device when done.
buzzer.close();
// Log the current temperature
Bmx280 sensor = RainbowHat.openSensor();
sensor.setTemperatureOversampling(Bmx280.OVERSAMPLING_1X);
Log.d(TAG, "temperature:" + sensor.readTemperature());
// Close the device when done.
sensor.close();
// Display the temperature on the segment display.
Bmx280 sensor = RainbowHat.openSensor();
sensor.setTemperatureOversampling(Bmx280.OVERSAMPLING_1X);
AlphanumericDisplay segment = RainbowHat.openDisplay();
segment.setBrightness(Ht16k33.HT16K33_BRIGHTNESS_MAX);
segment.display(sensor.readTemperature());
segment.setEnabled(true);
// Close the devices when done.
sensor.close();
segment.close();
// Light up the rainbow
Apa102 ledstrip = RainbowHat.openLedStrip();
ledstrip.setBrightness(31);
int[] rainbow = new int[RainbowHat.LEDSTRIP_LENGTH];
for (int i = 0; i < rainbow.length; i++) {
    rainbow[i] = Color.HSVToColor(255, new float[]{i * 360.f / rainbow.length, 1.0f, 1.0f});
}
ledstrip.write(rainbow);
// Close the device when done.
ledstrip.close();
// Detect when button 'A' is pressed.
Button button = RainbowHat.openButtonA();
button.setOnButtonEventListener(new Button.OnButtonEventListener() {
    @Override
    public void onButtonEvent(Button button, boolean pressed) {
        Log.d(TAG, "button A pressed:" + pressed);
    }
});
// Close the device when done.
button.close();
// Get native Android 'A' key events when button 'A' is pressed.
ButtonInputDriver inputDriver = RainbowHat.createButtonAInputDriver(
        KeyEvent.KEYCODE_A      // keyCode to send
);
inputDriver.register();

// In your Activity.
@Override
public boolean onKeyDown(int keyCode, KeyEvent event) {
    if (keyCode == KeyEvent.KEYCODE_A) {
        // ...
    }
    return super.onKeyDown(keyCode, event);
}
@Override
public boolean onKeyUp(int keyCode, KeyEvent event) {
    if (keyCode == KeyEvent.KEYCODE_A) {
        // ...
    }
    return super.onKeyUp(keyCode, event);
}
// Continuously report temperature.

// Register the sensor somewhere in your Activity initialization code
Bmx280SensorDriver  temperatureSensorDriver = new Bmx280SensorDriver("I2C1");
temperatureSensorDriver.registerTemperatureSensor();

// Now you can register the sensor callback for continously report temperature
final SensorManager sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
sensorManager.registerDynamicSensorCallback(new SensorManager.DynamicSensorCallback() {
    @Override
    public void onDynamicSensorConnected(Sensor sensor) {
        if (sensor.getType() == Sensor.TYPE_AMBIENT_TEMPERATURE) {
            sensorManager.registerListener(
                    new SensorEventListener() {
                        @Override
                        public void onSensorChanged(SensorEvent event) {
                            Log.i(TAG, "sensor changed: " + event.values[0]);
                        }
                        @Override
                        public void onAccuracyChanged(Sensor sensor, int accuracy) {
                            Log.i(TAG, "accuracy changed: " + accuracy);
                        }
                    },
                    sensor, SensorManager.SENSOR_DELAY_NORMAL);
        }
    }
});
