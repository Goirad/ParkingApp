package com.example.daeddy.loginregister;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        final EditText etName = (EditText) findViewById(R.id.etName);
        final EditText etUname = (EditText) findViewById(R.id.etUname);
        final EditText etVehicle = (EditText) findViewById(R.id.etVehicle);
        final Button bRegister = (Button) findViewById(R.id.bRegister);

        /*!!!!*/
    }
}
