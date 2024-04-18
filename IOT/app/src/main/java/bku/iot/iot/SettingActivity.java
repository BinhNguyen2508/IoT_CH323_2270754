package bku.iot.iot;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class SettingActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    EditText inputUpperHumi, inputLowerHumi , inputUpperLight, inputLowerLight, inputUpperTemp, inputLowerTemp;
    Button btnSubmit;
//    String username = "quocsang252/feeds";
    String username = "nbinhsdh222/feeds";
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.setting);

        inputUpperHumi = (EditText) findViewById(R.id.inputUpperHumi);
        inputLowerHumi = (EditText) findViewById(R.id.inputLowerHumi);
        inputUpperLight = (EditText) findViewById(R.id.inputUpperLight);
        inputLowerLight = (EditText) findViewById(R.id.inputLowerLight);
        inputUpperTemp = (EditText) findViewById(R.id.inputUpperTemp);
        inputLowerTemp = (EditText) findViewById(R.id.inputLowerTemp);

        btnSubmit = (Button) findViewById(R.id.btnSubmit);
        String cachedData = (String) Cache.getInstance().getData("setting");
//        System.out.println("cachedData "+ cachedData);
        if (cachedData != null) {
            String[] arrOfStr = cachedData.split(",");
            inputLowerTemp.setText(arrOfStr[0]);
            inputUpperTemp.setText(arrOfStr[1]);
            inputLowerLight.setText(arrOfStr[2]);
            inputUpperLight.setText(arrOfStr[3]);
            inputLowerHumi.setText(arrOfStr[4]);
            inputUpperHumi.setText(arrOfStr[5]);
        }
        startMQTT();
    }

    public void updateData(View view) {
//        System.out.println(";");
        String value      =  inputLowerTemp.getText().toString() + "," +
                            inputUpperTemp.getText().toString() + "," +
                            inputLowerLight.getText().toString() + "," +
                            inputUpperLight.getText().toString() + "," +
                            inputLowerHumi.getText().toString() + "," +
                            inputUpperHumi.getText().toString()
        ;
        sendDataMQTT(username+"/config",value);
        Cache.getInstance().putData("setting", value);
    }

    public void sendDataMQTT(String topic, String value)
    {
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            // Log.d("TEST", topic + "***" + msg.toString());
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        } catch (MqttException e){
            System.out.println(e);
        }
    }

    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                System.out.println("Connect");
            }

            @Override
            public void connectionLost(Throwable cause) {
                signal.error_count = "1";
                signal.adaConnect = false;
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}