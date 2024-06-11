package com.example.polycapglot.ui

import android.app.Application
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.BottomAppBar
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.polycapglot.ui.screen.HomeScreen
import com.example.polycapglot.ui.screen.SettingsScreen
import com.example.polycapglot.ui.ui.theme.PolyCapGlotTheme
import com.example.polycapglot.ui.viewmodel.MenuViewModel
import com.example.polycapglot.ui.viewmodel.models.Translation
import com.example.polycapglot.ui.viewmodel.models.Video
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class MenuActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val extras = intent.extras
            val username = extras?.getString("Username") ?: "This_is_me"
            val email = extras?.getString("Email") ?: "me@me.com"
            val token = extras?.getString("Token") ?: ""
            Log.i("MENU_TOKEN", token)
            PolyCapGlotTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    val vm: MenuViewModel = MenuViewModel(username, email, token, LocalContext.current.applicationContext as Application)
                    MyScaffold(vm, navController)
                }
            }
        }
    }
}

@Composable
fun CreateNavHost(vm:MenuViewModel, navController: NavController, paddingValues: PaddingValues) {
    NavHost(navController = navController as NavHostController, startDestination = "home") {
        composable("home") {
            HomeScreen(vm)
        }
        composable("settings") {
            SettingsScreen(vm)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyScaffold(vm: MenuViewModel, navController: NavController) {
    var home by remember { mutableStateOf(true) }
    var settings by remember { mutableStateOf(false) }
    Scaffold(
        topBar = {
            TopAppBar(title = {
                if(home)
                    Text(text = "Home")
                else if (settings)
                    Text(text = "Settings")
            })
        },
        bottomBar = {
            BottomAppBar() {
                NavigationBar {
                    NavigationBarItem(
                        selected = home,
                        onClick = {
                            home = true;
                            settings = false;
                            navController.navigate("home")
                        },
                        icon = {
                            if (home)
                                Icon(Icons.Filled.Home, "")
                            else
                                Icon(Icons.Outlined.Home, "")
                        },
                        label = {
                            Text(text = "Home")
                        })
                    NavigationBarItem(
                        selected = settings,
                        onClick = {
                            home = false;
                            settings = true;
                            navController.navigate("settings")
                        },
                        icon = {
                            if (settings)
                                Icon(Icons.Filled.Settings, "")
                            else
                                Icon(Icons.Outlined.Settings, "")
                        },
                        label = {
                            Text(text = "Settings")
                        })
                }
            }
        }
    ) {
        Box(
            modifier = Modifier
                .padding(it)
                .consumeWindowInsets(it)
        ){
            CreateNavHost(vm, navController = navController, it)
        }
    }
}



//Settings

