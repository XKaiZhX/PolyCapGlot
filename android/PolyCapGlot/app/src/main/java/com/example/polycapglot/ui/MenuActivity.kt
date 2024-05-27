package com.example.polycapglot.ui

import android.app.Application
import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.outlined.Add
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
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Composition
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.arthenica.mobileffmpeg.Config
import com.arthenica.mobileffmpeg.FFmpeg
import com.bumptech.glide.Glide
import com.bumptech.glide.request.FutureTarget
import com.example.polycapglot.ui.ui.theme.PolyCapGlotTheme
import com.example.polycapglot.ui.viewmodel.HomeViewModel
import com.example.polycapglot.ui.viewmodel.MenuViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

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
            SettingsScreen()
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

@Composable
fun HomeScreen(vm: MenuViewModel) {
    val context = LocalContext.current
    val videos = vm.videos.value
    val videoLinks = vm.videoDownloadLinks.value
    val thumbnails = vm.thumbnails.value

    // Fetch videos and generate thumbnails when the composable is first composed
    LaunchedEffect(Unit) {
        vm.requestVideos()
    }

    // Once videos are fetched, get download links and generate thumbnails
    LaunchedEffect(videos) {
        if (videos.isNotEmpty()) {
            val videoUris = videos.map { it.firebase_uri }
            vm.getDownloadLinks(videoUris) { downloadLinks ->
                vm.generateThumbnails(downloadLinks)
            }
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize()
        ) {
            items(videos.size) { index ->
                val video = videos[index]
                val thumbnail = thumbnails.getOrNull(index)
                VideoCard(video, thumbnail) { videoUrl ->
                    val intent = Intent(context, PlayerActivity::class.java).apply {
                        putExtra("videoUrl", videoUrl)
                    }
                    context.startActivity(intent)
                }
            }
        }

        FloatingActionButton(
            onClick = {
                val intent = Intent(context, UploadFileActivity::class.java).apply {
                    putExtra("token", vm.token) // Pass the token to UploadFileActivity
                }
                context.startActivity(intent)
            },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            Icon(
                imageVector = Icons.Default.Add,
                contentDescription = "Upload"
            )
        }
    }
}

@Composable
fun VideoCard(video: MenuViewModel.Video, thumbnail: Bitmap?, onClick: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    var selectedTranslation by remember { mutableStateOf<MenuViewModel.Translation?>(null) }

    LaunchedEffect(Unit){
        selectedTranslation = if (video.translations.size > 0) video.translations[0] else null
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable { onClick(selectedTranslation?.firebase_uri ?: video.firebase_uri) }
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(16.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .padding(8.dp)
            ) {
                thumbnail?.let {
                    Image(
                        bitmap = it.asImageBitmap(),
                        contentDescription = null,
                        modifier = Modifier.fillMaxSize()
                    )
                } ?: Text("Loading thumbnail...")
            }

            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 16.dp)
            ) {
                Text(text = video.title, style = MaterialTheme.typography.titleMedium)
                Text(text = "Language: ${video.language}", style = MaterialTheme.typography.labelSmall)
            }

            Box {
                Button(onClick = { expanded = true }) {
                    Text( selectedTranslation?.sub_language ?: "Generating")
                }
                DropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    video.translations.forEach { translation ->
                        DropdownMenuItem(
                            onClick = {
                                selectedTranslation = translation
                                expanded = false
                            },
                            text = {
                                Text(text = translation.sub_language)
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun SettingsScreen() {
    // Content for Settings Screen
    Column(Modifier
        .fillMaxSize()
        //.background(Color.Cyan)
    ) {
        Text(text = "Settings Screen")
    }
}