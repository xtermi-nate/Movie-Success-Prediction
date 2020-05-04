package com.example.frontend;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.view.textclassifier.TextSelection;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

public class MainActivity extends AppCompatActivity {

    private RequestQueue requestQueue;
    private EditText actorName1, actorName2, actorName3, director, year, budget, faceno, duration, color,c_rating, genre, lang, score, aspect_ratio;
    private Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        actorName1 = (EditText)findViewById(R.id.editText);
        actorName2 = (EditText)findViewById(R.id.editText2);
        actorName3 = (EditText)findViewById(R.id.editText3);
        director = (EditText)findViewById(R.id.editText4);
        year = (EditText)findViewById(R.id.editText5);
        budget = (EditText)findViewById(R.id.editText6);
        faceno = (EditText)findViewById(R.id.editText7);
        duration = (EditText)findViewById(R.id.editText8);
        color = (EditText)findViewById(R.id.editText9);
        c_rating = (EditText)findViewById(R.id.editText10);
        genre = (EditText)findViewById(R.id.editText11);
        lang = (EditText)findViewById(R.id.editText12);
        score = (EditText)findViewById(R.id.editText13);
        aspect_ratio = (EditText)findViewById(R.id.editText14);


        button = (Button) findViewById(R.id.button);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String data = "{"+
                        "\"actorName1\"" + "\"" + actorName1.getText().toString() + "\","+
                        "\"actorName2\"" + "\"" + actorName2.getText().toString() + "\""+
                        "\"actorName3\"" + "\"" + actorName3.getText().toString() + "\","+
                        "\"director\"" + "\"" + director.getText().toString() + "\""+
                        "\"year\"" + "\"" + year.getText().toString() + "\","+
                        "\"budget\"" + "\"" + budget.getText().toString() + "\""+
                        "\"faceno\"" + "\"" + faceno.getText().toString() + "\","+
                        "\"duration\"" + "\"" + duration.getText().toString() + "\","+
                        "\"color\"" + "\"" + color.getText().toString() + "\""+
                        "\"c_rating\"" + "\"" + c_rating.getText().toString() + "\","+
                        "\"genre\"" + "\"" + genre.getText().toString() + "\""+
                        "\"lang\"" + "\"" + lang.getText().toString() + "\""+
                        "\"score\"" + "\"" + score.getText().toString() + "\","+
                        "\"aspect_ratio\"" + "\"" + aspect_ratio.getText().toString() + "\""+
                        "}";
                Submit(data);
            }
        });
    }

    private void Submit(String data)
    {
        final String savedata= data;
        String URL="https:10.0.2.2:4000";

        requestQueue = Volley.newRequestQueue(getApplicationContext());
        StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONObject objres=new JSONObject(response);
                    Toast.makeText(getApplicationContext(),objres.toString(),Toast.LENGTH_LONG).show();


                } catch (JSONException e) {
                    Toast.makeText(getApplicationContext(),"Server Error",Toast.LENGTH_LONG).show();

                }
                //Log.i("VOLLEY", response);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                Toast.makeText(getApplicationContext(), error.getMessage(), Toast.LENGTH_SHORT).show();

                //Log.v("VOLLEY", error.toString());
            }
        }) {
            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";
            }

            @Override
            public byte[] getBody() throws AuthFailureError {
                try {
                    return savedata == null ? null : savedata.getBytes("utf-8");
                } catch (UnsupportedEncodingException uee) {
                    //Log.v("Unsupported Encoding while trying to get the bytes", data);
                    return null;
                }
            }

        };
        requestQueue.add(stringRequest);
    }
}
