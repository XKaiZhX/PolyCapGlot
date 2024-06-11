package com.example.polycapglot.ui.screen

import android.content.Context
import android.content.Intent
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import com.example.polycapglot.ui.StartSessionActivity
import com.example.polycapglot.ui.viewmodel.MenuViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

@Composable
fun SettingsScreen(vm: MenuViewModel) {
    var isUsernameDialogShown by remember { mutableStateOf(false) }
    var isPasswordDialogShown by remember { mutableStateOf(false) }
    var context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "Settings Screen", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(24.dp))

        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
            Text(text = "Modify Username", modifier = Modifier.clickable { isUsernameDialogShown = true })
            Text(text = vm.username, style = MaterialTheme.typography.bodyLarge)
        }
        Spacer(modifier = Modifier.height(24.dp))

        Text(text = "Modify Password", modifier = Modifier.clickable { isPasswordDialogShown = true })

        if (isUsernameDialogShown) {
            ModifyUsernameDialog(
                currentUsername = vm.username,
                onDismiss = { isUsernameDialogShown = false },
                onUsernameUpdated = { newUsername ->
                    CoroutineScope(Dispatchers.IO).launch {
                        val result = vm.updateUsername(newUsername)
                        showToast(result, context, "Username updated", "Failed to update username")
                    }
                }
            )
        }

        if (isPasswordDialogShown) {
            ModifyPasswordDialog(
                onDismiss = { isPasswordDialogShown = false },
                onPasswordUpdated = { newPassword ->
                    CoroutineScope(Dispatchers.IO).launch {
                        val result = vm.updatePassword(newPassword)
                        showToast(result, context, "Password updated", "Failed to update password")
                    }
                }
            )
        }
        Row(Modifier.fillMaxWidth().fillMaxHeight(), Arrangement.Center, Alignment.Bottom) {
            Text(
                text = "Delete Current User",
                modifier = Modifier
                    .clickable {
                        CoroutineScope(Dispatchers.IO).launch {
                            val result = vm.deleteCurrentUser()
                            showToast(
                                result,
                                context,
                                "Current user deleted",
                                "Failed to delete current user"
                            )
                            if (result) {
                                // Launch StartSessionActivity
                                val intent = Intent(context, StartSessionActivity::class.java)
                                context.startActivity(intent)
                            }
                        }
                    }
                    .fillMaxWidth()
                    .background(Color.Red)
                    .padding(16.dp),
                textAlign = TextAlign.Center,
                style = TextStyle(color = Color.White)
            )
        }
    }
}

fun showToast(success: Boolean, context: Context, successMessage: String, failedMessage: String) {
    CoroutineScope(Dispatchers.Main).launch {
        val message = if (success) successMessage else failedMessage
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
    }
}

@Composable
fun ModifyUsernameDialog(
    currentUsername: String,
    onDismiss: () -> Unit,
    onUsernameUpdated: (String) -> Unit
) {
    var newUsername by remember { mutableStateOf(currentUsername) }
    var usernameError by remember { mutableStateOf("") }

    Dialog(onDismissRequest = { onDismiss() }) {
        Surface(
            modifier = Modifier.width(300.dp),
            shape = MaterialTheme.shapes.medium,
            tonalElevation = 24.dp
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(text = "Modify Username", style = MaterialTheme.typography.headlineSmall)
                Spacer(modifier = Modifier.height(16.dp))
                TextField(
                    value = newUsername,
                    onValueChange = {
                        newUsername = it.replace("\\s".toRegex(), "")
                        usernameError = if (newUsername.isEmpty()) "Username cannot be empty" else ""
                    },
                    label = { Text("New Username") },
                    isError = usernameError.isNotEmpty()
                )
                if (usernameError.isNotEmpty()) {
                    Text(
                        text = usernameError,
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(top = 8.dp)
                    )
                }
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { onDismiss() }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(onClick = {
                        if (newUsername.isNotEmpty()) {
                            onUsernameUpdated(newUsername)
                            onDismiss()
                        } else {
                            usernameError = "Username cannot be empty"
                        }
                    }) {
                        Text("Accept")
                    }
                }
            }
        }
    }
}

@Composable
fun ModifyPasswordDialog(
    onDismiss: () -> Unit,
    onPasswordUpdated: (String) -> Unit
) {
    var newPassword by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var passwordError by remember { mutableStateOf("") }
    val context = LocalContext.current

    Dialog(onDismissRequest = { onDismiss() }) {
        Surface(
            modifier = Modifier.width(300.dp),
            shape = MaterialTheme.shapes.medium,
            tonalElevation = 24.dp
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(text = "Modify Password", style = MaterialTheme.typography.headlineSmall)
                Spacer(modifier = Modifier.height(16.dp))
                TextField(
                    value = newPassword,
                    onValueChange = {
                        newPassword = it.replace("\\s".toRegex(), "")
                        passwordError = if (newPassword.isEmpty()) "Password cannot be empty" else ""
                    },
                    label = { Text("New Password") },
                    visualTransformation = PasswordVisualTransformation(),
                    isError = passwordError.isNotEmpty()
                )
                Spacer(modifier = Modifier.height(8.dp))
                TextField(
                    value = confirmPassword,
                    onValueChange = {
                        confirmPassword = it.replace("\\s".toRegex(), "")
                    },
                    label = { Text("Confirm Password") },
                    visualTransformation = PasswordVisualTransformation()
                )
                if (passwordError.isNotEmpty()) {
                    Text(
                        text = passwordError,
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(top = 8.dp)
                    )
                }
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { onDismiss() }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(onClick = {
                        if (newPassword.isNotEmpty() && newPassword == confirmPassword) {
                            onPasswordUpdated(newPassword)
                            onDismiss()
                        } else if (newPassword.isEmpty()) {
                            passwordError = "Password cannot be empty"
                        } else {
                            showToast(false, context, "what?", "Passwords have to match")
                        }
                    }) {
                        Text("Accept")
                    }
                }
            }
        }
    }
}
