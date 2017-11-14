package com.example.daeddy.loginregister;

import android.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.content.Intent;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkError;
import com.android.volley.NoConnectionError;
import com.android.volley.ParseError;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.ServerError;
import com.android.volley.TimeoutError;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class UserAreaActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_area);

        final Button bLogout = (Button) findViewById(R.id.bLogout);
        final ProgressBar spinner = (ProgressBar)findViewById(R.id.progressBar3);
        spinner.setVisibility(View.GONE);
        Intent intent = getIntent();
        String name = intent.getStringExtra("name");
        final String Uname = intent.getStringExtra("Uname");
        String vehicle = intent.getStringExtra("vehicle");

        EditText etUname = (EditText) findViewById(R.id.etUname);
        EditText etVehicle = (EditText) findViewById(R.id.etVehicle);
        TextView welcomeMsg = (TextView) findViewById(R.id.tvWelcomMsg);

        // Display user details
        String message = name + " welcome to your user area";
        welcomeMsg.setText(message);
        etUname.setText(Uname);
        etVehicle.setText(vehicle);

        bLogout.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                final String uName = Uname;
                final String LOGOUT_REQUEST_URL = "http://10.0.2.2:27182/disconnect";
                spinner.setVisibility(View.VISIBLE);

                Response.Listener<JSONObject> responseListener = new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            spinner.setVisibility(View.INVISIBLE);
                            System.err.println("Resp");
                            JSONObject jsonResponse = response;
                            boolean success = jsonResponse.getBoolean("success");
                            if (success) {
                                Intent intent = new Intent(UserAreaActivity.this, LoginActivity.class);
                                UserAreaActivity.this.startActivity(intent);
                            } else {
                                AlertDialog.Builder builder = new AlertDialog.Builder(UserAreaActivity.this);
                                builder.setMessage("Logout Failed")
                                        .setNegativeButton("Retry", null)
                                        .create()
                                        .show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                };

                Response.ErrorListener errorListener = new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        spinner.setVisibility(View.INVISIBLE);
                        String errMsg = error.getMessage();

                        if (error instanceof TimeoutError || error instanceof NoConnectionError) {
                            errMsg = "No Connection";
                        } else if (error instanceof AuthFailureError) {
                            errMsg = "Auth Failure";
                        } else if (error instanceof ServerError) {
                            errMsg = "Server Error";
                        } else if (error instanceof NetworkError) {
                            errMsg = "Network Error";
                        } else if (error instanceof ParseError) {
                            errMsg = "Parse Error";
                        }
                        if (errMsg == null) {
                            errMsg = "Connection error!";
                        }

                        VolleyLog.e("Error: ", errMsg);

                        Toast.makeText(getApplicationContext(), errMsg,
                                Toast.LENGTH_SHORT).show();
                    }
                };

                JSONObject js = new JSONObject();
                try {
                    js.put("userID", uName);

                }catch (JSONException e) {
                    e.printStackTrace();
                }

                JsonObjectRequest request = new JsonObjectRequest(LOGOUT_REQUEST_URL, js, responseListener, errorListener);
                RequestQueue queue = Volley.newRequestQueue(UserAreaActivity.this);
                queue.add(request);
            }
        });
    }
}
