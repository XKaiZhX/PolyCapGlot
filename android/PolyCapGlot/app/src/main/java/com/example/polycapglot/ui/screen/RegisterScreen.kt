package com.example.polycapglot.ui.screen

import android.content.Intent
import android.util.Patterns
import android.widget.Toast
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.polycapglot.ui.StartSessionActivity
import com.example.polycapglot.ui.registerFunction
import com.example.polycapglot.ui.viewmodel.StartSessionViewModel
import kotlinx.coroutines.launch

@Composable
fun RegisterScreen(vm: StartSessionViewModel) {

    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var confirmPasswordError by remember { mutableStateOf("") }
    var emailError by remember { mutableStateOf("") } // Add a state variable for the email error message
    var passwordError by remember { mutableStateOf("") } // Add a state variable for the password error message
    var usernameError by remember { mutableStateOf("") } // Add a state variable for the username error message

    Column(
        Modifier.fillMaxHeight(0.6f),
        Arrangement.SpaceEvenly,
        Alignment.CenterHorizontally
    ) {

        Text(text = "Register", fontSize = 26.sp)

        TextField(
            value = username,
            onValueChange = { username = it },
            label = { Text(text = "Username") },
            isError = usernameError.isNotEmpty() // Highlight the TextField if there's an error
        )

        if (usernameError.isNotEmpty()) {
            Text(
                text = usernameError,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall,
                modifier = Modifier.padding(top = 8.dp)
            )
        }

        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text(text = "Email") },
            isError = emailError.isNotEmpty(), // Highlight the TextField if there's an error
        )

        if (emailError.isNotEmpty()) {
            Text(
                text = emailError,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall,
                modifier = Modifier.padding(top = 8.dp)
            )
        }

        TextField(
            value = password,
            onValueChange = { password = it.replace("\\s".toRegex(), "") },
            label = { Text(text = "Password") },
            isError = passwordError.isNotEmpty(), // Highlight the TextField if there's an error
            visualTransformation = VisualTransformation { TransformedText(
                AnnotatedString("*".repeat(it.length)),
                OffsetMapping.Identity
            ) }
        )

        TextField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it.replace("\\s".toRegex(), "") },
            label = { Text(text = "Confirm Password") },
            isError = confirmPasswordError.isNotEmpty(), // Highlight the TextField if there's an error
            visualTransformation = VisualTransformation { TransformedText(
                AnnotatedString("*".repeat(it.length)),
                OffsetMapping.Identity
            ) }
        )

        if (confirmPasswordError.isNotEmpty()) {
            Text(
                text = confirmPasswordError,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall,
                modifier = Modifier.padding(top = 8.dp)
            )
        }

        if (passwordError.isNotEmpty()) {
            Text(
                text = passwordError,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall,
                modifier = Modifier.padding(top = 8.dp)
            )
        }

        Button(onClick = {
            // Validate email
            if (!Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
                emailError = "Invalid email address" // Set error message if email is invalid
            } else {
                emailError = "" // Clear email error if valid
            }

            // Validate username
            if (username.isEmpty()) {
                usernameError = "Username cannot be empty" // Set error message if username is empty
            } else {
                usernameError = "" // Clear username error if not empty
            }

            // Validate password
            if (password.isEmpty()) {
                passwordError = "Password cannot be empty" // Set error message if password is empty
            } else {
                passwordError = "" // Clear password error if not empty
            }

            // Validate password confirmation
            if (password != confirmPassword) {
                confirmPasswordError = "Passwords do not match" // Set error message if passwords do not match
            } else {
                confirmPasswordError = "" // Clear error message if passwords match
            }

            // If there are no errors, proceed with registration
            if (emailError.isEmpty() && confirmPasswordError.isEmpty() && passwordError.isEmpty() && usernameError.isEmpty()) {
                coroutineScope.launch {
                    registerFunction(context, vm, username, email, password) {
                        // On successful registration, navigate to LoginScreen and show toast
                        Toast.makeText(context, "Register successful", Toast.LENGTH_SHORT).show()
                        context.startActivity(Intent(context, StartSessionActivity::class.java))
                    }
                }
            }
        }) {
            Text(text = "Register")
        }
    }
}
