package com.example.daeddy.loginregister;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class LeaveActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_leave);

        Intent intent = getIntent();
        final String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        final String vehicle = intent.getStringExtra("vehicle");
        final int points = intent.getIntExtra("points", 0);
        final int cost = 100;
        final boolean parking = false;

        List<String> list = new ArrayList<String>();
        list.add("PG6");
        list.add("PG5");
        list.add("PG4");

        final EditText etDirections = (EditText) findViewById(R.id.etDirections);
        final TextView tvPoints = (TextView) findViewById(R.id.tvPoints);
        final TextView tvCost = (TextView) findViewById(R.id.tvCost);
        final Spinner spinner = (Spinner) findViewById(R.id.spinner);
        final Button btnLeave = (Button) findViewById(R.id.btnLeave);
        tvPoints.append(" " + points);
        tvCost.append(" " + cost);

        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item, list);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(dataAdapter);

        btnLeave.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                final String directions = etDirections.getText().toString();
                Intent intent = new Intent(LeaveActivity.this, MatchingActivity.class);
                intent.putExtra("directions", directions);
                intent.putExtra("name", name);
                intent.putExtra("Uname", Uname);
                intent.putExtra("vehicle", vehicle);
                intent.putExtra("points", points);
                intent.putExtra("parking", parking);
                intent.putExtra("location", String.valueOf(spinner.getSelectedItem()));


                LeaveActivity.this.startActivity(intent);
            }

        });
    }
}
