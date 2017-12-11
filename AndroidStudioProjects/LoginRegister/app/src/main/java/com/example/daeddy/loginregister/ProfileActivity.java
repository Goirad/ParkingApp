package com.example.daeddy.loginregister;

import android.app.AlertDialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class ProfileActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        Intent intent = getIntent();
        final EditText etName = (EditText) findViewById(R.id.etName);
        final EditText etUname = (EditText) findViewById(R.id.etUname);
        final EditText etPassword = (EditText) findViewById(R.id.etPassword);
        final EditText etConfirmPassword = (EditText) findViewById(R.id.etConfirmPassword);
        final EditText etVehicle = (EditText) findViewById(R.id.etVehicle);
        final Button btnUpdate = (Button) findViewById(R.id.btnUpdate);

        etName.setHint("Current name: " + intent.getStringExtra("name"));
        etUname.setHint("Current username: " + intent.getStringExtra("Uname"));
        etPassword.setHint("New password");
        etConfirmPassword.setHint("Confirm new password");
        etVehicle.setHint("Current vehicle: " + intent.getStringExtra("vehicle"));

        btnUpdate.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                //Update profile info if passwords match, send request to the server, then come back to menu

                final String name = etName.getText().toString();
                final String Uname = etUname.getText().toString();
                final String password = etPassword.getText().toString();
                final String confirmPassword = etConfirmPassword.getText().toString();
                final String vehicle = etVehicle.getText().toString();

                final String UPDATE_REQUEST_URL = "http://10.0.2.2:27182/update";

                Response.Listener<JSONObject> responseListener = new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            JSONObject jsonResponse = response;
                            boolean success = jsonResponse.getBoolean("success");
                            if (success) {

                                // After a successful update, go back to the user area activity
                                Intent intent = new Intent(ProfileActivity.this, UserAreaActivity.class);
                                intent.putExtra("name", name);
                                intent.putExtra("Uname", Uname);
                                intent.putExtra("vehicle", vehicle);

                                ProfileActivity.this.startActivity(intent);

                            } else {
                                AlertDialog.Builder builder = new AlertDialog.Builder(ProfileActivity.this);
                                builder.setMessage("Update Failed")
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

                    public void onErrorResponse(VolleyError error) {

                        String errMsg = error.getMessage();

                        if (errMsg == null) {
                            errMsg = "Update error!";
                        }

                        VolleyLog.e("Error: ", errMsg);

                        Toast.makeText(getApplicationContext(), errMsg,
                                Toast.LENGTH_SHORT).show();
                    }
                };

               if(checkPasswordsMatch(password,confirmPassword)){
                   JSONObject js = new JSONObject();
                   try {
                       js.put("name", name);
                       js.put("userID", Uname);
                       js.put("password", password);
                       js.put("vehicle", vehicle);
                   } catch (JSONException e) {
                       e.printStackTrace();
                   }

                   JsonObjectRequest request = new JsonObjectRequest(UPDATE_REQUEST_URL, js, responseListener, errorListener);
                   RequestQueue queue = Volley.newRequestQueue(ProfileActivity.this);
                   queue.add(request);
                }
            }
        });
    }

    public boolean checkPasswordsMatch(String s1, String s2) {
        if (s1.equals(s2))
            return true;

        Toast.makeText(getApplicationContext(), "Error: passwords do not match.", Toast.LENGTH_SHORT).show();
        return false;
    }
}
