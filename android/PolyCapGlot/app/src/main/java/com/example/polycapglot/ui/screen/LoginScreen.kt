package com.example.polycapglot.ui.screen

import android.util.Log
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
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
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.sp
import com.example.polycapglot.ui.loginFunction
import com.example.polycapglot.ui.viewmodel.StartSessionViewModel
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(vm: StartSessionViewModel) {

    var context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    var error by remember { mutableStateOf(false) }

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Column(
        Modifier.fillMaxHeight(0.6f),
        Arrangement.SpaceEvenly,
        Alignment.CenterHorizontally
    ) {

        Text(text = "Login", fontSize = 26.sp)

        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text(text = "email") }
        )

        TextField(
            value = password,
            onValueChange = { password = it.replace("\\s".toRegex(), "") },
            label = { Text(text = "password") },
            visualTransformation = VisualTransformation { TransformedText(
                AnnotatedString("*".repeat(it.length)),
                OffsetMapping.Identity
            ) }
        )

        if (error) {
            Text(text = "Wrong credentials")
        }

        Button(onClick = {
            coroutineScope.launch {
                error = loginFunction(context, vm, email, password)
                Log.i("LOGIN_F", "error value: " + error)
            }
        }) {
            Text(text = "Login")
        }
    }
}