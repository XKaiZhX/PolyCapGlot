package com.example.polycapglot.ui.screen

import android.content.Intent
import android.graphics.Bitmap
import android.widget.Toast
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
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
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import com.example.polycapglot.ui.PlayerActivity
import com.example.polycapglot.ui.UploadFileActivity
import com.example.polycapglot.ui.viewmodel.MenuViewModel
import com.example.polycapglot.ui.viewmodel.models.Translation
import com.example.polycapglot.ui.viewmodel.models.Video
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

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
                VideoCard(video, thumbnail, vm) { videoUrl ->
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
fun VideoCard(
    video: Video,
    thumbnail: Bitmap?,
    vm: MenuViewModel,
    onClick: (String) -> Unit
) {
    val context = LocalContext.current

    var expanded by remember { mutableStateOf(false) }
    var moreOptionsExpanded by remember { mutableStateOf(false) }
    var selectedTranslation by remember { mutableStateOf<Translation?>(null) }
    var isAddTranslationDialogShown by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        selectedTranslation = if (video.translations.isNotEmpty()) video.translations[0] else null
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable {
                if (selectedTranslation?.status == 1) {
                    onClick(selectedTranslation?.firebase_uri ?: video.firebase_uri)
                }
            }
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

                when (selectedTranslation?.status) {
                    0 -> Text(text = "Translation in process...", color = Color.Gray, style = MaterialTheme.typography.bodySmall)
                    1 -> Text(text = "Translation available", color = Color.Green, style = MaterialTheme.typography.bodySmall)
                    -1 -> Text(text = "Translation failed", color = Color.Red, style = MaterialTheme.typography.bodySmall)
                }
            }

            Box {
                Button(
                    onClick = { expanded = true },
                    enabled = selectedTranslation?.status == 1
                ) {
                    Text(selectedTranslation?.sub_language ?: "Generating")
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

            Box(
                modifier = Modifier
                    .padding(start = 8.dp)
                    .align(Alignment.Top)
            ) {
                IconButton(onClick = { moreOptionsExpanded = true }) {
                    Icon(Icons.Default.MoreVert, contentDescription = "More Options")
                }
                DropdownMenu(
                    expanded = moreOptionsExpanded,
                    onDismissRequest = { moreOptionsExpanded = false }
                ) {
                    DropdownMenuItem(
                        onClick = {
                            moreOptionsExpanded = false
                            CoroutineScope(Dispatchers.IO).launch {
                                selectedTranslation?.let { vm.deleteTranslation(video, it) }
                            }
                        },
                        text = {
                            Text("Delete Current Translation")
                        }
                    )

                    DropdownMenuItem(
                        onClick = {
                            moreOptionsExpanded = false
                            CoroutineScope(Dispatchers.IO).launch {
                                vm.deleteVideo(video)
                            }
                        },
                        text = {
                            Text("Delete Video")
                        }
                    )

                    DropdownMenuItem(
                        onClick = {
                            moreOptionsExpanded = false
                            isAddTranslationDialogShown = true
                        },
                        text = {
                            Text("Add Translation")
                        }
                    )
                }
            }
        }
    }
    if (isAddTranslationDialogShown) {
        AddTranslationDialog(
            translations = listOf(
                "AR", "BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI", "FR",
                "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "PT-BR",
                "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"
            ),
            onDismiss = { isAddTranslationDialogShown = false },
            videoId = video.id,
            onTranslationSelected = { id, language ->
                // Perform action when translation is selected
                isAddTranslationDialogShown = false
                // Call the function to add translation with the selected language
                // You might need to pass the selected language to the ViewModel to handle the addition
                CoroutineScope(Dispatchers.Main).launch {
                    val success = withContext(Dispatchers.IO) {
                        vm.addTranslation(id, language)
                    }
                    if (success) {
                        Toast.makeText(context, "Translation in process", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(context, "Request failed", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        )
    }
}

@Composable
fun AddTranslationDialog(
    translations: List<String>,
    onDismiss: () -> Unit,
    videoId: String,
    onTranslationSelected: (String, String) -> Unit
) {
    Dialog(onDismissRequest = { onDismiss() }) {
        Surface(
            modifier = Modifier.width(300.dp),
            shape = MaterialTheme.shapes.medium,
            tonalElevation = 24.dp
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "Select Translation",
                    style = MaterialTheme.typography.headlineSmall
                )
                Spacer(modifier = Modifier.height(16.dp))
                LazyColumn(){
                    items(translations){
                        TextButton(
                            onClick = { onTranslationSelected(videoId, it) },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(text = it)
                        }
                    }
                }
            }
        }
    }
}