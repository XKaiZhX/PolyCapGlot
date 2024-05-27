package com.example.polycapglot.ui

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.JsonToken
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat.startActivity
import com.example.polycapglot.R
import com.example.polycapglot.services.retrofit.models.LoginData
import com.example.polycapglot.services.retrofit.models.LoginResponse
import com.example.polycapglot.services.retrofit.models.UserDataDTO
import com.example.polycapglot.ui.theme.PolyCapGlotTheme
import com.example.polycapglot.ui.viewmodel.StartSessionViewModel
import kotlinx.coroutines.launch

class StartSessionActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val viewModel = StartSessionViewModel()
            PolyCapGlotTheme {
                // A surface container using the 'background' color from the theme

                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    StartSession(viewModel)
                }
            }
        }
    }
}

fun changeActivity(context: Context, loginData: LoginResponse){
    val intent = Intent(context, MenuActivity::class.java)

    var passing = loginData

    //if(passing == null)
    //    passing = LoginResponse("Jhon Doe", "test@test.com", "")

    intent.putExtra("Username", passing.username)
    intent.putExtra("Email", passing.email)
    intent.putExtra("Token", passing.token)

    startActivity(context, intent, null)
}

fun showPrefs(context: Context) {
    var shPrefs = context.getSharedPreferences("server_ip", Context.MODE_PRIVATE)

    /*
    with(shPrefs.edit()){
        putString(context.resources.getString(R.string.server_ip_key), "test")
        apply()
    }
    */

    var defaultValue = context.resources.getString(R.string.server_ip)
    Log.i("PREFS", "changed: " + shPrefs.getString("server_ip", defaultValue))
    Log.i("PREFS", "default: " + defaultValue)
}

suspend fun loginFunction(context: Context, vm: StartSessionViewModel, email: String, password: String) : Boolean {
    val result = vm.login(email, password)

    if (result != null){
        changeActivity(context, result)
        return false
    }

    return true
}

suspend fun registerFunction(
    context: Context,
    vm: StartSessionViewModel,
    username: String,
    email: String,
    password: String
){
    val result: UserDataDTO? = vm.register(username, email, password)
    //if (result != null)
    //    changeActivity(context, result)
    //TODO: Show account already exists
}

fun isValidEmail(email: String): Boolean{
    return !email.matches(regex = Regex("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}\$"));
}

@Composable
fun Login(vm: StartSessionViewModel){

    var context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    var rememberMe by remember { mutableStateOf(false) }

    var error by remember { mutableStateOf(false) }

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Column(
        Modifier.fillMaxHeight(0.6f),
        Arrangement.SpaceEvenly,
        Alignment.CenterHorizontally
    ) {

        Text(text = "Login", fontSize = 26.sp)

        Row (
            Modifier.fillMaxWidth(0.7f),//.background(Color.Green),
            Arrangement.Start,
            Alignment.CenterVertically
        ) {
            Checkbox(checked = rememberMe, onCheckedChange = { rememberMe = it })
            Text(text = "Remember me?")
        }

        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text(text = "email") })

        TextField(
            value = password,
            onValueChange = { password = it },
            label = { Text(text = "password") },
            visualTransformation = VisualTransformation { TransformedText(
                AnnotatedString("*".repeat(it.length)),
                OffsetMapping.Identity
            ) })

        if (error){
            Text(text = "Wrong credentials")
        }
        
        Button(onClick = {
            coroutineScope.launch {
                error = loginFunction(context, vm, email, password);
                Log.i("LOGIN_F", "error value: " + error)
            }
        }) {
            Text(text = "Login")
        }
    }
}

@Composable
fun Register(vm: StartSessionViewModel){

    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }

    Column(
        Modifier.fillMaxHeight(0.6f),
        Arrangement.SpaceEvenly,
        Alignment.CenterHorizontally
    ) {

        Text(text = "Register", fontSize = 26.sp)

        TextField(
            value = username,
            onValueChange = { username = it },
            label = { Text(text = "email") }
        )

        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text(text = "email") }
        )

        TextField(
            value = password,
            onValueChange = { password = it },
            label = { Text(text = "password") },
            visualTransformation = VisualTransformation { TransformedText(
                AnnotatedString("*".repeat(it.length)),
                OffsetMapping.Identity
            ) })

        TextField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it },
            label = { Text(text = "confirm password") },
            visualTransformation = VisualTransformation { TransformedText(
                AnnotatedString("*".repeat(it.length)),
                OffsetMapping.Identity
            ) })

        Button(onClick = {
            //TODO: VALIDATE FIELDS
            if (password == confirmPassword){
                coroutineScope.launch {
                    registerFunction(context, vm, username, email, password)
                }
            }

        }) {
            Text(text = "Register")
        }
    }
}

@Composable
fun StartSession(vm: StartSessionViewModel){

    var operation by remember { mutableStateOf(true) }

    Column(
        Modifier.fillMaxSize(),
        Arrangement.SpaceAround,
        Alignment.CenterHorizontally
    ) {

        Text(text = stringResource(id = R.string.app_name), fontSize = 40.sp)

        if(operation)
            Login(vm)
        else
            Register(vm)

        Text(text = if(operation) "Don't have an account?" else "Already have an account?", Modifier.clickable { operation = !operation } )

    }
}