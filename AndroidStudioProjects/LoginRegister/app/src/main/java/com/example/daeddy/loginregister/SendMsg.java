package com.example.daeddy.loginregister;

import android.os.AsyncTask;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class SendMsg extends AsyncTask<String, Void, Void> {
    private Exception ex;
    @Override
    protected Void doInBackground(String... params){
        try{
            try{
                Socket socket = new Socket("10.0.2.2", 27182);
                PrintWriter outToServer = new PrintWriter(
                        new OutputStreamWriter(
                                socket.getOutputStream()));
                outToServer.print(params[0]);
                outToServer.flush();
            } catch (IOException e){
                e.printStackTrace();
            }
        } catch (Exception e){
            this.ex = e;
            return null;
        }
        return null;
    }
}
