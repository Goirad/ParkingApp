package com.example.daeddy.loginregister;

import java.util.ArrayList;
import java.util.List;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Spinner;
import android.view.View.OnClickListener;
import android.view.View;
import android.widget.Toast;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;

public class ParkingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_parking);

        Intent intent = getIntent();
        final String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        final String vehicle = intent.getStringExtra("vehicle");
        final int points = intent.getIntExtra("points", 0);
        final int cost = 100;
        final boolean parking = true;

        List<String> list = new ArrayList<String>();
        list.add("PG6");
        list.add("PG5");
        list.add("PG4");

        final TextView tvPoints = (TextView) findViewById(R.id.tvPoints);
        final TextView tvCost = (TextView) findViewById(R.id.tvCost);
        final Spinner spinner = (Spinner) findViewById(R.id.spinner);
        final Button btnPark = (Button) findViewById(R.id.btnPark);
        tvPoints.append(" " + points);
        tvCost.append(" " + cost);

        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item, list);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(dataAdapter);

        btnPark.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                Intent intent = new Intent(ParkingActivity.this, MatchingActivity.class);
                intent.putExtra("name", name);
                intent.putExtra("Uname", Uname);
                intent.putExtra("vehicle", vehicle);
                intent.putExtra("points", points);
                intent.putExtra("parking", parking);
                intent.putExtra("location", String.valueOf(spinner.getSelectedItem()));


                ParkingActivity.this.startActivity(intent);
            }

        });
    }
}
