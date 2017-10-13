package com.example.daeddy.loginregister;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;

public class UserAreaActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_area);

        final EditText etName = (EditText) findViewById(R.id.etName);
        final EditText etUname = (EditText) findViewById(R.id.etUname);
        final EditText etVehicle = (EditText) findViewById(R.id.etVehicle);
        final TextView welcomeMsg = (TextView) findViewById(R.id.tvWelcomMsg);
    }
}
