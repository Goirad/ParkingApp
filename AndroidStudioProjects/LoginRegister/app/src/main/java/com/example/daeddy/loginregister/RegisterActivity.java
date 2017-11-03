package com.example.daeddy.loginregister;

import android.app.AlertDialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;


import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.NetworkResponse;
import com.android.volley.toolbox.Volley;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;

import org.json.JSONException;
import org.json.JSONObject;

public class RegisterActivity extends AppCompatActivity {

    private EditText etName;
    private EditText etUname;
    private EditText etPassword;
    private EditText etConfirmPassword;
    private EditText etVehicle;
    private Button bRegister;
    private ProgressBar spinner;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        etName = (EditText) findViewById(R.id.etName);
        etUname = (EditText) findViewById(R.id.etUname);
        etPassword = (EditText) findViewById(R.id.etPassword);
        etConfirmPassword = (EditText) findViewById(R.id.etConfirmPassword);
        etVehicle = (EditText) findViewById(R.id.etVehicle);
        bRegister = (Button) findViewById(R.id.bRegister);
        spinner = (ProgressBar)findViewById(R.id.progressBar2);
        spinner.setVisibility(View.GONE);


        bRegister.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                final String name = etName.getText().toString();
                final String vehicle = etVehicle.getText().toString();
                final String uName = etUname.getText().toString();
                final String password = etPassword.getText().toString();
                final String confirmPassword = etConfirmPassword.getText().toString();
                final String LOGIN_REQUEST_URL = "http://10.0.2.2:27182/create";
                System.err.println("clicked!");
                spinner.setVisibility(View.VISIBLE);

                Response.Listener<JSONObject> responseListener = new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        spinner.setVisibility(View.INVISIBLE);
                        System.err.println("Resp");
                        try {
                            JSONObject jsonResponse = response;
                            boolean success = jsonResponse.getBoolean("success");
                            if (success) {
                                Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
                                RegisterActivity.this.startActivity(intent);
                            } else {
                                AlertDialog.Builder builder = new AlertDialog.Builder(RegisterActivity.this);
                                builder.setMessage("Register Failed")
                                        .setNegativeButton("Retry", null)
                                        .create()
                                        .show();
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                };

                Response.ErrorListener errorListener = new Response.ErrorListener(){
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        spinner.setVisibility(View.INVISIBLE);
                        String errMsg = error.getMessage();

                        if(errMsg == null){
                            errMsg = "Connection error!";
                        }

                        VolleyLog.e("Error: ", errMsg);

                        Toast.makeText(getApplicationContext(), errMsg,
                                Toast.LENGTH_SHORT).show();
                    }
                };

                JSONObject js = new JSONObject();

                if(checkPasswordsMatch()){
                    try {
                        js.put("name", name);
                        js.put("vehicle", vehicle);
                        js.put("userID", uName);
                        js.put("password", password);

                    }catch (JSONException e) {
                        e.printStackTrace();
                    }

                    JsonObjectRequest jsRequest = new JsonObjectRequest(LOGIN_REQUEST_URL, js, responseListener, errorListener);
                    RequestQueue queue = Volley.newRequestQueue(RegisterActivity.this);
                    queue.add(jsRequest);
                }
                else
                    spinner.setVisibility(View.INVISIBLE);
            }
        });
    }

    public boolean checkPasswordsMatch(){
        if(etPassword.getText().toString().equals(etConfirmPassword.getText().toString()))
            return true;

        Toast.makeText(getApplicationContext(), "Error: passwords do not match.", Toast.LENGTH_SHORT).show();
        return false;
    }
}
