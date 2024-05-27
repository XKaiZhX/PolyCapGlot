package com.example.polycapglot.ui

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.os.Bundle
import android.util.Log
import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.State
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.Key.Companion.C
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.LifecycleOwner
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import com.example.polycapglot.ui.viewmodel.PlayerViewModel
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.ktx.storage

class PlayerActivity : ComponentActivity() {

    private val playerViewModel: PlayerViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Retrieve the video path from the intent
        val videoPath = intent.getStringExtra("videoUrl")

        if (videoPath != null) {
            val storage = Firebase.storage
            val storageRef = storage.reference.child(videoPath)
            storageRef.downloadUrl.addOnSuccessListener { uri ->
                val videoUrl = uri.toString()
                Log.i("PLAYER_ACT", "Download URL: $videoUrl")

                playerViewModel.initializePlayer(this, videoUrl)

                setContent {
                    Column(Modifier.fillMaxSize().background(Color.Black)) {
                        ExoPlayerScreen(playerViewModel)
                    }
                }
            }.addOnFailureListener { exception ->
                Log.e("PLAYER_ACT", "Error getting download URL", exception)
                // Handle error (e.g., show a message to the user)
            }
        } else {
            Log.e("PLAYER_ACT", "Video path is null")
            // Handle error (e.g., show a message to the user)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        playerViewModel.releasePlayer()
    }
}


@Composable
fun ExoPlayerScreen(playerViewModel: PlayerViewModel) {
    val context = LocalContext.current
    val exoPlayer = playerViewModel.exoPlayer

    var showButton by remember { mutableStateOf(false) }

    Box(modifier = Modifier
        .fillMaxSize()
        .background(Color.Black)
        .pointerInput(Unit) {
            detectVerticalDragGestures(
                onVerticalDrag = { change, dragAmount ->
                    if (dragAmount < -10) {
                        showButton = true
                    } else if (dragAmount > 10) {
                        showButton = false
                    }
                }
            )
        }
    ) {
        AndroidView(
            factory = { context ->
                PlayerView(context).apply {
                    player = exoPlayer
                }
            },
            modifier = Modifier.fillMaxSize()
        )

        AnimatedVisibility(
            visible = showButton,
            modifier = Modifier.align(Alignment.BottomEnd)
        ) {
            FloatingActionButton(
                onClick = { rotateScreen(context) },
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(16.dp)
            ) {
                Icon(
                    imageVector = Icons.Filled.Refresh,
                    contentDescription = "Rotate"
                )
            }
        }
    }
}

private fun rotateScreen(context: Context) {
    val activity = context as? Activity ?: return
    val orientation = context.resources.configuration.orientation
    val newOrientation = if (orientation == Configuration.ORIENTATION_LANDSCAPE) {
        ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
    } else {
        ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
    }
    activity.requestedOrientation = newOrientation
}