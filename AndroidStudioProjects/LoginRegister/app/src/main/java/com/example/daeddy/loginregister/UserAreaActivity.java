package com.example.daeddy.loginregister;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;
import android.content.Intent;

public class UserAreaActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_area);

        Intent intent = getIntent();
        String name = intent.getStringExtra("name");
        String Uname = intent.getStringExtra("Uname");
        String vehicle = intent.getStringExtra("vehicle");

        EditText etUname = (EditText) findViewById(R.id.etUname);
        EditText etVehicle = (EditText) findViewById(R.id.etVehicle);
        TextView welcomeMsg = (TextView) findViewById(R.id.tvWelcomMsg);

        // Display user details
        String message = name + " welcome to your user area";
        welcomeMsg.setText(message);
        etUname.setText(Uname);
        etVehicle.setText(vehicle);
    }
}
