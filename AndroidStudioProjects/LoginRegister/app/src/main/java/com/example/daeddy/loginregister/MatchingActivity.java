package com.example.daeddy.loginregister;

import android.content.Intent;
import android.os.CountDownTimer;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import java.util.concurrent.TimeUnit;

public class MatchingActivity extends AppCompatActivity {

    @Override
    public void onBackPressed() {
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
        setContentView(R.layout.activity_matching);

        //final ProgressBar loading = (ProgressBar) findViewById(R.id.progressBar);
        final Intent intent = getIntent();
        final boolean parking = intent.getBooleanExtra("parking", true);
        final String location = intent.getStringExtra("location");
        final String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        final String vehicle = intent.getStringExtra("vehicle");
        final int points = intent.getIntExtra("points", 0);

        //Todo timer placeholder
        final TextView tvTimer = (TextView) findViewById(R.id.tvTimer);
        new CountDownTimer(120000, 1000) { // adjust the milli seconds here

            public void onTick(long millisUntilFinished) {
                tvTimer.setText(""+String.format("%d min, %d sec",
                        TimeUnit.MILLISECONDS.toMinutes( millisUntilFinished),
                        TimeUnit.MILLISECONDS.toSeconds(millisUntilFinished) -
                                TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(millisUntilFinished))));
            }

            public void onFinish() {
                tvTimer.setText("No Matches!");
            }
        }.start();

        Button btnCancel = (Button) findViewById(R.id.btnCancel);
        TextView tvMatching = (TextView) findViewById(R.id.tvMatching);
        tvMatching.append(" " + location);

        //todo remove this
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            public void run() {
                // Actions to do after 10 seconds


        if(parking){

            //Todo make parking request
            //Todo on success goto matched

            //placeholder
            Intent intent2 = new Intent(MatchingActivity.this, MatchedActivity.class);
            intent2.putExtra("name", name);
            intent2.putExtra("Uname", Uname);
            intent2.putExtra("vehicle", vehicle);
            intent2.putExtra("points", points);
            intent2.putExtra("parking", parking);
            intent2.putExtra("location", location);
            intent2.putExtra("match", "placeholder Name");
            intent2.putExtra("matchVehicle", "placeholder CAR");
            intent2.putExtra("matchText", "placeholder bla bla bla bla bla bla bla");
            intent2.putExtra("waitTime", 600000);
            MatchingActivity.this.startActivity(intent2);
        }
        else{
            final String directions = intent.getStringExtra("directions");

            //Todo make leaving request
            //Todo on success goto matched

            //placeholder
            Intent intent2 = new Intent(MatchingActivity.this, MatchedActivity.class);
            intent2.putExtra("name", name);
            intent2.putExtra("Uname", Uname);
            intent2.putExtra("vehicle", vehicle);
            intent2.putExtra("points", points);
            intent2.putExtra("parking", parking);
            intent2.putExtra("location", location);
            intent2.putExtra("match", "placeholder Name");
            intent2.putExtra("matchVehicle", "placeholder CAR");
            intent2.putExtra("waitTime", 600000);
            MatchingActivity.this.startActivity(intent2);
        }

        //todo remove this
            }
        }, 3000);
        btnCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                cancel(name, vehicle, Uname, points);
            }

        });
    }

    private void cancel (String name, String vehicle, String uName, int points){
        //Todo Make cancel request

        Intent intent = new Intent(MatchingActivity.this, UserAreaActivity.class);
        intent.putExtra("name", name);
        intent.putExtra("vehicle", vehicle);
        intent.putExtra("Uname", uName);
        intent.putExtra("points", points);

        MatchingActivity.this.startActivity(intent);
    }
}
