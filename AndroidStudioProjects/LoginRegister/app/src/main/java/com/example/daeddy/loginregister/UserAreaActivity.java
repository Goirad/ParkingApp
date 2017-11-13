package com.example.daeddy.loginregister;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.content.Intent;

// This class will serve to show the main activity after login, where the user can select a garage

public class UserAreaActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_area);

        Intent intent = getIntent();
        final String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        final String vehicle = intent.getStringExtra("vehicle");
        //final int points = intent.getStringExtra(name:"points");

        TextView welcomeMsg = (TextView) findViewById(R.id.tvWelcomMsg);
        TextView tvUname = (TextView) findViewById(R.id.tvUname);
        TextView tvPoints = (TextView) findViewById(R.id.tvPoints);
        Button toProfile = (Button) findViewById(R.id.btnProfile);

        // Display user details
        String message = "Welcome to your user area " + name + ".";
        welcomeMsg.setText(message);

        tvUname.append(" " + Uname);
        //tvPoints.append(" " + tvPoints.toString());

       toProfile.setOnClickListener(new View.OnClickListener(){
           @Override
           public void onClick(View v) {
              Intent intent = new Intent(UserAreaActivity.this, ProfileActivity.class);
               intent.putExtra("name", name);
               intent.putExtra("Uname", Uname);
               intent.putExtra("vehicle", vehicle);
               //intent.putExtra(name:"points", points);

               UserAreaActivity.this.startActivity(intent);
           };
        });
    }


}
