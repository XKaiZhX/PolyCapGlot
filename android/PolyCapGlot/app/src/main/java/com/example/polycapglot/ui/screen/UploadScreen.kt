package com.example.polycapglot.ui.screen

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import coil.ImageLoader
import coil.compose.AsyncImagePainter
import coil.compose.rememberAsyncImagePainter
import coil.decode.VideoFrameDecoder
import com.example.polycapglot.ui.viewmodel.UploadViewModel

@Composable
fun UploadScreen(viewModel: UploadViewModel, token: String) {
    val context = LocalContext.current
    var title by remember { mutableStateOf("") }
    var selectedOriginalLanguage by remember { mutableStateOf(viewModel.originalLanguages.first()) }
    var selectedTranslationLanguage by remember { mutableStateOf(viewModel.translationLanguages.first()) }
    var isOriginalLanguageMenuExpanded by remember { mutableStateOf(false) }
    var isTranslationLanguageMenuExpanded by remember { mutableStateOf(false) }
    var titleError by remember { mutableStateOf(false) }

    val singleVideoPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { viewModel.uri = it }
    )

    val imageLoader = ImageLoader.Builder(context)
        .components {
            add(VideoFrameDecoder.Factory())
        }
        .build()

    val painter = rememberAsyncImagePainter(
        model = viewModel.uri,
        imageLoader = imageLoader
    )

    Column(
        Modifier.fillMaxSize(),
        Arrangement.SpaceAround,
        Alignment.CenterHorizontally
    ) {
        Button(onClick = {
            viewModel.uploaded = 0
            singleVideoPicker.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.VideoOnly))
        }) {
            Text(text = "Select video")
        }

        if (viewModel.uri != null) {
            VideoThumbnail(painter, viewModel.storageFilename)

            TextField(
                value = title,
                onValueChange = {
                    title = it
                    titleError = title.isEmpty()
                },
                label = { Text("Enter title") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text),
                isError = titleError,
                singleLine = true,
                modifier = Modifier.fillMaxWidth(0.8f)
            )
            if (titleError) {
                Text(
                    text = "Title cannot be empty",
                    color = Color.Red,
                    modifier = Modifier.padding(8.dp)
                )
            }

            Row(Modifier.fillMaxWidth(0.8f), Arrangement.SpaceBetween) {
                Box {
                    Column {
                        Text(text = "Original")
                        Button(onClick = { isOriginalLanguageMenuExpanded = !isOriginalLanguageMenuExpanded }) {
                            Text(text = selectedOriginalLanguage)
                        }
                        DropdownMenu(
                            expanded = isOriginalLanguageMenuExpanded,
                            onDismissRequest = { isOriginalLanguageMenuExpanded = false }
                        ) {
                            viewModel.originalLanguages.forEach { language ->
                                DropdownMenuItem(
                                    onClick = {
                                        selectedOriginalLanguage = language
                                        isOriginalLanguageMenuExpanded = false
                                    },
                                    text = { Text(language) }
                                )
                            }
                        }
                    }
                }

                Box {
                    Column {
                        Text(text = "Translation")
                        Button(onClick = { isTranslationLanguageMenuExpanded = !isTranslationLanguageMenuExpanded }) {
                            Text(text = selectedTranslationLanguage)
                        }
                        DropdownMenu(
                            expanded = isTranslationLanguageMenuExpanded,
                            onDismissRequest = { isTranslationLanguageMenuExpanded = false }
                        ) {
                            viewModel.translationLanguages.forEach { language ->
                                DropdownMenuItem(
                                    onClick = {
                                        selectedTranslationLanguage = language
                                        isTranslationLanguageMenuExpanded = false
                                    },
                                    text = { Text(language) }
                                )
                            }
                        }
                    }
                }
            }

            Button(onClick = {
                if (title.isEmpty()) {
                    titleError = true
                } else {
                    viewModel.prerequestFunction(title, selectedOriginalLanguage, selectedTranslationLanguage, token,
                        onSuccess = {
                            viewModel.uploaded = 1
                        },
                        onError = {
                            viewModel.uploaded = -1
                        })
                }
            }) {
                Text(text = "Upload file")
            }

            if (viewModel.uploaded != 0)
                if (viewModel.uploaded == 1)
                    Text(text = "File uploaded successfully")
                else
                    Text(text = "Failed to upload file")
        } else {
            Spacer(Modifier)
        }
    }
}

@Composable
fun VideoThumbnail(painter: AsyncImagePainter, storageFilename: String) {
    var clicked by remember { mutableStateOf(false) }
    Card(
        Modifier
            .fillMaxWidth(0.8f)
            .height(300.dp)
            .clickable { clicked = !clicked },
        elevation = CardDefaults.elevatedCardElevation(100.dp, 10.dp)
    ) {
        Box(Modifier.fillMaxSize(), Alignment.Center) {
            Image(
                painter = painter,
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
            if (clicked)
                Surface(
                    Modifier.fillMaxSize(),
                    color = Color.Black.copy(alpha = 0.75f)
                ) {
                    Column(Modifier.fillMaxSize(), Arrangement.Center, Alignment.CenterHorizontally) {
                        Text(text = storageFilename)
                    }
                }
        }
    }
}