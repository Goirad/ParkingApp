package com.example.daeddy.loginregister;

import android.content.Intent;
import android.os.CountDownTimer;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.concurrent.TimeUnit;

public class MatchedActivity extends AppCompatActivity {
    //todo polling here would be ideal...


    @Override
    public void onBackPressed() {
        //todo toaster with "canceling!"
        Intent intent = getIntent();
        final String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        final String vehicle = intent.getStringExtra("vehicle");
        final int points = intent.getIntExtra("points", 0);
        cancel(name, vehicle, Uname, points);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_matched);

        Intent intent = getIntent();
        final boolean parking = intent.getBooleanExtra("parking", true);
        final String location = intent.getStringExtra("location");
        final String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        final String vehicle = intent.getStringExtra("vehicle");
        final String match = intent.getStringExtra("match");
        final String mVehicle = intent.getStringExtra("matchVehicle");
        final int points = intent.getIntExtra("points", 0);
        final int waitTime = intent.getIntExtra("waitTime", 0);

        Button btnCancel = (Button) findViewById(R.id.btnCancel);
        Button btnConfirm = (Button) findViewById(R.id.btnConfirm);
        TextView tvMatched = (TextView) findViewById(R.id.tvMatched);
        TextView tvLocation = (TextView) findViewById(R.id.tvLocation);
        TextView tvVehicle = (TextView) findViewById(R.id.tvVehicle);
        tvMatched.append(" " + match + '!');
        tvLocation.append(" " + location);
        tvVehicle.append(" " + mVehicle);

        final TextView tvTimer = (TextView) findViewById(R.id.tvTimer);
        new CountDownTimer(waitTime, 1000) { // adjust the milli seconds here

            public void onTick(long millisUntilFinished) {
                tvTimer.setText(""+String.format("%d min, %d sec",
                        TimeUnit.MILLISECONDS.toMinutes( millisUntilFinished),
                        TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))));
            }

            public void onFinish() {
                //todo loading animation with "Failed!"
                Intent intent = getIntent();
                String name = intent.getStringExtra("name");
                String Uname = intent.getStringExtra("Uname");
                String vehicle = intent.getStringExtra("vehicle");
                int points = intent.getIntExtra("points", 0);
                Intent intent2 = new Intent(MatchedActivity.this, UserAreaActivity.class);
                intent2.putExtra("name", name);
                intent2.putExtra("vehicle", vehicle);
                intent2.putExtra("Uname", Uname);
                intent2.putExtra("points", points);

                MatchedActivity.this.startActivity(intent2);
            }
        }.start();

        if(parking){
            final String matchText = intent.getStringExtra("matchText");
            EditText etmatchText = (EditText) findViewById(R.id.etmatchText);
            etmatchText.append(" " + matchText);

        }
        else{
            EditText etmatchText = (EditText) findViewById(R.id.etmatchText);
            TextView tvParking = (TextView) findViewById(R.id.tvParking);
            etmatchText.setVisibility(View.GONE);
            tvParking.setVisibility(View.GONE);
        }

        btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                cancel(name, vehicle, Uname, points);
            }

        });
        btnConfirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //todo conf request
                //todo update points

                //goto home
                //todo toaster with "Success!"
                cancel(name, vehicle, Uname, points);
            }

        });
    }

    private void cancel (String name, String vehicle, String uName, int points){
        //Todo Make cancel request
        //todo loading animation
        Intent intent = new Intent(MatchedActivity.this, UserAreaActivity.class);
        intent.putExtra("name", name);
        intent.putExtra("vehicle", vehicle);
        intent.putExtra("Uname", uName);
        intent.putExtra("points", points);

        MatchedActivity.this.startActivity(intent);
    }
}
